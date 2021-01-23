import pytest


@pytest.fixture
def api_data():
    # Same data than api.py
    return {
        "ConsultaMultas": {
            "Multas": {
                "Multa": [
                    {
                        "AIIP": "5E5E5E5E  ",
                        "Guia": 472535212,
                        "Valor": 20118,
                        "DescricaoEnquadramento": "Estacionar em Desacordo"
                                                  " com a Sinalizacao."
                    },
                    {
                        "AIIP": "6F6F6F6F  ",
                        "Valor": 13166,
                        "DescricaoEnquadramento": "Trans. Veloc. Super. a"
                                                  " Maxima Permitida"
                                                  "em Ate 20%."
                    }
                ]
            },
            "Servico": "Multas",
            "Veiculo": {
                "UF": "SP",
                "Placa": "ABC1234",
                "CPFCNPJ": "000.000.000-00",
                "Renavam": "11111111111",
                "Proprietario": "JOHN",
            }
        },
        "ConsultaIPVA": {
            "IPVAs": {
                "IPVA": [
                    {
                        "Cota": 8,
                        "Valor": 136569,
                        "Exercicio": 2021,
                    },
                    {
                        "Cota": 2,
                        "Valor": 101250,
                        "Exercicio": 2020,
                    }
                ]
            },
            "Servico": "IPVA",
            "Veiculo": {
                "UF": "SP",
                "Placa": "ABC1234",
                "CPFCNPJ": "000.000.000-00",
                "Renavam": "11111111111",
                "Proprietario": "JOHN",
            }
        },
        "ConsultaDPVAT": {
            "DPVATs": {
                "DPVAT": [
                    {
                        "Valor": 523,
                        "Exercicio": 2020,
                    }
                ]
            },
            "Servico": "DPVAT",
            "Veiculo": {
                "UF": "SP",
                "Placa": "ABC1234",
                "CPFCNPJ": "000.000.000-00",
                "Renavam": "11111111111",
                "Proprietario": "JOHN",
            }
        },
        "ConsultaLicenciamento": {
            "Servico": "Licenciamento",
            "Veiculo": {
                "UF": "SP",
                "Placa": "ABC1234",
                "CPFCNPJ": "000.000.000-00",
                "Renavam": "11111111111",
                "Proprietario": "JOHN",
            },
            "Exercicio": 2021,
            "TaxaLicenciamento": 9891
        }
    }
