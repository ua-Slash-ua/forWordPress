

def create_rest_route(word):
    return f'''
// Додаємо REST API маршрут {word}
function register_{word}_info_rest_route() {{
    register_rest_route('wp/v2', '/{word}', [
        'methods' => 'GET',
        'callback' => 'get_info_{word}',
        'permission_callback' => '__return_true', // або використовуйте власну перевірку доступу
    ]);
}}
add_action('rest_api_init', 'register_{word}_rest_route');
'''

def create_get_info_for_rest(word):
    return f'''
function get_info_{word}($custom_fields = [
    'some_name' => 'my_name',
]) {{
    // Ініціалізація порожнього масиву для збереження інформації
    $contact_info = [];

    // Проходимо через кожне передане поле
    foreach ($custom_fields as $field_name => $custom_name) {{
        // Викликаємо get_option для отримання значення поля з бази WordPress
        // Зберігаємо результат у масив з ключем $custom_name
        $contact_info[$custom_name] = get_option($field_name);
    }}

    // Повертаємо заповнений масив
    return $contact_info;
}}

'''

