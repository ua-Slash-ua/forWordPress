def create_start():
    return '<?php'


def create_register_post_type(settings):
    word = settings['word']
    return f"""// Реєстрація кастомного типу запису "{word}"
function create_{word}_post_type()
{{
    // Викликаємо функцію register_post_type для реєстрації нового типу запису
    register_post_type('{word.lower()}', [
        'labels' => [
            'name' => '{word.capitalize()}s',  // Загальна назва для цього типу запису
            'singular_name' => '{word.capitalize()}',  // Одинична назва для цього типу запису
            'add_new' => 'Add New {word.capitalize()}',  // Текст для кнопки додавання нового запису
            'add_new_item' => 'Add New {word.capitalize()}',  // Текст для додавання нового елемента
            'edit_item' => 'Edit {word.capitalize()}',  // Текст для редагування елемента
            'new_item' => 'New {word.capitalize()}',  // Текст для нової позиції
            'view_item' => 'View {word.capitalize()}',  // Текст для перегляду елемента
            'search_items' => 'Search {word.capitalize()}s',  // Текст для пошуку
            'not_found' => 'No {word.capitalize()}s found',  // Текст, що показується, коли немає записів
            'not_found_in_trash' => 'No {word.capitalize()}s found in Trash',  // Текст, що показується, коли в кошику немає записів
            'all_items' => 'All {word.capitalize()}s',  // Текст для перегляду всіх елементів
            'archives' => '{word.capitalize()} Archives',  // Архіви типу запису
        ],
        'public' => true,  // Робимо тип запису публічним, щоб він відображався на сайті
        'has_archive' => true,  // Дозволяємо мати архів цього типу запису
        'supports' => ['title'],  // Додаємо підтримку для полів заголовка
        'show_in_rest' => true,  // Дозволяє доступ через REST API
        'rest_base' => '{word.lower()}',  // Назва для доступу до типу запису через REST API
        'menu_icon' => 'dashicons-editor-help',  // Іконка в адмін-панелі
        // Інші параметри можна додати за потреби
    ]);
}}

// Реєструємо функцію для виконання при ініціалізації WordPress
add_action('init', 'create_{word}_post_type');
"""


def create_meta_fields_post_type(settings):
    word = settings['word']
    reg_meta_field = []
    if settings['create_base_func']['input_text']:
        reg_meta_field.append('\'faq_question\'')
    if settings['create_base_func']['img_link']:
        reg_meta_field.append('\'load_image_text\'')
    if settings['create_base_func']['check_box']:
        reg_meta_field.append('\'check\'')
    if settings['create_base_func']['img_svg']:
        reg_meta_field.append('\'text_svg_area\'')
    return f'''
// Функція для реєстрації мета-полів для типу запису "{word}"
function register_{word}_meta_fields() {{
    // Масив з назвами полів і їх описами
    $meta_fields = [
        'some_fields' => 'some_descriptions', // Наприклад, "some_fields" - ключ мета-поля, "some_descriptions" - його опис
        {',\n        '.join(reg_meta_field)}
    ];

    // Реєстрація кожного мета-поля з масиву
    foreach ($meta_fields as $field => $description) {{
        register_post_meta('{word}', $field, [
            'type' => 'string',         // Тип даних, що зберігається (наприклад, рядок)
            'description' => $description, // Опис поля
            'single' => true,           // Визначає, чи поле може мати лише одне значення для запису
            'show_in_rest' => true,     // Дозволяє доступ до поля через REST API
        ]);
    }}
}}

// Додаємо функцію реєстрації мета-полів до хуку ініціалізації WordPress
add_action('init', 'register_{word}_meta_fields');
'''


