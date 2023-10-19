import csv
import json

# Открываем файл invertary.csv и читаем данные
with open('csv/inventory2.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    data = []
    errors = []
    # Пропускаем заголовок
    next(csv_reader, None)
    for row in csv_reader:
        try:
            # Пытаемся извлечь данные из строки
            store_ext_id = int(row[0])
            price_ext_id = row[1]
            snsh_datetime = row[2]
            in_matrix = int(row[3])
            qty = float(row[4])
            sell_price = float(row[5])
            prime_cost = float(row[6])
            min_stock_level = float(row[7]) if row[7] else None
            stock_in_days = float(row[8]) if row[8] else None
            in_transit = float(row[9]) if row[9] else None

            # Добавляем данные в список
            data.append({
                "STORE_EXT_ID": store_ext_id,
                "PRICE_EXT_ID": price_ext_id,
                "SNSH_DATETIME": snsh_datetime,
                "IN_MATRIX": in_matrix,
                "QTY": qty,
                "SELL_PRICE": sell_price,
                "PRIME_COST": prime_cost,
                "MIN_STOCK_LEVEL": min_stock_level,
                "STOCK_IN_DAYS": stock_in_days,
                "IN_TRANSIT": in_transit
            })
        except Exception as e:
            # Если произошла ошибка, записываем предупреждение в лог и продолжаем обработку
            errors.append(f"Ошибка в строке '{','.join(row)}': {str(e)}")

# Преобразуем данные в формат JSON
with open('invertary2.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

# Записываем предупреждения в лог
if errors:
    with open('invertary_error_log2.txt', 'w', encoding='utf-8') as log_file:
        log_file.write('\n'.join(errors))
    print("Обнаружены ошибки в файле invertary.csv. Подробности записаны в файл 'invertary_error_log.txt'.")
else:
    print("Данные из файла invertary.csv успешно преобразованы в JSON и сохранены в файле 'invertary.json'.")
