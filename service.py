from enum import Enum

from api import API


class DebtOption(Enum):
    ALL = 'all'
    TICKET = 'tickets'
    IPVA = 'ipva'
    DPVAT = 'dpvat'


class ApiMethod(Enum):
    QUERY_TICKETS = 'ConsultaMultas'
    QUERY_IPVA = 'ConsultaIPVA'
    QUERY_DPVAT = 'ConsultaDPVAT'


class SPService:
    """
    Conecta com o webservice do Detran-SP.
    """

    def __init__(self, debt_option, license_plate, renavam):
        """
        Construtor.
        """

        self.debt_option = DebtOption(debt_option)
        self.license_plate = license_plate
        self.renavam = renavam

        self._api = {}

    def _connect_to_api(self, api_method):
        self._api[api_method] = API(self.license_plate,
                                    self.renavam, api_method)

    def get_json_response(self, api_method, *, enforce_connection=False):
        """
        Pega a resposta da requisição em json.
        """
        api_method = api_method.value

        # Connect just once
        if self._api.get(api_method) is None:  # Not connected
            if enforce_connection:
                self._connect_to_api(api_method)
            else:
                raise RuntimeError(
                    f"Not connected to API for method: '{api_method}'"
                )

        return self._api[api_method].fetch()

    def _query_debt_option(self, debt_option):
        option_to_api = {
            debt_option.TICKET: ApiMethod.QUERY_TICKETS,
            debt_option.IPVA: ApiMethod.QUERY_IPVA,
            debt_option.DPVAT: ApiMethod.QUERY_DPVAT,
        }

        try:
            api_method = option_to_api[debt_option]
        except KeyError:
            raise RuntimeError(f"Invalid debt_option: '{debt_option}'")

        response_json = self.get_json_response(
            api_method,
            enforce_connection=True
        )

        return response_json

    def _query_all_debt_options(self):
        responses = (self._query_debt_option(m) for m in DebtOption
                     if m != DebtOption.ALL)

        response_json = {}
        for response in responses:
            response_json.update(response)

        return response_json

    def debt_search(self):
        """
        Pega os débitos de acordo com a opção passada.
        """
        if self.debt_option == DebtOption.ALL:
            response_json = self._query_all_debt_options()
        else:
            response_json = self._query_debt_option(self.debt_option)

        ipvas = response_json.get('IPVAs') or {}
        dpvats = response_json.get('DPVATs') or {}
        tickets = response_json.get('Multas') or {}

        debts = {
            'IPVAs': ipvas.get('IPVA'),
            'DPVATs': dpvats.get('DPVAT'),
            'Multas': tickets.get('Multa'),
        }

        return debts
