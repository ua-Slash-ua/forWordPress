import os
import shutil
from core.functions import *
from core.logging.log import ErrorAndInitLogging
from core.wp_deploy.open_server_wp_deploy import OpenServerWPDeployer
from data.templates.wordpress.config_php import config_for_custom_values, config_debug, config_start_debug


class BaseWPThemesDeploy:
    def __init__(self, main_settings, wp_settings, CustomLogging:ErrorAndInitLogging):
        self.my_logger = CustomLogging
        self.path_to_wp_settings = get_value_in_dict(main_settings, "wp_config")
        self.main_settings = main_settings
        self.wp_settings = wp_settings
        self.data_folder = get_value_in_dict(main_settings, 'path_to_data')
        self.wordpress_template_folder = get_value_in_dict(main_settings, 'path_to_template_wordpress')
        self.environment_name = str(wp_settings['environment_name'])
        self.environment_path = str(wp_settings['environment_path'])

        self.full_path_to_themes = find_full_path(self.environment_path, 'themes')
        self.path_to_my_themes = f'{self.full_path_to_themes}\\{self.environment_name}'

        self.error_log = CustomLogging.write_debug
        self.info_log = CustomLogging.write_info



    def clear_themes(self):

        for filename in os.listdir(self.full_path_to_themes):
            file_path = os.path.join(self.full_path_to_themes, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Видаляє файл або символічне посилання
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Видаляє папку рекурсивно

            except Exception as e:
                msg = f'Помилка при видаленні {file_path}: {e}'
                print(msg)
                self.error_log(msg)
                self.info_log("error", msg)

        self.info_log("info", 'Усі файли в папці <themes> видалені!')

    def create_new_themes(self):
        pass
    def load_new_themes(self):
        self.clear_themes()
        path_to_mnt = find_full_path(self.wordpress_template_folder,'my_new_theme')
        os.makedirs(self.path_to_my_themes)

        data_index = read_txt_file(f'{path_to_mnt}\\main_index.html')
        data_style = read_txt_file(f'{path_to_mnt}\\main_style.css')
        data_functions = read_txt_file(f'{path_to_mnt}\\functions.php')

        data_style = data_style.replace('THEMES_NAME',self.wp_settings['environment_name'].capitalize())
        data_style = data_style.replace('THEMES_AUTHOR',self.wp_settings['themes_author'].capitalize())
        data_style = data_style.replace('THEMES_AUTHOR_URL',self.wp_settings['themes_author_url'])
        data_style = data_style.replace('THEMES_DESCRIPTION',self.wp_settings['themes_description'].capitalize())
        data_style = data_style.replace('THEMES_VERSION',self.wp_settings['themes_version'])

        path_to_index = f'{self.path_to_my_themes}\\index.php'
        path_to_style = f'{self.path_to_my_themes}\\style.css'
        path_to_functions = f'{self.path_to_my_themes}\\functions.php'
        path_to_screenshot = f'{self.path_to_my_themes}\\screenshot.png'
        path_to_inc = f'{self.path_to_my_themes}\\inc'
        path_to_inc_AP = f'{path_to_inc}\\admin_panel'
        path_to_inc_AP_styles = f'{path_to_inc_AP}\\ap_styles'
        path_to_inc_AP_scripts = f'{path_to_inc_AP}\\ap_scripts'



        write_txt_file(path_to_index,data_index)
        write_txt_file(path_to_style,data_style)
        write_txt_file(path_to_functions,data_functions)

        for path in [path_to_inc,
                     path_to_inc_AP,
                     path_to_inc_AP_styles,
                     path_to_inc_AP_scripts]:
            os.makedirs(path, exist_ok=True)


        copy_image(f'{path_to_mnt}\\screenshot.png', path_to_screenshot)

        self.wp_settings['environment_themes_path'] = self.path_to_my_themes
        write_json_settings(self.wp_settings, self.path_to_wp_settings, self.my_logger)
        self.info_log("success", 'Базові папки і файли для теми створені !')


if __name__ == '__main__':
    path_to_main_settings = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\config\main_config.json'
    path_to_wp_settings = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\config\wp_config.json'
    path_to_debug = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\debug.log'
    path_to_info = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\info.md'

    my_logger = ErrorAndInitLogging(path_to_debug, path_to_info)
    main_settings = read_json_settings(path_to_main_settings, my_logger)
    wp_settings = read_json_settings(path_to_wp_settings, my_logger)

    # deployer = OpenServerWPDeployer(main_settings, wp_settings, my_logger)
    # deployer.deploy_wp()
    # bd = BaseWPThemesDeploy(main_settings, wp_settings, my_logger)
    # bd.load_new_themes()