import os.path

from core.admin_panel.base_create_record import BaseCreateRecord
from core.functions import write_txt_file, get_value_in_dict, find_full_path
from data.templates.wordpress.themes.admin_panel.base import *
from data.templates.wordpress.themes.admin_panel.type_post import *

label_types = {
    "simple": ['input_text',
               'input_checkbox',
               'input_date',
               'input_time',
               'input_color',
               'textarea',
               'point',
               'img_link'
               ],
    "table": "table"
}


class CreatePostRecord(BaseCreateRecord):
    def __init__(self, ap_settings, main_settings, CustomLogging):
        super().__init__(ap_settings, main_settings, CustomLogging)

        self.labels_key = None
        self.tabs = []
        self.firs_tab = True
        self.data_tab = "None"
        self.tab_name = "None"

        self.data_content = []
        self.data_header = []
        self.tab = None
        self.meta_box = None
        self.data_item_setting = None

        self.path_to_php = None
        self.data = []
        self.self_type = 'post'

        self.path_to_css_folder = self.find_or_create_folder('ap_styles', fallback_folder=self.folder_inc,
                                                             parent_folder=self.path_to_ap)
        self.path_to_js_folder = self.find_or_create_folder('ap_scripts', fallback_folder=self.folder_inc,
                                                            parent_folder=self.path_to_ap)

        self.template_data = None

    def add_template(self, template_data):
        """
        Замінює плейсхолдери у шаблоні по ключу і додає результат у self.data.
        """
        value = self.replace_template(template_data)
        self.data.append(value)

    def process_field(self):

        lk = self.labels_key
        self.labels_key = fields_config[self.labels_key]
        self.data_content_label.append(f'<div class="{self.labels_key["container_class"]}">')

        self.data_css = list(set(self.data_css + [self.labels_key['data_css']]))
        self.data_js_func = list(set(self.data_js_func + [self.labels_key['data_js_func']]))

        # self.data_js_inc.append(
        #     self.labels_key['data_js_inc'].replace('DATA_JS', ','.join([f"'{name}'" for name in tab_name_list])))
        for self.label_name in self.label_names:
            if lk in label_types['table']:

                self.table_name = self.label_name['name']
                self.table_data = ','.join([f"'{name}'" for name in self.label_name['table_label']])
                self.data_content_label.append(self.replace_template_table(self.labels_key['data']))
                self.all_init.append(self.replace_template_table(self.labels_key[f'get_value_{self.self_type}']))
                self.all_inc.append(self.replace_template_table(self.labels_key['process_value']))
                self.data_js_inc.append(self.replace_template_table(self.labels_key['data_js_inc'])) if self.replace_template_table(
                    self.labels_key['data_js_inc']) else None
            else:
                self.data_content_label.append(self.replace_template(self.labels_key['data']))
                self.all_init.append(self.replace_template(self.labels_key[f'get_value_{self.self_type}']))
                self.all_inc.append(self.replace_template(self.labels_key['process_value']))
                self.data_js_inc.append(self.replace_template(self.labels_key['data_js_inc'])) if self.replace_template(
                    self.labels_key['data_js_inc']) else None
        self.data_content_label.append(f'</div>')

    def process_tab(self):
        self.tab_name = get_value_in_dict(self.tab, 'name_mi')
        self.data_content_label = []
        for self.labels_key in self.tab['label']:
            self.label_names = self.tab['label'][self.labels_key]
            self.process_field()
        if len(self.tabs) > 1:

            self.data_header.append(tab['data_header'].replace('LNAME_TAB', self.tab_name.lower()))
            self.data_content.append(tab['data_content'].replace('LNAME_TAB', self.tab_name.lower()))
            self.data_content[-1] = self.data_content[-1].replace('DATA_CONTENT_RECORD',
                                                                  '\n'.join(self.data_content_label))
            if self.firs_tab:
                self.data_header[-1] = self.data_header[-1].replace('mb_header_item', 'mb_header_item tab_active')
                self.data_content[-1] = self.data_content[-1].replace('mb_content_item',
                                                                      'mb_content_item content_active')

                self.firs_tab = False
            self.data_tab = tab['data_main'].replace('DATA_HEADER', '\n'.join(self.data_header))
            self.data_tab = self.data_tab.replace('DATA_CONTENT', '\n'.join(self.data_content))
        else:
            self.data_tab = '\n'.join(self.data_content_label)


    def process_meta_box(self):
        self.name_meta_box = get_value_in_dict(self.meta_box, 'name_area')
        self.priority_meta_box = get_value_in_dict(self.meta_box, 'priority_area') if get_value_in_dict(self.meta_box,
                                                                                                        'priority_area') else 'high'
        self.position_meta_box = get_value_in_dict(self.meta_box, 'position_area') if get_value_in_dict(self.meta_box,

                                                                                                        'position_area') else 'normal'

        register_meta_box = self.replace_template(self.template_data['register_meta_box'])
        self.data.append(register_meta_box)
        self.tabs = get_value_in_dict(self.meta_box, 'metabox_items')

        self.data_header = []
        self.data_content = []
        self.firs_tab = True
        tab_name_list = []
        for self.tab in self.tabs:
            self.process_tab()
            tab_name_list.append(self.tab_name)

        if len(self.tabs) > 1:
            self.data_css.append(tab['data_css'])
            self.data_js_func.append(tab['data_js_func'])
            self.data_js_inc.append(
                tab['data_js_inc'].replace('DATA_JS', ','.join([f"'{name}'" for name in tab_name_list])))
        render_meta_box = self.replace_template(self.template_data['render_meta_box'])
        render_meta_box = render_meta_box.replace('DATA_INC', '\n'.join(self.all_init))
        render_meta_box = render_meta_box.replace('DATA_RENDER', self.data_tab)

        self.data.append(render_meta_box)

    def start_create_record(self):
        try:
            self.template_data = data_ap_php

            meta_boxes = get_value_in_dict(self.data_item_setting, 'record_area')

            self.add_template(self.template_data['register_type'])

            self.add_template(self.template_data['register_rest_api_meta_fields'])

            for mb in meta_boxes:
                self.meta_box = mb
                self.process_meta_box()
            self.add_template(self.template_data['fields'])

            full_path_to_css, self.path_to_css = self.prepare_path(self.path_to_css_folder, f'style_{self.data_name}',
                                                                   'css')
            full_path_to_js, self.path_to_js = self.prepare_path(self.path_to_js_folder, f'script_{self.data_name}',
                                                                 'js')
            full_path_to_php, self.path_to_php = self.prepare_path(self.path_to_ap, f'ap_{self.data_name}',
                                                                   'php')

            self.add_template(self.template_data['save_meta'])

            self.add_template(self.template_data['enqueue_style_and_script'])

            self.data_js = '\n'.join(self.data_js_func) + '\n' * 3 + base_js.replace('DATA',
                                                                                     '\n'.join(self.data_js_inc))
            self.create_file(full_path_to_php, '\n\n'.join(self.data))
            self.create_file(full_path_to_js, self.data_js)
            self.create_file(full_path_to_css, '\n\n'.join(self.data_css))
            self.include_func('admin_panel', self.path_to_php)

            self.info_log("success", f"Створено")
        except Exception as e:
            self.error_log(f"❌ Не вдалося створити  : {e}")
            self.info_log("error", f"❌ Не вдалося створити  : {e}")
