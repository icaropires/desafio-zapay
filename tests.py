import pytest
from main import run_search, Option


@pytest.mark.parametrize("option", tuple(Option))
def test_search_ticket(option):
    # Num caso real teria que garantir que existem registros primeiro
    result = run_search(option.value, "ABC1234", "11111111111")

    expected_keys = {
        Option.TICKET: ("amount", "auto_infraction", "title", "type"),
        Option.DPVAT: ("amount", "description", "title", "type", "year"),
        Option.IPVA: ("amount", "description", "title", "type",
                      "year", "installment"),
    }

    assert result

    first = result[0]

    for key in expected_keys[option]:
        assert key in first.keys()

    expected_types = {
        Option.TICKET: "ticket",
        Option.IPVA: "ipva",
        Option.DPVAT: "insurance"
    }

    assert first["type"] == expected_types[option]
