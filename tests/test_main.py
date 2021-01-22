import pytest

from service import Option
from main import run_query


@pytest.mark.parametrize("option,keys", [
    (Option.TICKET, ("amount", "description", "auto_infraction", "title",
                                                                 "type")),

    (Option.DPVAT, ("amount", "description", "title", "type", "year")),

    (Option.IPVA, ("amount", "description", "title", "type",
                                                     "year", "installment")),
])
def test_run_query(option, keys):
    # Num caso real teria que garantir que existem registros primeiro
    result = run_query(option.value, "ABC1234", "11111111111")

    assert result

    first = result[0]

    assert set(first.keys()) == set(keys)

    expected_types = {
        Option.TICKET: "ticket",
        Option.IPVA: "ipva",
        Option.DPVAT: "insurance"
    }

    assert first["type"] == expected_types[option]
