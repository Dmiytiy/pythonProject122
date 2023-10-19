import csv
import json

# Открываем файл CSV и читаем данные
with open('csv/price.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    data = []
    errors = []
    for row in csv_reader:
        try:
            # Пытаемся извлечь данные из строки
            name = row[0]
            category = row[1]
            price = float(row[2])
            code = int(row[3])
            ratio = float(row[4])
            quantity = int(row[5])
            coefficient = float(row[6])

            # Добавляем данные в список
            data.append({
                "название": name,
                "категория": category,
                "цена": price,
                "код": code,
                "соотношение": ratio,
                "количество": quantity,
                "коэффициент": coefficient
            })
        except Exception as e:
            # Если произошла ошибка, записываем предупреждение в лог и продолжаем обработку
            errors.append(f"Ошибка в строке '{','.join(row)}': {str(e)}")

# Преобразуем данные в формат JSON
with open('price.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

# Записываем предупреждения в лог
if errors:
    with open('error_log.txt', 'w', encoding='utf-8') as log_file:
        log_file.write('\n'.join(errors))
    print("Обнаружены ошибки. Подробности записаны в файл 'error_log.txt'.")
else:
    print("Данные успешно преобразованы в JSON и сохранены в файле 'price.json'.")