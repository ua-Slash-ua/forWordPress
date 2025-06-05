from functions import *
from main_file_for_create_option import create_options
from main_file_for_create_post_type import create_post_type
from main_file_for_create_request import create_request

path_to_load = 'settings.json'

create_meta_type ={
    'post': create_post_type,
    'option': create_options,
    'request': create_request
}
def create_source_file():
    settings = load_settings(path_to_load)

    if not settings:
        coloreg('Налаштування введені не коректно, що не дає запустити програму!!! (перегляньте файл <debug.log>)', 'red')
        exit()
    else:
        upload_global_settings(settings)
        meta_type = settings['main']['type']
        create_meta_type[meta_type](settings)


if __name__ == '__main__':
    create_source_file()