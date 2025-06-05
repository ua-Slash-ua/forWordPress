<?php

// Реєстрація кастомного типу запису "contact"
function create_contact_post_type()
{
    // Викликаємо функцію register_post_type для реєстрації нового типу запису
    register_post_type('contact', [
        'labels' => [
            'name' => 'Contacts',  // Загальна назва для цього типу запису
            'singular_name' => 'Contact',  // Одинична назва для цього типу запису
            'add_new' => 'Add New Contact',  // Текст для кнопки додавання нового запису
            'add_new_item' => 'Add New Contact',  // Текст для додавання нового елемента
            'edit_item' => 'Edit Contact',  // Текст для редагування елемента
            'new_item' => 'New Contact',  // Текст для нової позиції
            'view_item' => 'View Contact',  // Текст для перегляду елемента
            'search_items' => 'Search Contacts',  // Текст для пошуку
            'not_found' => 'No Contacts found',  // Текст, що показується, коли немає записів
            'not_found_in_trash' => 'No Contacts found in Trash',  // Текст, що показується, коли в кошику немає записів
            'all_items' => 'All Contacts',  // Текст для перегляду всіх елементів
            'archives' => 'Contact Archives',  // Архіви типу запису
        ],
        'public' => true,  // Робимо тип запису публічним, щоб він відображався на сайті
        'has_archive' => true,  // Дозволяємо мати архів цього типу запису
        'supports' => ['title'],  // Додаємо підтримку для полів заголовка
        'show_in_rest' => true,  // Дозволяє доступ через REST API
        'rest_base' => 'contact',  // Назва для доступу до типу запису через REST API
        'menu_icon' => 'dashicons-editor-help',  // Іконка в адмін-панелі
        // Інші параметри можна додати за потреби
    ]);
}

// Реєструємо функцію для виконання при ініціалізації WordPress
add_action('init', 'create_contact_post_type');



// Функція для реєстрації мета-полів для типу запису "contact"
function register_contact_meta_fields() {
    // Масив з назвами полів і їх описами
    $meta_fields = [
        'some_fields' => 'some_descriptions', // Наприклад, "some_fields" - ключ мета-поля, "some_descriptions" - його опис
        'faq_question',
        'load_image_text',
        'check',
        'text_svg_area'
    ];

    // Реєстрація кожного мета-поля з масиву
    foreach ($meta_fields as $field => $description) {
        register_post_meta('contact', $field, [
            'type' => 'string',         // Тип даних, що зберігається (наприклад, рядок)
            'description' => $description, // Опис поля
            'single' => true,           // Визначає, чи поле може мати лише одне значення для запису
            'show_in_rest' => true,     // Дозволяє доступ до поля через REST API
        ]);
    }
}

// Додаємо функцію реєстрації мета-полів до хуку ініціалізації WordPress
add_action('init', 'register_contact_meta_fields');