def create_add_meta_fields_to_api_post_type(settings):
    word = settings['word']
    add_meta_field = []
    if settings['create_base_func']['input_text']:
        add_meta_field.append('\'faq_question\'')
    if settings['create_base_func']['img_link']:
        add_meta_field.append('\'load_image_text\'')
    if settings['create_base_func']['check_box']:
        add_meta_field.append('\'check\'')
    if settings['create_base_func']['img_svg']:
        add_meta_field.append('\'text_svg_area\'')
    return f'''
// Функція для додавання мета-полів до відповіді REST API для типу запису "{word}"
function add_{word}_meta_fields_to_api($data, $post, $request) {{

    // Перевіряємо, чи обробляється потрібний тип запису
    if ($post->post_type === '{word}') {{
        // Масив з назвами мета-полів, які ви хочете додати до відповіді API
        $meta_fields = [
            'some_fields', // Назва мета-поля, яке буде включено у відповідь
            {',\n            '.join(add_meta_field)}
        ];

        // Додаємо значення кожного мета-поля до об'єкта відповіді API
        foreach ($meta_fields as $field) {{
            $data->data[$field] = get_post_meta($post->ID, $field, true); // Отримуємо значення мета-поля
        }}

        // --- Друга частина: Розбір обраних полів ---
        $fields_to_parse = [
            'some_fields',
        ];
        foreach ($fields_to_parse as $field) {{
            if (!empty($data->data[$field])) {{
                // Спроба розпарсити JSON, якщо значення існує
                $decoded_value = json_decode($data->data[$field], true);

                // Якщо розбір вдалий, замінюємо рядок на масив
                if (json_last_error() === JSON_ERROR_NONE) {{
                    $data->data[$field] = $decoded_value;
                }}
            }}
        }}

    }}

    // Повертаємо змінений об'єкт відповіді
    return $data;
}}

// Прикріплюємо функцію до фільтра REST API для типу запису "{word}"
add_filter('rest_prepare_{word}', 'add_{word}_meta_fields_to_api', 10, 3);
'''


def create_add_meta_boxes_post_type(settings):
    word = settings['word']

    return f'''
function add_{word}_meta_boxes()
{{
    // Викликаємо функцію add_meta_box для додавання мета-боксу
    add_meta_box(
        '{word}_details', // Унікальний ID мета-боксу
        '{word.capitalize()} Details', // Заголовок мета-боксу
        'render_{word}_meta_box', // Функція для рендерингу вмісту мета-боксу
        '{word}', // Тип запису, до якого додається мета-бокс
        'normal', // Позиція: "normal" означає стандартну позицію
        'high' // Пріоритет: "high" означає високий пріоритет
    );
}}

// Підключаємо функцію до хука admin_menu
add_action('add_meta_boxes', 'add_{word}_meta_boxes');
'''


def create_render_meta_boxes_post_type(settings):
    word = settings['word']
    load_variable = []
    load_body = []
    if settings['create_base_func']['input_text']:
        load_variable.append('$question = get_post_meta($post->ID, \'faq_question\', true);')
        load_body.append('''<label for=\"faq_question\">Question</label>
            <input type=\"text\" value=\"\' . esc_attr($question) . \'\" name = \"faq_question\" id=\"faq_question\">''')
    if settings['create_base_func']['img_link']:
        load_variable.append('$image= get_post_meta($post->ID, \'load_image_text\', true);')
        load_body.append('''<div class=\"container_preview\">
                <input type=\"button\" value=\"Load Image\"  id=\"load_image\"/>
                <input type=\"text\" hidden=\"hidden\" value=\"\' . esc_attr($image) . \'\" name=\"load_image_text\"  id=\"load_image_text\"/>
                <img src=\"\" alt="image" id=\"preview_image\"/>
            </div>''')
    if settings['create_base_func']['check_box']:
        load_variable.append(f'''$check = get_post_meta($post->ID, 'check', true) =='on' ? 'checked' : '';''')
        load_body.append(f'''<label for="check" class="checkbox-label" >CheckBox</label>
            <input type="checkbox" name="check" id="check" ' . $check . ' class="checkbox-input">''')
    if settings['create_base_func']['img_svg']:
        load_variable.append(f'''$image_svg = get_post_meta($post->ID, 'text_svg_area', true);''')
        load_body.append(f'''<div class="container_preview_svg">
                <input type="text" hidden value="" id="text_svg">
                <textarea name="text_svg_area" id="text_svg_area"  rows="10">' . esc_attr($image_svg) . '</textarea>
                <div class="preview_svg" id ="preview_svg"></div>
            </div>''')
    return f'''
function render_{word}_meta_box($post)
{{
        {'\n        '.join(load_variable)}
        echo '
            {'\n            '.join(load_body)}
        ';
}}
'''


