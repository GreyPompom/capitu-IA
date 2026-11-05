"""Índice TF-IDF e ranking reproduzível das quatro intenções da CAPITU."""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.schemas import Intent, IntentCandidate
from nlp.preprocessing import normalize_text


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_SPLIT_PATH = ROOT / "data" / "splits" / "reference.csv"
ARTIFACTS_DIR = ROOT / "artifacts"
REQUIRED_COLUMNS = ("id", "texto", "intencao")


@dataclass(frozen=True)
class IntentIndexConfig:
    """Parâmetros versionados que determinam a representação TF-IDF."""

    ngram_range: tuple[int, int] = (1, 2)
    sublinear_tf: bool = True
    norm: str = "l2"
    aggregation: str = "maximum cosine similarity per intent"


@dataclass(frozen=True)
class ReferenceExample:
    """Exemplo de referência mantido para auditoria do ranking."""

    identifier: str
    text: str
    intent: Intent


class IntentSimilarityIndex:
    """Representa mensagens por TF-IDF e agrega o melhor cosseno por intenção.

    Cada frase da partição de referência funciona como protótipo. Para uma nova
    mensagem, o índice calcula o cosseno com todos os protótipos e conserva, para
    cada intenção, a maior similaridade. O score é similaridade cosseno, não uma
    probabilidade. Limiar, margem, abstenção e esclarecimento são decisões da E05.
    """

    def __init__(self, config: IntentIndexConfig | None = None) -> None:
        self.config = config or IntentIndexConfig()
        self.vectorizer = TfidfVectorizer(
            preprocessor=normalize_text,
            lowercase=False,
            ngram_range=self.config.ngram_range,
            sublinear_tf=self.config.sublinear_tf,
            norm=self.config.norm,
        )
        self.reference_examples: list[ReferenceExample] = []
        self.reference_matrix = None
        self.source_path: str | None = None
        self.source_sha256: str | None = None

    @property
    def is_fitted(self) -> bool:
        return self.reference_matrix is not None and bool(self.reference_examples)

    @property
    def reference_ids(self) -> tuple[str, ...]:
        return tuple(example.identifier for example in self.reference_examples)

    def fit(self, rows: list[dict[str, str]], *, source_path: Path | None = None) -> "IntentSimilarityIndex":
        """Ajusta vocabulário e matriz exclusivamente sobre linhas de referência."""

        if not rows:
            raise ValueError("A partição de referência não contém exemplos.")

        examples: list[ReferenceExample] = []
        for line_number, row in enumerate(rows, start=2):
            missing = [column for column in REQUIRED_COLUMNS if not row.get(column, "").strip()]
            if missing:
                raise ValueError(f"Linha {line_number}: campos ausentes: {missing}.")
            try:
                intent = Intent(row["intencao"].strip())
            except ValueError as error:
                raise ValueError(f"Linha {line_number}: intenção inválida: {row['intencao']}.") from error
            examples.append(
                ReferenceExample(
                    identifier=row["id"].strip(),
                    text=row["texto"].strip(),
                    intent=intent,
                )
            )

        if len({example.identifier for example in examples}) != len(examples):
            raise ValueError("A partição de referência contém IDs duplicados.")

        self.reference_examples = examples
        self.reference_matrix = self.vectorizer.fit_transform(
            [example.text for example in self.reference_examples]
        )
        self.source_path = str(source_path) if source_path else None
        self.source_sha256 = _sha256(source_path) if source_path else None
        return self

    def fit_from_csv(self, path: Path = REFERENCE_SPLIT_PATH) -> "IntentSimilarityIndex":
        """Carrega exclusivamente a partição de referência aprovada na E03."""

        path = path.resolve()
        if path != REFERENCE_SPLIT_PATH.resolve():
            raise ValueError(
                "O ajuste TF-IDF da E04 usa somente data/splits/reference.csv; "
                "validation.csv e test.csv permanecem reservados para avaliação."
            )
        if not path.is_file():
            raise FileNotFoundError(f"Partição de referência não encontrada: {path}")
        with path.open(encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or ())]
            if missing:
                raise ValueError(f"Cabeçalho inválido em {path}: faltam {missing}.")
            rows = list(reader)
        return self.fit(rows, source_path=path)

    def rank(self, message: str, limit: int = 3) -> list[IntentCandidate]:
        """Devolve até três intenções por score decrescente e posição reproduzível."""

        if not self.is_fitted:
            raise RuntimeError("O índice TF-IDF deve ser ajustado antes do ranking.")
        if not isinstance(message, str) or not message.strip():
            raise ValueError("A mensagem para classificação não pode estar vazia.")
        if not 1 <= limit <= 3:
            raise ValueError("O limite de candidatos deve estar entre 1 e 3.")

        message_vector = self.vectorizer.transform([message])
        similarities = cosine_similarity(message_vector, self.reference_matrix).ravel()
        scores = {intent: 0.0 for intent in Intent}
        for example, similarity in zip(self.reference_examples, similarities, strict=True):
            scores[example.intent] = max(scores[example.intent], float(similarity))

        ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0].value))
        return [
            IntentCandidate(intent=intent, rank=rank, similarity_score=score)
            for rank, (intent, score) in enumerate(ordered[:limit], start=1)
        ]

    def save_artifacts(self, output_dir: Path = ARTIFACTS_DIR) -> tuple[Path, Path]:
        """Salva índice binário e configuração JSON reproduzíveis fora do Git."""

        if not self.is_fitted:
            raise RuntimeError("Não é possível salvar um índice não ajustado.")
        output_dir.mkdir(parents=True, exist_ok=True)
        model_path = output_dir / "intent_index.joblib"
        config_path = output_dir / "intent_index_config.json"
        joblib.dump(self, model_path)
        config_path.write_text(
            json.dumps(
                {
                    "config": asdict(self.config),
                    "reference_examples": len(self.reference_examples),
                    "reference_ids": list(self.reference_ids),
                    "source_path": self.source_path,
                    "source_sha256": self.source_sha256,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return model_path, config_path


def build_reference_index() -> IntentSimilarityIndex:
    """Ponto de entrada da E04: usa apenas `data/splits/reference.csv` por padrão."""

    return IntentSimilarityIndex().fit_from_csv()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
