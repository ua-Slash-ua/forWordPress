
body_options ='''<?php
function register_LWORD_menu() {
    add_menu_page(
        'CWORD',          // Назва вкладки
        'CWORD',          // Назва меню
        'edit_posts',            // Права доступу (без manage_options)
        'LWORDs_slug',     // Унікальний ідентифікатор
        'render_LWORDs_page', // Функція, яка відображатиме контент
        'dashicons-email',       // Іконка
        6                         // Позиція у меню
    );
}
add_action('admin_menu', 'register_LWORD_menu');

function register_LWORD_rest_route() {
    register_rest_route('wp/v2', '/LWORD', [
        'methods' => 'GET',
        'callback' => 'get_LWORD_info',
        'permission_callback' => '__return_true', // або використовуйте власну перевірку доступу
    ]);
}
add_action('rest_api_init', 'register_LWORD_rest_route');

function get_LWORD_info() {
    // Ініціалізація масиву даних
    $data = [];

    // Опис полів для отримання
    $meta_fields = [

    ];

    // Проходимо по кожному полю
    foreach ($meta_fields as $key => $value) {
        if ($value == 'plain') {
            // Отримуємо значення опції як простий текст
            $data[$key] = get_option($key, ''); // Додаємо значення, якщо опція не знайдена, повертається порожній рядок
        } elseif ($value == 'json') {
            // Отримуємо JSON-значення з опції
            $json_value = get_option($key, '');
            $decoded_value = json_decode($json_value, true);

            // Перевірка на помилку декодування JSON
            if (json_last_error() === JSON_ERROR_NONE) {
                $data[$key] = $decoded_value;
            } else {
                $data[$key] = 'Invalid JSON'; // Якщо є помилка в JSON, повертаємо повідомлення про помилку
            }
        }
    }

    // Повертаємо дані як REST API відповідь
    return rest_ensure_response($data);
}

// Реєстрація групи налаштувань
function register_settings_LWORDs_group() {

    $meta_fields = [
    ];
    foreach ($meta_fields as $key ) {
    register_setting(
        'LWORD_group',  // Унікальна назва групи налаштувань
        $key   // Опція, яку ми будемо зберігати в цій групі
    );
    }
}

add_action('admin_init', 'register_settings_LWORDs_group');

// Виведення сторінки налаштувань
function render_LWORDs_page() {
    ?>
    <div class="wrap">
        <h1>CWORD Settings</h1>
        <form method="post" action="options.php" enctype="multipart/form-data">
            <?php
            settings_fields('LWORD_group'); // Виводимо nonce та інші безпечні дані для групи налаштувань
            do_settings_sections('LWORDs_slug'); // Виводимо секції та поля налаштувань  
            //++
            ?>

           <input type="submit" value="Save Changes" class="button button-primary">
        </form>
    </div>
    <?php
}


function enqueue_LWORD_style_and_script($hook) {
    // Перевіряємо, чи це сторінка кастомного меню "LWORDs_slug"
    if ($hook === 'toplevel_page_LWORDs_slug') {
        // Підключаємо CSS стилі
        wp_enqueue_style(
            'LWORD-style', // Унікальний ID для стилю
            get_template_directory_uri() . 'PartPathCSS', // Шлях до файлу стилю
            [], // Залежності
            '1.0.0' // Версія стилю
        );

        // Підключаємо JS скрипт
        wp_enqueue_script(
            'LWORD-script', // Унікальний ID для скрипту
            get_template_directory_uri() . 'PartPathJS', // Шлях до файлу скрипту
            ['jquery'], // Залежність від jQuery
            '1.0.0', // Версія скрипту
            true // Підключаємо скрипт внизу сторінки (після контенту)
        );
    }
}
add_action('admin_enqueue_scripts', 'enqueue_LWORD_style_and_script');
'''

get_value_options = '''           $LWORD = get_option('LWORD');'''

input_option = '''                  <label for="LWORD">CWORD</label>
                  <input type="text" id="LWORD" name="LWORD" value="<?php echo $LWORD ?>">'''
hl_input_option = '''                    <label for="LWORD">CWORD</label>
                    <input type="text" value="" name = "input_LWORD" id="LWORD" class ="">
'''

checkbox_option = '''        <label for="LWORD" >CWORD</label>
        <input type="hidden" name="LWORD" value="off">
        <input type="checkbox" name="LWORD" id="LWORD" <?php echo  $LWORD ?> class="checkbox-item">'''
hl_checkbox_option = '''                    <label for="LWORD" >CWORD</label>
                    <input type="hidden" name="LWORD" value="off">
                    <input type="checkbox" name="LWORD" id="LWORD"  class="">'''

img_link_option = '''        <div class="container_preview_LWORD">
                <input type="button" value="Load CWORD"  id="load_image_LWORD"/>
                <input type="text" hidden="hidden" value="<?php echo esc_attr($img_LWORD)  ?>" name="load_image_text_LWORD"  id="load_image_text_LWORD"/>
                <img src="" alt="image" id="preview_image_LWORD"/>
        </div>'''
hl_img_link_option = '''                    <input type="button" id="btn_LWORD" value="Upload CWORD">
                    <img id="LWORD" src="" alt="photo">'''

img_svg_option = '''        <div class="container_preview_svg">
                <label for="text_svg_area_LWORD">Write CWORD SVG code:</label>
                <textarea name="text_svg_area_LWORD" id="text_svg_area_LWORD"  rows="10"><?php echo esc_attr($svg_LWORD) ?></textarea>
                <div class="preview_svg" id ="preview_svg_LWORD"></div>
        </div>'''
hl_img_svg_option = '''                    <label for="LWORD">Write CWORD SVG code:</label>
                    <textarea name="LWORD" id="LWORD" cols="30" rows="10"></textarea>
                    <div class="preview_LWORD" id="preview_LWORD"></div>'''

points_option = '''            <div class="form_container_points" id="form_container_points_LWORD">
                <input type="text" name ='save_data_points_LWORD' id="save_data_points_LWORD"  hidden="hidden" value="<?php echo  esc_attr($points_LWORD)?>" >
                <label for="points_LWORD">CWORD</label>
                <input type="text" id="points_LWORD" class="points_input">
                <input type="button" id="btn_points_LWORD" value="Add CWORD">
                <div class="container_preview_points" id="preview_points_LWORD">
                </div>
            </div>'''

table_option = '''           <div class="form_container_table" >
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
