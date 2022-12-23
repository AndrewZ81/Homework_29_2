import csv
import json
from typing import Optional, List, Dict


"""
Для использования функции convert_from_csv_to_json выполнить в терминале:
1. python manage.py shell
2. from functions import convert_from_csv_to_json
3. convert_from_csv_to_json("data/categories.csv", "advertisements/fixtures/categories.json",
 "advertisements.Category")
4. convert_from_csv_to_json("data/ads.csv", "advertisements/fixtures/ads.json",
 "advertisements.Advertisement")
 5.convert_from_csv_to_json("data/locations.csv", "users/fixtures/locations.json",
 "users.Location")
 6.convert_from_csv_to_json("data/users.csv", "users/fixtures/users.json",
 "users.User")
"""


def convert_from_csv_to_json(csv_file_name: str, json_file_name: str, model: str) -> Optional[str]:
    """
    Преобразует файл формата CSV в файл с фикстурой формата JSON
    :param csv_file_name: Название файла формата CSV
    :param json_file_name: Название файла формата JSON
    :param model: Название модели
    :return: Опционально сообщение об ошибке
    """
    raw_data: List[Dict] = []
    try:
        with open(csv_file_name, encoding="utf-8") as file:
            csv_file_data = csv.DictReader(file)
            for row in csv_file_data:
                pk: int = int(row["id"])
                del row["id"]

                if "price" in row:
                    row["price"] = int(row["price"])

                if "is_published" in row:
                    if row["is_published"] == "TRUE":
                        row["is_published"] = True
                    else:
                        row["is_published"] = False

                if "location_id" in row:
                    row["location"] = list(row["location_id"])
                    del row["location_id"]

                record: dict = {
                    "model": model,
                    "pk": pk,
                    "fields": row
                }
                raw_data.append(record)
    except FileNotFoundError:
        return f"Файл {csv_file_name} не найден"

    with open(json_file_name, "w", encoding="utf-8") as file:
        json_data: str = json.dumps(raw_data, indent=4, ensure_ascii=False)
        file.write(json_data)

    return None
