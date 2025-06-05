import json
import os
import shutil
import traceback
import datetime
from wp_function_data.wp_global import *

def coloreg(text: str, color: str):
    COLORS = {
        'black': '\033[30m', 'red': '\033[31m', 'green': '\033[32m', 'yellow': '\033[33m',
        'blue': '\033[34m', 'magenta': '\033[35m', 'cyan': '\033[36m', 'white': '\033[37m',
        'bright_black': '\033[90m', 'bright_red': '\033[91m', 'bright_green': '\033[92m',
        'bright_yellow': '\033[93m', 'bright_blue': '\033[94m', 'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m', 'bright_white': '\033[97m',
        'reset': '\033[0m'
    }

    # Перевіряємо, чи правильний колір
    color_code = COLORS.get(color.lower(), COLORS['reset'])

    # Виводимо текст з кольором
    print(f"{color_code}{text}{COLORS['reset']}")

def audit_path(main_path, folder_name):
    found_path = None
    for root, dirs, files in os.walk(main_path, topdown=True):
        for dir_name in dirs:
            if dir_name == folder_name:
                found_path = os.path.join(root, dir_name)
                break
        if found_path:
            break
    return [bool(found_path), found_path or '']

def copy_files_with_folders(src, dest):

    if not os.path.exists(src):
        coloreg(f'Файли з {src} не скопійовано"','red')
        write_error(text = f'Вихідна папка не існує: {src}"')
        return False

    folder_name = src.split('\\')[-1]
    new_dest = os.path.join(dest, folder_name)
    for root, dirs, files in os.walk(src):
        # Обчислити відповідний шлях у цільовій папці
        relative_path = os.path.relpath(root, src)
        target_folder = os.path.join(new_dest, relative_path)

        # Створити всі підпапки у цільовій папці
        os.makedirs(target_folder, exist_ok=True)

        # Копіювати файли
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(target_folder, file)
            shutil.copy2(src_file, dest_file)
    else:
        coloreg(f'Всі файли з <{src}> до <{new_dest}> скопійовано','green')

def write_error(e:Exception = '', text = ''):
    now= datetime.datetime.now().replace(microsecond=0)
    if not text:
        # Отримання останнього запису у стеку викликів
        last_trace = traceback.extract_tb(e.__traceback__)[-1]
        filename = last_trace.filename
        lineno = last_trace.lineno
        message = f"Невідома помилка: {str(e)} (Файл: {filename}, Рядок: {lineno})"
    else:
        message = text
    with open('debug.log','a+',encoding='utf-8') as file:
        file.write(f'{now} ||| {message}\n')

def check_folder(settings_load,folders):
    count = 0
    for path in settings_load['path']:
        if path in folders:
            part_path = audit_path(settings_load['main']['main_path'], settings_load['path'][path])
            # print(part_path)
            if part_path[0]:
                settings_load['path'][path] = part_path[1]
                # coloreg(f'Path to <{path}> is already exist!!!', 'yellow')
            else:
                if settings_load['global']['create_folder']:
                    if path == 'inc':
                        path_file = '\\'.join([f'{settings_load['main']['main_path']}', f'{settings_load['path'][path]}'])
                        os.makedirs(path_file, exist_ok=True)
                        coloreg(f'Папку {settings_load['path'][path]} створено!!!', 'green')
                    else:
                        path_file = os.path.join(f'{settings_load['main']['main_path']}', f'{settings_load['path']['inc']}',
                                                 f'{settings_load['path'][path]}')
                        os.makedirs(path_file, exist_ok=True)
                        coloreg(f'Папку {settings_load['path'][path]} створено!!!', 'green')
                    settings_load['path'][path] = path_file
                else:
                    # coloreg(f'Папку {settings_load['path'][path]} не знайдено!!!', 'yellow')
                    write_error(text = f'Папку {settings_load['path'][path]} не знайдено!!!')
                    count+=1

    return False if count>0 else True,settings_load

def check_folder_name(root_directory, folder_name):

    matching_folders = []

    # Прохід по директорії та її піддиректоріях
    for dirpath, dirnames, filenames in os.walk(root_directory):
        if folder_name in dirnames:
            matching_folders.append(True)
            matching_folders.append(os.path.join(dirpath, folder_name))
            return matching_folders
    else:
        matching_folders.append(False)
        matching_folders.append('')

    return matching_folders