// Функція для додавання мета-полів до відповіді REST API для типу запису "contact"
function add_contact_meta_fields_to_api($data, $post, $request) {
    // Перевіряємо тип запису
    if ($post->post_type === 'contact') {
        // Мета-поля для додавання до API та спосіб їх обробки
        $meta_fields = [
            'some_fields' => 'json',  // Це поле буде розбиратися як JSON
            'faq_question' => 'plain', // Це поле додається як звичайний текст
            'load_image_text' => 'plain',
            'check' => 'plain',
            'text_svg_area' => 'plain',
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


// Прикріплюємо функцію до фільтра REST API для типу запису "contact"
add_filter('rest_prepare_contact', 'add_contact_meta_fields_to_api', 10, 3);



function add_contact_meta_boxes()
{
    // Викликаємо функцію add_meta_box для додавання мета-боксу
    add_meta_box(
        'contact_details', // Унікальний ID мета-боксу
        'Contact Details', // Заголовок мета-боксу
        'render_contact_meta_box', // Функція для рендерингу вмісту мета-боксу
        'contact', // Тип запису, до якого додається мета-бокс
        'normal', // Позиція: "normal" означає стандартну позицію
        'high' // Пріоритет: "high" означає високий пріоритет
    );
}

// Підключаємо функцію до хука admin_menu
add_action('add_meta_boxes', 'add_contact_meta_boxes');



function render_contact_meta_box($post)
{
        $question = get_post_meta($post->ID, 'faq_question', true);
        $image= get_post_meta($post->ID, 'load_image_text', true);
        $check = get_post_meta($post->ID, 'check', true) =='on' ? 'checked' : '';
        $image_svg = get_post_meta($post->ID, 'text_svg_area', true);
        echo '
            <label for="faq_question">Question</label>
            <input type="text" value="' . esc_attr($question) . '" name = "faq_question" id="faq_question">
            <div class="container_preview">
                <input type="button" value="Load Image"  id="load_image"/>
                <input type="text" hidden="hidden" value="' . esc_attr($image) . '" name="load_image_text"  id="load_image_text"/>
                <img src="" alt="image" id="preview_image"/>
            </div>
            <label for="check" class="checkbox-label" >CheckBox</label>
            <input type="checkbox" name="check" id="check" ' . $check . ' class="checkbox-input">
            <div class="container_preview_svg">
                <input type="text" hidden value="" id="text_svg">
                <textarea name="text_svg_area" id="text_svg_area"  rows="10">' . esc_attr($image_svg) . '</textarea>
                <div class="preview_svg" id ="preview_svg"></div>
            </div>
        ';
}



// Функція для збереження мета-даних для типу запису "contact"
function save_contact_meta_data($post_id) {
    // Перевіряємо, чи це не автозбереження
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return $post_id; // Якщо це автозбереження, зупиняємо виконання
    }

    // Перевіряємо, чи тип запису відповідає "contact"
    if (get_post_type($post_id) !== 'contact') {
        return $post_id; // Якщо тип запису не збігається, припиняємо обробку
    }

    // Список мета-полів для обробки
    $meta_fields = [
        'some_field' => 'some_function_for_field', // 'some_field' - назва поля, 'some_function_for_field' - функція для його обробки
        'some_field2' => 'sanitize_text_field', // 'some_field' - назва поля, 'sanitize_text_field' - стандартна  функція для  обробки
        'faq_question' => 'sanitize_text_field',
        'load_image_text' => 'sanitize_text_field'
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
    function sanitize_checkbox($value)
    {
        return $value ? 'on' : 'off';
    }


// Збереження SVG-коду, якщо він переданий
    if (!empty($_POST['text_svg_area'])) {
        update_post_meta($post_id, 'text_svg_area', $_POST['text_svg_area']);
    }

    return $post_id; // Повертаємо ID запису після обробки
}

// Додаємо функцію до хуку 'save_post', який викликається під час збереження запису
add_action('save_post', 'save_contact_meta_data');



// Функція для підключення стилів та скриптів для адміністративної панелі типу запису "contact"
function enqueue_contact_style_and_script($hook) {
    // Перевіряємо, чи ми знаходимося на сторінці редагування або створення запису
    if ($hook === 'post.php' || $hook === 'post-new.php') {
        global $post;

        // Перевіряємо, чи поточний пост є типом "contact"
        if (isset($post) && get_post_type($post) === 'contact') {
            // Підключаємо стилі
            wp_enqueue_style(
                'contact_style', // Унікальний ID для стилю
                get_template_directory_uri() . '/inc/inc_css/contact_style.css', // Шлях до файлу стилю
                [], // Массив залежностей, якщо немає - залишаємо порожнім
                '1.0.0' // Версія стилю
            );

            // Підключаємо скрипти
            wp_enqueue_script(
                'contact_script', // Унікальний ID для скрипту
                get_template_directory_uri() . '/inc/inc_js/contact_script.js', // Шлях до файлу скрипту
                ['jquery'], // Масив залежностей, наприклад jQuery
                '1.0.0', // Версія скрипту
                true // Вказуємо, що скрипт потрібно підключити в кінці сторінки
            );
        }
    }
}

// Додаємо функцію до хуку для підключення стилів та скриптів в адмін-панелі
add_action('admin_enqueue_scripts', 'enqueue_contact_style_and_script');



function enqueue_contact_media_uploader() {
    wp_enqueue_media(); // Підключаємо медіа-скрипти WordPress

}
add_action('admin_enqueue_scripts', 'enqueue_contact_media_uploader');
