import csv

def csv_get_delimiter(file: str) -> str:
    with open(file, 'r') as csvfile:
        delimiter = str(csv.Sniffer().sniff(csvfile.read()).delimiter)
        return delimiter

def csv_get_records(file: str) -> str:
    data = []

    try:
        delimiter_str = csv_get_delimiter(file)
    except csv.Error:
        print(f"File '{file}' has no csv-delimiter. File is empty?")
        exit()

    with open('records.csv', 'r') as file:
        reader = csv.reader(file, delimiter = delimiter_str)
        next(reader)
        for line in reader:
            data.append(line)

    return data