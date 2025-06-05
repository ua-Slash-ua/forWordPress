from create_options import options
from functions import *
from create_post_type import post_type

def create_css_file(word,settings):
    path = '/'.join([settings['path']['path_to_main'], settings['path']['path_to_inc'],settings['path']['path_to_css']] )
    styles = []
    if settings['create_base_func']['input_text']:
        styles.append('''/*----------------   < Input styles >   ----------------*/
    label {
    display: block; /* Розташовує текст на окремій лінії */
    font-size: 16px; /* Розмір шрифту */
    font-weight: bold; /* Напівжирний текст */
    color: #333; /* Колір тексту */
    margin-bottom: 8px; /* Відступ знизу */
    cursor: pointer; /* Робить курсор у вигляді руки при наведенні */
}

input[type="text"] {
    width: 100%; /* Ширина заповнює контейнер */
    padding: 10px; /* Внутрішній відступ */
    font-size: 16px; /* Розмір шрифту */
    border: 1px solid #ccc; /* Сіра рамка */
    border-radius: 4px; /* Закруглені кути */
    background-color: #f9f9f9; /* Світло-сірий фон */
    color: #333; /* Колір тексту */
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1); /* Тінь всередині */
    transition: border-color 0.3s, box-shadow 0.3s; /* Анімація */
}

input[type="text"]:focus {
    border-color: #007BFF; /* Синій колір рамки при фокусі */
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5); /* Тінь при фокусі */
    outline: none; /* Видаляє стандартне виділення */
}''')
    if settings['create_base_func']['img_link']:
        styles.append('''.container_preview {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 20px;
    border: 2px solid #ccc;
    border-radius: 10px;
    width: 300px;
    background-color: #f9f9f9;
}

.container_preview input[type="button"] {
    padding: 10px 20px;
    font-size: 16px;
    border: none;
    background-color: #007bff;
    color: white;
    border-radius: 5px;
    cursor: pointer;
}

.container_preview input[type="button"]:hover {
    background-color: #0056b3;
}

.container_preview img {
    max-width: 100%;
    height: auto;
    display: block;
    border: 2px solid #ddd;
    border-radius: 5px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.container_preview input[type="text"] {
    display: none; /* Прихований текстовий інпут */
}
''')
    if settings['create_base_func']['check_box']:
        styles.append('''.checkbox-label {
    font-size: 14px;
    color: #333;
    cursor: pointer;
    margin-right: 8px;
}

/* Стилі для чекбокса */
.checkbox-input {
    width: 20px;
    height: 20px;
    border: 2px solid #333;
    border-radius: 4px;
    cursor: pointer;
    background-color: white;
    vertical-align: middle;
}

/* Стиль для активного (відміченого) чекбокса */
.checkbox-input:checked {
    background-color: #4CAF50;  /* Зелений колір для відміченого чекбокса */
    border-color: #4CAF50;  /* Зелена обводка */
}
''')
    if settings['create_base_func']['img_svg']:
        styles.append('''.container_preview_svg {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 20px;
    background-color: #f7f7f7;
    border-radius: 8px;
    border: 1px solid #ccc;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
}

/* Стилі для текстового поля для SVG коду */
#text_svg_area {
    width: 100%;
    font-family: "Courier New", Courier, monospace;
    font-size: 14px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: vertical; /* дає можливість змінювати висоту textarea */
    background-color: #fff;
    color: #333;
}

/* Стилі для відображення попереднього перегляду SVG */
.preview_svg {
    width: 100%;
    min-height: 200px;  /* мінімальна висота попереднього перегляду */
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-top: 20px;
    padding: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    box-sizing: border-box;
}

/* Вигляд при появі помилки (невірний SVG код) */
.preview_svg.error {
    background-color: #ffdddd;
    border-color: #ff0000;
    color: #ff0000;
    font-size: 14px;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Вигляд для заголовка/інструкцій */
.container_preview_svg h3 {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
    color: #333;
}

/* Підказки для textarea */
#text_svg_area::placeholder {
    color: #aaa;
    font-style: italic;
}
''')
    with open(f'{path}\\{word}_style.css', 'w', encoding='utf-8') as f:
        f.write(f'/* This file for styles */\n{f'\\n\n'.join(styles)}')
    coloreg(f'<{word}_style.css > was created !!!', 'green')


