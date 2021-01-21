#!/bin/python3

import sys
import json
from service import SPService
from parser import SPParser
from enum import Enum


class Option(Enum):
    TICKET = 'ticket'
    IPVA = 'ipva'
    DPVAT = 'dpvat'


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


def build_options(search_result):
    parser = SPParser(search_result)

    options = {
        Option.TICKET: parser.collect_ticket_debts,
        Option.IPVA: parser.collect_ipva_debts,
        Option.DPVAT: parser.collect_insurance_debts,
    }

    return options


def run_search(debt_option, license_plate, renavam):
    sp_service = SPService(
        license_plate=license_plate,
        renavam=renavam,
        debt_option=debt_option
    )

    try:
        search_result = sp_service.debt_search()
    except Exception as exc:
        print(exc)
        sys.exit(1)

    options = build_options(search_result)

    try:
        option = Option(debt_option)
        run_option = options[option]
    except KeyError:
        valid_options = ','.join(options.keys())

        print(f"Opção inválida. Escolha entre: {valid_options}")
        sys.exit(1)

    return run_option()


if __name__ == "__main__":
    debt_option, license_plate, renavam = get_user_input()

    result = run_search(debt_option, license_plate, renavam)

    print(
        json.dumps(result, indent=4, ensure_ascii=False)
    )
    sys.exit(0)
