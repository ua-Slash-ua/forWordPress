import os

from core.custom_file_editors.FunctionEditor import FunctionEditor
from core.custom_file_editors.WpConfigEditor import WpConfigEditor
from core.custom_functions.BaseAdminPanel import BaseAdminPanel
from core.custom_functions.CustomBaseFunctions import CustomBaseFunctions
from core.custom_themes.WpBaseStructure import WpBaseStructure
from core.tools.data_finder.data_finder import DataFinder
from core.tools.file_manager.FileContentManager import FileContentManager
from core.tools.file_manager.file_manager import FileManager
from core.tools.handlers.handler_path import HandlerPath
from logger.logger import CustomLogger


class CustomThemes:
    def __init__(self):
        self.error_log = CustomLogger().error_log
        self.file_manager = FileManager()
        self.fcontent_manager = FileContentManager()
        self.handler_path = HandlerPath()



        self.ct_config_path = self.handler_path.find_file('custom_themes_config.json',self.handler_path.base_dir)
        self.ct_config = self.file_manager.read_file(self.ct_config_path)
        self.data_finder = DataFinder(self.ct_config)

        self.themes_path = self.data_finder.find('path_to_themes', 0)
        self.themes_name = self.data_finder.find('themes_name', 0).lower()

        self.template_wp_dir = self.handler_path.find_file(['templates', 'wordpress'], self.handler_path.base_dir)


    def create_index_php(self,path_to_theme):
        try:
            file_name = 'index.php'
            full_path_to_file = os.path.join(path_to_theme, file_name)
            data = '''<?php'''
            self.file_manager.write_file(full_path_to_file,data)
            self.error_log(f'Файл < {file_name} > створено')
        except Exception as e:
            self.error_log(e)

    def create_style_css(self, path_to_theme):
        try:
            path_to_template = self.handler_path.find_file('main_style.css',self.template_wp_dir)
            file_name = 'style.css'
            full_path_to_file = os.path.join(path_to_theme, file_name)
            data = self.file_manager.read_file(path_to_template).replace('THEMES_NAME', self.themes_name.capitalize() )
            self.file_manager.write_file(full_path_to_file,data)
            self.error_log(f'Файл < {file_name} > створено')
        except Exception as e:
            self.error_log(e)

    def create_functions_php(self,path_to_theme):
        try:
            file_name = 'functions.php'
            full_path_to_file = os.path.join(path_to_theme, file_name)
            func_editor = FunctionEditor(full_path_to_file)
            data = '<?php\n\n'
            data += "define('THEME_PATH',get_template_directory());\n"
            data += "define('THEME_URI',get_template_directory_uri());\n\n"
            data +=  '\n\n'.join(func_editor.get_all_include())
            self.file_manager.write_file(full_path_to_file,data)
            self.error_log(f'Файл < {file_name} > створено')
        except Exception as e:
            self.error_log(e)



    def deploy(self):
        try:
            path_to_theme = self.fcontent_manager.create_folder(self.themes_path, self.themes_name.capitalize(),exist_ok = True)
            self.create_index_php(path_to_theme)
            self.create_style_css(path_to_theme)
            self.create_functions_php(path_to_theme)
            # Створення базової структури теми
            wp_base_structure = WpBaseStructure(path_to_theme)
            wp_base_structure.base_deploy()
            # Підключення стандартних функцій
            base_func = CustomBaseFunctions(path_to_theme)
            base_func.create_helper_funcs()
            # Підключення стандартної(головної) адмін панелі
            data = {
                'path_to_admin_panel': 'admin_panel',
                'path_to_ap_styles': 'ap_styles',
                'path_to_ap_scripts': 'ap_scripts',
            }
            bap = BaseAdminPanel(path_to_theme, data)
            bap.create()
            path_to_wp_config = os.path.join(path_to_theme[:path_to_theme.find('wp-content')],'wp-config.php')
            ce = WpConfigEditor(path_to_wp_config)
            ce.edit_wp_debug()

            self.error_log(f'Тему < {self.themes_name.capitalize()} > створено')
        except Exception as e:
            self.error_log(e)



if __name__ == '__main__':
    ct = CustomThemes()
    ct.deploy()