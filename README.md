# Pac Man

### Configurando o Ambiente

Tenha as seguintes dependências instaladas:

- `python 2`
- `tkinter`
- `jupyter`
- `pipenv`

Na pasta do projeto, inicie o ambiente virtual com:

```sh
pipenv install

pipenv shell
```

Inicie o notebook com:

```sh
jupyter notebook
```

### Comandos

Existem vários layouts/mapas possíveis. Para escolher um, basta passar a flag `--layout [nome-do-layout]` para o comando:

```python
! python pacman.py
```

> No ambiente Jupyter

Para o Projeto 3, deve-se considerar os seguintes layouts:

- `smallClassic`
- `mediumClassic` (default)
- `originalClassic`


Para rodar o algoritmo de programação genética, basta executar o comando:

```sh
! python p3.py
```

### Projeto

Inicialmente foi criado o arquivo `p3.py` para ser o script a ser rodado para criar as gerações, avaliar os indivíduos (rodando os jogos), reproduzir, etc.

Por enquanto, o que acontece é que o script inicializa a 1ª geração (geração 0) com o agente `RandomAgent`, que basicamente anda aleatoriamente pelo mapa. A partir desta geração, são escolhidos os 6 melhores para reproduzir. A reprodução consiste em mesclar os caminhos dos pais (meio a meio) para gerar 1 indivíduo (cada par de pais gera 1 filho). A próxima geração será composta pelos 10 melhores indivíduos (entre pais e filhos) e a partir da 2ª geração, o agente utilizado é o `EvolutiveAgent`, que executa o caminho gerado pelo processo de reprodução e anda aleatoriamente após percorrer todo o histórico (se sobreviver até lá).

> Esse processo continua até a última geração estar completa