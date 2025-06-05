
def create_start():
    return '<?php'

def create_enqueue_media_uploader_options(settings):
    word = settings['word']

    return f'''
function enqueue_{word}_media_uploader() {{
    wp_enqueue_media(); // Підключаємо медіа-скрипти WordPress

}}
add_action('admin_enqueue_scripts', 'enqueue_{word}_media_uploader');
'''

def create_register_menu_options(settings:dict):
    word = settings['word']
    return f'''function register_{word.lower()}_menu() {{
    add_menu_page(
        '{word.capitalize()}',          // Назва вкладки
        '{word.capitalize()}',          // Назва меню
        'edit_posts',            // Права доступу (без manage_options)
        '{word.lower()}s-slug',     // Унікальний ідентифікатор
        'render_{word.lower()}s_page', // Функція, яка відображатиме контент
        'dashicons-email',       // Іконка
        6                         // Позиція у меню
    );
}}
add_action('admin_menu', 'register_{word.lower()}_menu');'''

def create_transform_on_array_options(settings):

    word = settings['word']
    return f'''function get_array($option_key) {{
    // Отримуємо значення з опцій за переданим ключем
    $option_value = get_option($option_key);

    if (is_string($option_value) && !empty($option_value)) {{
        // Спроба розпарсити JSON, якщо значення є рядком
        $decoded_value = json_decode($option_value, true);

        if (json_last_error() === JSON_ERROR_NONE) {{
            return $decoded_value; // Повертаємо масив, якщо JSON успішно розпарсено
        }} else {{
            // Логування помилки, якщо JSON некоректний
            error_log("Failed to parse JSON for option '{{$option_key}}': " . json_last_error_msg());
            return []; // Повертаємо порожній масив у разі помилки
        }}
    }} elseif (is_array($option_value)) {{
        // Якщо значення вже є масивом, повертаємо його
        return $option_value;
    }}

    // Якщо значення не є ні рядком, ні масивом, повертаємо порожній масив
    return [];
}}'''

def create_render_options(settings):
    word = settings['word']
    load_variable = []
    load_body = []
    if settings['create_base_func']['input_text']:
        load_variable.append('$question = get_option(\'faq_question\');')
        load_body.append('''<label for=\"faq_question\">Question</label>
                <input type=\"text\" value=\"\' . esc_attr($question) . \'\" name = \"faq_question\" id=\"faq_question\">''')
    if settings['create_base_func']['img_link']:
        load_variable.append('$image= get_option(\'load_image_text\');')
        load_body.append('''<div class=\"container_preview\">
                    <input type=\"button\" value=\"Load Image\"  id=\"load_image\"/>
                    <input type=\"text\" hidden=\"hidden\" value=\"\' . esc_attr($image) . \'\" name=\"load_image_text\"  id=\"load_image_text\"/>
                    <img src=\"\" alt="image" id=\"preview_image\"/>
                </div>''')
    if settings['create_base_func']['check_box']:
        load_variable.append(f'''$check = get_option('check') =='on' ? 'checked' : '';''')
        load_body.append(f'''<label for="check" class="checkbox-label" >CheckBox</label>
                <input type="checkbox" name="check" id="check" ' . $check . ' class="checkbox-input">''')
    if settings['create_base_func']['img_svg']:
        load_variable.append(f'''$image_svg = get_option('text_svg_area');''')
        load_body.append(f'''<div class="container_preview_svg">
                    <input type="text" hidden value="" id="text_svg">
                    <textarea name="text_svg_area" id="text_svg_area"  rows="10">' . esc_attr($image_svg) . '</textarea>
                    <div class="preview_svg" id ="preview_svg"></div>
                </div>''')
    return f'''function render_{word.lower()}s_page() {{
    
    echo '<form method="post" action="options.php" enctype="multipart/form-data">';
        // Викликаємо settings_fields для реєстрації налаштувань
        settings_fields('{word.lower()}s_group'); // 'contact_group' - це група налаштувань, яку ви реєстрували
        {'\n        '.join(load_variable)}
    echo'
         {'\n            '.join(load_body)}
         ';
    submit_button();
    echo '</form>';
}}'''

def create_register_rest_route_options(settings):
    word = settings['word']
    return f'''function register_{word.lower()}_rest_route() {{
    register_rest_route('wp/v2', '/{word.lower()}', [
        'methods' => 'GET',
        'callback' => 'get_{word.lower()}_info',
        'permission_callback' => '__return_true', // або використовуйте власну перевірку доступу
    ]);
}}
add_action('rest_api_init', 'register_{word.lower()}_rest_route');'''

