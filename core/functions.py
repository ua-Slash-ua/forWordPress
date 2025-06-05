import json
import os
import shutil
import psutil
from typing import List
from packaging import version

from core.logging.log import ErrorAndInitLogging


def version_comparison(old_version, new_version):
    if version.parse(new_version) > version.parse(old_version):
        return True
    else:
        return False

def is_program_running(name: str) -> bool:
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and name.lower() in proc.info['name'].lower():
            return True
    return False



def kill_program(os_process: List[str]) -> int:
    killed_count = 0
    targets = [name.lower() for name in os_process]

    for proc in psutil.process_iter(['name']):
        try:
            proc_name = proc.info.get('name', '')
            if proc_name and any(target in proc_name.lower() for target in targets):
                proc.kill()
                killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return killed_count



def copy_all(src_folder, dst_folder):
    for root, dirs, files in os.walk(src_folder):
        relative_path = os.path.relpath(root, src_folder)
        target_dir = os.path.join(dst_folder, relative_path)
        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)
            shutil.copy2(src_file, dst_file)

def read_json_settings(path_to_settings, logger: ErrorAndInitLogging):
    if not os.path.exists(path_to_settings):
        msg = f"❌ Файл {path_to_settings} не знайдено."
        logger.write_debug(msg)
        logger.write_info("error", msg)
        return []

    try:
        with open(path_to_settings, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, dict):
            msg = f"❌ JSON-файл має містити масив (dict) на верхньому рівні, але отримано: {type(data)}"
            logger.write_debug(msg)
            logger.write_info("error", msg)
            return []

        return data

    except json.JSONDecodeError as e:
        msg = f"❌ Помилка декодування JSON: {e}"
        logger.write_debug(msg)
        logger.write_info("error", msg)
        return []


def write_json_settings(data, path_to_settings, logger: ErrorAndInitLogging):
    try:
        # Перевіряємо, чи дані є валідними (мають бути в форматі dict)
        if not isinstance(data, dict):
            msg = f"❌ Дані повинні бути у форматі dict, але отримано: {type(data)}"
            logger.write_debug(msg)
            logger.write_info("error", msg)
            return False

        # Записуємо дані в файл
        with open(path_to_settings, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        logger.write_info("success", f"🎉 Файл {path_to_settings} успішно збережено.")
        return True

    except Exception as e:
        msg = f"❌ Помилка при записі файлу JSON: {e}"
        logger.write_debug(msg)
        logger.write_info("error", msg)
        return False


def read_txt_file(path_to_file):
    with open(path_to_file,'r', encoding='utf-8') as file:
        return file.read()

def write_txt_file(path_to_file, data: str, ftype = 'w'):
    with open(path_to_file,ftype, encoding='utf-8') as file:
        return file.write(data)

def get_value_in_dict(data, target_key):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            result = get_value_in_dict(value, target_key)
            if result is not None:
                return result

    elif isinstance(data, list):
        for item in data:
            result = get_value_in_dict(item, target_key)
            if result is not None:
                return result

    return None


def get_value_on_other_value(data, target_key, target_value):
    result = []

    if isinstance(data, dict):
        for key, value in data.items():
            # Якщо target_value є рядком або числом, перевіряємо чи значення починається з target_value
            if key == target_key:
                if isinstance(target_value, bool):
                    # Якщо target_value булеве, перевіряємо на рівність
                    if value == target_value:
                        result.append(data)
                elif isinstance(target_value, (str, int)) and isinstance(value, str) and str(value).startswith(str(target_value)):
                    # Якщо target_value рядок або число, перевіряємо, чи значення починається з target_value
                    result.append(data)
            # Рекурсивно перевіряємо значення, якщо це словник або список
            result.extend(get_value_on_other_value(value, target_key, target_value))

    elif isinstance(data, list):
        for item in data:
            result.extend(get_value_on_other_value(item, target_key, target_value))

    return result

def find_full_path(start_dir, target_name):
    """
    Шукає повний шлях до файлу або папки з іменем target_name,
    починаючи з директорії start_dir.

    :param start_dir: Стартова директорія для пошуку
    :param target_name: Назва файлу або папки для пошуку
    :return: Повний шлях або None, якщо не знайдено
    """
    for root, dirs, files in os.walk(start_dir):
        if target_name in dirs or target_name in files:
            return os.path.join(root, target_name)
    return None

def copy_image(src, dst):
    try:
        # Копіює файл з src до dst
        shutil.copy(src, dst)
    except Exception as e:
        print(f"Помилка при копіюванні фото: {e}")

if __name__ == '__main__':
    path_to_debug = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\debug.log'
    path_to_info = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\info.md'
    errorlog = ErrorAndInitLogging(path_to_debug, path_to_info)
    main_settings = read_json_settings(r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\config\main_config.json',errorlog)
