import os

from core.custom_file_editors.FunctionEditor import FunctionEditor
from core.tools.file_manager.file_manager import FileManager
from core.tools.handlers.handler_path import HandlerPath
from logger.logger import CustomLogger


class BaseAdminPanel:
    def __init__(self, theme_path, data_path):
        self.theme_path = theme_path
        self.handler_path = HandlerPath()
        self.file_manager = FileManager()
        self.error_log = CustomLogger().error_log
        self.function_editor = FunctionEditor(os.path.join(theme_path, 'functions.php'))
        self.function_editor = FunctionEditor(os.path.join(theme_path, 'functions.php'))

        self.path_to_admin_panel = data_path['path_to_admin_panel']
        self.path_to_ap_styles = data_path['path_to_ap_styles']
        self.path_to_ap_scripts = data_path['path_to_ap_scripts']
        self.part_path_to_css = ''
        self.part_path_to_js = ''

        custom_func_template = self.handler_path.find_file(['wordpress', 'admin_page'], self.handler_path.base_dir)
        self.custom_func_template = self.handler_path.find_file('base_admin_panel.txt', custom_func_template)

    def __get_part_path(self, full_path):
        try:
            return full_path.replace(self.theme_path, '')
        except Exception as e:
            self.error_log(e)
            return ''

    def __get_data(self, phrase):
        file_data = self.file_manager.read_file(self.custom_func_template)
        index_start = file_data.find(phrase) + len(phrase)
        index_end = file_data[index_start:].find('/***/') + index_start
        return file_data[index_start:index_end]

    def __create_file(self, file_name, parent_folder, init_phrase):
        try:
            data_file = self.__get_data(init_phrase)
            full_path_to_file = str(os.path.join(self.handler_path.find_file(parent_folder, self.theme_path),file_name))
            if file_name.endswith('.css'):
                self.part_path_to_css = full_path_to_file.replace(self.theme_path,'').replace('\\','/')

            elif file_name.endswith('.js'):
                self.part_path_to_js = full_path_to_file.replace(self.theme_path,'').replace('\\','/')

            else:


                data_file = data_file.replace('CSS_PATH',self.part_path_to_css)
                data_file = data_file.replace('JS_PATH',self.part_path_to_js)
                part_path_php = full_path_to_file.replace(self.theme_path,'')
                self.function_editor.include_in_functions(part_path_php, 'admin_panel')

            self.file_manager.write_file(full_path_to_file,data_file)
            self.error_log(f'Файл < {file_name} > додано!')
        except Exception as e:
            self.error_log(e)

    def create(self):
        try:
            data_files = {
                'ap_theme_settings_styles.css': [self.path_to_ap_styles, "/***/ CSS"],
                'ap_theme_settings_scripts.js': [self.path_to_ap_scripts, "/***/ JS"],
                'theme_settings.php': [self.path_to_admin_panel, "/***/ HTML"],
            }
            for data_file in data_files:
                file_name = data_file
                parent_folder = data_files[data_file][0]
                init_phrase = data_files[data_file][1]
                self.__create_file(file_name, parent_folder, init_phrase)
            self.error_log(f'Базову адмін панель додано!')
        except Exception as e:
            self.error_log(e)


if __name__ == '__main__':
    data = {
        'path_to_admin_panel': 'admin_panel',
        'path_to_ap_styles': 'ap_styles',
        'path_to_ap_scripts': 'ap_scripts',
    }
    bap = BaseAdminPanel(r'D:\Programms\OSPanel\home\Example\wp-content\themes\Example', data)
    bap.create()
