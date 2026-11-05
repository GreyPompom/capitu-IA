"""Curate CAPITU intent data into deterministic, group-safe evaluation splits."""

from __future__ import annotations

import csv
import hashlib
import json
import random
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "intents.csv"
SPLITS_DIR = ROOT / "data" / "splits"
HUMAN_REVIEW_PATH = ROOT / "data" / "e03_human_validation.csv"
SEED = 20261023
INTENT_ORDER = (
    "buscar_por_titulo",
    "buscar_obras_autor",
    "buscar_por_assunto",
    "consultar_detalhes",
)
DATA_COLUMNS = (
    "id",
    "texto",
    "intencao",
    "entidade",
    "campo_solicitado",
    "grupo_variacao",
    "origem",
)
REVIEW_COLUMNS = (
    "id",
    "texto",
    "intencao_humana",
    "entidade_humana",
    "campo_solicitado_humano",
    "precisa_contexto_humano",
    "duvida_observacao",
)


def normalize_text(text: str) -> str:
    """Normalize only for duplicate detection; preserve source text in files."""

    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def validate_dataset(rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("O dataset não contém exemplos.")

    ids: set[str] = set()
    texts: set[str] = set()
    groups_by_intent: dict[str, str] = {}
    valid_intents = set(INTENT_ORDER)

    for line_number, row in enumerate(rows, start=2):
        missing = [column for column in DATA_COLUMNS if column not in row]
        if missing:
            raise ValueError(f"Linha {line_number}: colunas ausentes: {missing}.")

        for column in ("id", "texto", "intencao", "entidade", "grupo_variacao", "origem"):
            if not row[column].strip():
                raise ValueError(f"Linha {line_number}: campo obrigatório vazio: {column}.")

        if row["intencao"] not in valid_intents:
            raise ValueError(f"Linha {line_number}: intenção não prevista: {row['intencao']}.")

        if row["id"] in ids:
            raise ValueError(f"ID duplicado: {row['id']}.")
        ids.add(row["id"])

        normalized = normalize_text(row["texto"])
        if normalized in texts:
            raise ValueError(f"Texto duplicado após normalização: {row['texto']}.")
        texts.add(normalized)

        group = row["grupo_variacao"]
        previous_intent = groups_by_intent.setdefault(group, row["intencao"])
        if previous_intent != row["intencao"]:
            raise ValueError(
                f"O grupo {group} contém mais de uma intenção: "
                f"{previous_intent} e {row['intencao']}."
            )


def _select_groups(
    groups: list[tuple[str, list[dict[str, str]]]], target_rows: int, rng: random.Random
) -> set[str]:
    """Choose whole groups closest to a target count, preferring no overshoot."""

    shuffled = list(groups)
    rng.shuffle(shuffled)
    reachable: dict[int, tuple[str, ...]] = {0: ()}
    for group_id, group_rows in shuffled:
        additions = {}
        for current_count, selected in reachable.items():
            new_count = current_count + len(group_rows)
            if new_count not in reachable and new_count not in additions:
                additions[new_count] = (*selected, group_id)
        reachable.update(additions)

    best_count = min(reachable, key=lambda count: (abs(count - target_rows), count > target_rows, count))
    return set(reachable[best_count])


def create_splits(rows: list[dict[str, str]], seed: int = SEED) -> dict[str, list[dict[str, str]]]:
    """Create approximately 70/15/15 splits without separating variation groups."""

    validate_dataset(rows)
    by_intent_group: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        by_intent_group[row["intencao"]][row["grupo_variacao"]].append(row)

    split_groups: dict[str, set[str]] = {"reference": set(), "validation": set(), "test": set()}
    all_groups_by_intent = {}
    for intent_index, intent in enumerate(INTENT_ORDER):
        groups = list(by_intent_group.get(intent, {}).items())
        if not groups:
            raise ValueError(f"O dataset não contém exemplos para {intent}.")
        all_groups_by_intent[intent] = {group_id: group_rows for group_id, group_rows in groups}
        count = sum(len(group_rows) for _, group_rows in groups)

        # Para classes de mesmo tamanho, alternar 4/5 exemplos nos dois splits
        # mantém o alvo global 70/15/15 em corpus de 30 exemplos por classe.
        low_target = int(count * 0.15)
        high_target = count - round(count * 0.70) - low_target
        validation_target, test_target = (
            (low_target, high_target) if intent_index % 2 == 0 else (high_target, low_target)
        )

        rng = random.Random(seed + intent_index)
        test_groups = _select_groups(groups, test_target, rng)
        remaining = [(group_id, group_rows) for group_id, group_rows in groups if group_id not in test_groups]
        validation_groups = _select_groups(remaining, validation_target, rng)
        reference_groups = {group_id for group_id, _ in remaining} - validation_groups

        split_groups["reference"].update(reference_groups)
        split_groups["validation"].update(validation_groups)
        split_groups["test"].update(test_groups)

    splits = {name: [] for name in split_groups}
    for intent, groups in all_groups_by_intent.items():
        for group_id, group_rows in groups.items():
            target_split = next(name for name, group_ids in split_groups.items() if group_id in group_ids)
            splits[target_split].extend(group_rows)

    for split_rows in splits.values():
        split_rows.sort(key=lambda row: row["id"])
    audit_splits(splits)
    return splits


def audit_splits(splits: dict[str, list[dict[str, str]]]) -> None:
    seen_ids: set[str] = set()
    seen_texts: set[str] = set()
    seen_groups: dict[str, str] = {}

    for split_name, rows in splits.items():
        for row in rows:
            if row["id"] in seen_ids:
                raise ValueError(f"ID repetido entre splits: {row['id']}.")
            seen_ids.add(row["id"])

            normalized = normalize_text(row["texto"])
            if normalized in seen_texts:
                raise ValueError(f"Texto repetido entre splits: {row['texto']}.")
            seen_texts.add(normalized)

            group = row["grupo_variacao"]
            previous_split = seen_groups.setdefault(group, split_name)
            if previous_split != split_name:
                raise ValueError(
                    f"Vazamento: o grupo {group} aparece em {previous_split} e {split_name}."
                )


def _read_dataset(path: Path = DATASET_PATH) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if tuple(reader.fieldnames or ()) != DATA_COLUMNS:
            raise ValueError(f"Cabeçalho inesperado em {path}: {reader.fieldnames}.")
        rows = list(reader)
    validate_dataset(rows)
    return rows


def _write_csv(path: Path, columns: Iterable[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_human_review(rows: list[dict[str, str]]) -> None:
    if HUMAN_REVIEW_PATH.exists():
        return  # Preserve human annotations if the split script is rerun.
    additions = [row for row in rows if row["id"].startswith("E03-")]
    review_rows = [
        {
            "id": row["id"],
            "texto": row["texto"],
            "intencao_humana": "",
            "entidade_humana": "",
            "campo_solicitado_humano": "",
            "precisa_contexto_humano": "",
            "duvida_observacao": "",
        }
        for row in additions
    ]
    _write_csv(HUMAN_REVIEW_PATH, REVIEW_COLUMNS, review_rows)


def main() -> None:
    rows = _read_dataset()
    splits = create_splits(rows)
    SPLITS_DIR.mkdir(parents=True, exist_ok=True)
    for name, split_rows in splits.items():
        _write_csv(SPLITS_DIR / f"{name}.csv", DATA_COLUMNS, split_rows)
    _write_human_review(rows)

    source_hash = hashlib.sha256(DATASET_PATH.read_bytes()).hexdigest()
    counts = {
        split: {
            "examples": len(split_rows),
            "by_intent": {
                intent: sum(row["intencao"] == intent for row in split_rows)
                for intent in INTENT_ORDER
            },
            "variation_groups": len({row["grupo_variacao"] for row in split_rows}),
        }
        for split, split_rows in splits.items()
    }
    manifest = {
        "dataset_version": "0.2.0",
        "generated_on": date.today().isoformat(),
        "source": "data/intents.csv",
        "source_sha256": source_hash,
        "method": "Deterministic split by group_variacao, stratified by intent; target 70/15/15.",
        "seed": SEED,
        "human_blind_review": "pending; complete data/e03_human_validation.csv before treating labels as finalized",
        "test_policy": "Do not use test.csv for fitting TF-IDF, choosing thresholds, or tuning rules.",
        "counts": counts,
        "negative_evaluation_data": "data/Fora_Do_Escopo_Ambiguo.csv (kept outside intent training splits)",
    }
    (SPLITS_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(counts, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
