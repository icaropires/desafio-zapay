import pytest
from service import SPService, Option


@pytest.mark.parametrize("option,main_key,inner_keys", [
    # Eventually, 'Guia' appears as a key for 'Multas' but not always
    (Option.TICKET, "Multas",
        ('AIIP', 'Valor', 'DescricaoEnquadramento')),

    (Option.DPVAT, "DPVATs",
        ('Valor', 'Exercicio')),

    (Option.IPVA, "IPVAs",
        ('Cota', 'Valor', 'Exercicio')),
])
def test_debt_search(option, main_key, inner_keys):
    sp_service = SPService(option, 'ABC1234', '11111111111')
    result = sp_service.debt_search()

    for key, values in result.items():
        if key != main_key:
            assert values is None
            continue

        for element in values:
            assert set(element.keys()) >= set(inner_keys)
