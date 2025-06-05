import datetime
import io
import os
import zipfile
import requests
from core.functions import version_comparison, copy_all, get_value_in_dict, get_value_on_other_value
from core.logging.log import ErrorAndInitLogging


class BaseWPDeployer:

    def __init__(self,  main_settings, wp_settings, CustomLogging:ErrorAndInitLogging):
        self.main_settings = main_settings
        self.wp_settings = wp_settings
        self.url_version  = get_value_in_dict(main_settings, 'wordpress_version')
        self.url_download  = get_value_in_dict(main_settings, 'wordpress_download')
        self.data_folder = get_value_in_dict(main_settings, 'path_to_data')
        self.environment_name = wp_settings['environment_name']
        self.error_log = CustomLogging.write_debug
        self.info_log = CustomLogging.write_info

    def check_file_in_folder(self,filename_startswith,source_file = None):
        source_file = self.data_folder if not source_file else source_file
        # Перевіряємо наявність файлів, назва яких починається з "wordpress-" у вказаній папці
        for filename in os.listdir(source_file):
            if filename.startswith(filename_startswith):
                return filename
        self.error_log(f"Файл {source_file} не знайдений.")
        self.info_log('error', f"Файл {source_file} не знайдений.")
        return False

    def delete_wp_file(self, wp_file):
        # Формуємо повний шлях до файлу
        file_path = os.path.join(self.data_folder, wp_file)

        try:
            # Перевіряємо, чи існує файл
            if os.path.exists(file_path):
                os.remove(file_path)  # Видаляємо файл
                self.info_log('info',f"Файл {wp_file} успішно видалений з {self.data_folder}.")
            else:
                self.info_log('error',f"Файл {wp_file} не знайдений у {self.data_folder}.")

        except Exception as e:
            self.error_log(f"Помилка при видаленні файлу {wp_file}: {e}")
            self.info_log('error', f"Помилка при видаленні файлу {wp_file}: {e}")

    def get_latest_wordpress_version(self):
        latest_version = None
        try:
            # Отримуємо дані з API
            response = requests.get(self.url_version)
            if response.status_code == 200:
                data = response.json()
                latest_version = data['offers'][0]['version']
                self.info_log("info",f"Остання доступна версія WordPress: {latest_version}")

            else:
                self.error_log(f"❌ Помилка при отриманні даних. Код: {response.status_code}")

        except Exception as e:
            self.error_log(f"❌ Помилка: {e}")

        finally:
            return latest_version

    def download_wp(self):
        try:
            latest_version_wp = self.get_latest_wordpress_version()
        except Exception as e:
            self.error_log(f"Помилка при отриманні версії WordPress: {e}")
            self.info_log("info",f"Помилка при отриманні версії WordPress: {e}")
            return

        wp_in_folder = self.check_file_in_folder('wordpress-')
        if wp_in_folder:
            version_wp_in_folder = wp_in_folder.replace('wordpress-', '')
        else:
            version_wp_in_folder = '0.0.0'

        if version_comparison(version_wp_in_folder, latest_version_wp):
            self.info_log("info", f"⬇️ Доступна нова версія WordPress!")

            if version_wp_in_folder != '0.0.0':
                self.delete_wp_file(f'wordpress-{version_wp_in_folder}')

            self.info_log("info", f"⬇️ Завантаження WordPress з {self.url_version}...")
            try:
                response = requests.get(self.url_download)
                response.raise_for_status()  # Перевірка на помилки HTTP
                self.info_log("success", "✅ Успішно завантажено!")
                # Розпаковка архіву
                # Розпаковка архіву
                with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                    # Отримуємо ім'я першої папки в архіві
                    archive_name = zip_ref.namelist()[0].split('/')[0]  # Видасть 'wordpress' або інше ім'я

                    # Формуємо шлях до нової папки з версією
                    target_folder = os.path.join(self.data_folder, f'wordpress-{latest_version_wp}')
                    os.makedirs(target_folder, exist_ok=True)

                    # Розпаковка архіву в зазначену папку
                    self.info_log("info", f"📦 Розпаковка в папку: {target_folder}")

                    zip_ref.extractall(target_folder)

                    self.info_log("success", f"🎉 WordPress завантажено в папку: {target_folder}")

            except requests.exceptions.RequestException as e:
                self.info_log("error", f"❌ Помилка при завантаженні! {e}")
                self.error_log(f"❌ Помилка при завантаженні! {e}")

        else:
            self.info_log("info", f"Встановлена остання версія WordPress !!!")
    
    def copy_wp(self,folder_path, folder_name):
        global source_path_folder
        self.download_wp()
        path_to_wp_version = self.check_file_in_folder('wordpress-')
        path_to_wp_files = None
        if path_to_wp_version:
            path_to_wp_files = rf'{self.data_folder}\{path_to_wp_version}\{self.check_file_in_folder('wordpress',rf'{self.data_folder}\{path_to_wp_version}')}'
            if path_to_wp_files:
                try:
                    source_path_folder = rf'{folder_path}\{folder_name}'
                    os.makedirs(source_path_folder, exist_ok=False)  # Якщо папка вже є, помилки не буде todo - замінити на False
                    self.info_log('success', f"✅ Папку створено: {folder_path}")
                except Exception as e:
                    suffics = f'{datetime.datetime.now().strftime('%Y_%m_%d')}'
                    source_path_folder = rf'{folder_path}\{folder_name}___{suffics}'
                    os.makedirs(source_path_folder, exist_ok=False)  # Якщо папка вже є, помилки не буде
                    self.error_log(f"❌ Помилка при створенні папки: {e}")
                    self.info_log('exist', f"✅ Папка {folder_name} уже існує, то було створено < {folder_name}___{suffics} > ")
                finally:
                    try:
                        copy_all(path_to_wp_files, source_path_folder)
                        self.info_log('info', f"✅ WordPress скопійовано")
                        return source_path_folder
                    except Exception as e:
                        self.error_log(f"❌ Помилка при копіюванні WordPress: {e}")
                        self.info_log('error',f"❌ Помилка при копіюванні WordPress: {e}")

        else:
                self.error_log(f"❌ Якимось чином WordPress не знайдено")
                self.info_log('error',f"❌ Якимось чином WordPress не знайдено")

    def get_active_environments(self, name_filter):
        by_name = get_value_on_other_value(self.main_settings, 'name', name_filter)
        by_active = get_value_on_other_value(self.main_settings, 'active', True)
        return [item for item in by_name if item in by_active]

    def deploy_wp(self):
        raise NotImplementedError('Перевизначено в дочірніх класах!')
    def reload_program(self):
        raise NotImplementedError('Перевизначено в дочірніх класах!')

if __name__ == '__main__':
    pass
    # url = 'https://wordpress.org/latest.zip'
    # path = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\data'
    # path_to_debug = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\debug.log'
    # path_to_info = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\info.md'
    # dep = BaseDeployer(url,path,ErrorAndInitLogging(path_to_debug,path_to_info))
    # dep.copy_wp(r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\data','say')
    # dep.deploy_wp()