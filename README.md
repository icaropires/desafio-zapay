# Desafio - Zapay

[![CI](https://github.com/icaropires/desafio-zapay/workflows/CI/badge.svg)](https://github.com/icaropires/desafio-zapay/actions?query=workflow%3ACI)
[![Maintainability](https://api.codeclimate.com/v1/badges/dc1cb7ea704a290e125e/maintainability)](https://codeclimate.com/github/icaropires/desafio-zapay/maintainability)
[![codecov](https://codecov.io/gh/icaropires/desafio-zapay/branch/main/graph/badge.svg?token=I001DHBL7A)](https://codecov.io/gh/icaropires/desafio-zapay)

Repositório contendo meu resultado do desafio técnico para vaga de desenvolvedor back-end na [Zapay Pagamentos](https://usezapay.com.br/). Para mais detalhes, consulte o [LEIA-ME](./LEIA-ME.pdf).

## Instalando

A aplicação não necessita de instalação, ela não possui dependências externas e suporta versões do python >= 3.7.

Para desenvolvimento, pode ser executado o seguinte comando para instalar algumas ferramentas de checagem:

``` bash
$ pip3 install -r requirements-dev.txt
```

## Executando a aplicação

A aplicação possui uma CLI que entrega resultados de algumas requisições simuladas.

A sintaxe da CLI é a seguinte:

``` bash
# De dentro da pasta app
$ python3 main.py [all|tickets|ipva|dpvat|licensing] [placa_do_veículo] [renavam_do_veículo]
```

Exemplo que busca todos os débitos de um veículo com placa `ABC1C34` e renavam `11111111111`:

``` bash
# De dentro da pasta app
$ python3 main.py all ABC1C34 11111111111
```

## Executando os testes

Para executar os testes, instale as dependências do `requirements-dev.txt` e utilize algum dos seguintes comandos de **dentro da pasta `app`**:

``` python3
$ python3 -m pytest
```

``` python3
# Ou com cobertura de testes:
$ python3 -m pytest --cov=. tests
```
