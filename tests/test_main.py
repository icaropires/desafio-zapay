import pytest

from service import DebtOption
from main import run_query


DEBT_OPTIONS_KEYS = {
    DebtOption.TICKET: ("amount", "description",
                        "auto_infraction", "title", "type"),

    DebtOption.DPVAT: ("amount", "description", "title", "type", "year"),

    DebtOption.IPVA: ("amount", "description", "title",
                      "type", "year", "installment"),
}

DEBT_OPTION_TYPES = {
    DebtOption.TICKET: "ticket",
    DebtOption.IPVA: "ipva",
    DebtOption.DPVAT: "insurance"
}


@pytest.mark.parametrize(
    "debt_option,expected_keys",
    DEBT_OPTIONS_KEYS.items()
)
def test_run_query(debt_option, expected_keys):
    # Num caso real teria que garantir que existem registros
    results = run_query(debt_option, "ABC1234", "11111111111")

    assert results

    expected_keys = DEBT_OPTIONS_KEYS[debt_option]

    for result in results:
        assert set(result.keys()) == set(expected_keys)
        assert result["type"] == DEBT_OPTION_TYPES[debt_option]


def test_run_query_all():
    # Num caso real teria que garantir que existem registros
    results = run_query(DebtOption.ALL, "ABC1234", "11111111111")

    assert results

    types = set(result['type'] for result in results)

    assert types == set(DEBT_OPTION_TYPES.values())
