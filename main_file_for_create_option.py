import os.path

from functions import *
from wp_function_data.scripts import *
from wp_function_data.styles import *
from wp_function_data.wp_option import *


def wp_option_data(settings:dict):
    lword = settings['main']['word'].lower()
    cword = settings['main']['word'].lower().capitalize()
    partpathcss = f'{settings['path']['css'].replace(settings['main']['main_path'], '')}\\{settings['main']['word']}_styles.css'.replace('\\','/')
    partpathjs = f'{settings['path']['js'].replace(settings['main']['main_path'], '')}\\{settings['main']['word']}_script.js'.replace('\\','/')
    full_data = body_options
    if settings['global']['enqueue_media_uploader_wp']:
        full_data+=wp_media_uploader
    data = full_data.replace('LWORD',lword).replace('CWORD',cword).replace('PartPathCSS',partpathcss).replace('PartPathJS',partpathjs)
    return data

def create_php_js_css(settings):
    status_create = 0
    path_php = f'{settings['path']['inc']}\\{settings['main']['word']}_admin_panel.php'
    path_js = f'{settings['path']['js']}\\{settings['main']['word']}_script.js'
    path_css = f'{settings['path']['css']}\\{settings['main']['word']}_styles.css'
    if not os.path.exists(path_php) or (os.path.exists(path_php) and settings['dev_mod']['rewrite']):
        with open(f'{path_php}', 'w', encoding='utf-8') as file:
            file.write(wp_option_data(settings))
            settings['main']['main_file'] = path_php
        if not os.path.exists(path_php):
            coloreg(f'Файл {settings['main']['word']}_admin_panel.php створено !!!', 'green')
        else:
            coloreg(f'Файл {settings['main']['word']}_admin_panel.php оновлено !!!', 'yellow')
    else:
        status_create += 1
        write_error(
            text=f'Файл {settings['main']['word']}_admin_panel.php не створено так як він уже існує і <rewrite> виключено !!! ')
    if not os.path.exists(path_js) or (os.path.exists(path_js) and settings['dev_mod']['rewrite']):
        with open(f'{path_js}', 'w', encoding='utf-8') as file:
            scr = '''// SCRIPTS


document.addEventListener("DOMContentLoaded",function () {


})'''
            file.write(scr)
            settings['main']['js_file'] = path_js
        if not os.path.exists(path_js):
            coloreg(f'Файл {settings['main']['word']}_script.js створено !!!', 'green')
        else:
            coloreg(f'Файл {settings['main']['word']}_script.js оновлено !!!', 'yellow')

    else:
        status_create += 1
        write_error(
            text=f'Файл {settings['main']['word']}_script.js не створено так як він уже існує і <rewrite> виключено !!! ')
    if not os.path.exists(path_css) or (os.path.exists(path_css) and settings['dev_mod']['rewrite']):
        with open(f'{path_css}', 'w', encoding='utf-8') as file:
            file.write('/* STYLES */')
            settings['main']['css_file'] = path_css
        if not os.path.exists(path_css):
            coloreg(f'Файл {settings['main']['word']}_styles.css створено !!!', 'green')
        else:
            coloreg(f'Файл {settings['main']['word']}_styles.css оновлено !!!', 'yellow')
    else:
        status_create += 1
        write_error(
            text=f'Файл {settings['main']['word']}_styles.css не створено так як він уже існує і <rewrite> виключено !!! ')

    if status_create == 0:
        coloreg('Усі файли створені(оновлені) !!!', 'bright_green')
    elif 1 <= status_create < 3:
        coloreg('Не усі файли створені(оновлені) !!! (перегляньте файл <debug.log>)', 'yellow')
    else:
        coloreg('Файли не створено(не оновлено) !!! (перегляньте файл <debug.log>)', 'red')

