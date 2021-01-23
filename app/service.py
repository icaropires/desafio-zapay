from enum import Enum

from api import API


class DebtOption(Enum):
    ALL = 'all'
    TICKET = 'tickets'
    IPVA = 'ipva'
    DPVAT = 'dpvat'
    LICENSING = 'licensing'


class ApiMethod(Enum):
    QUERY_TICKETS = 'ConsultaMultas'
    QUERY_IPVA = 'ConsultaIPVA'
    QUERY_DPVAT = 'ConsultaDPVAT'
    QUERY_LICENSING = 'ConsultaLicenciamento'


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

        self._normalize_license_plate()

    def _normalize_license_plate(self):
        """
        Transforma a placa para o padrão antigo, se for mercosul.
        """
        mapping = {k: str(v) for v, k in enumerate('ABCDEFGHIJ')}

        change_index = 4
        old_char = self.license_plate[change_index]
        new_char = mapping.get(old_char, old_char)

        plate = self.license_plate
        plate = plate[:change_index] + new_char + plate[change_index+1:]

        self.license_plate = plate

    def _connect_to_api(self, api_method):
        """
        Se conecta à API.
        """
        self._api[api_method] = API(self.license_plate,
                                    self.renavam, api_method.value)

    def get_json_response(self, api_method, *, enforce_connection=False):
        """
        Pega a resposta da requisição em json.
        """

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
        """
        Dado a opção de busca, realiza a query na API
        """
        option_to_api = {
            DebtOption.TICKET: ApiMethod.QUERY_TICKETS,
            DebtOption.IPVA: ApiMethod.QUERY_IPVA,
            DebtOption.DPVAT: ApiMethod.QUERY_DPVAT,
            DebtOption.LICENSING: ApiMethod.QUERY_LICENSING,
        }

        try:
            api_method = option_to_api[debt_option]
        except KeyError as error:
            error_msg = f"Invalid debt_option: '{debt_option}'"
            raise RuntimeError(error_msg) from error

        response_json = self.get_json_response(
            api_method,
            enforce_connection=True
        )

        # Special handling for licensing
        if debt_option == DebtOption.LICENSING:
            response_json = self._normalize_licensing(response_json)

        return response_json

    def _query_all_debt_options(self):
        """
        Realiza busca na API para todas as opções de débito
        """
        responses = (self._query_debt_option(m) for m in DebtOption
                     if m != DebtOption.ALL)

        response_json = {}
        for response in responses:
            response_json.update(response)

        return response_json

    @staticmethod
    def _normalize_licensing(response):
        """
        Transforma o resultado da query do atributo de licensiamento para o
        mesmo formato dos outros atributos.
        """
        normalized = {}

        normalized['Licenciamentos'] = {
            'Licenciamento': [
                {
                    'Valor': response['TaxaLicenciamento'],
                    'Exercicio': response['Exercicio'],
                }
            ]
        }

        return normalized

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
        licensings = response_json.get('Licenciamentos') or {}

        debts = {
            'IPVAs': ipvas.get('IPVA'),
            'DPVATs': dpvats.get('DPVAT'),
            'Multas': tickets.get('Multa'),
            'Licenciamentos': licensings.get('Licenciamento'),
        }

        return debts
