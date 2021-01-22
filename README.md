# Desafio - Zapay

[![CI](https://github.com/icaropires/desafio-zapay/workflows/CI/badge.svg)](https://github.com/icaropires/desafio-zapay/actions?query=workflow%3ACI)
[![Maintainability](https://api.codeclimate.com/v1/badges/dc1cb7ea704a290e125e/maintainability)](https://codeclimate.com/github/icaropires/desafio-zapay/maintainability)
[![codecov](https://codecov.io/gh/icaropires/desafio-zapay/branch/main/graph/badge.svg?token=I001DHBL7A)](https://codecov.io/gh/icaropires/desafio-zapay)

Repositório contendo resultado ao desafio técnico para vaga de desenvolvedor backend para a [Zapay Pagamentos](https://usezapay.com.br/). Mais detalhes [LEIA-ME](./LEIA-ME.pdf).

## Instalando

A aplicação não necessida de instalação, ela não possui dependências externas e suporta versões do python >= 3.7.

Para desenvolvimento, pode ser executado o seguinte comando, para instalar algumas ferramentas de checagem:

``` bash
$ pip3 install -r requirements-dev.txt
```

## Executando a aplicação

A aplicação possui uma CLI que entrega resultados de algumas requisições simuladas.

A sintaxe da CLI é a seguinte:

``` bash
# De dentro da pasta app
$ python3 main.py [all|tickets|ipva|dpvat] [placa do veículo] [renavam do veículo]
```

## Executando os testes

Para executar os testes, instale o `pytest` e utilize o seguinte comando na raiz do repositório:

``` python3
# De dentro da pasta app
$ python3 -m pytest
```

ou com cobertura de testes:

``` python3
# De dentro da pasta app
$ python3 -m pytest --cov=. tests
```
