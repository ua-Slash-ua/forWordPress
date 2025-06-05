from data.templates.wordpress.themes.admin_panel.type_post import *

include_functions = f'''include_once PATH_TO_THEMES . 'PART_PATH';'''

include_place = {
    'admin_panel': "// For includes admin panel",
    'endpoint': "// For includes admin panel",
    'custom_labels_wc': "// For includes admin panel",
    'keycrm': "// For includes admin panel"

}
base_js = '''document.addEventListener('DOMContentLoaded',function (){
    DATA
})'''

fields_config = {
    'input_text': input_text,
    'input_date': input_date,
    'input_time': input_time,
    'input_color': input_color,
    'textarea': textarea,
    'input_checkbox': input_checkbox,
    'point': point,
    'table': table,
    'img_link': img_link,

}