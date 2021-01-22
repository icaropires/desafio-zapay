from service import DebtOption

UNIQUE_INSTALLMENTS = frozenset([0, 7, 8])


class SPParser:
    def __init__(self, data):
        self._data = data

    def collect_debts(self, debt_option):
        parsers = {
            DebtOption.TICKET: ('Multas', self._parse_ticket),
            DebtOption.IPVA: ('IPVAs', self._parse_ipva),
            DebtOption.DPVAT: ('DPVATs', self._parse_insurance),
            DebtOption.LICENSING: ('Licenciamentos', self._parse_licensing),
        }

        if debt_option == DebtOption.ALL:
            debts = (self.collect_debts(option) for option in parsers)
            return [debt for debt_list in debts for debt in debt_list]

        main_key, method = parsers[debt_option]

        debts = self.get_debts_from_json(main_key)

        if debts is None:
            return []

        return [method(debt) for debt in debts]

    def get_debts_from_json(self, category):
        return self._data.get(category)

    @staticmethod
    def _parse_ticket(debt):
        return {
            'amount': float(debt.get('Valor'))/100,
            'auto_infraction': debt.get('AIIP'),
            'description': debt.get('DescricaoEnquadramento'),
            'title': 'Infração de Trânsito',
            'type': "ticket",
        }

    @staticmethod
    def _parse_ipva(debt):
        year = debt.get('Exercicio')
        description = f"IPVA {debt.get('Exercicio')}"

        installment = debt.get('Cota')
        is_installment_unique = installment in UNIQUE_INSTALLMENTS
        installment = 'Única' if is_installment_unique else installment

        subtitle = f"- Cota {installment}"

        formatted = {
            'amount': float(debt.get('Valor'))/100,
            'description': description,
            'title': f"IPVA {subtitle}",
            'type': 'ipva',
            'year': year,
        }

        if installment is not None:
            installment = 'unique' if is_installment_unique else installment

            formatted['installment'] = installment

        return formatted

    @staticmethod
    def _parse_insurance(debt):
        return {
            'amount': float(debt.get('Valor'))/100,
            'description': debt.get(
                'DescricaoServico',
                f"DPVAT {debt['Exercicio']}"
            ),
            'title': 'Seguro Obrigatório',
            'type': 'insurance',
            'year': debt['Exercicio'],
        }

    @staticmethod
    def _parse_licensing(debt):
        return {
            "amount": float(debt.get('Valor'))/100,
            "title": f"Licenciamento {debt['Exercicio']}",
            "description": "Licenciamento do Veículo",
            "year": debt["Exercicio"],
            "type": "licensing"
        }
