data_ap_php = {
    'register_type':
        '''<?php
add_action('init', 'register_LNAME_RT_post_type');
                        
function register_LNAME_RT_post_type() {
    register_post_type('LNAME_RT', [
        'label' => 'CNAME_RT',
        'labels' => [
            'name' => 'CNAME_RTs',
            'singular_name' => 'CNAME_RT',
            'add_new' => 'Add New',
            'add_new_item' => 'Add New CNAME_RT',
            'edit_item' => 'Edit CNAME_RT',
            'new_item' => 'New CNAME_RT',
            'view_item' => 'View CNAME_RT',
            'search_items' => 'Search CNAME_RTs',
            'not_found' => 'No CNAME_RTs found',
            'not_found_in_trash' => 'No CNAME_RTs found in Trash',
            'all_items' => 'All CNAME_RTs',
        ],
        'public' => true,
        'show_in_rest' => true,
        'has_archive' => true,
        'rewrite' => ['slug' => 'LNAME_RT'],
        'supports' => ['title'],
        'menu_position' => 1,
        'menu_icon' => 'ICON',
        'capability_type' => 'post',
    ]);
}''',
    'register_meta_box':
        '''/**
 * Реєструє мета-бокс "LNAME_MB" для кастомного типу записів "LNAME_RT".
 */
add_action('add_meta_boxes', 'add_LNAME_MB_meta_boxes');
function add_LNAME_MB_meta_boxes() {
    add_meta_box(
        'LNAME_RT_LNAME_MB_meta',                 // Унікальний ID мета-боксу
        'CNAME_MB Поля',                 // Назва, яка відображається у редакторі
        'render_LNAME_MB_meta_box',      // Назва функції, яка виводить HTML в середині боксу
        'LNAME_RT',                      // Тип запису, до якого прив’язується бокс (у нашому випадку це "LNAME_MB")
        'POSITION_MB',                   // Розміщення мета-боксу: 'normal', 'side', 'advanced'
        'PRIORITY_MB'                   // Пріоритет: 'high', 'core', 'default', 'low'
    );
}
''',
    'fields':
        '''$fields = [
    DATA_LABEL_INC
];''',
    'register_meta_fields':
        '''// Функція для реєстрації мета-полів для типу запису "LNAME"
function register_LNAME_meta_fields() {
    // Глобальний доступ до масиву полів
    global $fields;

    // Реєстрація кожного мета-поля з масиву
    foreach ($fields as $field) {
        // Реєструємо кожне поле за допомогою параметрів з масиву
        register_post_meta('LNAME', $field['key'], [
            'type'         => 'string',          // Тип даних
            'description'  => $field['key'],    // Опис поля
            'single'       => true,              // Одна одиниця для кожного запису
            'show_in_rest' => true,              // Доступ до поля через REST API
        ]);
    }
}

// Додаємо функцію реєстрації мета-полів до хуку ініціалізації WordPress
add_action('init', 'register_LNAME_RT_meta_fields');''',
    'register_rest_api_meta_fields':
        '''// Функція для додавання мета-полів до відповіді REST API для типу запису "LNAME_RT"
function register_LNAME_RT_rest_api_meta_fields($data, $post, $request) {
    // Перевіряємо, чи обробляється потрібний тип запису
    if ($post->post_type === 'LNAME_RT') {
        // Глобальний доступ до масиву полів
        global $fields;
        // Додаємо кожне значення мета-поля до відповіді API
        foreach ($fields as $field) {
            // Отримуємо значення мета-поля
            $raw_value = get_post_meta($post->ID, $field['key'], true);

            // Якщо вказано кастомну функцію для REST API
            if ($field['sanitize_for_rest_api'] && function_exists($field['sanitize_for_rest_api'])) {
                // Викликаємо функцію для обробки значення
                $raw_value = call_user_func($field['sanitize_for_rest_api'], $raw_value);
            }

            // Додаємо оброблене значення до відповіді API
            $data->data[$field['name_rest_api']] = $raw_value;
        }


    }

    // Повертаємо змінений об'єкт відповіді
    return $data;
}

// Прикріплюємо функцію до фільтра REST API для типу запису "LNAME_RT"
add_filter('rest_prepare_LNAME_RT', 'register_LNAME_RT_rest_api_meta_fields', 10, 3);''',
    'render_meta_box':
        '''
function render_LNAME_MB_meta_box($post) {
    DATA_INC
    ?>
             
      DATA_RENDER
        
    <?php
    
}
        ''',
    'save_meta':
        '''add_action('save_post_LNAME_RT', 'save_LNAME_RT_meta');
function save_LNAME_RT_meta($post_id) {
    global $fields;

    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) return;
    if (!current_user_can('edit_post', $post_id)) return;

    foreach ($fields as $field) {
        $key = $field['key'];
        $sanitize = $field['sanitize_for_save'];

        // Викликаємо sanitize-функцію для кожного поля
        $value = call_user_func($sanitize, $_POST[$key]);

        // Оновлюємо мета-дані
        update_post_meta($post_id, $key, $value);
    }
}''',
    'enqueue_style_and_script':
        '''// Функція для підключення стилів та скриптів для адміністративної панелі типу запису "LNAME_RT"
    function enqueue_LNAME_RT_style_and_script($hook) {
        // Перевіряємо, чи ми знаходимося на сторінці редагування або створення запису
        if ($hook === 'post.php' || $hook === 'post-new.php') {
            global $post;
    
            // Перевіряємо, чи поточний пост є типом "LNAME_RT"
            if (isset($post) && get_post_type($post) === 'LNAME_RT') {
                // Підключаємо стилі
                wp_enqueue_style(
                    'LNAME_RT_style', // Унікальний ID для стилю
                    get_template_directory_uri() . '/CSS_PATH', // Шлях до файлу стилю
                    [], // Массив залежностей, якщо немає - залишаємо порожнім
                    '1.0.0' // Версія стилю
                );
    
                // Підключаємо скрипти
                wp_enqueue_script(
                    'LNAME_RT_script', // Унікальний ID для скрипту
                    get_template_directory_uri() . '/JS_PATH', // Шлях до файлу скрипту
                    ['jquery'], // Масив залежностей, наприклад jQuery
                    '1.0.0', // Версія скрипту
                    true // Вказуємо, що скрипт потрібно підключити в кінці сторінки
                );
            }
        }
    }
    
    // Додаємо функцію до хуку для підключення стилів та скриптів в адмін-панелі
    add_action('admin_enqueue_scripts', 'enqueue_LNAME_RT_style_and_script');'''
}