def add_styles(settings):
    if os.path.exists(settings['path']['css']):
        try:
            with open(settings['main']['css_file'], 'r', encoding='utf-8') as file:
                data = file.read()
            styles = []
            if settings['types']['option']['input']:
                styles.append('\n\n/* ---------- input styles ---------- */')
                styles.append(style_input)
            if settings['types']['option']['checkbox']:
                styles.append('\n\n/* ---------- checkbox styles ---------- */')
                styles.append(style_checkbox)
            if settings['types']['option']['img_link']:
                styles.append('\n\n/* ---------- image link styles ---------- */')
                styles.append(style_image)
            if settings['types']['option']['img_svg']:
                styles.append('\n\n/* ---------- image svg styles ---------- */')
                styles.append(style_svg)
            if settings['types']['option']['points']:
                styles.append('\n\n/* ---------- points styles ---------- */')
                styles.append(style_points)
            if settings['types']['option']['table']:
                styles.append('\n\n/* ---------- table styles ---------- */')
                styles.append(style_table)
            if settings['types']['option']['hl_mixed']['img_svg'] or settings['types']['option']['hl_mixed']['img_link'] or settings['types']['option']['hl_mixed']['checkbox'] or settings['types']['option']['hl_mixed']['input']:
                styles.append('\n\n/* ---------- hard label mixed styles ---------- */')
                styles.append(style_hl_mixed)
            data += ''.join(styles)
            with open(settings['main']['css_file'], 'w', encoding='utf-8') as file:
                file.write(data)
                coloreg('Стилі додані !!! ', 'green')
        except Exception as e:
            write_error(e=e)
            coloreg('Не вдалося прочитати або записати файл!!! (перегляньте файл <debug.log>)', 'red')
    else:
        coloreg('Стилі не додані !!! (перегляньте файл <debug.log>)', 'red')
        write_error(
            text=f'Файл {settings['path']['css']}не існує !!! ')

def add_scripts(settings):
    if os.path.exists(settings['path']['js']):
        try:
            with open(settings['main']['js_file'], 'r', encoding='utf-8') as file:
                data = file.read()
            scripts_func = []
            scripts_incl = []
            if settings['types']['option']['img_link']:
                scripts_func.append(script_image_func)
                for label in settings['types']['option']['img_link']:
                    scripts_incl.append(script_image_inc.replace('LWORD',label.lower()))
            if settings['types']['option']['img_svg']:
                scripts_func.append(script_svg_func)
                for label in settings['types']['option']['img_svg']:
                    scripts_incl.append(script_svg_inc.replace('LWORD',label.lower()))
            if settings['types']['option']['points']:
                scripts_func.append(script_points_func)
                for label in settings['types']['option']['points']:
                    scripts_incl.append(script_points_inc.replace('LWORD',label.lower()))

            if settings['types']['option']['table']:
                scripts_func.append(script_table_func)
                data_word = []
                for label in settings['types']['option']['table']:
                    data_word.append(f'\'table_{label.lower()}\'')
                scripts_incl.append(script_table_inc.replace('DATA_WORD',','.join(data_word)))
            if settings['types']['option']['hl_mixed']['img_svg'] or settings['types']['option']['hl_mixed']['img_link'] or settings['types']['option']['hl_mixed']['checkbox'] or settings['types']['option']['hl_mixed']['input']:
                names_var = []
                scripts_incl.append('uploadElements();')
                for word in settings['types']['option']['hl_mixed']['input']:
                    names_var.append(f'hl_input_{word}')
                for word in settings['types']['option']['hl_mixed']['checkbox']:
                    names_var.append(f'hl_check_{word}')
                for word in settings['types']['option']['hl_mixed']['img_link']:
                    names_var.append(f'hl_image_{word}')
                    scripts_incl.append(f'''uploadImage('btn_hl_image_{word}','hl_image_{word}');''')

                for word in settings['types']['option']['hl_mixed']['img_svg']:
                    names_var.append(f'hl_svg_{word}')
                    scripts_incl.append(f'''updateSvgPreviewInRealTime('preview_hl_svg_{word}','hl_svg_{word}');''')
                scripts_incl.append(f'''    document.getElementById('save_data').addEventListener('click',function (){{
        let items = {[i for i in names_var]}
        createElement(items)
        resetValue(items)
    }})''')
                scripts_func.append(script_hl_func)

            index_dom_func = data.index('document.addEventListener("DOMContentLoaded"')
            index_dom_func_start = data[index_dom_func:].index('{')+1
            index_dom_start = index_dom_func+index_dom_func_start
            data = data[:index_dom_start] + f'\n'.join(scripts_incl)+ data[index_dom_start:]
            data = data[:index_dom_func] + f'\n'.join(scripts_func)+'\n' +data[index_dom_func:]


            with open(settings['main']['js_file'], 'w', encoding='utf-8') as file:
                file.write(data)
                coloreg('Скрипти додані !!! ', 'green')
        except Exception as e:
            write_error(e=e)
            coloreg('Не вдалося прочитати або записати файл!!! (перегляньте файл <debug.log>)', 'red')
    else:
        coloreg('Скрипти не додані !!! (перегляньте файл <debug.log>)', 'red')
        write_error(
            text=f'Файл {settings['path']['js']}не існує !!! ')

