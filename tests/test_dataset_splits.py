"""Auditorias dos dados e dos splits produzidos para a E03."""

import csv
import unittest

from scripts.prepare_dataset_splits import DATA_COLUMNS, INTENT_ORDER, ROOT, audit_splits, create_splits, validate_dataset


def example(row_id: str, text: str, group: str, intent: str = "buscar_por_titulo") -> dict[str, str]:
    return {
        "id": row_id,
        "texto": text,
        "intencao": intent,
        "entidade": "Dom Casmurro",
        "campo_solicitado": "",
        "grupo_variacao": group,
        "origem": "fixture",
    }


class DatasetSplitTests(unittest.TestCase):
    def test_current_splits_cover_every_dataset_row_once_and_keep_groups_together(self) -> None:
        dataset_path = ROOT / "data" / "intents.csv"
        with dataset_path.open(encoding="utf-8-sig", newline="") as source:
            dataset = list(csv.DictReader(source))

        splits = {}
        for split_name in ("reference", "validation", "test"):
            path = ROOT / "data" / "splits" / f"{split_name}.csv"
            with path.open(encoding="utf-8-sig", newline="") as source:
                reader = csv.DictReader(source)
                self.assertEqual(tuple(reader.fieldnames or ()), DATA_COLUMNS)
                splits[split_name] = list(reader)

        audit_splits(splits)
        self.assertEqual(sum(map(len, splits.values())), len(dataset))
        self.assertEqual(
            {row["id"] for rows in splits.values() for row in rows},
            {row["id"] for row in dataset},
        )
        self.assertGreater(len(splits["test"]), 0)

    def test_dataset_rejects_duplicate_ids_and_texts(self) -> None:
        with self.assertRaisesRegex(ValueError, "ID duplicado"):
            validate_dataset([example("E1", "buscar livro A", "G1"), example("E1", "buscar livro B", "G2")])

        with self.assertRaisesRegex(ValueError, "Texto duplicado"):
            validate_dataset([example("E1", "Buscar livro A", "G1"), example("E2", "  buscar   LIVRO a ", "G2")])

    def test_dataset_rejects_one_variation_group_with_conflicting_intents(self) -> None:
        rows = [
            example("E1", "buscar livro A", "same-template", "buscar_por_titulo"),
            example("E2", "listar obras de A", "same-template", "buscar_obras_autor"),
        ]
        with self.assertRaisesRegex(ValueError, "mais de uma intenção"):
            validate_dataset(rows)

    def test_split_audit_detects_variation_group_leakage(self) -> None:
        splits = {
            "reference": [example("E1", "buscar livro A", "shared-group")],
            "validation": [example("E2", "encontre livro B", "shared-group")],
            "test": [],
        }
        with self.assertRaisesRegex(ValueError, "Vazamento"):
            audit_splits(splits)

    def test_split_creation_is_deterministic(self) -> None:
        rows = [
            example(f"E{intent_index}-{i}", f"mensagem {intent_index}-{i}", f"G{intent_index}-{i}", intent)
            for intent_index, intent in enumerate(INTENT_ORDER)
            for i in range(1, 4)
        ]
        first = create_splits(rows, seed=17)
        second = create_splits(rows, seed=17)
        self.assertEqual(
            {name: [row["id"] for row in part] for name, part in first.items()},
            {name: [row["id"] for row in part] for name, part in second.items()},
        )


if __name__ == "__main__":
    unittest.main()