tab = {
    'data_main' : '''<div class="mb_hero">
        <ul class="mb_header">
DATA_HEADER
        </ul>
        <div class="mb_content">
DATA_CONTENT
        </div>
    </div>''',
    'data_header' : '''            <li class="mb_header_item" id="LNAME_TAB">LNAME_TAB</li>''',
    'data_content' : '''            <div class="mb_content_item" id="content_LNAME_TAB">
                DATA_CONTENT_RECORD
            </div>''',
    'data_js_func':'''function actionTab(tabs){
    tabs.forEach(tabName =>{
        document.getElementById(tabName).addEventListener('click', function (){
            document.querySelectorAll('.mb_header_item').forEach( navEl => {
                navEl.classList.remove('tab_active')
            })
            document.querySelectorAll('.mb_content_item').forEach( navEl => {
                navEl.classList.remove('content_active')
            })
            document.getElementById(tabName).classList.add('tab_active')
            document.getElementById(`content_${tabName}`).classList.add('content_active')
        })
    })
}
    ''',
    'data_js_inc':'''let tabs = [DATA_JS]
    actionTab(tabs)''',
    'data_css':'''/*Tab styles*/
.mb_hero {
    width: 100%;
    min-height: 70vh;
}

.mb_header {
    width: 100%;
    height: 7vh;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    font-size: 1.3vw;
}

.mb_header_item {
    border: 0.1vw solid black ;
    width: 100%;
    height: 100%;
    display: flex;
    text-align: center;
    justify-content: center;
    align-items: center;
    background: linear-gradient(180deg, #00aee3, #ffffff);
    color: #000000;
}

.mb_header_item:hover {
    background: linear-gradient(180deg, #0086ae, #ffffff);
    cursor: pointer;
}

.mb_header_item.tab_active{
    background: linear-gradient(0deg, #00aee3, #000000);
    color: #ffffff;
}
.mb_header_item.tab_active:hover {
    background: linear-gradient(0deg, #0086ae, rgba(18, 18, 18, 0.85));
}

.mb_content_item{
    display: none;
}

.mb_content_item.content_active {
    display: flex;
}'''
}

input_text = {
        'data' : '''        <label for="input_text_LLABEL">CLABEL</label>
        <input type="text" value="<?php echo esc_attr($input_text_LLABEL); ?>" name = "input_text_LLABEL" id="input_text_LLABEL" class ="input-item">
''',
        'get_value_post' : '''$input_text_LLABEL = get_post_meta($post->ID, 'input_text_LLABEL', true);''',
        'process_value' : '''create_meta_field_config('input_text_LLABEL','CLABEL')''',
        'container_class' : 'form-container-input',
        'data_css' : '/*Input text styles*/',
        'data_js_func' : '',
        'data_js_inc' : '',
    }

input_date = {
        'data' : '''        <label for="input_date_LLABEL">CLABEL</label>
        <input type="date" value="<?php echo esc_attr($input_date_LLABEL); ?>" name = "input_date_LLABEL" 
        id="input_date_LLABEL" class ="input_date-item">
''',
        'get_value_post' : '''$input_date_LLABEL = get_post_meta($post->ID, 'input_date_LLABEL', true);''',
        'process_value' : '''create_meta_field_config('input_date_LLABEL','CLABEL')''',
        'container_class' : 'form-container-input_date',
        'data_css' : '/*Input date styles*/',
        'data_js_func' : '',
        'data_js_inc' : '',
    }

