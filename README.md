# codificador-morse
Um codificador para código morse escrito em python

## Dependências

- `PortAudio`
- `Python3.12 >=`

## Configuração de ambiente

O programa foi projetado para ser utilizado dentro de um espaço separado do workspace do usuário por questões de evitar conflitos. Desse modo, recomenda-se a utilização de um ambiente virtual python para a instalação das dependências.

### Uso do ambiente virtual com `uv`

O pacote `uv` nos permite ter um controle mais refinado da versão do python que estamos utilizando, então caso opte por usar ele os comandos são esses:

```bash
uv venv --python 3.12 .venv # cria o ambiente virtual com python v3.12

# Sistemas Unix like
source .venv/bin/activate 

# se seu sistema for Windows, use: 
venv\Scripts\activate.bat
```

# Ambiente virtual com python venv

Caso opte por utilizar o módulo nativo do python `venv`, então use os comando a seguir:

```bash
# Windows
python -m venv venv
venv\Scripts\activate.bat

# Linux
python3 -m venv venv
source venv/bin/activate
```

### Instalação das dependências

Utilize o comando pip de acordo com o ambiente virtual que foi utilizado previamente:

```bash
# caso tenha usado o uv
uv pip install .

# caso tenha usado o venv
pip install .
```

## Execução

Para executar o código, basta executar o comando `python -m src.codificador-morse.main`.

## Autores
- Arthur Negrão
- Murilo Henrique
