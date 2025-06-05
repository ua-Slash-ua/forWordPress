
from core.functions import read_json_settings, get_value_in_dict, get_value_on_other_value, write_json_settings
from core.logging.log import ErrorAndInitLogging
from core.wp_deploy.base_wp_deploy import BaseWPDeployer


class CustomWPDeployer(BaseWPDeployer):
    def __init__(self, main_settings, wp_settings, CustomLogging):
        super().__init__(main_settings, wp_settings, CustomLogging)
        self.path_to_main_settings = get_value_in_dict(main_settings,"main_config")
        self.path_to_wp_settings = get_value_in_dict(main_settings,"wp_config")


    def deploy_wp(self):
        active_custom_environment = self.get_active_environments('Custom_')
        for environment in active_custom_environment:
            folder_path = environment['path']
            folder_name = self.wp_settings['environment_name']
            try:
                self.info_log("info", "🚀 Розгортання WordPress в кастомне середовище розпочато")

                path_to_folder_environment = self.copy_wp(folder_path=folder_path, folder_name=folder_name)
                self.info_log("success", f"🎉 WordPress успішно скопійовано в {path_to_folder_environment}")
                self.wp_settings['environment_path'] = path_to_folder_environment
                write_json_settings(self.wp_settings,path_to_wp_settings,my_logger)


            except Exception as e:
                self.error_log(f"❌ Помилка під час розгортання: {e}")
                self.info_log("error", f"❌ Помилка під час розгортання: {e}")


if __name__ == '__main__':
    path_to_main_settings = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\config\main_config.json'
    path_to_wp_settings = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\config\wp_config.json'
    path_to_debug = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\debug.log'
    path_to_info = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\info.md'

    my_logger = ErrorAndInitLogging(path_to_debug, path_to_info)
    main_settings = read_json_settings(path_to_main_settings,my_logger)
    wp_settings = read_json_settings(path_to_wp_settings,my_logger)

    deployer = CustomWPDeployer(main_settings, wp_settings, my_logger)
    deployer.deploy_wp()
