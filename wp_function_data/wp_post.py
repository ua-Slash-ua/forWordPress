
body_post = '''
<?php

// Реєстрація кастомного типу запису "LWORD"
function create_LWORD_post_type()
{
    // Викликаємо функцію register_post_type для реєстрації нового типу запису
    register_post_type('LWORD', [
        'labels' => [
            'name' => 'CWORDs',  // Загальна назва для цього типу запису
            'singular_name' => 'CWORD',  // Одинична назва для цього типу запису
            'add_new' => 'Add New CWORD',  // Текст для кнопки додавання нового запису
            'add_new_item' => 'Add New CWORD',  // Текст для додавання нового елемента
            'edit_item' => 'Edit CWORD',  // Текст для редагування елемента
            'new_item' => 'New CWORD',  // Текст для нової позиції
            'view_item' => 'View CWORD',  // Текст для перегляду елемента
            'search_items' => 'Search CWORDs',  // Текст для пошуку
            'not_found' => 'No CWORDs found',  // Текст, що показується, коли немає записів
            'not_found_in_trash' => 'No CWORDs found in Trash',  // Текст, що показується, коли в кошику немає записів
            'all_items' => 'All CWORDs',  // Текст для перегляду всіх елементів
            'archives' => 'CWORD Archives',  // Архіви типу запису
        ],
        'public' => true,  // Робимо тип запису публічним, щоб він відображався на сайті
        'has_archive' => true,  // Дозволяємо мати архів цього типу запису
        'supports' => ['title'],  // Додаємо підтримку для полів заголовка
        'show_in_rest' => true,  // Дозволяє доступ через REST API
        'rest_base' => 'LWORD',  // Назва для доступу до типу запису через REST API
        'menu_icon' => 'dashicons-editor-help',  // Іконка в адмін-панелі
        // Інші параметри можна додати за потреби
    ]);
}

// Реєструємо функцію для виконання при ініціалізації WordPress
add_action('init', 'create_LWORD_post_type');


// Функція для реєстрації мета-полів для типу запису "LWORD"
function register_LWORD_meta_fields() {
    // Масив з назвами полів і їх описами
    $meta_fields = [
        
    ];

    // Реєстрація кожного мета-поля з масиву
    foreach ($meta_fields as $field => $description) {
        register_post_meta('LWORD', $field, [
            'type' => 'string',         // Тип даних, що зберігається (наприклад, рядок)
            'description' => $description, // Опис поля
            'single' => true,           // Визначає, чи поле може мати лише одне значення для запису
            'show_in_rest' => true,     // Дозволяє доступ до поля через REST API
        ]);
    }
}

// Додаємо функцію реєстрації мета-полів до хуку ініціалізації WordPress
add_action('init', 'register_LWORD_meta_fields');


// Функція для додавання мета-полів до відповіді REST API для типу запису "LWORD"
function add_LWORD_meta_fields_to_api($data, $post, $request) {
    // Перевіряємо тип запису
    if ($post->post_type === 'LWORD') {
        // Мета-поля для додавання до API та спосіб їх обробки
        $meta_fields = [

        ];

        // Обробка мета-полів
        foreach ($meta_fields as $field => $type) {
            $value = get_post_meta($post->ID, $field, true);

            // Обробляємо поле відповідно до вказаного типу
            if ($type === 'json' && !empty($value)) {
                $decoded_value = json_decode($value, true);
                if (json_last_error() === JSON_ERROR_NONE) {
                    $value = $decoded_value;
                }
            }

            // Додаємо значення до відповіді
            $data->data[$field] = $value;
        }
    }
    return $data;
}


// Прикріплюємо функцію до фільтра REST API для типу запису "LWORD"
add_filter('rest_prepare_LWORD', 'add_LWORD_meta_fields_to_api', 10, 3);


function add_LWORD_meta_boxes()
{
    // Викликаємо функцію add_meta_box для додавання мета-боксу
    add_meta_box(
        'LWORD_details', // Унікальний ID мета-боксу
        'CWORD Details', // Заголовок мета-боксу
        'render_LWORD_meta_box', // Функція для рендерингу вмісту мета-боксу
        'LWORD', // Тип запису, до якого додається мета-бокс
        'normal', // Позиція: "normal" означає стандартну позицію
        'high' // Пріоритет: "high" означає високий пріоритет
    );
}

// Підключаємо функцію до хука admin_menu
add_action('add_meta_boxes', 'add_LWORD_meta_boxes');


function render_LWORD_meta_box($post)
{
?>


<?php
}


// Функція для збереження мета-даних для типу запису "LWORD"
function save_LWORD_meta_data($post_id) {
    // Перевіряємо, чи це не автозбереження
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return $post_id; // Якщо це автозбереження, зупиняємо виконання
    }

    // Перевіряємо, чи тип запису відповідає "LWORD"
    if (get_post_type($post_id) !== 'LWORD') {
        return $post_id; // Якщо тип запису не збігається, припиняємо обробку
    }

    // Список мета-полів для обробки
    $meta_fields = [
    
    ];
    // Обробка кожного мета-поля
    foreach ($meta_fields as $field => $sanitize_function) {
        // Перевіряємо, чи значення мета-поля передано у POST-запиті
        if (isset($_POST[$field])) {
            // Використовуємо функцію обробки для санітизації значення
            $sanitized_value = $sanitize_function($_POST[$field]);
            // Зберігаємо значення у базу даних
            update_post_meta($post_id, $field, $sanitized_value);
        }
        
    }
    
    return $post_id; // Повертаємо ID запису після обробки
}

// Додаємо функцію до хуку 'save_post', який викликається під час збереження запису
add_action('save_post', 'save_LWORD_meta_data');

function sanitize_checkbox_LWORD($value)
{
    return ($value === 'on') ? 'on' : 'off';
}

function sanitize_svg_area_LWORD($value)
{
    return $value;
}

// Функція для підключення стилів та скриптів для адміністративної панелі типу запису "LWORD"
function enqueue_LWORD_style_and_script($hook) {
    // Перевіряємо, чи ми знаходимося на сторінці редагування або створення запису
    if ($hook === 'post.php' || $hook === 'post-new.php') {
        global $post;

        // Перевіряємо, чи поточний пост є типом "LWORD"
        if (isset($post) && get_post_type($post) === 'LWORD') {
            // Підключаємо стилі
            wp_enqueue_style(
                'LWORD_style', // Унікальний ID для стилю
                get_template_directory_uri() . 'PartPathCSS', // Шлях до файлу стилю
                [], // Массив залежностей, якщо немає - залишаємо порожнім
                '1.0.0' // Версія стилю
            );

            // Підключаємо скрипти
            wp_enqueue_script(
                'LWORD_script', // Унікальний ID для скрипту
                get_template_directory_uri() . 'PartPathJS', // Шлях до файлу скрипту
                ['jquery'], // Масив залежностей, наприклад jQuery
                '1.0.0', // Версія скрипту
                true // Вказуємо, що скрипт потрібно підключити в кінці сторінки
            );
        }
    }
}

// Додаємо функцію до хуку для підключення стилів та скриптів в адмін-панелі
add_action('admin_enqueue_scripts', 'enqueue_LWORD_style_and_script');
'''

