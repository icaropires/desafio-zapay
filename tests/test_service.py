import pytest
from service import SPService, DebtOption


@pytest.mark.parametrize("debt_option,main_key,inner_keys", [
    # Eventually, 'Guia' appears as a key for 'Multas' but not always
    (DebtOption.TICKET, "Multas",
        ('AIIP', 'Valor', 'DescricaoEnquadramento')),

    (DebtOption.DPVAT, "DPVATs",
        ('Valor', 'Exercicio')),

    (DebtOption.IPVA, "IPVAs",
        ('Cota', 'Valor', 'Exercicio')),
])
def test_debt_search(debt_option, main_key, inner_keys):
    sp_service = SPService(debt_option, 'ABC1234', '11111111111')
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
