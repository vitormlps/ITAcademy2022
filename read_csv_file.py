import csv


def read_csv_file() -> dict[str, dict]:
    with open("TA_PRECO_MEDICAMENTO.csv", "r") as file:
        table = table_cleaner(csv.DictReader(file, delimiter=";"))
        return table


def table_cleaner(table) -> dict[str, dict]:
    to_remain = [
        "SUBSTÂNCIA",
        "LABORATÓRIO",
        "EAN 1",
        "PRODUTO",
        "APRESENTAÇÃO",
        "CLASSE TERAPÊUTICA",
        "PF Sem Impostos",
        "RESTRIÇÃO HOSPITALAR",
        "TARJA",
    ]
    dict_temp: dict = {}
    temp: dict = {}

    for row in table:
        for header, info in row.items():
            if header in to_remain:
                temp.setdefault(header, info)
        dict_temp.setdefault(f"{temp['PRODUTO']} {temp['APRESENTAÇÃO']}", temp.copy())
        temp.clear()

    for content in dict_temp.values():
        for header, info in content.items():
            if header == "SUBSTÂNCIA" and ";" in info:
                content[header] = info.strip().split(";")
                for pos, sub_info in enumerate(content[header]):
                    content[header][pos] = sub_info.strip()
                content[header] = tuple(content[header])

            if header == "CLASSE TERAPÊUTICA" and "-" in info:
                content[header] = info.strip().split("-")
                for pos, sub_info in enumerate(content[header]):
                    content[header][pos] = sub_info.strip()
                content[header] = tuple(content[header])

            if header == "TARJA":
                content[header] = info.replace("Tarja", "").replace("-", "").strip()

    table = dict_temp
    return table


read_csv_file()