def create_get_info_options(settings):
    reg_meta_field = []
    if settings['create_base_func']['input_text']:
        reg_meta_field.append(''''faq_question' => ['faq_question', null]''')
    if settings['create_base_func']['img_link']:
        reg_meta_field.append(''''load_image_text' => ['load_image_text', null]''')
    if settings['create_base_func']['check_box']:
        reg_meta_field.append(''''check' => ['check', null]''')
    if settings['create_base_func']['img_svg']:
        reg_meta_field.append(''''text_svg_area' => ['text_svg_area', null]''')
    word = settings['word']
    return f'''function get_{word.lower()}_info () {{
    $items = [
        'some_field' => ['some_field', null], // Поле без обробки
        //'some_field2' => ['some_field2', 'get_array'], // Поле з обробкою
        {',\n        '.join(reg_meta_field)}
    ];

    $return_items = [];
    foreach ($items as $field_for_rest_api => $value) {{
        if (isset($value[1]) && is_callable($value[1])) {{ // Перевірка, чи вказана функція обробки
            $return_items[$field_for_rest_api] = $value[1]($value[0]); // Викликаємо функцію обробки
        }} else {{
            $return_items[$field_for_rest_api] = get_option($value[0]);
        }}
    }}

    return $return_items;
}}'''

def create_add_meta_fields_options(settings):
    word = settings['word']
    add_meta_field=[]
    if settings['create_base_func']['input_text']:
        add_meta_field.append('\'faq_question\'')
    if settings['create_base_func']['img_link']:
        add_meta_field.append('\'load_image_text\'')
    if settings['create_base_func']['check_box']:
        add_meta_field.append('\'check\'')
    if settings['create_base_func']['img_svg']:
        add_meta_field.append('\'text_svg_area\'')

    return f'''function add_{word.lower()}_meta_fields() {{
    $meta_fields = [
        'some_field',
        {',\n        '.join(add_meta_field)}

    ];

    foreach ($meta_fields as $key) {{
        register_meta('options', $key, [
            'type' => 'string',
            'single' => true,
            'show_in_rest' => true,
            'description' => ucfirst(str_replace('_', ' ', $key)), // Автоматичний опис
        ]);
    }}
}}

add_action('init', 'add_{word.lower()}_meta_fields');
'''

def create_register_settings_options(settings):
    word = settings['word']
    save_meta_field = []
    if settings['create_base_func']['input_text']:
        save_meta_field.append('\'faq_question\' => \'sanitize_text_field\'')
    if settings['create_base_func']['img_link']:
        save_meta_field.append('\'load_image_text\'=> \'sanitize_text_field\'')
    if settings['create_base_func']['check_box']:
        save_meta_field.append('\'check\'=> \'sanitize_text_field\'')
    if settings['create_base_func']['img_svg']:
        save_meta_field.append('\'text_svg_area\'=> null ')
    return f'''function register_{word.lower()}_settings() {{
    // Реєстрація налаштувань для кожного поля
    $settings = [
        'some_field' => 'sanitize_text_field',
        //'some_field2' => 'sanitize_text_to_json',
        {',\n        '.join(save_meta_field)}

    ];

    foreach ($settings as $option => $sanitize) {{
        // Реєстрація налаштувань з відповідною функцією санітаризації
        register_setting('{word.lower()}s_group', $option, ['sanitize_callback' => $sanitize]);
    }}
}}
add_action('admin_init', 'register_{word.lower()}_settings');
'''

def create_sanitize_json_decode_options(settings):
    word = settings['word']
    return f'''// Функція для фільтрації та очищення social_media_images
function sanitize_text_to_json($value) {{
    // Повертаємо розпарсений JSON або порожній масив
    return json_decode($value, true) ?: [];
}}'''

def create_enqueue_style_and_script_options(settings:dict):
    word = settings['word']
    return f'''function enqueue_{word.lower()}_style_and_script($hook) {{
    // Перевіряємо, чи це сторінка кастомного меню "{word.lower()}s-slug"
    if ($hook === 'toplevel_page_{word.lower()}s-slug') {{
        // Підключаємо CSS стилі
        wp_enqueue_style(
            '{word.lower()}-style', // Унікальний ID для стилю
            get_template_directory_uri() . '/{settings['path']['path_to_inc']}/{settings['path']['path_to_css']}/{word}_style.css', // Шлях до файлу стилю
            [], // Залежності
            '1.0.0' // Версія стилю
        );

        // Підключаємо JS скрипт
        wp_enqueue_script(
            '{word.lower()}-script', // Унікальний ID для скрипту
            get_template_directory_uri() . '/{settings['path']['path_to_inc']}/{settings['path']['path_to_js']}/{word}_script.js', // Шлях до файлу скрипту
            ['jquery'], // Залежність від jQuery
            '1.0.0', // Версія скрипту
            true // Підключаємо скрипт внизу сторінки (після контенту)
        );
    }}
}}
add_action('admin_enqueue_scripts', 'enqueue_{word.lower()}_style_and_script');'''

def options(settings):
    components_for_post = [
        create_start(),
        create_transform_on_array_options(settings),
        create_register_menu_options(settings),
        create_register_rest_route_options(settings),
        create_get_info_options(settings),
        create_render_options(settings),
        create_add_meta_fields_options(settings),
        create_register_settings_options(settings),
        create_sanitize_json_decode_options(settings),
        create_enqueue_style_and_script_options(settings),
    ]
    if settings['enqueue_media_uploader']:
        components_for_post.append(create_enqueue_media_uploader_options(settings))

    return '\n\n'.join(components_for_post)