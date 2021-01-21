from enum import Enum

from api import API


class Option(Enum):
    TICKET = 'ticket'
    IPVA = 'ipva'
    DPVAT = 'dpvat'


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

    def _connect(self, method):
        self._api[method] = API(self.license_plate, self.renavam, method)

    def get_json_response(self, method, *, enforce_connection=False):
        """
        Pega a resposta da requisição em json.
        """
        if self._api.get(method) is None:  # Not connected
            if enforce_connection:
                self._connect(method)
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
            self.debt_option.TICKET: "ConsultaMultas",
            self.debt_option.IPVA: "ConsultaIPVA",
            self.debt_option.DPVAT: "ConsultaDPVAT"
        }

        try:
            api_method = option_to_api[self.debt_option]
        except KeyError:
            raise RuntimeError(f"Invalid debt_option: '{self.debt_option}'")

        response_json = self.get_json_response(
            api_method,
            enforce_connection=True
        )

        debts = {
            'IPVAs': response_json.get('IPVAs', {}),
            'DPVATs': response_json.get('DPVATs', {}),
            'Multas': response_json.get('Multas', {}),
        }

        for debt in debts:
            if debts[debt] == {}:
                debts[debt] = None

        return debts
