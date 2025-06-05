import os.path
import secrets
import string
from core.custom_file_editors.FunctionEditor import FunctionEditor
from core.custom_file_editors.WpConfigEditor import WpConfigEditor
from core.tools.file_manager.FileContentManager import FileContentManager
from core.tools.file_manager.file_manager import FileManager
from core.tools.handlers.handler_path import HandlerPath
from logger.logger import CustomLogger


class CustomBaseFunctions:
    def __init__(self, path_to_theme, ):
        self.path_to_theme = path_to_theme
        self.path_to_wp_config = os.path.join(path_to_theme[:path_to_theme.find('wp-content')],'wp-config.php')
        self.func_folder = ''

        self.handler_path = HandlerPath()
        self.fcontent_manager = FileContentManager()
        self.error_log = CustomLogger().error_log
        self.file_manager = FileManager()
        self.handler_path = HandlerPath()
        self.function_editor = FunctionEditor(os.path.join(path_to_theme,'functions.php'))
        self.config_editor = WpConfigEditor(self.path_to_wp_config)

    def __check_folder(self, func_folder='helper_func'):
        try:
            path_func_folder_full = self.handler_path.find_file(func_folder, self.path_to_theme)
            if not path_func_folder_full:
                path_func_folder_full = self.fcontent_manager.create_folder(self.path_to_theme, func_folder)

            return path_func_folder_full
        except Exception as e:
            self.error_log(e)
            return ''

    def _create_base_helper_funcs(self, file_name, template_file_name):
        try:
            path_to_file = str(os.path.join(self.__check_folder(), file_name))
            custom_func_template = self.handler_path.find_file(['wordpress', 'custom_func'], self.handler_path.base_dir)
            data = '<?php\n'
            main_data = self.file_manager.read_file(self.handler_path.find_file(template_file_name, custom_func_template))
            data += main_data
            self.file_manager.write_file(path_to_file, data)
            part_path = path_to_file.replace(self.path_to_theme,'')
            self.function_editor.include_in_functions(part_path,'helper_func')
            self.error_log(f'Базова кастомна функція {file_name} створена!')
        except Exception as e:
            self.error_log(e)

    def create_helper_funcs(self):
        template_names = {
            'hf_base_auth.php': 'hf_base_auth.txt',
            'hf_sanitize_checkbox.php': 'hf_sanitize_checkbox.txt',
            'hf_sanitize_svg.php': 'hf_sanitize_svg.txt',
            'hf_normalize_to_array.php': 'hf_normalize_to_array.txt',
            'hf_normalize_array_or_string.php': 'hf_normalize_array_or_string.txt',
            'hf_enqueue_media_uploader.php': 'hf_enqueue_media_uploader.txt',
            'hf_create_meta_field_config.php': 'hf_create_meta_field_config.txt',
            'reorder_theme_settings_sub_menu.php': 'reorder_theme_settings_sub_menu.txt',
        }

        for file_name_php in template_names:
            if file_name_php == 'hf_base_auth.php':
                # Символи, які можна використовувати
                alphabet = string.ascii_letters + string.digits  # A-Z, a-z, 0-9

                # Генеруємо логін і пароль по 32 символи
                login = ''.join(secrets.choice(alphabet) for _ in range(32))
                password = ''.join(secrets.choice(alphabet) for _ in range(32))

                # Формуємо PHP-код
                data = f"define('BASE_AUTH_LOGIN','sl_{login}');\n"
                data += f"define('BASE_AUTH_PASS','sp_{password}');"
                self.config_editor.edit_custom_values(data)
            file_name_txt = template_names[file_name_php]

            self._create_base_helper_funcs(file_name_php,file_name_txt)


if __name__ == '__main__':
    cbf = CustomBaseFunctions(r'D:\Programms\OSPanel\home\Example\wp-content\themes\Example')
    cbf.create_helper_funcs()
