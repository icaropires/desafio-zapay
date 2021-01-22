UNIQUE_INSTALLMENTS = frozenset([0, 7, 8])


class SPParser:
    def __init__(self, data):
        self._data = data

    def collect_debts(self, option):
        parsers = {
            option.TICKET: ('Multas', self._parse_ticket),
            option.IPVA: ('IPVAs', self._parse_ipva),
            option.DPVAT: ('DPVATs', self._parse_insurance),
        }

        main_key, method = parsers[option]

        debts = self.get_debts_from_json(main_key)

        if debts is None:
            return []

        debts = debts[main_key[:-1]]  # TODO: remove

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
            # Why change 'Única' to 'unique'?
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
            'year': debt.get('Exercicio'),
        }