def check_labels(settings_load):
    status=[]
    status_none = False
    status_repeat = True
    status_label_none = False

    types = settings_load['main']['type']
    for labels in settings_load['types'][types]:
        # print(type(settings_load['types'][types][labels]))
        if type(settings_load['types'][types][labels]) is list:
            # print(settings_load['types'][types][labels])
            labels_set = []
            if len(settings_load['types'][types][labels]) != 0:
                status_none = True
            num = 1
            for label in settings_load['types'][types][labels]:
                if label == '' and settings_load['global']['auto_name_label']:
                    labels_set.append(f'{labels}_{num}')
                    num += 1
                    status_label_none = True
                else:
                    if label != '':
                        labels_set.append(label)
                        status_label_none = True
            else:
                settings_load['types'][types][labels] = labels_set
                # print(settings_load['types'][types][labels])

            for label in set(settings_load['types'][types][labels]):
                label_count = list(settings_load['types'][types][labels]).count(label)
                # print(f'{label_count} - {label} ')
                if label_count>1:
                    status_repeat = False
        elif type(settings_load['types'][types][labels]) is dict:
            for hl_label in settings_load['types'][types][labels]:
                labels_set = []
                if len(settings_load['types'][types][labels][hl_label]) != 0:
                    status_none = True
                num = 1
                for label in settings_load['types'][types][labels][hl_label]:
                    if label == '' and settings_load['global']['auto_name_label']:
                        labels_set.append(f'hl_{hl_label}_{num}')
                        num += 1
                        status_label_none = True
                    else:
                        if label != '':
                            labels_set.append(label)
                            status_label_none = True
                else:
                    settings_load['types'][types][labels][hl_label] = labels_set

    if not status_none:
        write_error(text='Масив полів пустий, а в налаштування включено створення полів!!! labels:[]')
    if not status_repeat:
        write_error(text='Назви полів не повинні бути однакові в одному типі !!!')
    if not status_label_none:
        write_error(text='Назви полів на вказані, і авто іменування полів виключене !!!')

    status.append(status_none)
    status.append(status_repeat)
    status.append(status_label_none)
    return False if False in status else True

def load_settings(path_to_load:str) -> dict:
    status = []
    try:
        settings = []
        with open(path_to_load, 'r', encoding='utf-8') as file:
            settings_load = json.load(file)
        if settings_load['main']['type'] =='post' or settings_load['main']['type'] =='option':
            status_0, settings = check_folder(settings_load,('inc','js','css'))
            status.append(status_0)
            if settings['global']['create_with_label']:
                status.append(check_labels(settings))
        elif settings_load['main']['type'] =='request':
            status_0, settings = check_folder(settings_load,'inc')
            status.append(status_0)
        # print(settings['path'])
        with open('s.json', 'r+',encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        return {} if False in status else settings
    except FileNotFoundError as e:
        write_error(e)
    except json.JSONDecodeError as e:
        write_error(e)
    except Exception as e:
        write_error(e)
    return {}

def upload_global_settings(settings_load):
    if settings_load['global']['debug_on']:
        count_debug = 0
        path_to_config = settings_load['main']['main_path'][:settings_load['main']['main_path'].index('wp-content')] + 'wp-config.php'
        with open(path_to_config, 'r', encoding='utf-8') as file:
            data_config = file.read()
        index_end_debug = data_config.index('''/* Add any custom values between this line and the "stop editing" line. */''')-2

        for debug_line in debug_global:
            if  not debug_line[debug_line.index('\''):debug_line.rindex('\'')-1] in data_config:
                data_config = data_config[:index_end_debug] + f'\n{debug_line}' + data_config[index_end_debug:]
                count_debug+=1
        with open(path_to_config, 'w', encoding='utf-8') as file:
            file.write(data_config)
        if count_debug == 0:
            coloreg('<DEBUG> already exist !!!', 'yellow')
        elif count_debug == 4:
            coloreg('<DEBUG> включено !!!', 'green')
            coloreg('Не забудьте оновити <wp-config.php> !', 'magenta')
        else:
            coloreg('<DEBUG> update !!!', 'yellow')
            coloreg('Не забудьте оновити <wp-config.php> !', 'magenta')


