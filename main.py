import csv, re
import datetime
import sys


def get_csv_to_dict(path):
    list = []
    reader = csv.DictReader(open(path, "r"))
    for line in reader:
        list.append(line)

    return list


def is_mobile(phone):
    if len(phone) < 9:
        return False
    return phone[::-1][8] == "9"


def extract_mobile(phone):
    phone = phone[::-1][:9]
    phone = phone[::-1]
    return phone


def adjust_data(data):
    phone = data["Telefone"]
    phone = phone.replace(" ", "")
    phone = phone.replace("\n", "")

    phone = re.findall("\d+", phone)[0]
    phone = extract_mobile(phone)
    phone = "+5511" + phone

    data["Telefone"] = phone
    return data


def save_data_to_csv(list, path):
    w = csv.writer(open(path, 'w'))
    for d in list:
        data = []
        data.append(d["Telefone"])
        data.append(d["Nome"])
        w.writerow(data)


if __name__ == '__main__':
    file_path = sys.argv[1]
    if file_path.replace(" ", "") == "":
        print("file path is required")

    out_extension = file_path[file_path.find("."):]
    out_path = file_path[:file_path.find(".")]
    out_path = out_path + "-" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    out_path = out_path + out_extension

    data = get_csv_to_dict(file_path)
    new_data = []
    for d in data:
        if d["Nome"] == "Homero leads":
            print("entrou")
        phone = d["Telefone"]
        if is_mobile(phone):
            new_data.append(adjust_data(d))

    print("processing file...")
    save_data_to_csv(new_data, out_path)
    print("file generated on: " + out_path)