input_time = {
        'data' : '''        <label for="input_time_LLABEL">CLABEL</label>
        <input type="time" value="<?php echo esc_attr($input_time_LLABEL); ?>" name = "input_time_LLABEL" 
        id="input_time_LLABEL" class ="input_time-item">
''',
        'get_value_post' : '''$input_time_LLABEL = get_post_meta($post->ID, 'input_time_LLABEL', true);''',
        'process_value' : '''create_meta_field_config('input_time_LLABEL','CLABEL')''',
        'container_class' : 'form-container-input_time',
        'data_css' : '/*Input time styles*/',
        'data_js_func' : '',
        'data_js_inc' : '',
    }

input_color = {
        'data' : '''        <label for="input_color_LLABEL">CLABEL</label>
        <input type="color" value="<?php echo esc_attr($input_color_LLABEL); ?>" name = "input_color_LLABEL" 
        id="input_color_LLABEL" class ="input_color-item">
''',
        'get_value_post' : '''$input_color_LLABEL = get_post_meta($post->ID, 'input_color_LLABEL', true);''',
        'process_value' : '''create_meta_field_config('input_color_LLABEL','CLABEL')''',
        'container_class' : 'form-container-input_color',
        'data_css' : '/*Input time styles*/',
        'data_js_func' : '',
        'data_js_inc' : '',
    }

textarea = {
        'data' : '''<label for="textarea_LLABEL">CLABEL</label>
                    <textarea name="textarea_LLABEL" id="textarea_LLABEL" class="textarea_LLABEL" cols="30"
                              rows="10"><?php echo esc_attr($textarea_LLABEL); ?></textarea>''',
        'get_value_post' : '''$textarea_LLABEL = get_post_meta($post->ID, 'textarea_LLABEL', true);''',
        'process_value' : '''create_meta_field_config('textarea_LLABEL', 'CLABEL', 'sanitize_textarea_field')''',
        'container_class' : 'form-container-textarea',
        'data_css' : '/*Textarea styles*/',
        'data_js_func' : '',
        'data_js_inc' : '',
    }

input_checkbox = {
        'data' : '''<label for="input_checkbox_LLABEL">CLABEL</label>
                    <input type="checkbox" name="input_checkbox_LLABEL" id="input_checkbox_LLABEL" class="input-checkbox-item"
                        <?php checked( $input_checkbox_LLABEL, 1 ); ?>>''',
        'get_value_post' : '''$input_checkbox_LLABEL = get_post_meta($post->ID, 'input_checkbox_LLABEL', true);''',
        'process_value' : '''create_meta_field_config('input_checkbox_LLABEL', 'CLABEL', 'sanitize_checkbox')''',
        'container_class' : 'form-container-input_checkbox',
        'data_css' : '/*Checkbox styles*/',
        'data_js_func' : '',
        'data_js_inc' : '',
    }

