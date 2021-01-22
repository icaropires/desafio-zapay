#!/bin/python3

import sys
import json

from service import SPService, Option
from parser import SPParser


def get_user_input():
    valid_options = tuple(o.value for o in Option)

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
    parser = SPParser(raw_query)

    return parser.collect_debts(debt_option)


def run_query(debt_option, license_plate, renavam):
    debt_option = Option(debt_option)

    sp_service = SPService(
        license_plate=license_plate,
        renavam=renavam,
        debt_option=debt_option
    )

    # try:
    raw_query = sp_service.debt_search()
    # except Exception as exc:  # TODO: better handling
    #     print(exc)
    #     sys.exit(1)

    return parse(raw_query, debt_option)


if __name__ == "__main__":
    debt_option, license_plate, renavam = get_user_input()

    result = run_query(debt_option, license_plate, renavam)

    print(
        json.dumps(result, indent=4, ensure_ascii=False)
    )
    sys.exit(0)
