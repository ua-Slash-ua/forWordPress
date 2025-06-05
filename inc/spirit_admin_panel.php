
<?php

// Реєстрація кастомного типу запису "spirit"
function create_spirit_post_type()
{
    // Викликаємо функцію register_post_type для реєстрації нового типу запису
    register_post_type('spirit', [
        'labels' => [
            'name' => 'Spirits',  // Загальна назва для цього типу запису
            'singular_name' => 'Spirit',  // Одинична назва для цього типу запису
            'add_new' => 'Add New Spirit',  // Текст для кнопки додавання нового запису
            'add_new_item' => 'Add New Spirit',  // Текст для додавання нового елемента
            'edit_item' => 'Edit Spirit',  // Текст для редагування елемента
            'new_item' => 'New Spirit',  // Текст для нової позиції
            'view_item' => 'View Spirit',  // Текст для перегляду елемента
            'search_items' => 'Search Spirits',  // Текст для пошуку
            'not_found' => 'No Spirits found',  // Текст, що показується, коли немає записів
            'not_found_in_trash' => 'No Spirits found in Trash',  // Текст, що показується, коли в кошику немає записів
            'all_items' => 'All Spirits',  // Текст для перегляду всіх елементів
            'archives' => 'Spirit Archives',  // Архіви типу запису
        ],
        'public' => true,  // Робимо тип запису публічним, щоб він відображався на сайті
        'has_archive' => true,  // Дозволяємо мати архів цього типу запису
        'supports' => ['title'],  // Додаємо підтримку для полів заголовка
        'show_in_rest' => true,  // Дозволяє доступ через REST API
        'rest_base' => 'spirit',  // Назва для доступу до типу запису через REST API
        'menu_icon' => 'dashicons-editor-help',  // Іконка в адмін-панелі
        // Інші параметри можна додати за потреби
    ]);
}

// Реєструємо функцію для виконання при ініціалізації WordPress
add_action('init', 'create_spirit_post_type');


// Функція для реєстрації мета-полів для типу запису "spirit"
function register_spirit_meta_fields() {
    // Масив з назвами полів і їх описами
    $meta_fields = [
          'input_email '=>'some_descriptions',
         'input_email2 '=>'some_descriptions',
        
    ];

    // Реєстрація кожного мета-поля з масиву
    foreach ($meta_fields as $field => $description) {
        register_post_meta('spirit', $field, [
            'type' => 'string',         // Тип даних, що зберігається (наприклад, рядок)
            'description' => $description, // Опис поля
            'single' => true,           // Визначає, чи поле може мати лише одне значення для запису
            'show_in_rest' => true,     // Дозволяє доступ до поля через REST API
        ]);
    }
}

// Додаємо функцію реєстрації мета-полів до хуку ініціалізації WordPress
add_action('init', 'register_spirit_meta_fields');


// Функція для додавання мета-полів до відповіді REST API для типу запису "spirit"
function add_contact_meta_fields_to_api($data, $post, $request) {
    // Перевіряємо тип запису
    if ($post->post_type === 'contact') {
        // Мета-поля для додавання до API та спосіб їх обробки
        $meta_fields = [
          'input_email '=>'some_descriptions',
         'input_email2 '=>'some_descriptions'

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


// Прикріплюємо функцію до фільтра REST API для типу запису "spirit"
add_filter('rest_prepare_spirit', 'add_spirit_meta_fields_to_api', 10, 3);


function add_spirit_meta_boxes()
{
    // Викликаємо функцію add_meta_box для додавання мета-боксу
    add_meta_box(
        'spirit_details', // Унікальний ID мета-боксу
        'spirit Details', // Заголовок мета-боксу
        'render_spirit_meta_box', // Функція для рендерингу вмісту мета-боксу
        'spirit', // Тип запису, до якого додається мета-бокс
        'normal', // Позиція: "normal" означає стандартну позицію
        'high' // Пріоритет: "high" означає високий пріоритет
    );
}

// Підключаємо функцію до хука admin_menu
add_action('add_meta_boxes', 'add_spirit_meta_boxes');


function render_spirit_meta_box($post)
{
 $email = get_post_meta($post->ID, 'input_email', true);
$email2 = get_post_meta($post->ID, 'input_email2', true);
?>


             <label for="input_email">Email</label>
            <input type="text" value="' . esc_attr($input_email) . '" name = "input_email" id="input_email" class ="input-item">

            <label for="input_email2">Email2</label>
            <input type="text" value="' . esc_attr($input_email2) . '" name = "input_email2" id="input_email2" class ="input-item">

<?php
}


// Функція для збереження мета-даних для типу запису "spirit"
function save_spirit_meta_data($post_id) {
    // Перевіряємо, чи це не автозбереження
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return $post_id; // Якщо це автозбереження, зупиняємо виконання
    }

    // Перевіряємо, чи тип запису відповідає "spirit"
    if (get_post_type($post_id) !== 'spirit') {
        return $post_id; // Якщо тип запису не збігається, припиняємо обробку
    }

    // Список мета-полів для обробки
    $meta_fields = [
          'input_email '=>'sanitize_text_field',
         'input_email2 '=>'sanitize_text_field',
    
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
    
    

    return $post_id; // Повертаємо ID запису після обробки
}

// Додаємо функцію до хуку 'save_post', який викликається під час збереження запису
add_action('save_post', 'save_spirit_meta_data');


// Функція для підключення стилів та скриптів для адміністративної панелі типу запису "spirit"
function enqueue_spirit_style_and_script($hook) {
    // Перевіряємо, чи ми знаходимося на сторінці редагування або створення запису
    if ($hook === 'post.php' || $hook === 'post-new.php') {
        global $post;

        // Перевіряємо, чи поточний пост є типом "spirit"
        if (isset($post) && get_post_type($post) === 'spirit') {
            // Підключаємо стилі
            wp_enqueue_style(
                'spirit_style', // Унікальний ID для стилю
                get_template_directory_uri() . 'D:\Slash\Programming\Project\ForWordPress\for_WP_2_0', // Шлях до файлу стилю
                [], // Массив залежностей, якщо немає - залишаємо порожнім
                '1.0.0' // Версія стилю
            );

            // Підключаємо скрипти
            wp_enqueue_script(
                'spirit_script', // Унікальний ID для скрипту
                get_template_directory_uri() . 'D:\Slash\Programming\Project\ForWordPress\for_WP_2_0', // Шлях до файлу скрипту
                ['jquery'], // Масив залежностей, наприклад jQuery
                '1.0.0', // Версія скрипту
                true // Вказуємо, що скрипт потрібно підключити в кінці сторінки
            );
        }
    }
}

// Додаємо функцію до хуку для підключення стилів та скриптів в адмін-панелі
add_action('admin_enqueue_scripts', 'enqueue_spirit_style_and_script');

function enqueue_spirit_media_uploader() {
    wp_enqueue_media(); // Підключаємо медіа-скрипти WordPress

}
add_action('admin_enqueue_scripts', 'enqueue_spirit_media_uploader');