point = {
        'data' : '''<div class="point_hero" id="point_hero_LLABEL">
            <div class="point-edit">
                <label for="point_input_LLABEL">CLABEL
                    <input type="text" id="point_input_LLABEL" class="point_input">
                </label>
                <input type="button" value="+" id="point_add_LLABEL" class="point_add">
            </div>

            <label for="point_data_LLABEL">
                <input type="text" hidden="hidden" id="point_data_LLABEL" name="point_data_LLABEL"
                       value="<?php echo esc_attr($point_LLABEL); ?>">
            </label>
            <div id="point_container_LLABEL" class="point_container">

            </div>
        </div>''',
        'get_value_post' : '''$point_LLABEL = get_post_meta($post->ID, 'point_data_LLABEL', true);''',
        'process_value' : '''create_meta_field_config('point_data_LLABEL', 'CLABEL','sanitize_text_field', 'normalize_to_array')''',
        'container_class' : 'form-container-point',
        'data_css' : '''/*Point style*/
.form-container-point {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    gap: 2vw;
    margin-bottom: 2vh;
}

.point_hero {
    flex: 0 1 40vw;
    max-width: 45vw;
    min-width: 35vw;
    border: 0.1vw solid #ccc;
    padding: 2vh 2vw;
    border-radius: 1vw;
    background-color: #f9f9f9;
    box-sizing: border-box;
}

@media (max-width: 768px) {
    .point_hero {
        flex: 1 1 100%;
        max-width: 90vw;
    }
}

/* Рядок з інпутом і кнопкою + */
.point-edit {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 1vw;
    margin-bottom: 2vh;
}

.point-edit label {
    display: flex;
    flex-direction: column;
    font-weight: bold;
    font-size: 1vw;
    flex: 1;
}

.point_input {
    margin-top: 0.5vh;
    padding: 1vh 1vw;
    font-size: 1vw;
    border: 0.1vw solid #ccc;
    border-radius: 0.8vw;
    box-sizing: border-box;
    width: 100%;
}

.point_add {
    padding: 1vh 1.5vw;
    background-color: #28a745;
    color: #fff;
    border: none;
    font-weight: bold;
    border-radius: 0.8vw;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
    font-size: 1vw;
    height: 100%;
}

.point_add:hover {
    background-color: #218838;
}

.point_container {
    margin-top: 1.5vh;
}

.point_item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: #e9ecef;
    padding: 1vh 1vw;
    margin-bottom: 1vh;
    border-radius: 0.8vw;
    font-size: 1vw;
}

.point_item span {
    font-size: 1vw;
}

.point_del {
    background-color: #dc3545;
    color: #fff;
    border: none;
    font-weight: bold;
    border-radius: 0.6vw;
    padding: 0.5vh 1vw;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
    font-size: 1vw;
}

.point_del:hover {
    background-color: #c82333;
}

.point_input.error {
    border: 0.2vw solid red;
    background-color: rgba(255, 0, 0, 0.1);
    box-shadow: 0 0 0.5vw rgba(255, 0, 0, 0.4);
    transition: all 0.3s ease-in-out;
}

''',
        'data_js_func' : '''function processPoint(pointName) {
    function enableDragAndDrop(container, pointName) {
        let draggedItem = null;

        // Add event listeners to all existing items in the container
        container.querySelectorAll('.point_item').forEach(item => {
            item.setAttribute('draggable', 'true');
            addDragEvents(item);
        });

        function addDragEvents(item) {
            // When drag starts
            item.addEventListener('dragstart', function(e) {
                draggedItem = item;
                setTimeout(() => {
                    item.classList.add('dragging');
                }, 0);
            });

            // When drag ends
            item.addEventListener('dragend', function() {
                item.classList.remove('dragging');
                draggedItem = null;
                // Update data after dragging is complete
                pointUpdateForRestApi(pointName);
            });

            // Prevent default behaviors for some events
            item.addEventListener('dragover', function(e) {
                e.preventDefault();
            });

            item.addEventListener('dragenter', function(e) {
                e.preventDefault();
                if (this !== draggedItem) {
                    this.classList.add('drag-over');
                }
            });

            item.addEventListener('dragleave', function() {
                this.classList.remove('drag-over');
            });

            // Handle dropping
            item.addEventListener('drop', function(e) {
                e.preventDefault();
                this.classList.remove('drag-over');

                if (draggedItem && this !== draggedItem) {
                    // Get positions to determine order
                    const thisRect = this.getBoundingClientRect();
                    const draggedRect = draggedItem.getBoundingClientRect();

                    // Determine if dragged item should be before or after this item
                    if (draggedRect.top < thisRect.top) {
                        container.insertBefore(draggedItem, this);
                    } else {
                        container.insertBefore(draggedItem, this.nextSibling);
                    }
                }
            });
        }

        // Container level events
        container.addEventListener('dragover', function(e) {
            e.preventDefault();
            // Only proceed if we have a valid draggedItem
            if (!draggedItem) return;

            const afterElement = getDragAfterElement(container, e.clientY);
            if (afterElement === null) {
                // Only append if draggedItem exists
                container.appendChild(draggedItem);
            } else if (afterElement !== draggedItem) {
                container.insertBefore(draggedItem, afterElement);
            }
        });

        container.addEventListener('drop', function(e) {
            e.preventDefault();
            // Update after drop
            pointUpdateForRestApi(pointName);
        });

        function getDragAfterElement(container, y) {
            // Convert NodeList to Array and filter out the currently dragged element
            const draggableElements = [...container.querySelectorAll('.point_item:not(.dragging)')];

            // If no elements, return null
            if (draggableElements.length === 0) return null;

            // Find the closest element after cursor position
            return draggableElements.reduce((closest, child) => {
                const box = child.getBoundingClientRect();
                const offset = y - box.top - box.height / 2;

                if (offset < 0 && offset > closest.offset) {
                    return { offset: offset, element: child };
                } else {
                    return closest;
                }
            }, { offset: Number.NEGATIVE_INFINITY }).element;
        }
    }
    function pointAdd(pointName, pointValue){

        const pointItemMain = document.getElementById(`point_container_${pointName}`)

        const pointItemDiv = document.createElement('div')
        pointItemDiv.classList.add('point_item')


        const pointItemSpan = document.createElement('span')
        pointItemSpan.textContent = pointValue

        const pointItemBtn = document.createElement('input')
        pointItemBtn.type='button'
        pointItemBtn.value='x'
        pointItemBtn.classList.add('point_del')
        pointItemBtn.addEventListener('click', function (){
            pointItemMain.removeChild(pointItemDiv)
            pointUpdateForRestApi(pointName)
        })

        pointItemDiv.appendChild(pointItemSpan)
        pointItemDiv.appendChild(pointItemBtn)
        pointItemMain.appendChild(pointItemDiv)
        pointUpdateForRestApi(pointName)
        enableDragAndDrop(pointItemMain, pointName)
    }

    function pointUpdateForRestApi(pointName){
        const pointItemMain = document.getElementById(`point_container_${pointName}`)
        const pointData = document.getElementById(`point_data_${pointName}`)
        let pointDataArray = []

        pointItemMain.querySelectorAll('.point_item').forEach( item =>{
            const pointValue = item.querySelector('span').textContent.trim()
            pointDataArray.push(pointValue)
        })

        pointData.setAttribute('value',JSON.stringify(pointDataArray))

    }

    function pointLoad(pointName) {
        const pointData = document.getElementById(`point_data_${pointName}`);
        let pointDataArray = [];

        try {
            const parsed = JSON.parse(pointData.value);
            if (Array.isArray(parsed)) {
                pointDataArray = parsed;
            }
        } catch (e) {
            console.warn(`Не вдалося розпарсити дані для ${pointName}:`, e);
        }

        pointDataArray.forEach(pointValue => {
            pointAdd(pointName, pointValue);
        });
    }


    pointLoad(pointName)
        document.getElementById(`point_add_${pointName}`).addEventListener('click', function (){
            const pointValue = document.getElementById(`point_input_${pointName}`)

            if (!pointValue.value.trim()) {
                // Додаємо клас одразу
                pointValue.classList.add('error');

                // А потім через деякий час — прибираємо, щоб ефект був тимчасовий
                setTimeout(function () {
                    pointValue.classList.remove('error');
                }, 1500); // наприклад, через 0.8 сек
            }else {
                pointAdd(pointName, pointValue.value.trim())
                pointValue.value = ''

            }

        })
}''',
        'data_js_inc' : '''processPoint('DATA_JS_POINT')''',
    }

