import csv
import re
from datetime import datetime


def logger(path):
    def dec_logger(func):
        def wrapped(contacts_list):
            return_value = func(contacts_list)
            current_fulldate = datetime.now()
            current_time = datetime.time(current_fulldate)
            current_date = datetime.date(current_fulldate)
            with open(path + 'log.txt', 'w') as f:
                result = f'Time: {current_time}\nDate: {current_date}\nName func: ' \
                         f'{func.__name__}\nValue: {contacts_list}\nReturn value: {return_value}'
                f.write(str(result))
            return result

        return wrapped

    return dec_logger


def get_fullname_list(contacts_list):
    last_name = []
    full_name = []
    for i in range(1, len(contacts_list)):
        if contacts_list[i][0] != '' and contacts_list[i][1] != '' and contacts_list[i][2] != '':
            if contacts_list[i][0] not in last_name:
                last_name += [contacts_list[i][0]]
                full_name += [contacts_list[i][0], contacts_list[i][1], contacts_list[i][2]]
        elif contacts_list[i][0] != '' and contacts_list[i][1] != '':
            if contacts_list[i][0] not in last_name:
                full_name += [(f'{contacts_list[i][0]} {contacts_list[i][1]}').split()]
                last_name += [contacts_list[i][0]]
        elif contacts_list[i][0] != '':
            if contacts_list[i][0].split()[0] not in last_name:
                full_name += [contacts_list[i][0].split()]
                last_name += [contacts_list[i][0].split()[0]]
    return full_name


@logger('')
def get_list(contacts_list):
    phone_list = []
    fullname_list = get_fullname_list(contacts_list)
    fullname_list.insert(0, ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email'])
    for fullname in fullname_list:
        for i in range(1, len(contacts_list)):
            if fullname[0] in contacts_list[i][0]:
                if contacts_list[i][3] != '':
                    fullname.append(contacts_list[i][3])
                if contacts_list[i][4] != '':
                    fullname.append(contacts_list[i][4])
                if contacts_list[i][5] != '':
                    fullname.append(format_phone(contacts_list[i][5]))
                if contacts_list[i][6] != '':
                    fullname.append(contacts_list[i][6])
    phone_list += fullname_list
    return phone_list


def format_phone(number_phone):
    pattern1 = r"((\+7|8)495(\d{3})(\d{2})(\d{2}))|((\+7|8)?\s*(\((\d+)\)|)\s*(\d+)[-\s](\d+)[-\s](\d{2})(\d{2}))|((\+7|8)?\s*(\((\d+)\)|)\s*(\d+)[-\s](\d+)[-\s](\d+))"
    pattern2 = r"\(*доб.+((\d{4}))\)*"
    sub_text1 = r"+7(495)\18\11\3-\19\4\12-\20\5\13"
    sub_text2 = r'доб.\2'
    res = re.sub(pattern1, sub_text1, number_phone)
    number_phone = re.sub(pattern2, sub_text2, res)
    return number_phone


def main():
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    # TODO 1: выполните пункты 1-3 ДЗ
    contacts_list = get_list(contacts_list)
    # TODO 2: сохраните получившиеся данные в другой файл
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    main()
