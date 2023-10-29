import json
import difflib
import pandas as pd
import os


def parse_excel_to_json(file_name: str):
    with open("./data/data.json", "r", encoding="utf-8") as file:
        data: dict = json.load(file)
    current_count_file = len(data.keys())
    excel_data = pd.read_excel("./data/files/xxx.xlsx").to_dict()
    print(excel_data)
    new_strings_count = len(excel_data['№'].keys()) - current_count_file
    # print(new_strings_count, len(excel_data.keys()), current_count_file)
    for i in range(new_strings_count):
        number_of_doc = excel_data['№'].get(current_count_file+i)
        doc_type = excel_data['Тип'][number_of_doc-1]
        number = excel_data['Номер'][number_of_doc-1]
        name = excel_data['Название'][number_of_doc-1]
        date = excel_data['Дата выхода'][number_of_doc-1].split(".")
        date = date[2] + "-" + date[1] + "-" + date[0]
        enter_date = excel_data['Дата ввода действие'][number_of_doc-1].split(".")
        enter_date = enter_date[2] + "-" + enter_date[1] + "-" + enter_date[0]
        key_words = ""
        file_stored = False
        file_type = ".pdf"
        data[number_of_doc] = {}
        data[number_of_doc]["type"] = doc_type
        data[number_of_doc]["document_name"] = name
        data[number_of_doc]["number"] = number
        data[number_of_doc]["date"] = date
        data[number_of_doc]["enter_date"] = enter_date
        data[number_of_doc]["key_words"] = key_words
        data[number_of_doc]["file_stored"] = file_stored
        data[number_of_doc]["file_type"] = file_type
    with open('./data/data.json', 'w',  encoding="utf-8") as outfile:
        json.dump(data, outfile, sort_keys=False, ensure_ascii=False, indent=4,  separators=(',', ': '))
    os.remove("./data/files/xxx.xlsx")


def get_matches(name: str, check_name: str):
    arr_name: list = name.split()
    arr_check_name: list = check_name.split()
    matches_count = 0
    for j in range(0, len(arr_check_name)):
        matches = False
        for i in range(0, len(arr_name)):
            matches_percent: float = float(difflib.SequenceMatcher(a=arr_name[i].lower(), b=arr_check_name[j].lower()).ratio())
            if matches_percent >= 0.80:
                matches = True
                break
        if matches:
            matches_count += 1

    if len(arr_check_name) != 0 and matches_count / len(arr_check_name) >= 0.5:
        return True
    else:
        return False


def find_matches_keywords(current_data_keywords, searching_document_keywords):
    for i in range(0, len(searching_document_keywords)):
        for j in range(0, len(current_data_keywords)):
            if difflib.SequenceMatcher(a=searching_document_keywords[i].lower(), b=current_data_keywords[j].lower()).ratio() >= 0.8:
                return True
    return False


def search_documents(searching_document: dict) -> dict:
    found_documents = {}
    with open("./data/data.json", "r", encoding="utf-8") as file:
        data: dict = json.load(file)

    for number_of_document in data.keys():
        current_data: dict = data[number_of_document]

        if current_data["document_name"] == searching_document["document_name"]:
            found_documents[number_of_document] = current_data
            break
        if get_matches(current_data["document_name"], searching_document["document_name"]):
            found_documents[number_of_document] = current_data

        for element_of_document in current_data.keys():
            if searching_document.get(element_of_document) is not None:
                print(current_data[element_of_document], searching_document[element_of_document])
                if current_data[element_of_document] == searching_document[element_of_document]:
                    # TODO: Нужно продумать боллее логичную систему отбора данных по критериям
                    if len(searching_document[element_of_document]) != 0:
                        found_documents[number_of_document] = current_data
                        break
                if element_of_document == "key_words":
                    searching_data_keywords: list = searching_document[element_of_document].split()
                    current_data_keywords: list = current_data[element_of_document].split(", ")

                    if find_matches_keywords(current_data_keywords, searching_data_keywords):
                        found_documents[number_of_document] = current_data
                        print("here")
                        break
    return found_documents


def get_documents(searching_document: dict) -> dict:
    return search_documents(searching_document)