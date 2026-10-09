# Guia de anotação

## Intenções
Use somente `buscar_por_titulo`, `buscar_obras_autor`, `buscar_por_assunto` e `consultar_detalhes` quando a mensagem tiver uma dessas ações claras. Registre ambiguidade/fora de escopo em conjunto separado de avaliação, não como uma intenção bibliográfica inventada.

## Boas práticas
- Preserve reformulações naturais e entidades de nomes variados.
- Agrupe paráfrases quase idênticas ao separar treino, validação e teste.
- Registre autoria/origem e versão do dataset.
- Não mova falhas do teste para o treino sem documentar nova versão e criar avaliação independente.
