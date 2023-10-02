## Como rodar
1. Certifique-se de que o Python3 ou superior está instalado em sua máquina.

2. Clone ou faça download do repositório no seu computador.

3. Acesse a pasta raiz do projeto em seu terminal.

4. Agora, temos que instalar as dependências desse projeto.

    4.1. Ainda no terminal, crie uma um ambiente virtual com o comando:
    - Caso seu sistema operacional seja Windows/Linux: 
    
            `python -m venv env`

    - Caso seu sistema operacional seja MacOS:

            `python3 -m venv env`

    4.2. Após criado o ambiente virtual, ative-o com o comando:
    - Caso seu sistema operacional seja Windows/Linux: 
    
            `env\Scripts\activate.bat`

    - Caso seu sistema operacional seja MacOS:
    
            `source env/bin/activate`

    4.3. Agora, instale as dependências do projeto com o comando:
        
            `pip install -r requirements.txt`

5. Agora, basta rodar o projeto!!!


## Como funciona o projeto:

- `Mapa.py`: nesse arquivo, contém a solução para o problema do Mapa, de maneira genérica. Esse **não** responde as perguntas do enunciado! Em outras palavras, ele apenas demonstra a implementação da solucão de maneira gérica desse problema em um arquivo `.py` separado.

- `Rotas.py`: nesse arquivo, contém a solução para o problema das Rotas, de maneira genérica. Esse **não** responde as perguntas do enunciado! Em outras palavras, ele apenas demonstra a implementação da solucão de maneira gérica desse problema em um arquivo `.py` separado.

- `requirements.txt`: nesse arquivo, contém as dependências do projeto.

- `main.ipynb`: nesse arquivo, contém a solução de ambos os problemas ```Mapa``` e ```Rotas```, contendo as respostas para as perguntas de cada problema e, com a implementação em código para cada uma dessas.

## Observações:
- No arquivo ```main.ipynb```, já estará com os outputs das respostas para cada uma das perguntas de cada problema!!!. 

    Caso queira rodar o código novamente, **não** rodar com o comando **Run All**, rodas as células uma por uma, pois, em um determinado problema, há a necessidade de provar que não há solução para uma situação, e, quando isso acontece, se não estivermos rodando uma célula a uma, de maneira manual, o jupyter só rodará até a célula que irá dar o "erro".

- Ainda no mesmo arquivo, a estrutura de **todas** as respostas é a seguinte:
    1. Pergunta
    2. Resposta texto do problema
    3. Implementação em código do problema