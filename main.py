from main_create import *

path_to_settings = 'settings.json'



def start_creating(word, type, settings):
    if settings['include_in_function']:
        include_in_func(word, settings)
    if not settings['overwrite']:
        status_create = 0
        if is_created(f'{settings['path']['path_to_main']}/{settings['path']['path_to_inc']}\\{word}_admin_panel.php'):
            meta_type[type](word,settings)
            status_create += 1
        if is_created(
                f'{settings['path']['path_to_main']}\\{settings['path']['path_to_inc']}\\{settings['path']['path_to_css']}\\{word}_style.css'):
            create_css_file(word.lower(),settings)
            status_create += 1
        if is_created(
                f'{settings['path']['path_to_main']}\\{settings['path']['path_to_inc']}\\{settings['path']['path_to_js']}\\{word}_script.js'):
            create_js_file(word.lower(),settings)
            status_create += 1
        get_status_create(status_create,settings)
    else:
        meta_type[type](word, settings)
        create_css_file(word.lower(), settings)
        create_js_file(word.lower(), settings)
        get_status_create(3, settings)

meta_type= {
    'post':create_main_file_meta_post,
    'options':create_main_file_options,
}

if __name__ == '__main__':
    settings = load_settings(path_to_settings)
    create_type = settings['meta_type'] if settings['meta_type'] else input('What do you wand to create\n>post\n>options\n>>>').strip().lower()
    word = settings['word'] if settings['word'] else input('Write <<< word >>> for data').strip().lower()

    if not check_path_and_folder(settings):
        exit()
    else:
        start_creating(word, create_type, settings)



