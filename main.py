from core.functions import read_json_settings
from core.logging.log import ErrorAndInitLogging
from core.wp_deploy.open_server_wp_deploy import OpenServerWPDeployer
from core.wp_themes_deploy.base_edit_config_php import BaseEditConfigPhp
from core.wp_themes_deploy.base_wp_themes_deploy import BaseWPThemesDeploy

def create_new_project_os(main_settings, wp_settings, my_logger):




    deployer = OpenServerWPDeployer(main_settings, wp_settings, my_logger)
    deployer.deploy_wp()
    deployer.reload_program()

    bd = BaseWPThemesDeploy(main_settings, wp_settings, my_logger)
    bd.load_new_themes()

def write_debug(env_path, my_logger):
    bec = BaseEditConfigPhp(env_path, my_logger)
    bec.edit_config()

def create_ap():
    pass

def main():
    path_to_main_settings = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\config\main_config.json'
    path_to_wp_settings = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\config\wp_config.json'
    path_to_ap_settings = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\config\admin_panel_config.json'
    path_to_debug = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\debug.log'
    path_to_info = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\info.md'

    my_logger = ErrorAndInitLogging(path_to_debug, path_to_info)
    main_settings = read_json_settings(path_to_main_settings, my_logger)
    ap_settings = read_json_settings(path_to_main_settings, my_logger)
    wp_settings = read_json_settings(path_to_wp_settings, my_logger)

    # create_new_project_os(main_settings, wp_settings, my_logger)

    # write_debug(wp_settings['environment_themes_path'],my_logger)


    create_ap()
if __name__ == '__main__':
    main()