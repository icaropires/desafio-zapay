#!/bin/python3

import sys
import json

from parser import SPParser
from service import SPService, DebtOption


def get_user_input():
    """
    Captura a entrada do usuário pela CLI.
    """
    valid_options = frozenset(o.value for o in DebtOption)

    try:
        _, debt_option, license_plate, renavam = sys.argv
    except ValueError:
        options_str = '|'.join(valid_options)

        print(
            "Argumentos inválidos."
            f"\nUso: python3 main.py [{options_str}] [placa] [renavam]"
        )
        sys.exit(1)

    if debt_option not in valid_options:
        options_str = ', '.join(valid_options)
        error_msg = f"Opção inválida: '{debt_option}'! Válidas: {options_str}."

        # raise ValueError(error_msg)
        print(error_msg)
        sys.exit(1)

    return debt_option, license_plate, renavam


def parse(raw_query, debt_option):
    """
    Aplica o parser no resultado da query.
    """
    parser = SPParser(raw_query)

    return parser.collect_debts(debt_option)


def run_query(debt_option, license_plate, renavam):
    """
    Invoca o serviço para realizar busca na API.
    """
    debt_option = DebtOption(debt_option)

    sp_service = SPService(
        license_plate=license_plate,
        renavam=renavam,
        debt_option=debt_option
    )

    try:
        raw_query = sp_service.debt_search()
    except Exception as error:
        print(f"Não foi possível realizar a busca: {error}")
        sys.exit(1)

    return parse(raw_query, debt_option)


if __name__ == "__main__":
    debt_option, license_plate, renavam = get_user_input()

    result = run_query(debt_option, license_plate, renavam)

    print(
        json.dumps(result, indent=4, ensure_ascii=False)
    )
    sys.exit(0)