table = {
        'data' : '''<div class="table_hero_container_LTDLABEL">
            <div class="table_input_container" id="table_input_container_LTDLABEL">
                <input type="text" hidden="hidden" value="<?php echo esc_attr($table_LTDLABEL); ?>" name="table_data_LTDLABEL"
                       id="table_data_LTDLABEL">
            </div>
            <table class="table_hero" id="table_hero_LTDLABEL">
                <caption class="table_caption" id="table_caption_LTDLABEL">CTDLABEL</caption>
                <thead class="table_head" id="table_head_LTDLABEL">
                </thead>
                <tbody class="table_body" id="table_body_LTDLABEL">
                </tbody>
            </table>

        </div>''',
        'get_value_post' : '''$table_LTDLABEL = get_post_meta($post->ID, 'table_data_LTDLABEL', true);''',
        'process_value' : '''create_meta_field_config('table_data_LTDLABEL', 'CTDLABEL', 'sanitize_text_field', 'normalize_to_array')''',
        'container_class' : 'form-container-table',
        'data_css' : '''/* Table styles */
.form-container-table {
    max-width: 900px;
    margin: 40px auto;
    padding: 20px;
    background-color: #fdfdfd;
    border: 1px solid #ddd;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    font-family: 'Segoe UI', sans-serif;
}

.table_input_container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 20px;
}

.table_input_text,
.table_input_textarea {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 14px;
    transition: border-color 0.3s;
}

.table_input_text:focus,
.table_input_textarea:focus {
    border-color: #0073aa;
    outline: none;
    box-shadow: 0 0 0 2px rgba(0, 115, 170, 0.2);
}

.table_input_container_action {
    display: flex;
    justify-content: flex-end;
}

.table_input_add {
    padding: 8px 16px;
    background-color: #0073aa;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s;
}

.table_input_add:hover {
    background-color: #005f8c;
}

.table_hero {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}

.table_caption {
    caption-side: top;
    text-align: left;
    font-weight: bold;
    font-size: 18px;
    padding: 10px 0;
}

.table_hero th,
.table_hero td {
    padding: 12px;
    border: 1px solid #ddd;
}

.table_hero thead {
    background-color: #f0f0f0;
}

.table_body_action {
    display: flex;
    gap: 8px;
    justify-content: center;
}

.table_btn_remove,
.table_btn_edit {
    padding: 6px 12px;
    border: none;
    border-radius: 4px;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.1s ease-in-out;
}

.table_btn_remove {
    background-color: #e74c3c;
    color: white;
}

.table_btn_remove:hover {
    background-color: #c0392b;
    transform: scale(1.05);
}

.table_btn_edit {
    background-color: #f1c40f;
    color: black;
}

.table_btn_edit:hover {
    background-color: #d4ac0d;
    transform: scale(1.05);
}

/* Мобільна адаптація */
@media (max-width: 600px) {
    .table_hero th,
    .table_hero td {
        padding: 8px;
        font-size: 12px;
    }

    .table_input_text,
    .table_input_textarea {
        font-size: 13px;
    }

    .table_input_add {
        padding: 6px 12px;
        font-size: 13px;
    }
}
.table_input_container .error {
    border: 1px solid red !important;
    box-shadow: 0 0 3px red;
}
''',
        'data_js_func' : '''function processTable(tableName, tableLabels) {
    function tableInit(tableName, tableLabels) {
        const container = document.getElementById(`table_input_container_${tableName}`);

        // Створення полів вводу
        tableLabels.forEach(label => {
            const labelElement = document.createElement('label');
            labelElement.setAttribute('for', `table_input_${tableName}_${label}`);
            labelElement.textContent = label.charAt(0).toUpperCase() + label.replace(/_+$/, '').replace(label.charAt(0),''); // Чистимо "_" для відображення
            let inputElement;
            if (label.endsWith('_')) {
                inputElement = document.createElement('textarea');
                inputElement.setAttribute('cols', '30');
                inputElement.setAttribute('rows', '10');
                inputElement.className = `table_input_${tableName}_textarea`;
            } else {
                inputElement = document.createElement('input');
                inputElement.setAttribute('type', 'text');
                inputElement.className = `table_input_${tableName}_text`;
            }

            inputElement.id = `table_input_${tableName}_${label}`;

            container.appendChild(labelElement);
            container.appendChild(inputElement);
        });

        // Кнопка "Add"
        const actionDiv = document.createElement('div');
        actionDiv.className = 'table_input_container_action';

        const addButton = document.createElement('input');
        addButton.setAttribute('type', 'button');
        addButton.className = 'table_input_add';
        addButton.id = `table_input_add_${tableName}`;
        addButton.value = 'Add';

        actionDiv.appendChild(addButton);
        container.appendChild(actionDiv);

        // Генерація <thead>
        const thead = document.getElementById(`table_head_${tableName}`);
        thead.innerHTML = ''; // Очищення, якщо вже є

        const headerRow = document.createElement('tr');

        // Перший стовпець — Number
        const numberTh = document.createElement('th');
        numberTh.textContent = 'Number';
        headerRow.appendChild(numberTh);

        // Колонки з label
        tableLabels.forEach(label => {
            const th = document.createElement('th');
            th.textContent = label.charAt(0).toUpperCase() + label.replace(/_+$/, '').replace(label.charAt(0),''); // Чистимо "_" для відображення
            headerRow.appendChild(th);
        });

        // Останній стовпець — Action
        const actionTh = document.createElement('th');
        actionTh.textContent = 'Action';
        headerRow.appendChild(actionTh);

        thead.appendChild(headerRow);
    }


    function tableUpdateValueForRestApi(tableName, tableLabels) {
        const tableData = document.getElementById(`table_data_${tableName}`);
        if (!tableData) {
            console.log("Елемент tableData не знайдений");
            return;
        }

        let tableDataArray = [];
        const tableBody = document.getElementById(`table_body_${tableName}`);
        const tableBodyRow = tableBody.querySelectorAll('tr');

        tableBodyRow.forEach(row => {
            let tableDataRow = {};
            const rowElement = row.querySelectorAll('td');
            const filteredRowElement = Array.from(rowElement).slice(1, rowElement.length - 1); // всі td, крім першого і останнього

            // Перевірка, чи кожна клітинка має значення
            let isValidRow = false;
            filteredRowElement.forEach((element, index) => {
                const value = element.textContent.trim(); // Збираємо значення клітинки
                if (value !== "") {
                    const label = tableLabels[index];
                    tableDataRow[label] = value;
                    isValidRow = true;
                }
            });

            if (isValidRow) {
                tableDataArray.push(tableDataRow);
            }
        });

        // Перевірка масиву перед записом
        if (tableDataArray.length > 0) {
            try {
                const jsonData = JSON.stringify(tableDataArray);
                tableData.setAttribute('value', jsonData); // Записуємо в value атрибут
            } catch (error) {
                console.error("Помилка серіалізації JSON:", error);
            }
        } else {
            const jsonData = JSON.stringify([]);
            tableData.setAttribute('value', jsonData); // Записуємо в value атрибут
        }
    }

    function tableUpdateNumber() {
        const tableBody = document.getElementById(`table_body_${tableName}`);
        let num = 1;
        tableBody.querySelectorAll('tr').forEach(element => {
            const elNum = element.querySelector('td');
            elNum.textContent = num;
            num++;
        });
    }

    function enableDragAndDrop(tableBodyId) {
        const tableBody = document.getElementById(tableBodyId);
        let draggedRow = null;

        // Function that adds drag events to a table row
        function addDragEventsToRow(row) {
            row.setAttribute('draggable', 'true');

            row.addEventListener('dragstart', function(e) {
                draggedRow = row;
                // Add a delay to prevent browser from immediately hiding the element
                setTimeout(() => {
                    row.classList.add('dragging');
                }, 0);
            });

            row.addEventListener('dragend', function() {
                row.classList.remove('dragging');
                // Update row numbers and REST API data
                tableUpdateNumber(tableName);
                tableUpdateValueForRestApi(tableName, tableLabels);
                draggedRow = null;
            });

            row.addEventListener('dragover', function(e) {
                e.preventDefault();
            });

            row.addEventListener('dragenter', function(e) {
                e.preventDefault();
                if (this !== draggedRow) {
                    this.classList.add('drag-over');
                }
            });

            row.addEventListener('dragleave', function() {
                this.classList.remove('drag-over');
            });

            row.addEventListener('drop', function(e) {
                e.preventDefault();
                this.classList.remove('drag-over');

                if (draggedRow && this !== draggedRow) {
                    // Get positions to determine whether to place above or below
                    const thisRect = this.getBoundingClientRect();
                    const draggedRect = draggedRow.getBoundingClientRect();

                    // If dragged row's center is above this row's center, place before
                    const draggedCenter = draggedRect.top + draggedRect.height / 2;
                    const thisCenter = thisRect.top + thisRect.height / 2;

                    if (draggedCenter < thisCenter) {
                        tableBody.insertBefore(draggedRow, this);
                    } else {
                        tableBody.insertBefore(draggedRow, this.nextSibling);
                    }

                    // Update row numbers and API data
                    tableUpdateNumber(tableName);
                    tableUpdateValueForRestApi(tableName, tableLabels);
                }
            });
        }

        // Add drag events to all existing rows
        tableBody.querySelectorAll('tr').forEach(row => {
            addDragEventsToRow(row);
        });

        // Handle dragover on the table body for cases when there are no rows
        tableBody.addEventListener('dragover', function(e) {
            e.preventDefault();
            const afterElement = getDragAfterElement(tableBody, e.clientY);
            if (draggedRow) {
                if (afterElement === null) {
                    tableBody.appendChild(draggedRow);
                } else if (afterElement !== draggedRow) {
                    tableBody.insertBefore(draggedRow, afterElement);
                }
            }
        });

        tableBody.addEventListener('drop', function(e) {
            e.preventDefault();
            // Update data after drop
            tableUpdateNumber(tableName);
            tableUpdateValueForRestApi(tableName, tableLabels);
        });

        // Helper function to find the row to insert before
        function getDragAfterElement(container, y) {
            const draggableElements = [...container.querySelectorAll('tr:not(.dragging)')];

            if (draggableElements.length === 0) return null;

            return draggableElements.reduce((closest, child) => {
                const box = child.getBoundingClientRect();
                const offset = y - box.top - box.height / 2;

                if (offset < 0 && offset > closest.offset) {
                    return { offset, element: child };
                } else {
                    return closest;
                }
            }, { offset: Number.NEGATIVE_INFINITY }).element;
        }

        return {
            // Function to add drag events to newly created rows
            addDragEventsToNewRow: addDragEventsToRow
        };
    }

    function tableAddRow(tableName, tableValues) {
        const tableBody = document.getElementById(`table_body_${tableName}`);
        const trRow = document.createElement('tr');
        const tdNum = document.createElement('td');
        trRow.appendChild(tdNum);

        tableValues.forEach(value => {
            const tdValue = document.createElement('td');
            tdValue.textContent = value;
            trRow.appendChild(tdValue);
        });

        const tdAction = document.createElement('td');
        const divAction = document.createElement('div');
        divAction.classList.add('table_body_action');

        const btnEdit = document.createElement('input');
        btnEdit.type = 'button';
        btnEdit.value = 'i';
        btnEdit.classList.add('table_btn_edit');
        btnEdit.addEventListener('click', function () {
            tableLabels.forEach((elem, index) => {
                const element = tableContainer.querySelector(`#table_input_${tableName}_${elem}`);
                if (element.endsWith === '_') {
                    element.textContent = tableValues[index];
                } else {
                    element.value = tableValues[index];
                }
            });
            tableBody.removeChild(trRow);
            tableUpdateNumber(tableName);
        });

        const btnRemove = document.createElement('input');
        btnRemove.type = 'button';
        btnRemove.value = 'x';
        btnRemove.classList.add('table_btn_remove');
        btnRemove.addEventListener('click', function () {
            tableBody.removeChild(trRow);
            tableUpdateNumber(tableName);
            tableUpdateValueForRestApi(tableName, tableLabels);
        });

        divAction.appendChild(btnEdit);
        divAction.appendChild(btnRemove);
        tdAction.appendChild(divAction);
        trRow.appendChild(tdAction);
        tableBody.appendChild(trRow);

        // Add drag and drop functionality to the new row
        dragDropHandler.addDragEventsToNewRow(trRow);

        tableUpdateNumber(tableName);
        tableUpdateValueForRestApi(tableName, tableLabels);
    }

    function tableLoad(tableName) {
        const tableData = document.getElementById(`table_data_${tableName}`);
        const tableDataArray = JSON.parse(tableData.value);

        tableDataArray.forEach(element => {
            const tableValues = Object.values(element);
            tableAddRow(tableName, tableValues);
        });
    }

    // Initialize drag and drop functionality
    const dragDropHandler = enableDragAndDrop(`table_body_${tableName}`);
    tableInit(tableName, tableLabels)
    tableLoad(tableName);
    const tableContainer = document.querySelector(`.table_hero_container_${tableName}`);
    const tableBtnAdd = tableContainer.querySelector(`#table_input_add_${tableName}`);



    tableBtnAdd.addEventListener('click', function () {
        const tableValues = [];
        let isAtLeastOneFilled = false;

        tableLabels.forEach(label => {
            const element = tableContainer.querySelector(`#table_input_${tableName}_${label}`);
            let value;

            if (element.endsWith === '_') {
                value = element.textContent.trim();
            } else {
                value = element.value.trim();
            }

            tableValues.push(value);

            if (value !== '') {
                isAtLeastOneFilled = true;
            }
        });

        if (!isAtLeastOneFilled) {
            // Підсвітити всі інпути/текстереа червоним
            tableLabels.forEach(label => {
                const element = tableContainer.querySelector(`#table_input_${tableName}_${label}`);
                element.classList.add('error');

                setTimeout(() => {
                    element.classList.remove('error');
                }, 1500);
            });
            return; // Вихід, якщо все порожнє
        }

        tableAddRow(tableName, tableValues);

        // Очистка полів
        tableLabels.forEach(label => {
            const element = tableContainer.querySelector(`#table_input_${tableName}_${label}`);
            element.value = '';
        });
    });


}''',
        'data_js_inc' : '''processTable('LTDLABEL', [DTLABEL])''',
    }

