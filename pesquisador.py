#### IMPORTS #############################################################
from dataclasses import dataclass
from typing import Protocol

#### CLASSES #############################################################
# Receiver
@dataclass
class MedsTable:
    __table: dict[str, dict]

    @property
    def table(self) -> dict[str, dict]:
        return self.__table


# Command interface
class Search(Protocol):
    def search(self, by_input, meds_table):
        ...


# Command concreto
class Seeker:
    def search(self, by_input, meds_table: dict[str, dict]):
        found = False
        for header, med_info in meds_table.items():
            if (
                by_input in header
                or by_input in med_info["SUBSTÂNCIA"]
                or by_input in med_info["EAN 1"]
                or by_input in med_info["CLASSE TERAPÊUTICA"]
                or by_input in med_info["PF Sem Impostos"]
            ):
                print(
                    f"""Nome: {med_info["PRODUTO"]} | Apresentação: {med_info["APRESENTAÇÃO"]}
Valor: R${replace_separator(med_info["PF Sem Impostos"])} | Classe Terapêutica: {med_info["CLASSE TERAPÊUTICA"]}
Substância(s): {med_info["SUBSTÂNCIA"]} | Tarja: {med_info["TARJA"]}
Restrição Hospitalar: {med_info["RESTRIÇÃO HOSPITALAR"]} | Laboratório: {med_info["LABORATÓRIO"]}
                """
                )
                found = True

        if not found:
            not_found_msg()
            return False
        return True


# Invoker
class SearchCategory:
    def by_name(self, seeker: Search, meds_table: dict[str, dict]):
        nome_med = input(
            "Informe o nome do medicamento [digite 'Não' p/ voltar ao menu]: "
        ).upper()

        if is_no(nome_med):
            return True
        if not is_string(nome_med):
            invalid_msg()
            return self.by_name(seeker, meds_table)

        found = seeker.search(nome_med, meds_table)

        if not found:
            return self.by_name(seeker, meds_table)
        return input("Aperte ENTER para continuar.")

    def by_bar_code(self, seeker: Search, meds_table: dict[str, dict]):
        cod_barras = input(
            "Informe o código de barras do medicamento [digite 'Não' p/ voltar ao menu]: "
        )

        if is_no(cod_barras):
            return True
        if not is_number(cod_barras):
            invalid_msg()
            return self.by_bar_code(seeker, meds_table)

        found = seeker.search(cod_barras, meds_table)

        if not found:
            return self.by_bar_code(seeker, meds_table)
        return input("Aperte ENTER para continuar.")

    def by_price(self, seeker: Search, meds_table: dict[str, dict]):
        value = input(
            "Informe o valor aproximado do medicamento [digite 'Não' p/ voltar ao menu]: "
        )

        if is_no(value):
            return True
        if not is_number(value):
            invalid_msg()
            return self.by_price(seeker, meds_table)

        found = seeker.search(value, meds_table)

        if not found:
            return self.by_price(seeker, meds_table)
        return input("Aperte ENTER para continuar.")

    def by_therapeutic_class(self, seeker: Search, meds_table):
        therap_class = input(
            "Informe a classe terapêutica do medicamento [digite 'Não' p/ voltar ao menu]: "
        ).upper()

        if is_no(therap_class):
            return True

        found = seeker.search(therap_class, meds_table)

        if not found:
            return self.by_therapeutic_class(seeker, meds_table)
        return input("Aperte ENTER para continuar.")


class Menu:
    def print_menu(self):
        print(
            """#### MENU ####
1. Consultar medicamentos por NOME
2. Consultar medicamentos por CÓDIGO DE BARRAS
3. Consultar medicamentos por PREÇO
4. Consultar medicamentos por CLASSE TERAPÊUTICA
0. Terminar o programa"""
        )

    def search_choice(self):
        choice = input("Digite o número de acordo com sua escolha das opcões acima: ")
        if not choice.isdigit() or int(choice) >= 6:
            invalid_msg()
            return self.search_choice()
        return int(choice)


#### MISC #############################################################
def invalid_msg():
    print("Entrada inválida.\n")


def not_found_msg():
    print("Valor não encontrado.\n")


def is_string(string):
    if string.upper().replace(" ", "").isalpha():
        return True
    return False


def is_no(string):
    if string.upper().strip() in ("N", "NA", "NO", "NAO", "NÃO"):
        return True
    return False


def is_number(number):
    if number.isdigit() or int(number) > 0:
        return True
    return False


def replace_separator(number):
    number_str = str(number)

    if "," in number_str:
        number_str = number_str.replace(",", ".")
    elif "." in number_str:
        number_str = number_str.replace(".", ",")

    return number_str
