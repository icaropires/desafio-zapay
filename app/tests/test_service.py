import pytest
from service import SPService, DebtOption, ApiMethod


@pytest.mark.parametrize("debt_option,main_key,inner_keys,api_method", [
    # Eventually, 'Guia' appears as a key for 'Multas' but not always
    (DebtOption.TICKET, "Multas",
        ('AIIP', 'Valor', 'DescricaoEnquadramento'), ApiMethod.QUERY_TICKETS),

    (DebtOption.DPVAT, "DPVATs",
        ('Valor', 'Exercicio'), ApiMethod.QUERY_DPVAT),

    (DebtOption.IPVA, "IPVAs",
        ('Cota', 'Valor', 'Exercicio'), ApiMethod.QUERY_IPVA),

    (DebtOption.LICENSING, "Licenciamentos",
        ('Valor', 'Exercicio'), ApiMethod.QUERY_LICENSING),
])
def test_debt_search(mocker, debt_option, main_key, inner_keys,
                     api_method, api_data):

    sp_service = SPService(debt_option, 'ABC1234', '11111111111')

    # A classe API do api.py já é um mock, mas simulando aqui um caso real
    #   de uso do mock para satisfazer a atividade BÔNUS 5 do LEIA-ME.pdf
    mock_api = mocker.Mock()
    mock_api.fetch.return_value = api_data[api_method.value]
    sp_service._api[api_method] = mock_api

    result = sp_service.debt_search()

    for key, values in result.items():
        if key != main_key:
            assert values is None
            continue

        assert values

        for element in values:
            assert set(element.keys()) >= set(inner_keys)


def test_debt_search_all():
    sp_service = SPService(DebtOption.ALL, 'ABC1234', '11111111111')
    result = sp_service.debt_search()

    for value in result.values():
        assert value is not None


@pytest.mark.parametrize('plate,result', [
    # To normalize
    ('ABC1C34', 'ABC1234'),
    ('ACI6J67', 'ACI6967'),
    ('MAA0B92', 'MAA0192'),
    ('BCG7G17', 'BCG7617'),
    ('FAL7D00', 'FAL7300'),
    ('HAH2H74', 'HAH2774'),
    ('POD5A60', 'POD5060'),

    # To keep
    ('ABC1234', 'ABC1234'),
    ('ACI6967', 'ACI6967'),
])
def test_license_plate_normalization(plate, result):
    sp_service = SPService(DebtOption.TICKET, plate, '11111111111')

    assert sp_service.license_plate == result