img_link = {
        'data' : '''<div class="form-container-img_link">
        <div class="img_link_hero" id="img_link_hero_LLABEL">
            <input type="button" value="Upload CLABEL" id="img_link_upload_LLABEL">
            <input type="text" hidden="hidden" value="<?php echo esc_attr($img_link_LLABEL); ?>"
                   id="img_link_data_LLABEL" name="img_link_data_LLABEL">
            <div class="img_link_preview_container" id="img_link_preview_container_LLABEL">

            </div>
        </div>
    </div>''',
        'get_value_post' : '''$img_link_LLABEL = get_post_meta($post->ID, 'img_link_data_LLABEL', true);''',
        'process_value' : '''create_meta_field_config('img_link_data_LLABEL', 'CLABEL', 'sanitize_text_field', 'normalize_array_or_string')''',
        'container_class' : 'form-container-img_link',
        'data_css' : '''/*Img Link styles*/
.form-container-img_link {
    padding: 2vh 2vw;
    box-sizing: border-box;
    max-width: 100%;
}

.img_link_hero {
    display: flex;
    flex-direction: column;
    gap: 2vh;
}

.img_link_hero input[type="button"] {
    align-self: flex-start;
    padding: 1vh 2vw;
    font-size: 1rem;
    border: none;
    border-radius: 0.5vh;
    background-color: #0073aa;
    color: #fff;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.img_link_hero input[type="button"]:hover {
    background-color: #005f8d;
}

.img_link_preview_container {
    display: flex;
    flex-wrap: wrap;
    gap: 2vh;
    padding: 1vh 0;
}

.img_link_preview_item {
    position: relative;
    width: 28vw;
    height: 28vh;
    border-radius: 1vh;
    overflow: hidden;
    background-color: #f0f0f0;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
}

.img_link_preview_item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.img_link_preview_btn {
    position: absolute;
    top: 1vh;
    right: 1vh;
    background-color: rgba(255, 0, 0, 0.75);
    color: white;
    border: none;
    border-radius: 50%;
    font-weight: bold;
    width: 3vh;
    height: 3vh;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 10;
    transition: background-color 0.2s ease;
}

.img_link_preview_btn:hover {
    background-color: rgba(255, 0, 0, 1);
}
''',
        'data_js_func' : '''function processedImgLink(imgName) {

    function imgLinkUploadPhoto(data) {
        console.log(data)
        const previewContainer = document.querySelector(`#img_link_preview_container_${imgName}`);
        if (!previewContainer) return;
        // Очистити попередній вміст
        previewContainer.innerHTML = '';

        const attachments = Array.isArray(data) ? data : [data];

        attachments.forEach(attachment => {
            const imageWrapper = document.createElement('div');
            imageWrapper.className = 'img_link_preview_item';

            const btnRemove = document.createElement('input');
            btnRemove.type = 'button'
            btnRemove.value = 'x'
            btnRemove.classList.add('img_link_preview_btn')
            btnRemove.addEventListener('click', function (){
                previewContainer.removeChild(imageWrapper);
                imgLinkUpdateForRestApi()
            })

            const img = document.createElement('img');
            img.src = attachment


            imageWrapper.appendChild(img);
            imageWrapper.appendChild(btnRemove);
            previewContainer.appendChild(imageWrapper);
        });
        imgLinkUpdateForRestApi()
    }

    function imgLinkInitMediaUploader() {
        const uploadBtn = document.getElementById(`img_link_upload_${imgName}`);
        if (!uploadBtn) return;

        let mediaUploader;
        const multiple = imgName.endsWith('_');


        uploadBtn.addEventListener('click', function (e) {
            e.preventDefault();

            if (mediaUploader) {
                mediaUploader.open();
                return;
            }

            mediaUploader = wp.media({
                title: 'Select or Upload Images',
                button: {
                    text: 'Use this image'
                },
                multiple: multiple
            });

            mediaUploader.on('select', function () {
                const selection = mediaUploader.state().get('selection');
                const attachments = selection.toArray();
                let attachments_data = []
                attachments.forEach( el =>{
                    attachments_data.push(el.attributes.url)
                    }

                )
                imgLinkUploadPhoto(attachments_data);

            });

            mediaUploader.open();
        });
    }

    function imgLinkUpdateForRestApi(){
        const imgLinkData = document.querySelector(`#img_link_data_${imgName}`);
        const previewContainer = document.querySelectorAll(`#img_link_preview_container_${imgName} .img_link_preview_item`);
        let dataLink = []
        previewContainer.forEach( el =>{
            let link = el.querySelector('img').src
            dataLink.push(link)
        })
        imgLinkData.setAttribute('value',JSON.stringify(dataLink))
    }

    function imgLinkLoad(){
        const imgLinkData = document.querySelector(`#img_link_data_${imgName}`);
        let imgLinkDataArray = JSON.parse(imgLinkData.value)
        imgLinkUploadPhoto(imgLinkDataArray)
    }

    imgLinkInitMediaUploader();
    imgLinkLoad()
}''',
        'data_js_inc' : '''processedImgLink('LLABEL');''',
    }