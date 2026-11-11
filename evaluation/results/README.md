# Resultados de avaliação

Guardar aqui relatórios reproduzíveis e tabelas de métricas. Distinguir fixtures controladas de consultas reais à API.

## G05 — tabela de aceitação

Execute `py -3.13 scripts/run_g05_acceptance.py` na raiz do repositório para gerar `evaluation/g05_acceptance.csv`. Por padrão, o runner executa duas trilhas identificadas pela coluna `evidencia_tipo`:

- `fixture`: T01–T24 com catálogo controlado, sem rede; respostas vazias, timeout e múltiplos resultados são determinísticos.
- `live`: T01–T24 com o cliente E09/Open Library real. A API pode mudar seus resultados; indisponibilidade ou falta de resultados necessários para completar um cenário fica `pendente`, nunca aprovada. T21 fica pendente ao vivo, pois não se provoca falha artificial na API real.

Use `--mode fixture` ou `--mode live` para atualizar apenas uma trilha. A tabela contém um registro por caso e por tipo de evidência; repetições atualizam a trilha escolhida, sem misturar fixture e API real. T13 tem oráculo de esclarecimento, aprovado em 2026-11-10.

Os três testes pytest simples da G05 estão em `tests/test_g05_acceptance.py`; usam o padrão `TestClient` dos testes HTTP da E02 para título, autor e assunto, com serviço E09 e catálogo controlado. A indisponibilidade controlada de T21 também é verificada pela integração E09, e as retentativas/limites HTTP da E10 são exercitadas em `tests/test_open_library_resilience.py`.
