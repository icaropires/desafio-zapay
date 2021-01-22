import pytest
from service import SPService, Option


@pytest.mark.parametrize("option,main_key,main_inner_key,inner_keys", [
    # Eventually, 'Guia' appears as a key for 'Multas' but not always
    (Option.TICKET, "Multas", "Multa",
        ('AIIP', 'Valor', 'DescricaoEnquadramento')),

    (Option.DPVAT, "DPVATs", "DPVAT",
        ('Valor', 'Exercicio')),

    (Option.IPVA, "IPVAs", "IPVA",
        ('Cota', 'Valor', 'Exercicio')),
])
def test_debt_search(option, main_key, main_inner_key, inner_keys):
    sp_service = SPService(option, 'ABC1234', '11111111111')
    result = sp_service.debt_search()

    for key, value in result.items():
        if key != main_key:
            assert value is None
            continue

        assert value.get(main_inner_key) is not None

        for element in value[main_inner_key]:
            assert set(element.keys()) >= set(inner_keys)
