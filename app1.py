from datetime import datetime

import csv
import json

# Открываем файл invertary1.csv и читаем данные
with open('csv/inventory1.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    data = []
    errors = []
    # Пропускаем заголовок
    next(csv_reader, None)
    for row in csv_reader:
        try:
            # Пытаемся извлечь данные из строки
            first_column = int(row[0])
            second_column = int(row[1])
            third_column = datetime.strptime(row[2], "%Y-%m-%d %H:%M")
            fourth_column = int(row[3])
            fifth_column = float(row[4])
            sixth_column = float(row[5])
            seventh_column = float(row[6])
            eighth_column = float(row[7])

            # Добавляем данные в список
            data.append({
                "first_column": first_column,
                "second_column": second_column,
                "third_column": third_column.strftime("%Y-%m-%d %H:%M"),
                "fourth_column": fourth_column,
                "fifth_column": fifth_column,
                "sixth_column": sixth_column,
                "seventh_column": seventh_column,
                "eighth_column": eighth_column
            })
        except Exception as e:
            # Если произошла ошибка, записываем предупреждение в лог и продолжаем обработку
            errors.append(f"Ошибка в строке '{','.join(row)}': {str(e)}")

# Преобразуем данные в формат JSON
with open('invertary1.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

# Записываем предупреждения в лог
if errors:
    with open('invertary1_error_log.txt', 'w', encoding='utf-8') as log_file:
        log_file.write('\n'.join(errors))
    print("Обнаружены ошибки в файле invertary1.csv. Подробности записаны в файл 'invertary1_error_log.txt'.")
else:
    print("Данные из файла invertary1.csv успешно преобразованы в JSON и сохранены в файле 'invertary1.json'.")