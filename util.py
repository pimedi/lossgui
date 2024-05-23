import json

def load_daily_wages(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['city_daily_wages'], data['rural_daily_wages']
