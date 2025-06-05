
from core.admin_panel.create_post_record import *
from core.functions import *
from core.logging.log import ErrorAndInitLogging
from data.templates.wordpress.themes.admin_panel.base import *


class BaseCreateRecord:
    def __init__(self, ap_settings, main_settings, CustomLogging):
        self.my_logger = CustomLogging
        self.error_log = CustomLogging.write_debug
        self.info_log = CustomLogging.write_info

        self.ap_settings = ap_settings
        self.main_settings = main_settings
        self.path_to_themes =  self.ap_settings['path_to_themes']

        self.folder_inc =  self.ap_settings['folder_inc']
        self.folder_ap =  self.ap_settings['folder_admin_panel']
        self.folder_css =  self.ap_settings['folder_styles']
        self.folder_js =  self.ap_settings['folder_scripts']

        self.path_to_func = self.path_to_themes + '\\functions.php'
        self.path_to_inc = self.find_or_create_folder('inc', fallback_folder=self.folder_inc)
        self.path_to_ap = self.find_or_create_folder('admin_panel', fallback_folder=self.folder_inc, parent_folder=self.path_to_inc)
        self.path_to_css = 'None'
        self.path_to_js = 'None'

        self.template_wp = get_value_in_dict(main_settings, 'path_to_template_wordpress')
        self.template_wp_base = find_full_path(self.template_wp, 'base')
        self.template_wp_post = find_full_path(self.template_wp, 'type_post')




        self.post_type = get_value_in_dict(self.ap_settings,'record_type')
        self.self_type = 'none'
        self.data_name = get_value_in_dict(self.ap_settings,'record_name')
        self.data_icon = get_value_in_dict(self.ap_settings,'record_icon')
        self.name_meta_box = 'None'
        self.priority_meta_box = 'None'
        self.position_meta_box = 'None'
        self.data_item_setting = 'None'

        self.data_js = 'None'
        self.data_js_func = []
        self.data_js_inc = []
        self.data_js_inc_point = []
        self.data_css = []

        self.all_init = []
        self.all_inc = []
        self.data_content_label = []
        self.label_names = []
        self.label_name = 'None'

        self.table_name = 'None'
        self.table_data = 'None'

    def create_file(self, file_path, data):
        try:
            write_txt_file(file_path, data, 'w')
            self.info_log("info", f"Створено файл <{file_path}>")
        except Exception as e:
            self.error_log(f"❌ Не вдалося створити файл '{file_path}': {e}")
            self.info_log("error", f"❌ Не вдалося створити файл '{file_path}': {e}")

    def prepare_path(self, folder, filename, extension):
        """
        Повертає кортеж з повного шляху та відносного (від themes) шляху до файлу.
        """
        rel_path = os.path.join(folder.replace(self.path_to_themes, '').lstrip('/\\'), f"{filename}.{extension}")
        full_path = os.path.join(self.path_to_themes, rel_path)
        return full_path, rel_path

    def replace_template(self, template_string: str) -> str:
        """
        Виконує заміну плейсхолдерів у шаблоні.
        """

        label = '' if isinstance(self.label_name, dict) else str(self.label_name)

        replacements = {
            'LNAME_RT': self.data_name.lower(),
            'CNAME_RT': self.data_name.capitalize(),
            'ICON': self.data_icon.strip(),
            'CSS_PATH': self.path_to_css.replace('\\', '/'),
            'JS_PATH': self.path_to_js.replace('\\', '/'),
            'LNAME_MB': self.name_meta_box.lower(),
            'CNAME_MB': self.name_meta_box.capitalize(),
            'POSITION_MB': self.position_meta_box.lower(),
            'PRIORITY_MB': self.priority_meta_box.lower(),
            'DATA_LABEL_INC': ',\n    '.join(self.all_inc),
            'LLABEL': label.lower(),
            'CLABEL': label.capitalize(),
            'DATA_JS_POINT': label.lower(),
            'LTDLABEL': self.table_name.lower(),
            'CTDLABEL': self.table_name.capitalize(),
            'DTLABEL': self.table_data,
        }

        for key, val in replacements.items():
            if key in template_string:
                template_string = template_string.replace(key, val)

        return template_string

    def replace_template_table(self, template_string: str) -> str:
        """
                Виконує заміну плейсхолдерів у table.
                """
        replacements = {
            'LTDLABEL': self.table_name.lower(),
            'CTDLABEL': self.table_name.capitalize(),
            'DTLABEL': self.table_data,

        }
        for key, val in replacements.items():
            template_string = template_string.replace(key, val)
        return template_string

    def include_func(self, type, part_path):
        data_func = read_txt_file(self.path_to_func)
        search_marker = include_place[type]
        insert_code = include_functions.replace('PART_PATH', f'\\{part_path}')

        index_start_include = data_func.find(search_marker)
        if part_path not in data_func:
            if index_start_include != -1:
                index_start_include += len(search_marker)
                data_func = data_func[:index_start_include + 1] + insert_code + data_func[index_start_include:]
                write_txt_file(self.path_to_func, data_func)
            else:
                # Якщо немає маркера, додай його сам разом із вставкою
                full_insert = f"{search_marker}\n{insert_code}"
                write_txt_file(self.path_to_func, full_insert, 'a+')

    def find_or_create_folder(self, folder_name, fallback_folder=None, parent_folder=None):
        folder_path = ''


        # якщо parent_folder є повним шляхом
        if parent_folder and os.path.isabs(parent_folder):
            base_path = parent_folder
        else:
            base_path = os.path.join(self.path_to_themes, parent_folder) if parent_folder else self.path_to_themes
        stock_path = find_full_path(base_path, folder_name)
        fallback_path = find_full_path(base_path, fallback_folder) if fallback_folder else None

        if stock_path:
            folder_path = stock_path
        elif fallback_path:
            folder_path = fallback_path
        else:
            try:
                folder_path = os.path.join(base_path, folder_name)

                os.makedirs(folder_path, exist_ok=True)
                self.info_log("info", f"Створено папку <{folder_name}> за шляхом {folder_path}")
            except Exception as e:
                self.error_log(f"❌ Не вдалося створити папку '{folder_name}': {e}")
                self.info_log("error", f"❌ Не вдалося створити папку '{folder_name}': {e}")
                return ''  # або підняти виняток
        return folder_path

    def start_create_record(self):
        sub_classes = [
            CreatePostRecord
        ]
        data_items = get_value_in_dict(self.ap_settings, 'items')
        for item in data_items:
            self.data_item_setting = item
            item_type = get_value_in_dict(item,'record_type')
            for item_class in sub_classes:
                ex_class = item_class(self.ap_settings, self.main_settings, self.my_logger)
                if ex_class.self_type == item_type:
                    ex_class.data_item_setting = self.data_item_setting
                    self.info_log("info", f" Починаю створювати < {self.post_type} >")
                    ex_class.start_create_record()
                    break
            else:
                self.error_log(f"❌ Невідомий тип запису < {self.post_type} >")
                self.info_log("error", f"❌ Невідомий тип запису < {self.post_type} >")



if __name__ == '__main__':
    path_to_main_settings = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\config\main_config.json'
    path_to_wp_settings = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\config\wp_config.json'
    path_to_ap_settings = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\config\admin_panel_config.json'
    path_to_debug = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\debug.log'
    path_to_info = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\info.md'

    my_logger = ErrorAndInitLogging(path_to_debug, path_to_info)
    main_settings = read_json_settings(path_to_main_settings, my_logger)
    ap_settings = read_json_settings(path_to_ap_settings, my_logger)
    wp_settings = read_json_settings(path_to_wp_settings, my_logger)
    bcr = BaseCreateRecord(ap_settings,main_settings, my_logger)
    bcr.start_create_record()