def add_labels_options(settings):
    if os.path.exists(settings['main']['main_file']):
        try:
            with open(settings['main']['main_file'], 'r', encoding='utf-8') as file:
                data = file.read()
            get_rest_info = []
            register_settings = []
            get_value =[]
            fields = []
            # Додаємо поля label + input
            if settings['types']['option']['input']:
                fields.append(f'            <div class="form-container-input">')
                for word in settings['types']['option']['input']:
                    get_value.append(get_value_options.replace('LWORD',f'input_{word.lower()}'))
                    get_rest_info.append(f'        \'input_{word.lower()}\' => \'plain\'')
                    register_settings.append(f'        \'input_{word.lower()}\'')
                    fields.append(input_option.replace('LWORD',f'input_{word.lower()}').replace('CWORD',word.capitalize()))
                else:
                    fields.append(f'            </div>')
                    coloreg('Всі поля <input> додані !!!', 'green')

            # Додаємо поля label + checkbox
            if settings['types']['option']['checkbox']:
                fields.append(f'    <div class="form-container-check">')
                for word in settings['types']['option']['checkbox']:
                    get_value.append(f'{get_value_options[:-1]} ==\'on\' ? \'checked\' : \'\';'.replace('LWORD',f'check_{word.lower()}'))
                    fields.append(checkbox_option.replace('LWORD', f'check_{word.lower()}').replace('CWORD', word.capitalize()))
                    get_rest_info.append('''         \'check_LWORD\' => \'plain\''''.replace('LWORD', f'{word.lower()}'))
                    register_settings.append(f'''         \'check_{word.lower()}\'''')
                else:
                    fields.append(f'    </div>')
                    coloreg('Всі поля <checkbox> додані !!!', 'green')

            # Додаємо поля image link
            if settings['types']['option']['img_link']:
                fields.append(f'    <div class="form-container-image">')
                for word in settings['types']['option']['img_link']:
                    get_value.append(get_value_options.replace('LWORD', f'img_{word.lower()}').replace(f'img_{word.lower()}\');',f'load_image_text_{word.lower()}\');'))
                    get_rest_info.append(f'        \'load_image_text_{word.lower()}\' => \'plain\'')
                    register_settings.append(f'        \'load_image_text_{word.lower()}\'')
                    fields.append(img_link_option.replace('LWORD', f'{word.lower()}').replace('CWORD', word.capitalize()))
                else:
                    fields.append(f'    </div>')
                    coloreg('Всі поля <img_link> додані !!!', 'green')

            # Додаємо поля image svg
            if settings['types']['option']['img_svg']:
                fields.append(f'    <div class="form-container-image-svg">')
                for word in settings['types']['option']['img_svg']:
                    get_value.append(get_value_options.replace('LWORD', f'svg_{word.lower()}').replace(f'svg_{word.lower()}\');',f'text_svg_area_{word.lower()}\');'))
                    get_rest_info.append(f'        \'text_svg_area_{word.lower()}\' => \'plain\'')
                    register_settings.append(f'        \'text_svg_area_{word.lower()}\'')
                    fields.append(img_svg_option.replace('LWORD', f'{word.lower()}').replace('CWORD', word.capitalize()))
                else:
                    fields.append(f'    </div>')
                    coloreg('Всі поля <img_link> додані !!!', 'green')

            # Додаємо поля points
            if settings['types']['option']['points']:
                for word in settings['types']['option']['points']:
                    get_value.append(
                        f'''            $points_{word.lower()} = get_option('save_data_points_{word.lower()}') ? : '[]';''')
                    fields.append(points_option.replace('LWORD', word.lower()).replace('CWORD', word.capitalize()))
                    get_rest_info.append(f'        \'save_data_points_{word.lower()}\' => \'json\'')
                    register_settings.append(f'        \'save_data_points_{word.lower()}\'')
                    coloreg('Всі <points> додані !!!', 'green')

            # Додаємо поля table
            if settings['types']['option']['table']:
                t_value = []
                l_table = []
                get_value.append(f'''    $table_data = get_option('table_data') ? : '[]';''')
                l_table.append('''<th>#</th>''')
                for word in settings['types']['option']['table']:
                    t_value.append(table_input.replace('LWORD', word.lower()).replace('CWORD', word.capitalize()))
                    l_table.append(f'''                        <th>{word.capitalize()}</th>''')
                l_table.append('''                        <th>Action</th>''')
                fields.append(
                    table_option.replace('LABEL_WORD', '\n'.join(t_value)).replace('LINES_WORD', '\n'.join(l_table)))
                get_rest_info.append(f'''            \'table_data\' => \'json\'''')
                register_settings.append(f'        \'table_data\'')
                coloreg('Всі поля  <table> додані !!!', 'green')

            # Додаємо поля hard label
            if settings['types']['option']['hl_mixed']['img_svg'] or settings['types']['option']['hl_mixed']['img_link'] or \
                    settings['types']['option']['hl_mixed']['checkbox'] or settings['types']['option']['hl_mixed']['input']:
                get_value.append('''            $data = get_option('save_data_text') ? : '[]';''')
                fields.append('''           <div class="hl_container_hero">
                <div class="hl_container_data">
                    <input type="text" hidden="hidden" id="save_data_text" name="save_data_text" value="<?php echo esc_attr($data) ?>">''')

                get_rest_info.append(f'        \'save_data_text\' => \'json\'''')
                register_settings.append(f'         \'save_data_text\'')

                for word in settings['types']['option']['hl_mixed']['input']:
                    fields.append(
                        hl_input_option.replace('LWORD', f'hl_input_{word.lower()}').replace('CWORD', word.capitalize()))
                for word in settings['types']['option']['hl_mixed']['checkbox']:
                    fields.append(
                        hl_checkbox_option.replace('LWORD', f'hl_check_{word.lower()}').replace('CWORD',
                                                                                              word.capitalize()))
                for word in settings['types']['option']['hl_mixed']['img_link']:
                    fields.append(hl_img_link_option.replace('LWORD', f'hl_image_{word.lower()}').replace('CWORD',
                                                                                                       word.capitalize()))
                for word in settings['types']['option']['hl_mixed']['img_svg']:
                    fields.append(
                        hl_img_svg_option.replace('LWORD', f'hl_svg_{word.lower()}').replace('CWORD', word.capitalize()))
                fields.append('''                    <input type="button" value="Save data" id="save_data">
                </div>
                <div class="hl_preview_all" id="hl_preview_all">

                </div>
            </div>''')
                coloreg('Всі поля <hl_mixed> додані !!!', 'green')

            if settings['types']['option']['img_svg'] or settings['types']['option']['img_link'] or \
                    settings['types']['option']['checkbox'] or settings['types']['option']['input'] or \
                    settings['types']['option']['hl_mixed']['img_svg'] or settings['types']['option']['hl_mixed'][
                'img_link'] or settings['types']['option']['hl_mixed']['checkbox'] or \
                    settings['types']['option']['hl_mixed']['input'] or settings['types']['option']['points'] or \
                    settings['types']['option']['table']:
                index_render_func = data.index('function render_')
                index_start_render = data[index_render_func:].index('//++')
                index_func = index_render_func + index_start_render + 4
                data = data[:index_func] + f'\n{'\n'.join(get_value)}' + data[index_func:]

                index_render_func = data.index('function render_')
                index_end_func = data[index_render_func:].index('//++')
                index_star_value = data[index_render_func+index_end_func:].index('?>')
                index_func = index_render_func + index_end_func + index_star_value + 2
                data = data[:index_func] + f'\n {'\n'.join(fields)}' + data[index_func:]

                index_save_func = data.index('function get_')
                index_start_save = data[index_save_func:].index('$meta_fields = [')
                index_save = index_save_func + index_start_save + 16
                data = data[:index_save] + f'\n {',\n'.join(get_rest_info)},' + data[index_save:]

                index_add_func = data.index('function register_settings')
                index_start_add = data[index_add_func:].index('$meta_fields = [')
                index_add = index_add_func + index_start_add + 16
                data = data[:index_add] + f'\n {',\n'.join(register_settings)}' + data[index_add:]


            with open(settings['main']['main_file'], 'w', encoding='utf-8') as file:
                file.write(data)
        except Exception as e:
            write_error(e=e)
            coloreg('Не вдалося прочитати або записати файл!!! (перегляньте файл <debug.log>)', 'red')
    else:
        coloreg('Поля не додані !!! (перегляньте файл <debug.log>)', 'red')
        write_error(
            text=f'Файл {settings['main']['main_file']}не існує, або назва введена не коректно !!! ')

def create_options(settings):
    create_php_js_css(settings)
    if  settings['global']['create_with_label']:
        add_labels_options(settings)
        add_styles(settings)
        add_scripts(settings)
    if settings['global']['include_in_func']:
        try:
            with open(f"{settings['main']['main_path']}\\functions.php", 'r+', encoding='utf-8') as file:
                part_path = f"{settings['path']['inc']}\\{settings['main']['word']}_admin_panel.php".replace(f'{settings['main']['main_path']}','')
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