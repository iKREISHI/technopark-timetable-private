"""
Module for creating a schedule in the classrooms of the ShSPU Technopark.
"""
import locale
import requests
import json
import openpyxl.styles
import translate
import datetime
import copy
import os


def json_to_excel(json_couples, json_list="http://tpbook2.shgpi/api/v0/get-auditoriums/?format=json", lang="ru"):
    """
Creates an Excel file.
Keyword arguments:
json_couples (str): link to JSON file with pairs
json_list (str): link to JSON file with audiences (default "http://tpbook2.shgpi/api/v0/get-auditoriums/?format=json")
lang (str): the language in which the Excel file will be created (default "ru")
    """
    weekdays = (
        ("ПН", "MO"),
        ("ВТ", "TU"),
        ("СР", "WE"),
        ("ЧТ", "TH"),
        ("ПТ", "FR"),
        ("СБ", "SA"),
    )
    times = (
        "8:00-9:30",
        "9:40-11:10",
        "11:20-12:50",
        "13:20-14:50",
        "15:00-16:30",
        "16:40-18:10",
    )
    path = os.getcwd()
    couples_indexes = {}
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    teacher_name = ''
    let_num = 2
    row_num = 3
    times_index = 0
    sym_count = 0
    skip = False
    response = requests.get(json_list)
    if response.status_code == 200:
        data = json.loads(response.text)
    else:
        return "ERROR"
    auditoriums_num = len(data)
    schedule = openpyxl.Workbook()
    schedule.remove(schedule.active)
    if lang == "ru":
        sheet = schedule.create_sheet("Расписание")
    else:
        sheet = schedule.create_sheet("Schedule")
    sheet.freeze_panes = "C3"
    sheet.row_dimensions[1].height = 25
    sheet.row_dimensions[2].height = 70
    for auditorium in data:
        sheet.column_dimensions[alphabet[let_num]].width = 50
        couples_indexes[auditorium["name"]] = []
        sheet[f"{alphabet[let_num]}1"] = auditorium["name"]
        sheet[f"{alphabet[let_num]}1"].font = openpyxl.styles.Font(name="Times New Roman", size=22, bold=True)
        sheet[f"{alphabet[let_num]}1"].alignment = openpyxl.styles.Alignment(horizontal="center", vertical="center")
        sheet[f"{alphabet[let_num]}1"].border = openpyxl.styles.Border(left=openpyxl.styles.Side(style="thin"))
        if lang == "ru":
            sheet[f"{alphabet[let_num]}2"] = auditorium["info"]
        else:
            sheet[f"{alphabet[let_num]}2"] = translate.Translator("en", "ru").translate(auditorium["info"])
        sheet[f"{alphabet[let_num]}2"].font = openpyxl.styles.Font(name="Times New Roman", size=12)
        sheet[f"{alphabet[let_num]}2"].alignment = openpyxl.styles.Alignment(horizontal="center", vertical="center",
                                                                             wrap_text=True)
        sheet[f"{alphabet[let_num]}2"].border = openpyxl.styles.Border(bottom=openpyxl.styles.Side(style="thick"),
                                                                       left=openpyxl.styles.Side(style="thin"))
        if let_num == 2:
            sheet["B1"].border = openpyxl.styles.Border(right=openpyxl.styles.Side(style="thick"))
        elif len(data) == let_num - 1:
            sheet.column_dimensions[alphabet[let_num + 1]].width = 50
            if lang == "ru":
                sheet[f"{alphabet[let_num + 1]}1"] = "Мероприятия"
            else:
                sheet[f"{alphabet[let_num + 1]}1"] = "Events"
            sheet[f"{alphabet[let_num + 1]}1"].font = openpyxl.styles.Font(name="Times New Roman", size=22, bold=True)
            sheet[f"{alphabet[let_num + 1]}1"].alignment = openpyxl.styles.Alignment(horizontal="center",
                                                                                     vertical="center")
            sheet[f"{alphabet[let_num + 1]}1"].border = openpyxl.styles.Border(
                right=openpyxl.styles.Side(style="thick"),
                left=openpyxl.styles.Side(style="thin"))
            sheet[f"{alphabet[let_num + 1]}2"].border = openpyxl.styles.Border(
                bottom=openpyxl.styles.Side(style="thick"),
                right=openpyxl.styles.Side(style="thick"),
                left=openpyxl.styles.Side(style="thin"))
        let_num += 1
    aud_index = let_num
    response = requests.get(json_couples)
    if response.status_code == 200:
        data = json.loads(response.text)
    else:
        return "ERROR"
    sheet.column_dimensions['A'].width = 15
    sheet[f"A{row_num}"].border = openpyxl.styles.Border(top=openpyxl.styles.Side(style="thick"))
    date = datetime.datetime(int(data["start_week"][:4]), int(data["start_week"][5:7]), int(data["start_week"][8:10]))
    for day in weekdays:
        if lang == "ru":
            sheet[f"A{row_num}"] = day[0]
            sheet[f"A{row_num + 2}"] = f"{date.day}.{date.month}.{date.year}"
        else:
            sheet[f"A{row_num}"] = day[1]
            sheet[f"A{row_num + 2}"] = f"{date.month}.{date.day}.{date.year}"
        sheet[f"A{row_num}"].font = openpyxl.styles.Font(name="Times New Roman", size=14)
        sheet[f"A{row_num + 2}"].font = openpyxl.styles.Font(name="Times New Roman", size=14)
        row_num += 13
        sheet[f"A{row_num - 1}"].border = openpyxl.styles.Border(top=openpyxl.styles.Side(style="thick"),
                                                                 bottom=openpyxl.styles.Side(style="thick"))
        sheet[f"A{row_num - 1}"].fill = openpyxl.styles.PatternFill(start_color="C0C0C0", fill_type="solid")
        date += datetime.timedelta(1)
    sheet["A1"].border = openpyxl.styles.Border(right=openpyxl.styles.Side(style="thin"))
    sheet["B2"].border = openpyxl.styles.Border(left=openpyxl.styles.Side(style="thin"),
                                                right=openpyxl.styles.Side(style="thick"),
                                                bottom=openpyxl.styles.Side(style="thick"))
    sheet.column_dimensions['B'].width = 15
    for row_num in range(3, 81):
        if times_index == 6 and not skip:
            times_index = 0
            sheet[f"B{row_num}"].border = openpyxl.styles.Border(top=openpyxl.styles.Side(style="thick"),
                                                                 bottom=openpyxl.styles.Side(style="thick"))
            sheet[f"B{row_num}"].fill = openpyxl.styles.PatternFill(start_color="C0C0C0", fill_type="solid")
            continue
        elif skip:
            sheet[f"B{row_num}"].border = openpyxl.styles.Border(bottom=openpyxl.styles.Side(style="thin"),
                                                                 left=openpyxl.styles.Side(style="thin"),
                                                                 right=openpyxl.styles.Side(style="thick"))
            skip = False
            continue
        sheet[f"B{row_num}"] = times[times_index]
        sheet[f"B{row_num}"].font = openpyxl.styles.Font(name="Times New Roman", size=14)
        sheet[f"B{row_num}"].border = openpyxl.styles.Border(left=openpyxl.styles.Side(style="thin"),
                                                             right=openpyxl.styles.Side(style="thick"))
        skip = True
        times_index += 1
    for info in data["results"]:
        if info["auditorium"][0]["name"] in couples_indexes:
            couples_indexes[info["auditorium"][0]["name"]].append(data["results"].index(info))
    couples_indexes_copy = copy.deepcopy(couples_indexes)
    for key, value in couples_indexes.items():
        for index_value in value:
            info = data["results"][index_value]["name"]
            if info.rfind('.') != -1 and info.rfind('.') != len(info) - 1:
                teacher_name = info[:info.rfind('.') + 1]
                info = info[info.rfind('.') + 2:].replace(f" {key}", '')
            elif info.rfind('.') == -1:
                teacher_name = ''
            else:
                for index_info in range(len(info) - 1, -1, -1):
                    if info[index_info] == ' ':
                        sym_count += 1
                    if sym_count == 2:
                        sym_count = 0
                        teacher_name = info[index_info + 1:len(info)]
                        info = info[:index_info - 2].replace(f" {key}", '')
                        break
            for let_num in range(len(couples_indexes)):
                if sheet[f"{alphabet[let_num + 2]}1"].value == key:
                    times_index = 0
                    day_index = 5
                    skip = False
                    for row_num in range(3, 79):
                        if times_index == 6 and not skip:
                            times_index = 0
                            day_index += 13
                            continue
                        elif skip:
                            skip = False
                            continue
                        skip = True
                        times_index += 1
                        excel_date = sheet[f"A{day_index}"].value.split('.')
                        data_date = data["results"][index_value]["date"].split('-')
                        excel_end_time = datetime.time(int(sheet[f"B{row_num}"].value.split('-')[1].split(':')[0]),
                                                       int(sheet[f"B{row_num}"].value.split('-')[1].split(':')[1]))
                        data_end_time = datetime.time(int(data["results"][index_value]["end_time"].split(':')[0]),
                                                      int(data["results"][index_value]["end_time"].split(':')[1]))
                        if lang == "ru":
                            if (datetime.date(int(excel_date[2]),
                                              int(excel_date[1]),
                                              int(excel_date[0])) == datetime.date(int(data_date[2]),
                                                                                   int(data_date[1]),
                                                                                   int(data_date[0]))
                                    and excel_end_time == data_end_time):
                                sheet[f"{alphabet[let_num + 2]}{row_num}"] = teacher_name
                                sheet[f"{alphabet[let_num + 2]}{row_num + 1}"] = info
                                couples_indexes_copy[key].remove(index_value)
                        else:
                            if (datetime.date(int(excel_date[2]),
                                              int(excel_date[0]),
                                              int(excel_date[1])) == datetime.date(int(data_date[2]),
                                                                                   int(data_date[0]),
                                                                                   int(data_date[1]))
                                    and excel_end_time == data_end_time):
                                sheet[f"{alphabet[let_num + 2]}{row_num}"] = (
                                    translate.Translator("en", "ru").translate(teacher_name))
                                sheet[f"{alphabet[let_num + 2]}{row_num + 1}"] = (
                                    translate.Translator("en", "ru").translate(info))
                                couples_indexes_copy[key].remove(index_value)
                        sheet[f"{alphabet[let_num + 2]}{row_num}"].font = openpyxl.styles.Font(name="Times New Roman",
                                                                                               size=12)
                        sheet[f"{alphabet[let_num + 2]}{row_num}"].alignment = openpyxl.styles.Alignment(
                            horizontal="center", vertical="center")
                        sheet[f"{alphabet[let_num + 2]}{row_num + 1}"].font = openpyxl.styles.Font(
                            name="Times New Roman", size=12)
                        sheet[f"{alphabet[let_num + 2]}{row_num + 1}"].alignment = openpyxl.styles.Alignment(
                            horizontal="center", vertical="center")
                    break
    couples_indexes = copy.deepcopy(couples_indexes_copy)
    for key, value in couples_indexes.items():
        if len(value) != 0:
            for index_value in value:
                info = data["results"][index_value]["name"]
                times_index = 0
                day_index = 5
                skip = False
                for row_num in range(3, 79):
                    if times_index > 5 and not skip:
                        times_index = 0
                        day_index += 13
                        continue
                    elif skip:
                        skip = False
                        continue
                    skip = True
                    times_index += 1
                    excel_date = sheet[f"A{day_index}"].value.split('.')
                    data_date = data["results"][index_value]["date"].split('-')
                    if (lang == "ru" and datetime.date(int(excel_date[2]),
                                                       int(excel_date[1]),
                                                       int(excel_date[0])) == datetime.date(int(data_date[2]),
                                                                                            int(data_date[1]),
                                                                                            int(data_date[0]))
                            or lang != "ru" and datetime.date(int(excel_date[2]),
                                                              int(excel_date[0]),
                                                              int(excel_date[1])) == datetime.date(int(data_date[2]),
                                                                                                   int(data_date[0]),
                                                                                                   int(data_date[1]))
                            and sheet[f"{alphabet[aud_index]}{row_num}"].value is None
                            and sheet[f"{alphabet[aud_index]}{row_num + 1}"].value is None):
                        sheet[f"{alphabet[aud_index]}{row_num}"] = \
                            (f"{key} {data['results'][index_value]['start_time'][:-3]}-"
                             f"{data['results'][index_value]['end_time'][:-3]}")
                        if lang == "ru":
                            sheet[f"{alphabet[aud_index]}{row_num + 1}"] = info
                        else:
                            sheet[f"{alphabet[aud_index]}{row_num + 1}"] = (
                                translate.Translator("en", "ru").translate(info))
                        sheet[f"{alphabet[aud_index]}{row_num}"].font = openpyxl.styles.Font(name="Times New Roman",
                                                                                             size=12)
                        sheet[f"{alphabet[aud_index]}{row_num}"].alignment = openpyxl.styles.Alignment(
                            horizontal="center", vertical="center")
                        sheet[f"{alphabet[aud_index]}{row_num + 1}"].font = openpyxl.styles.Font(
                            name="Times New Roman", size=12)
                        sheet[f"{alphabet[aud_index]}{row_num + 1}"].alignment = openpyxl.styles.Alignment(
                            horizontal="center", vertical="center")
                        couples_indexes_copy[key].remove(index_value)
                        break
    for let_num in range(2, auditoriums_num + 3):
        times_index = 0
        skip = False
        for row_num in range(3, 81):
            if let_num == auditoriums_num + 2:
                sheet[f"{alphabet[let_num + 1]}{row_num}"].border = openpyxl.styles.Border(
                    left=openpyxl.styles.Side(style="thick"))
            if times_index == 6 and not skip:
                times_index = 0
                sheet[f"{alphabet[let_num]}{row_num}"].border = openpyxl.styles.Border(
                    top=openpyxl.styles.Side(style="thick"),
                    bottom=openpyxl.styles.Side(style="thick"))
                sheet[f"{alphabet[let_num]}{row_num}"].fill = openpyxl.styles.PatternFill(start_color="C0C0C0",
                                                                                          fill_type="solid")
                continue
            elif skip:
                sheet[f"{alphabet[let_num]}{row_num}"].border = openpyxl.styles.Border(
                    bottom=openpyxl.styles.Side(style="thin"),
                    right=openpyxl.styles.Side(style="thin"))
                skip = False
                continue
            sheet[f"{alphabet[let_num]}{row_num}"].border = openpyxl.styles.Border(
                left=openpyxl.styles.Side(style="thin"),
                right=openpyxl.styles.Side(style="thin"))
            skip = True
            times_index += 1
    file_name = \
            f"Technopark_schedule_{sheet['A5'].value.replace('.', '_')}_"\
            f"{sheet['A70'].value.replace('.', '_')}.xlsx"
    schedule.save(path + '/' + file_name)

    return file_name


#
#
# if __name__ == "__main__":
#     if locale.getlocale()[0][:2] == "ru":
#         print("Это модуль для создания расписания в аудиториях Технопарка ШГПУ.")
#     else:
#         print("This is a module for creating a schedule in the classrooms of the ShSPU Technopark.")
#     print(json_to_excel.__doc__)
# file_name = \
#         f"Technopark_schedule_{sheet['A5'].value.replace('.', '_')}_"\
#         f"{sheet['A70'].value.replace('.', '_')}.xlsx"
#     schedule.save(path + '/' + file_name) path = os.getcwd()