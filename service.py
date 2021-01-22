from enum import Enum

from api import API


class Option(Enum):
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

        self.debt_option = Option(debt_option)
        self.license_plate = license_plate
        self.renavam = renavam

        self._api = {}

    def _connect_to_api(self, method):
        self._api[method] = API(self.license_plate, self.renavam, method)

    def get_json_response(self, method, *, enforce_connection=False):
        """
        Pega a resposta da requisição em json.
        """
        method = method.value

        # Connect just once
        if self._api.get(method) is None:  # Not connected
            if enforce_connection:
                self._connect_to_api(method)
            else:
                raise RuntimeError(
                    f"Not connected to API for method: '{method}'"
                )

        return self._api[method].fetch()

    def debt_search(self):
        """
        Pega os débitos de acordo com a opção passada.
        """

        option_to_api = {
            self.debt_option.TICKET: ApiMethod.QUERY_TICKETS,
            self.debt_option.IPVA: ApiMethod.QUERY_IPVA,
            self.debt_option.DPVAT: ApiMethod.QUERY_DPVAT,
        }

        try:
            api_method = option_to_api[self.debt_option]
        except KeyError:
            raise RuntimeError(f"Invalid debt_option: '{self.debt_option}'")

        response_json = self.get_json_response(
            api_method,
            enforce_connection=True
        )

        ipvas = response_json.get('IPVAs') or {}
        dpvats = response_json.get('DPVATs') or {}
        tickets = response_json.get('Multas') or {}

        debts = {
            'IPVAs': ipvas.get('IPVA'),
            'DPVATs': dpvats.get('DPVAT'),
            'Multas': tickets.get('Multa'),
        }

        return debts
