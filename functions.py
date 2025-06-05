import json

import os



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




def load_settings(path_to_settings):
    with open(path_to_settings, 'r', encoding='utf-8') as fj:
        settings = json.load(fj)
    coloreg(f'Settings loaded', 'green')
    return settings

def check_path_and_folder(settings):
    status = True
    for path in settings['path']:
        if path == 'path_to_main':
            if not os.path.exists(settings['path'][path]):
                coloreg(f'Path < {settings['path'][path]} > isn`t exist','bright_red')
                return status
        elif path == 'path_to_inc':
            if not os.path.exists(f'{settings['path']['path_to_main']}/{settings['path'][path]}'):

                if settings['is_create_file']:
                    folder_path = os.path.join(f'{settings['path']['path_to_main']}/', f'{settings['path']['path_to_inc']}')
                    os.makedirs(folder_path)
                    coloreg(f'Folder < {path} > created!!!', 'cyan')
                else:
                    coloreg(f' < {path} > isn`t exist', 'yellow')
                    status = False
        else:
            if not os.path.exists(f'{settings['path']['path_to_main']}/{settings['path']['path_to_inc']}/{settings['path'][path]}'):
                if settings['is_create_file']:
                    folder_path = os.path.join(f'{settings['path']['path_to_main']}/{settings['path']['path_to_inc']}/', f'{settings['path'][path]}')
                    os.makedirs(folder_path)
                    coloreg(f'Folder < {path} > created!!!', 'cyan')
                else:
                    coloreg(f' < {path} > isn`t exist', 'yellow')
                    status = False
    return status

def include_in_func(word,settings):
    incl = f"require get_template_directory() . '/{settings['path']['path_to_inc']}/{word}_admin_panel.php';"
    path_to_func = f'{settings['path']['path_to_main']}/functions.php'
    with open(path_to_func,'r',encoding='utf-8') as f:
        data = f.read()
        if incl in data:
            coloreg(f'Include already exist!!!', 'bright_yellow')
        else:
            with open(path_to_func, 'a', encoding='utf-8') as file:
                file.write(f'\n{incl}')
            coloreg(f'Include in functions added!!!', 'green')

def is_created(path_to_file):
    file = path_to_file.split('/')[-1]
    if not os.path.exists(f'{path_to_file}'):
        return True
    else:
        coloreg(f'File  < {file} > already exist!!!', 'bright_yellow')
        return False

def get_status_create(status_create,settings):
    if status_create == 0:
        coloreg(f'<{settings['meta_type']}> for < {settings['word']} > don`t was created !!!', 'bright_yellow')
    elif 0 < status_create < 3 :
        coloreg(f'<{settings['meta_type']}> for < {settings['word']} > was update !!!', 'green')
    else:
        coloreg(f'<{settings['meta_type']}> for < {settings['word']} > was created !!!', 'bright_green')

