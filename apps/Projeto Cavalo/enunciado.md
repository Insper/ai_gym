<h1>Cavalo e tabuleiro de xadrez</h1>

Segundo a Wikipedia, o problema do cavalo, ou passeio do cavalo, é um problema matemático envolvendo o movimento da peça do cavalo no tabuleiro de xadrez. O cavalo é colocado no tabuleiro vazio em qualquer uma das posições e, seguindo as regras do jogo, precisa passar por todas as casas exatamente uma vez em movimentos consecutivos. Existem diversas soluções para o problema, dentre elas 26.534.728.821.064 terminam numa casa onde ele ataca a casa na qual iniciou o seu movimento (versão fechada do problema).

![gif](./cavalo.gif)

Segundo alguns textos, é possível implementar um algoritmo que encontre uma solução para o problema do cavalo usando árvores de busca e heurísticas. Neste exercício você deverá implementar um agente que resolve o problema do cavalo fechado usando algoritmos de busca e heurísticas.

<h2>Entrega do exercício</h2

- Este exercício deverá ser feito individualmente.
- O prazo máximo para entrega é 06/10/2023 (sexta-feira) até às 23:30 horas.
- A entrega deverá ser feita via Github Classroom. O link para a entrega é https://classroom.github.com/a/sAi4kKq3.
Cada estudante deverá entregar a implementação do cavalo no tabuleiro de xadrez e um arquivo de documentação (README.md).
- A implementação deve ter um arquivo de testes usando pytest.
- O projeto deve ter um arquivo de requirements.txt que descreve os pacotes necessário para a execução.
- O projeto também deve ter um arquivo python que implementa a solução para o problema.

<h2>Questões que precisam ser respondidas na documentação do exercício</h2>

**O arquivo README.md deve responder as seguintes perguntas:**

- O que é relevante representar nos estados do mundo? Como os estados são estruturados (estrutura de dados) e qual o significado dela (dos campos)?
- Mostre como ficam representados os estados inicial e final segundo a representação adotada.
- Quais as operações sobre os estados? (detalhe como cada operação irá alterar os estados e quais as condições para cada operação ser executada)
- Que algoritmo de busca foi utilizado para resolver este problema?
- A equipe fez uso de heurísticas? Se sim, explique as heurísticas utilizadas.
- Uma explicação de como deve ser usada a implementação com exemplos.

<h2>Requisitos da implementação</h2>

- O estudante deverá implementar no minímo dois arquivos: um arquivo python com a lógica do agente e um arquivo de testes usando pytest. Qualquer entrega que não tenha os dois arquivos, o arquivo da solução e o arquivo de testes, terá nota I.

- O arquivo de testes deve ter no mínimo 3 testes. Cada teste deve iniciar em uma posição diferente.

- Todas as questões precisam estar respondidas para que o estudante tenha no mínimo nota B no trabalho como um todo. Se o estudante deixou de responder uma (1) ou duas (2) questões então a nota é D, caso contrário I. A documentação completa e coerente com a impĺementação é pré-requisito para que a nota seja B.

- Ao responder todas as questões e entregar o arquivo de implementação e o arquivo de testes, o estudante terá nota:

    - D se a implementação não encontrar uma solução para o problema do cavalo fechado.
    - B se a implementação encontrar uma solução para o problema do cavalo fechado.

<br>

- Para alcançar uma nota B o aluno deverá entregar o arquivo README.md, um arquivo de testes usando pytest com no mínimo 3 testes e um arquivo python com a implementação do agente que resolve o problema do cavalo fechado e fornece a solução em modo texto.

- Para conseguir A+ o estudante deverá implementar uma interface gráfica que permite com o usuário possa escolher qualquer posição do tabuleiro para iniciar o passeio do cavalo. Após apertar qualquer botão para iniciar o processamento, a interface gráfica deverá mostrar o cavalo realizando o passeio sobre o tabuleiro. Esta implementação deverá usar alguma interface gráfica como tkinter ou pygame.