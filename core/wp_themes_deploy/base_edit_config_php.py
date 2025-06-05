import os
import shutil
from core.functions import *
from core.logging.log import ErrorAndInitLogging
from core.wp_deploy.open_server_wp_deploy import OpenServerWPDeployer
from data.templates.wordpress.config_php import config_for_custom_values, config_debug, config_start_debug

class BaseEditConfigPhp:
    def __init__(self, environment_path, CustomLogging:ErrorAndInitLogging):
        self.environment_path = environment_path

        self.error_log = CustomLogging.write_debug
        self.info_log = CustomLogging.write_info

        name_config_file = r'\wp-config-sample.php'
        self.path_to_config = self.environment_path[:self.environment_path.index('wp-content')] + name_config_file

    def write_config(self, index_start, index_end, data: list):
        source = read_txt_file(self.path_to_config)
        try:
            source = source[:index_start] + '\n'.join(data) + source[index_end:]
            write_txt_file(self.path_to_config, source)
            self.info_log('success', f"Файл конфігурації успішно оновлено: {self.path_to_config}")
        except Exception as e:
            self.error_log(f"[edit_config] Unknown error: {e}")
            self.info_log('error', f"Невідома помилка при редагуванні конфігурації: {e}")

    def find_index(self, init_phrase, stop_phrase, reverse = False):
        data_config = read_txt_file(self.path_to_config)
        index_config_start = data_config.index(config_for_custom_values)
        if not reverse:
            index_config_end = index_config_start + data_config[index_config_start + len(init_phrase) + 1 :].index(stop_phrase)  - 1
            return index_config_start,index_config_end
        else:
            index_config_end = data_config[:index_config_start - 1].rfind(stop_phrase) + len(stop_phrase) + 1
            return  index_config_end, index_config_start - 1


    def edit_config(self):
        try:
            istart, isstop = self.find_index( config_for_custom_values, config_start_debug, True)
            self.write_config(istart, isstop,  config_debug)

            self.info_log('success', f"Файл конфігурації успішно оновлено: {self.path_to_config}")

        except ValueError as e:
            self.error_log(f"[edit_config] ValueError: {e}")
            self.info_log('error', f"Помилка при роботі з рядками у конфіг-файлі: {e}")

        except FileNotFoundError as e:
            self.error_log(f"[edit_config] FileNotFoundError: {e}")
            self.info_log('error', f"Файл конфігурації не знайдено: {e}")

        except Exception as e:
            self.error_log(f"[edit_config] Unknown error: {e}")
            self.info_log('error', f"Невідома помилка при редагуванні конфігурації: {e}")

