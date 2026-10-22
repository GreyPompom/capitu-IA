# Guia de anotação

## Intenções
Use somente `buscar_por_titulo`, `buscar_obras_autor`, `buscar_por_assunto` e `consultar_detalhes` quando a mensagem tiver uma dessas ações claras. Ambiguidade e fora de escopo ficam em conjuntos separados de avaliação, não como intenções bibliográficas inventadas.

## Casos fora do escopo e ambíguos

- **Fora do escopo:** o pedido não é uma busca ou consulta bibliográfica coberta pelo MVP. Isso inclui conhecimento geral e operações como empréstimos, reservas, multas, compras ou consulta ao acervo institucional. Registre `out_of_scope`; não classifique como uma intenção válida só porque a frase menciona um livro.
- **Ambíguo:** há uma possível relação com livros, mas não é possível determinar a intenção, a obra ou o parâmetro com segurança. Registre `awaiting_clarification` e anote a pergunta de esclarecimento necessária. Não escolha uma classe por aproximação.
- **Malformado não significa negativo:** erros de digitação, abreviações e frases incompletas que ainda expressem uma intenção recuperável pertencem à avaliação de robustez da intenção correspondente, não automaticamente ao conjunto fora do escopo.
- **Contexto de sessão:** referências como “o segundo” só são resolvíveis quando a sessão contém resultados compatíveis. Sem esse contexto, anote a necessidade de esclarecimento; não invente uma obra referida.
- **Não confundir operação e descoberta:** buscar obras por assunto é permitido; pedir recomendação personalizada, garantia de adequação ou ação sobre empréstimo/reserva não é coberto pelo MVP.

## Boas práticas
- Preserve reformulações naturais e entidades de nomes variados.
- Agrupe paráfrases quase idênticas ao separar treino, validação e teste.
- Preserve um ID estável por exemplo e registre autoria/origem e versão do dataset.
- Não mova falhas do teste para o treino sem documentar nova versão e criar avaliação independente.
