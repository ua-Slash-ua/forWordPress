import os.path

from functions import *
from wp_function_data.wp_request import *

def wp_request_data(settings:dict):
    lword = settings['main']['word'].lower()
    cword = settings['main']['word'].lower().capitalize()
    full_data = body_request

    data = full_data.replace('LWORD',lword).replace('CWORD',cword)
    return data

def create_php(settings):
    status_create = 0
    path_php = f'{settings['path']['inc']}\\{settings['main']['word']}_request.php'

    if not os.path.exists(path_php) or (os.path.exists(path_php) and settings['dev_mod']['rewrite']):
        with open(f'{path_php}', 'w', encoding='utf-8') as file:
            file.write(wp_request_data(settings))
            settings['main']['main_file'] = path_php
        if not os.path.exists(path_php):
            coloreg(f'Файл {settings['main']['word']}_request.php створено !!!', 'green')
        else:
            coloreg(f'Файл {settings['main']['word']}_request.php оновлено !!!', 'yellow')
    else:
        status_create += 1
        write_error(
            text=f'Файл {settings['main']['word']}_request.php не створено так як він уже існує і <rewrite> виключено !!! ')

    if status_create == 0:
        pass
        # coloreg('Файл створено(оновлена) !!!', 'bright_green')
    else:
        coloreg('Файл не створено(не оновлено) !!! (перегляньте файл <debug.log>)', 'red')

def add_labels(settings):
    with open(settings['main']['main_file'], 'r', encoding='utf-8') as file:
        data = file.read()
    if settings['types']['request']['email']:
        send_email =  send_email_incl
        index_start_handle = data.index('function handle_')
        index_end_handle = data[index_start_handle:].index('}') + index_start_handle + 1

        data = data[:index_end_handle] + send_email_func.replace('SMTP_EMAIL',settings['secret_data']['smtp']['smtp_email']) + data[index_end_handle:]
        data = data[:index_end_handle-1] + standart_func_mail + data[index_end_handle-1:]
        try:
            path_to_config = settings['main']['main_path'][:settings['main']['main_path'].index('wp-content')]+'wp-config.php'
            with open(path_to_config, 'r', encoding='utf-8') as file:
                data_config = file.read()
                if not '''define('SMTP_PASSWORD', ''''' in data_config:
                    index_start_add_define = data_config.index('/* Add any custom values between this line and the "stop editing" line. */')+74
                    data_config = data_config[:index_start_add_define] + '''\ndefine('SMTP_PASSWORD', 'SMTP__PASSWORD');'''.replace('SMTP__PASSWORD',settings['secret_data']['smtp']['smtp_password']) +  data_config[index_start_add_define:]
                    coloreg('Додано <SMTP_PASSWORD> !!!', 'green')
                    coloreg('Не забудьте оновити <wp-config.php> !', 'magenta')
                else:
                    coloreg('SMTP_PASSWORD is already exist!!!', 'yellow')
            with open(path_to_config, 'w', encoding='utf-8') as file:
                file.write(data_config)

        except Exception as e:
            write_error(e = e)
            coloreg('Помилка!!! (перегляньте файл <debug.log>)', 'red')
        coloreg('Функцію <send_email> додано!!!','green')
        if  settings['types']['request']['load_phpmailer']:
            path_to_vendor_th = check_folder_name(settings['main']['main_path'].replace('\\','/'),'vendor')
            if not path_to_vendor_th[0]:
                current_dir = os.path.abspath(os.path.dirname(__file__))
                path_to_vendor_my = check_folder_name(current_dir,'PHPMailer-master')
                if path_to_vendor_my[0]:
                    copy_files_with_folders(path_to_vendor_my[1],settings['main']['main_path'])
            else:
                coloreg('<phpmailer> is already exist!!!','yellow')
            path_to_vendor_th = check_folder_name(settings['main']['main_path'].replace('\\', '/'), 'PHPMailer-master')
            part_path_to_vendor = path_to_vendor_th[1].replace('\\', '/').replace((settings['main']['main_path'].replace('\\', '/')),'')[1:]
            send_email = send_email.replace('PATH',part_path_to_vendor)

        index_start_file = data.index('<?php') + 5

        data = data[:index_start_file] + send_email + data[index_start_file:]




    with open(settings['main']['main_file'], 'w', encoding='utf-8') as file:
        file.write(data)

def create_request(settings):
    create_php(settings)
    add_labels(settings)
    if settings['global']['include_in_func']:
        try:
            with open(f"{settings['main']['main_path']}\\functions.php", 'r+', encoding='utf-8') as file:
                part_path = f"{settings['path']['inc']}\\{settings['main']['word']}_request.php".replace(f'{settings['main']['main_path']}','')
                line = f"require get_template_directory() . '{part_path}';".replace('\\','/')
                data = file.read()
                if line not in data:
                    with open(f"{settings['main']['main_path']}\\functions.php", 'a', encoding='utf-8') as f:
                        f.write(f"\n{line}")
                        coloreg('Файл підключено в <functions.php> !!! ', 'green')
                else:
                    coloreg('Файл вже підключено в <functions.php> !!! ', 'yellow')
        except Exception as e:
            write_error(e)
            coloreg('Файл не підключено в <functions.php> !!! (перегляньте файл <debug.log>)', 'yellow')
