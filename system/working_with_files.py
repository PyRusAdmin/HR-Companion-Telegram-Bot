# -*- coding: utf-8 -*-
import json
import os


def load_bot_info(messages):
    with open(messages, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def save_bot_info(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


QUESTIONS_FILE = "media/questions/questions_map.json"


def load_questions_map():
    if not os.path.exists(QUESTIONS_FILE):
        os.makedirs(os.path.dirname(QUESTIONS_FILE), exist_ok=True)
        return {}
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_questions_map(data):
    os.makedirs(os.path.dirname(QUESTIONS_FILE), exist_ok=True)
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_department_channels():
    """Чтение данных из файла с группами и каналами"""
    try:
        with open("database/data.json", "r", encoding="utf-8") as f:
            DEPARTMENT_CHANNELS = json.load(f)
        return DEPARTMENT_CHANNELS
    except Exception as e:
        logger.exception(e)
