"""Constrói os artefatos locais TF-IDF somente da partição de referência."""

from __future__ import annotations

import argparse
from pathlib import Path

from nlp.intent_similarity import ARTIFACTS_DIR, build_reference_index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ARTIFACTS_DIR)
    args = parser.parse_args()

    index = build_reference_index()
    model_path, config_path = index.save_artifacts(args.output_dir)
    print(f"Índice criado com {len(index.reference_examples)} exemplos de referência.")
    print(f"Modelo: {model_path}")
    print(f"Configuração: {config_path}")


if __name__ == "__main__":
    main()
