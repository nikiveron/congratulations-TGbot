import csv
import os
from datetime import datetime

__log_file = 'congratulations_log.csv'

def logfile_define():
    if not os.path.exists(__log_file):
        with open(__log_file, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Дата", "Время", "Имя", "Возраст", "Пол", "Праздник", "Стиль", "Длина поздравления"
            ])


def log_to_csv(name, age, sex, holiday, style, text_length):
    now = datetime.now()
    with open(__log_file, mode="a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow([
            now.date(),
            now.strftime("%H:%M:%S"),
            name,
            age,
            sex,
            holiday,
            style,
            text_length
        ])