def create_js_file(word,settings):
    path = '/'.join([settings['path']['path_to_main'], settings['path']['path_to_inc'],settings['path']['path_to_js']] )
    data_func = []
    data_include = []
    if settings['create_base_func']['img_link']:
        data_func.append(f'''function handleImage(idBtn,idPrevImg,idPrevDiv){{
    const textBtn = document.getElementById(idBtn)

    var mediaUploader = wp.media({{
        title: 'Select Image',
        button: {{
            text: 'Select'
        }},
        multiple: false // Тільки один файл
    }});

    // Коли вибрано зображення з медіатеки
    mediaUploader.on('select', function() {{
        var attachment = mediaUploader.state().get('selection').first().toJSON();
        if (idPrevImg !=='' && idPrevDiv ===''){{
            const prevImg = document.getElementById(idPrevImg);
            prevImg.src = attachment.url;
        }}

        if (idPrevDiv !=='' && idPrevImg ===''){{
            const prevDiv = document.getElementById(idPrevDiv);
            prevDiv.style.backgroundImage= 'url(' + attachment.url + ')';
        }}

        textBtn.setAttribute('value',attachment.url);
        textBtn.value = attachment.url;
    }});


    mediaUploader.open(); // Відкриваємо медіатеку



}}

function loadImage(idValue,idPrevImg,idPrevDiv){{
    const textImg = document.getElementById(idValue)

    if (idPrevImg !=='' && idPrevDiv ===''){{
        const prevImg = document.getElementById(idPrevImg);
        prevImg.src = textImg.value;
    }}

    if (idPrevDiv !=='' && idPrevImg ===''){{
        const prevDiv = document.getElementById(idPrevDiv);
        prevDiv.style.backgroundImage= 'url(' + textImg.value + ')';
    }}
}}''')
        data_include.append(f'''document.getElementById('load_image').addEventListener('click',function (){{
        handleImage('load_image_text', 'preview_image', '');
    }})
    loadImage('load_image_text', 'preview_image', '');''')
    if settings['create_base_func']['img_svg']:
        data_func.append(f'''function updateSvgPreviewById(textAreaId, previewDivId) {{
    const textArea = document.getElementById(textAreaId);
    const previewDiv = document.getElementById(previewDivId);
    const svgCode = textArea.value.trim();

    // Очистка попереднього контенту
    previewDiv.innerHTML = "";

    // Перевірка, чи поле не порожнє
    if (!svgCode) {{
        previewDiv.textContent = "Please enter SVG code.";
        return;
    }}

    try {{
        // Перевірка, чи це валідний SVG
        const parser = new DOMParser();
        const doc = parser.parseFromString(svgCode, "image/svg+xml");
        const svgElement = doc.documentElement;

        if (svgElement.tagName.toLowerCase() === "svg") {{
            // Вставка SVG у div
            previewDiv.appendChild(svgElement);
        }} else {{
            previewDiv.textContent = "Invalid SVG code.";
        }}
    }} catch (error) {{
        previewDiv.textContent = "Error rendering SVG.";
    }}
}}

// Функція для ініціалізації слухачів подій
function handleSvgInput(idText, idPrevDiv) {{
    const textArea = document.getElementById(idText);
    const previewDiv = document.getElementById(idPrevDiv);

    // Додавання прослуховувача для оновлення SVG при введенні тексту
    textArea.addEventListener("input", () => updateSvgPreviewById(idText, idPrevDiv));
}}
''')
        data_include.append(f'''handleSvgInput('text_svg_area', 'preview_svg');
    // Додатково викликаємо функцію після завантаження, якщо поле вже містить SVG
    updateSvgPreviewById('text_svg_area', 'preview_svg');''')

    data = f'''
{'\n\n'.join(data_func)}


document.addEventListener("DOMContentLoaded",function () {{
    {'\n\n'.join(data_include)}
}})

'''
    with open(f'{path}\\{word}_script.js', 'w', encoding='utf-8') as f:
        f.write(f'// This file for script\n{data}')
    coloreg(f'<{word}_script.js > was created !!!', 'green')


def create_main_file_meta_post(word,settings):
    with open(f'{settings['path']['path_to_main']}\\{settings['path']['path_to_inc']}\\{word}_admin_panel.php', 'w', encoding='utf-8') as f:
        f.write(post_type(settings))
    coloreg(f'<{word}_admin_panel.php > was created !!!', 'green')

def create_main_file_options(word,settings):
    with open(f'{settings['path']['path_to_main']}\\{settings['path']['path_to_inc']}\\{word}_admin_panel.php', 'w',
              encoding='utf-8') as f:
        f.write(options(settings))
    coloreg(f'<{word}_admin_panel.php > was created !!!', 'green')