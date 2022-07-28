import sys
from pesquisador import MedsTable, SearchCategory, Seeker, Menu
from read_csv_file import read_csv_file


def main():
    menu = Menu()
    meds_table = MedsTable(read_csv_file())
    category = SearchCategory()
    searchs = {
        1: category.by_name,
        2: category.by_bar_code,
        3: category.by_price,
        4: category.by_therapeutic_class,
    }

    while True:
        menu.print_menu()
        choice = menu.search_choice()
        if 1 <= choice <= 5:
            searchs.get(choice)(Seeker(), meds_table.table)
        elif choice == 0:
            print("Obrigado por utilizar o pesquisador!.\n")
            sys.exit()


if __name__ == "__main__":
    main()