get_value_post = '''    $LWORD = get_post_meta($post->ID, 'LWORD', true);'''

input_post = '''        <label for="LWORD">CWORD</label>
        <input type="text" value="<?php echo esc_attr($LWORD); ?>" name = "LWORD" id="LWORD" class ="input-item">
'''
hl_input_post = '''            <label for="LWORD">CWORD</label>
            <input type="text" value="" name = "input_LWORD" id="LWORD" class ="">
'''

checkbox_post = '''        <label for="LWORD" >CWORD</label>
        <input type="hidden" name="LWORD" value="off">
        <input type="checkbox" name="LWORD" id="LWORD" <?php echo  $LWORD ?> class="checkbox-item">'''
hl_checkbox_post = '''            <label for="LWORD" >CWORD</label>
            <input type="hidden" name="LWORD" value="off">
            <input type="checkbox" name="LWORD" id="LWORD"  class="">'''

img_link_post = '''        <div class="container_preview_LWORD">
                <input type="button" value="Load CWORD"  id="load_image_LWORD"/>
                <input type="text" hidden="hidden" value="<?php echo esc_attr($img_LWORD)  ?>" name="load_image_text_LWORD"  id="load_image_text_LWORD"/>
                <img src="" alt="image" id="preview_image_LWORD"/>
        </div>'''
hl_img_link_post = '''            <input type="button" id="btn_LWORD" value="Upload CWORD">
            <img id="LWORD" src="" alt="photo">'''

img_svg_post = '''        <div class="container_preview_svg">
                <label for="text_svg_area_LWORD">Write CWORD SVG code:</label>
                <textarea name="text_svg_area_LWORD" id="text_svg_area_LWORD"  rows="10"><?php echo esc_attr($svg_LWORD) ?></textarea>
                <div class="preview_svg" id ="preview_svg_LWORD"></div>
        </div>'''
hl_img_svg_post = '''            <label for="LWORD">Write CWORD SVG code:</label>
            <textarea name="LWORD" id="LWORD" cols="30" rows="10"></textarea>
            <div class="preview_LWORD" id="preview_LWORD"></div>'''

points_post = '''    <div class="form_container_points" id="form_container_points_LWORD">
        <input type="text" name ='save_data_points_LWORD' id="save_data_points_LWORD"  hidden="hidden" value="<?php echo  esc_attr($points_LWORD)?>" >
        <label for="points_LWORD">CWORD</label>
        <input type="text" id="points_LWORD" class="points_input">
        <input type="button" id="btn_points_LWORD" value="Add CWORD">
        <div class="container_preview_points" id="preview_points_LWORD">
        </div>
    </div>'''

table_post = '''    <div class="form_container_table" >
        <input type="text" hidden="hidden" name="table_data" id="table_data" value="<?php echo  esc_attr($table_data)?>">
        <div class="container_data">
LABEL_WORD
            <input type="button" id ="btn_table_add" value="Add">
        </div>
        <div class="container_table">
            <table class="custom-table">
                <thead>
                    <tr>
                        LINES_WORD
                    </tr>
                </thead>
                <tbody id="body_table">

                </tbody>
            </table>
        </div>
    </div>'''
table_input ='''            <label for="table_LWORD">CWORD</label>
            <input type="text" id ="table_LWORD" value="">'''

wp_media_uploader = '''
function enqueue_LWORD_media_uploader() {
    wp_enqueue_media(); // Підключаємо медіа-скрипти WordPress

}
add_action('admin_enqueue_scripts', 'enqueue_LWORD_media_uploader');
'''

