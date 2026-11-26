# Artefatos locais

Índices vetoriais e modelos derivados podem ser gerados localmente pelos scripts. Não versionar caches ou binários reproduzíveis sem necessidade; registrar versão do dataset e parâmetros.

Para gerar os artefatos da E04, execute:

```powershell
python scripts/build_index.py
```

O script lê somente `data/splits/reference.csv` por padrão e cria `intent_index.joblib` e `intent_index_config.json`. A configuração registra IDs de referência, hash da fonte e parâmetros TF-IDF para reprodução. Não usar `validation.csv` ou `test.csv` no ajuste do índice.
