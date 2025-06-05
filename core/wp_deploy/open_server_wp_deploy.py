import os
import time
from core.functions import *
from core.logging.log import ErrorAndInitLogging
from core.wp_deploy.base_wp_deploy import BaseWPDeployer
import webbrowser




os_process = ['mysqld.exe', 'msedgewebview2.exe', 'httpd.exe']

class OpenServerWPDeployer(BaseWPDeployer):
    def __init__(self, main_settings, wp_settings, CustomLogging):
        super().__init__(main_settings,wp_settings, CustomLogging)
        self.path_to_template_osp = get_value_in_dict(main_settings, 'path_to_template_wordpress')
        self.path_to_main_settings = get_value_in_dict(main_settings, "main_config")
        self.path_to_wp_settings = get_value_in_dict(main_settings, "wp_config")




    def deploy_wp(self):
        active_custom_environment = self.get_active_environments('OpenServer')
        for environment in active_custom_environment:
            folder_path = environment['path']
            folder_name = self.wp_settings['environment_name']
            try:
                self.info_log("info", "🚀 Розгортання WordPress в кастомне середовище розпочато")

                path_to_folder_environment = self.copy_wp(folder_path=folder_path, folder_name=folder_name)
                folder_name_right_index = path_to_folder_environment.rfind('\\')
                folder_name = path_to_folder_environment[folder_name_right_index+1:]
                try:
                    os.makedirs(rf'{path_to_folder_environment}\.osp', exist_ok=True)
                    template_osp = read_txt_file(rf'{self.path_to_template_osp}\osp')
                    template_osp = template_osp.replace('NAME',f'{folder_name.lower()}')
                    write_txt_file(rf'{path_to_folder_environment}\.osp\project.ini',template_osp)
                    self.info_log("success", f"🎉 WordPress успішно скопійовано в {folder_path}")
                    self.reload_program()
                    # Відкриває нову вкладку з URL
                    url_env = f'https://{folder_name.lower()}/wp-admin/setup-config.php'
                    webbrowser.open_new_tab(url_env)
                    webbrowser.open_new_tab("https://phpmyadmin.local/")
                    self.wp_settings['environment_path'] = path_to_folder_environment
                    write_json_settings(self.wp_settings, self.path_to_wp_settings, my_logger)
                except Exception as e:
                    self.error_log(f"❌ Помилка під час створення < project.ini >: {e}")
                    self.info_log("error", f"❌ Помилка під час створення < project.ini >: {e}")


                # Тут можна ще додати логіку: копіювання теми, плагінів, зміна wp-config.php тощо

            except Exception as e:
                self.error_log(f"❌ Помилка під час розгортання: {e}")
                self.info_log("error", f"❌ Помилка під час розгортання: {e}")

    def reload_program(self):
        program_path = get_value_in_dict(self.main_settings, 'OpenServer_program')
        program_name = program_path[program_path.rindex('\\') + 1:]

        try:
            if is_program_running(program_name):
                os_process.append(program_name)
                print(os_process)
                kill_program(os_process)
                self.info_log("info", f"⏹ Програму < {program_name} > завершено")
                time.sleep(1)  # даємо трішки часу системі
            os.startfile(program_path)
            self.info_log("success", f"🎉 Програму < {program_name} > перезапущено")
        except Exception as e:
            self.error_log(f"❌ Помилка під час перезавантаження < {program_name} >: {e}")
            self.info_log("error", f"❌ Помилка під час перезавантаження < {program_name} >: {e}")



if __name__ == '__main__':
    path_to_main_settings = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\config\main_config.json'
    path_to_wp_settings = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\config\wp_config.json'
    path_to_debug = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\debug.log'
    path_to_info = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\info.md'

    my_logger = ErrorAndInitLogging(path_to_debug, path_to_info)
    main_settings = read_json_settings(path_to_main_settings,my_logger)
    wp_settings = read_json_settings(path_to_wp_settings,my_logger)

    deployer = OpenServerWPDeployer(main_settings, wp_settings, my_logger)
    deployer.deploy_wp()
    deployer.reload_program()
