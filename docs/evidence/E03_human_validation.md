# E03 — revisão humana cega do corpus

**Status:** pendente de validação de Emely. Os 40 exemplos E03 são rascunhos preparados com assistência de IA e estão identificados dessa forma em `data/intents.csv`.

## Como fazer a validação

1. Abra somente `data/e03_human_validation.csv`. Não consulte `data/intents.csv`, os arquivos em `data/splits/` nem o manifesto enquanto anota: eles contêm os rótulos propostos.
2. Para cada linha, preencha `intencao_humana`, `entidade_humana`, `campo_solicitado_humano` quando a pergunta pedir um dado específico, `precisa_contexto_humano` (`sim` ou `não`) e `duvida_observacao`.
3. Use uma das quatro intenções do guia se a solicitação estiver clara. Se não estiver, escreva `ambígua` e explique qual esclarecimento faltou. Não force uma classe só porque o exemplo está no corpus positivo.
4. Verifique também se a frase soa natural, se a entidade está explícita e se o campo solicitado corresponde ao pedido. Para `consultar_detalhes`, indique quando uma referência como “essa obra” depende de conversa anterior.
5. Depois de anotar todas as linhas, compare com os mesmos IDs em `data/intents.csv`. Registre cada divergência e uma decisão: manter, corrigir rótulo/entidade/campo ou retirar/substituir o exemplo. Não apague as anotações cegas.
6. Se houver alteração nos rótulos ou textos, atualize `intents.csv` somente após registrar a decisão, execute novamente `scripts/prepare_dataset_splits.py` e os testes da E03. A geração preserva a folha preenchida; confira se ela contém todas as anotações antes de concluir.
7. Registre sua decisão e data em `docs/evidence/E03.md`. Até essa revisão terminar, o corpus e os splits são provisórios e não devem ser usados para ajustar limiares nem reportar métricas finais.

## Como conferir a separação

O arquivo `data/splits/manifest.json` registra a contagem, o hash do dataset e a semente de geração. `reference.csv` é a única partição que a E04 pode usar para ajustar TF-IDF. `validation.csv` pode apoiar decisões de configuração; `test.csv` fica reservado para a avaliação final. Os três CSVs mantêm grupos completos, sem separar paráfrases entre partições. `data/Fora_Do_Escopo_Ambiguo.csv` permanece separado, pois negativos e ambíguos avaliam abstenção/esclarecimento e não são uma quinta intenção positiva.

## Registro da revisão humana

| Data | Exemplos revisados | Rótulos concordantes | Divergências | Decisões/arquivo atualizado |
|---|---:|---:|---:|---|
| Pendente | — | — | — | — |