def create_save_meta_data_post_type(settings):
    word = settings['word']
    add_meta_field = []
    add_other_save = []
    if settings['create_base_func']['input_text']:
        add_meta_field.append('\'faq_question\' => \'sanitize_text_field\'''')
    if settings['create_base_func']['img_link']:
        add_meta_field.append('\'load_image_text\' => \'sanitize_text_field\'''')
    if settings['create_base_func']['check_box']:
        add_other_save.append(f'''if (isset($_POST['check'])) {{
        update_post_meta($post_id, 'check', 'on');
    }} else {{
        update_post_meta($post_id, 'check', 'off');
    }}''')
    if settings['create_base_func']['img_svg']:
        add_other_save.append(f'''// Перевірка, чи є дані для збереження
    if (isset($_POST['text_svg_area'])) {{
        $svg_code = $_POST['text_svg_area']; // Отримуємо значення SVG як текст

        // Зберігаємо SVG-код у мета-поле
        update_post_meta($post_id, 'text_svg_area', $svg_code);
    }}''')


    return f'''
// Функція для збереження мета-даних для типу запису "{word}"
function save_{word}_meta_data($post_id) {{
    // Перевіряємо, чи це не автозбереження
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {{
        return $post_id; // Якщо це автозбереження, зупиняємо виконання
    }}

    // Перевіряємо, чи тип запису відповідає "{word}"
    if (get_post_type($post_id) !== '{word}') {{
        return $post_id; // Якщо тип запису не збігається, припиняємо обробку
    }}

    // Список мета-полів для обробки
    $meta_fields = [
        'some_field' => 'some_function_for_field', // 'some_field' - назва поля, 'some_function_for_field' - функція для його обробки
        'some_field2' => 'sanitize_text_field', // 'some_field' - назва поля, 'sanitize_text_field' - стандартна  функція для  обробки
        {',\n        '.join(add_meta_field)}
    ];
    // Обробка кожного мета-поля
    foreach ($meta_fields as $field => $sanitize_function) {{
        // Перевіряємо, чи значення мета-поля передано у POST-запиті
        if (isset($_POST[$field])) {{
            // Використовуємо функцію обробки для санітизації значення
            $sanitized_value = $sanitize_function($_POST[$field]);
            // Зберігаємо значення у базу даних
            update_post_meta($post_id, $field, $sanitized_value);
        }}
        
    }}
    
    {'\n\n        '.join(add_other_save)}

    return $post_id; // Повертаємо ID запису після обробки
}}

// Додаємо функцію до хуку 'save_post', який викликається під час збереження запису
add_action('save_post', 'save_{word}_meta_data');
'''


def create_enqueue_style_and_script_post_type(settings):
    word = settings['word']

    return f'''
// Функція для підключення стилів та скриптів для адміністративної панелі типу запису "{word}"
function enqueue_{word}_style_and_script($hook) {{
    // Перевіряємо, чи ми знаходимося на сторінці редагування або створення запису
    if ($hook === 'post.php' || $hook === 'post-new.php') {{
        global $post;

        // Перевіряємо, чи поточний пост є типом "{word}"
        if (isset($post) && get_post_type($post) === '{word}') {{
            // Підключаємо стилі
            wp_enqueue_style(
                '{word}_style', // Унікальний ID для стилю
                get_template_directory_uri() . '/{settings['path']['path_to_inc']}/{settings['path']['path_to_css']}/{word}_style.css', // Шлях до файлу стилю
                [], // Массив залежностей, якщо немає - залишаємо порожнім
                '1.0.0' // Версія стилю
            );

            // Підключаємо скрипти
            wp_enqueue_script(
                '{word}_script', // Унікальний ID для скрипту
                get_template_directory_uri() . '/{settings['path']['path_to_inc']}/{settings['path']['path_to_js']}/{word}_script.js', // Шлях до файлу скрипту
                ['jquery'], // Масив залежностей, наприклад jQuery
                '1.0.0', // Версія скрипту
                true // Вказуємо, що скрипт потрібно підключити в кінці сторінки
            );
        }}
    }}
}}

// Додаємо функцію до хуку для підключення стилів та скриптів в адмін-панелі
add_action('admin_enqueue_scripts', 'enqueue_{word}_style_and_script');
'''


def create_enqueue_media_uploader_post_type(settings):
    word = settings['word']

    return f'''
function enqueue_{word}_media_uploader() {{
    wp_enqueue_media(); // Підключаємо медіа-скрипти WordPress

}}
add_action('admin_enqueue_scripts', 'enqueue_{word}_media_uploader');
'''



def post_type(settings):
    components_for_post = [
        create_start(),
        create_register_post_type(settings),
        create_meta_fields_post_type(settings),
        create_add_meta_fields_to_api_post_type(settings),
        create_add_meta_boxes_post_type(settings),
        create_render_meta_boxes_post_type(settings),
        create_save_meta_data_post_type(settings),
        create_enqueue_style_and_script_post_type(settings),
    ]
    if settings['enqueue_media_uploader']:
        components_for_post.append(create_enqueue_media_uploader_post_type(settings))

    return '\n\n'.join(components_for_post)