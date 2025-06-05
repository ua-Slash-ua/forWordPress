style_input = '''
.form-container-input {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Два стовпці */
    gap: 10px; /* Відстань між елементами */
    padding: 15px;
    background-color: #fafafa;
    border-radius: 6px;
    border: 1px solid #ddd;
}

.form-container-input label {
    grid-column: span 2; /* Лейбли займають весь ряд */
    font-size: 14px;
    color: #333;
    margin-bottom: 5px;
}

.input-item {
    width: 100%; /* Поля заповнюють ширину */
    padding: 8px 10px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #fff;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.input-item:hover {
    border-color: #999;
}

.input-item:focus {
    border-color: #007bff;
    outline: none;
    box-shadow: 0 0 4px rgba(0, 123, 255, 0.3);
}

.form-container-input label + .input-item {
    margin-bottom: 5px; /* Невеликий відступ між лейблом і полем */
}

@media (max-width: 768px) {
    .form-container-input {
        grid-template-columns: 1fr; /* Один стовпець на мобільних */
    }
}

'''

style_checkbox = '''
.form-container-check {
    display: grid;
    grid-template-columns: auto;
    gap: 15px;
    margin-bottom: 20px;
    padding: 10px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.form-container-check label {
    font-size: 16px;
    color: #333;
    font-weight: bold;
}

.checkbox-item {
    width: 22px;
    height: 22px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid #ddd;
    border-radius: 5px;
}

.checkbox-item:checked {
    background-color: #4CAF50;
    border-color: #4CAF50;
}

.checkbox-item:focus {
    outline: none;
    box-shadow: 0 0 3px rgba(0, 123, 255, 0.6);
}

.checkbox-item:not(:checked) {
    background-color: #fff;
    border-color: #ddd;
}

.checkbox-item:hover {
    border-color: #bbb;
}'''

style_image = '''
.form-container-image {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* До 3 блоків у рядку */
    gap: 15px; /* Відстань між блоками */
    padding: 15px;
    background-color: #fafafa;
    border: 1px solid #ddd;
    border-radius: 6px;
}

.form-container-image > div {
    display: flex;
    flex-direction: column; /* Вирівнювання елементів вертикально */
    align-items: center; /* Горизонтальне вирівнювання по центру */
    padding: 10px;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-container-image > div > input[type="button"] {
    margin-bottom: 10px;
    padding: 8px 12px;
    font-size: 14px;
    color: #fff;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.form-container-image > div > input[type="button"]:hover {
    background-color: #0056b3;
}

.form-container-image > div > input[type="text"] {
    display: none; /* Сховане поле, як і було задумано */
}

.form-container-image > div > img {
    max-width: 100%;
    height: auto;
    border: 1px solid #ddd;
    border-radius: 6px;
    object-fit: cover;
}
'''

style_svg = '''
.form-container-image-svg {
    display: flex;
    flex-wrap: wrap; /* Дозволяє перенесення елементів */
    gap: 20px; /* Відстань між блоками */
    justify-content: space-between; /* Рівномірне розташування блоків */
    padding: 20px; /* Внутрішній відступ */
    border: 2px solid #bebebe; /* Видима синя рамка */
    border-radius: 12px; /* Заокруглення країв */
    background-color: #ffffff; /* Світло-блакитний фон */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Додає тінь для глибини */
}


.form-container-image-svg .container_preview_svg {
    flex: 1 1 calc(33.333% - 20px); /* Три елементи в рядок */
    box-sizing: border-box; /* Врахування відступів у ширині */
    max-width: calc(33.333% - 20px); /* Фіксація максимальної ширини */
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 16px;
    background-color: #f9f9f9;
    text-align: center; /* Центрування тексту */
}

.container_preview_svg label {
    display: block; /* Розташування у стовпчик */
    margin-bottom: 8px; /* Відступ між лейблом та полем */
    font-weight: bold;
}

.container_preview_svg textarea {
    width: 100%;
    height: auto; /* Динамічна висота за кількістю рядків */
    resize: none; /* Вимкнення можливості зміни розмірів */
    padding: 8px;
    margin-bottom: 10px; /* Відступ між полем та прев’ю */
    border: 1px solid #ddd;
    border-radius: 4px;
    font-family: monospace; /* Для кращого вигляду коду */
    font-size: 14px;
}

.container_preview_svg .preview_svg {
    width: 100%;
    height: 150px; /* Фіксована висота для прев’ю */
    border: 1px dashed #aaa;
    border-radius: 4px;
    background-color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #999;
    font-size: 14px;
    overflow: hidden; /* Усічення великого контенту */
}

@media (max-width: 768px) {
    .form-container-image-svg .container_preview_svg {
        flex: 1 1 calc(50% - 10px); /* Два елементи в рядок на середніх екранах */
        max-width: calc(50% - 10px);
    }
}

@media (max-width: 480px) {
    .form-container-image-svg .container_preview_svg {
        flex: 1 1 100%; /* Один елемент в рядок на малих екранах */
        max-width: 100%;
    }
}
'''

style_hl_mixed = '''
/* Стиль для контейнера */
.hl_container_hero {
    display: flex;
    flex-direction: column;
    gap: 20px;
    background-color: #f9f9f9;
    padding: 20px 5px 20px 5px;
    border-radius: 10px;
    width: 100%;
    margin: 0 auto;
    align-items: center;
}

/* Стиль для форми */
.hl_container_data {
    width: 100%;
    max-width: 500px;
    display: flex;
    flex-direction: column;
    gap: 15px;

}

/* Стиль для лейблів */
.hl_container_data label {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 5px;
}

/* Стиль для полів вводу */
.hl_container_data input[type="text"],
.hl_container_data textarea {
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-bottom: 10px;
}

/* Стиль для текстового поля (textarea) */
.hl_container_data textarea {
    resize: vertical;
    min-height: 100px;
}

/* Стиль для чекбоксу */
.hl_container_data input[type="checkbox"] {
    margin-right: 10px;
}

/* Стиль для кнопок */
.hl_container_data input[type="button"] {
    padding: 10px 20px;
    font-size: 14px;
    background-color: #0073e6;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.hl_container_data input[type="button"]:hover {
    background-color: #005bb5;
}

/* Стиль для зображення */
.hl_container_data img {
    max-width: 100%;
    margin-top: 10px;
    border-radius: 8px;
}

/* Стиль для контейнера прев'ю */
.hl_preview_all {
    width:100%;
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: space-between;
    margin-top: 20px;
}

/* Стиль для кожного елемента прев'ю */
.hl_preview_all .hl_preview_item {
    width: 48%;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.hl_preview_all .hl_preview_item p {
    margin: 5px 0;
}

/* Стиль для прев'ю SVG */
.hl_preview_all .hl_preview_item .prev_svg {
    margin-top: 10px;
    padding: 20px;
    background-color: #f0f0f0;
    text-align: center;
}

.hl_preview_all .hl_preview_item .prev_svg p {
    color: red;
    font-weight: bold;
}

/* Стиль для зображення прев'ю */
.hl_preview_all .hl_preview_item img {
    max-width: 100%;
    margin-top: 10px;
    border-radius: 8px;
}


/* Стиль для кнопки збереження */
.hl_container_data #save_data {
    margin-top: 20px;
    background-color: #28a745;
}

.hl_container_data #save_data:hover {
    background-color: #218838;
}


.hl_preview_all {
    display: flex;
    flex-wrap: wrap; /* Дозволяє елементам переноситися на новий рядок */
    gap: 20px; /* Відстань між елементами */
    justify-content: flex-start; /* Вирівнювання елементів зліва */
}

.hl_preview_item {
    width: calc(33.333% - 20px); /* Три елементи в ряд, враховуючи gap */
    box-sizing: border-box; /* Враховує padding та border в ширині */
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    overflow: hidden;
}

.hl_preview_item p {
    margin: 5px 0;
    font-size: 14px;
    color: #333;
}

.hl_preview_item .prev_svg p {
    color: red; /* Червоний колір для помилки */
    font-size: 14px;
    margin: 0;
}

.hl_preview_item img.prev_image {
    max-width: 100%;
    height: auto;
    margin-top: 10px;
    border-radius: 8px;
}

.hl_preview_item .prev_svg {
    margin-top: 10px;
    padding: 10px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
}

.hl_preview_item img.prev_image {
    display: block;
    margin: 10px auto 0;
}

@media (max-width: 768px) {
    .hl_preview_item {
        width: calc(50% - 20px); /* Для менших екранів два елементи в ряд */
    }
}

@media (max-width: 480px) {
    .hl_preview_item {
        width: 100%; /* Для мобільних екранів один елемент в ряд */
    }
}

/* Контейнер для кнопок */
.manage_label {
    display: flex;
    justify-content: flex-end; /* Вирівнюємо кнопки праворуч */
    gap: 10px; /* Відступ між кнопками */
    padding: 10px; /* Внутрішні відступи для естетики */
    background-color: #f9f9f9; /* Легкий фоновий колір */
    border-top: 1px solid #ddd; /* Лінія для відділення від попереднього елемента */
}

/* Стиль для кнопок */
.manage_label button {
    padding: 8px 12px; /* Внутрішні відступи для розміру кнопок */
    font-size: 14px; /* Розмір тексту */
    border: 1px solid #ccc; /* Рамка кнопки */
    border-radius: 4px; /* Згладжені кути */
    cursor: pointer; /* Курсор у вигляді руки при наведенні */
    background-color: #fff; /* Білий фон */
    color: #333; /* Темний текст */
    transition: background-color 0.3s ease, color 0.3s ease; /* Анімація при наведенні */
}

/* Стиль при наведенні */
.manage_label button:hover {
    background-color: #f0f0f0; /* Легкий сірий фон */
}

/* Стиль для кнопки Delete */
.manage_label button:first-child {
    background-color: #ffdddd; /* Світлий червоний фон */
    color: #d9534f; /* Червоний текст */
    border-color: #d9534f; /* Червона рамка */
}

/* Стиль при наведенні на Delete */
.manage_label button:first-child:hover {
    background-color: #d9534f; /* Темніший червоний фон */
    color: #fff; /* Білий текст */
}

/* Стиль для кнопки Edit */
.manage_label button:last-child {
    background-color: #d9edf7; /* Світлий синій фон */
    color: #31708f; /* Синій текст */
    border-color: #31708f; /* Синя рамка */
}

/* Стиль при наведенні на Edit */
.manage_label button:last-child:hover {
    background-color: #31708f; /* Темніший синій фон */
    color: #fff; /* Білий текст */
}

'''

style_points = '''
/* Загальний контейнер форми */
.form_container_points {
    display: flex;
    flex-direction: column;
    gap: 15px;
    padding: 20px;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
    max-width: 400px;
    font-family: Arial, sans-serif;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Поле для вводу і кнопка */
.form_container_points label {
    font-weight: bold;
    color: #333;
}

.form_container_points input[type="text"] {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
    font-size: 14px;
}



.form_container_points input[type="text"]:focus {
    border-color: #7F54B3;
    outline: none;
    box-shadow: 0 0 5px rgba(127, 84, 179, 0.5);
}

.form_container_points input[type="button"] {
    padding: 10px 15px;
    background-color: #7F54B3;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
}

.form_container_points input[type="button"]:hover {
    background-color: #693ea6;
}

/* Контейнер попереднього перегляду */
.container_preview_points {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 10px;
}

/* Елемент попереднього перегляду */
.container_preview_points_item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 8px 12px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.container_preview_points_item p {
    margin: 0;
    font-size: 14px;
    color: #333;
}

.container_preview_points_item button {
    padding: 5px 10px;
    background-color: #a00;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    transition: background-color 0.3s ease;
}

.container_preview_points_item button:hover {
    background-color: #900;
}

/* Базовий стиль для поля вводу */
.points_input {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
    font-size: 14px;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

/* Стан вводу з помилкою */
.points_input.error-inp {
    border-color: rgba(203, 0, 0, 0.7);
    box-shadow: 0 0 5px rgba(255, 0, 0, 0.5);
    background-color: #ffe6e6;
}

/* Стан при фокусі */
.points_input:focus {
    border-color: #7F54B3;
    outline: none;
    box-shadow: 0 0 5px rgba(127, 84, 179, 0.5);
}

/* Анімація похитування для помилки */
@keyframes shake {
    0%, 100% {
        transform: translateX(0);
    }
    25% {
        transform: translateX(-5px);
    }
    50% {
        transform: translateX(5px);
    }
    75% {
        transform: translateX(-5px);
    }
}

/* Ефект похитування */
.points_input.error-inp {
    animation: shake 0.3s ease-in-out;
}
'''

style_table = '''
/* Загальний стиль таблиці */
.custom-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 16px;
    font-family: Arial, sans-serif;
    text-align: left;
}

/* Заголовки таблиці */
.custom-table thead tr {
    background-color: #7F54B3;
    color: #ffffff;
    text-align: left;
    font-weight: bold;
}

.custom-table th, .custom-table td {
    padding: 12px 15px;
    border: 1px solid #ddd;
}

/* Ряди таблиці */
.custom-table tbody tr {
    border-bottom: 1px solid #ddd;
}

.custom-table tbody tr:nth-of-type(even) {
    background-color: #f3f3f3;
}

.custom-table tbody tr:last-of-type {
    border-bottom: 2px solid #7F54B3;
}

/* Кнопки дій */
.btn-edit {
    background-color: #2ea2cc;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.btn-edit:hover {
    background-color: #1a85a0;
}

.btn-delete {
    background-color: #a00;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.btn-delete:hover {
    background-color: #800000;
}

/* Базовий стиль для таблиці */
.custom-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 18px;
    text-align: left;
}

.custom-table th, .custom-table td {
    border: 1px solid #ddd;
    padding: 12px;
}

/* Стиль для рядків таблиці */
.custom-table tr {
    background-color: #f9f9f9;
    transition: background-color 0.2s ease;
}

.custom-table tr:nth-child(even) {
    background-color: #f1f1f1;
}

/* Стиль для активного (перетягуваного) рядка */
.custom-table tr[draggable="true"] {
    cursor: grab;
}

.custom-table tr[draggable="true"]:active {
    cursor: grabbing;
}

/* Стиль для рядка під час перетягування */
.custom-table tr.dragging {
    opacity: 0.6;
    background-color: #e6e6e6;
    border: 2px dashed #0073e6;
}

/* Стиль для цільової області під час перетягування */
.custom-table tr.dragover {
    background-color: #cce5ff;
    border: 2px dashed #0056b3;
}

/* Основний контейнер */
.container_data {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    padding: 15px;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 6px;
    max-width: 500px;
    margin: 15px auto;
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
}

/* Загальні стилі для міток */
.container_data label {
    flex: 1 1 100%;
    font-size: 12px;
    font-weight: 500;
    color: #333;
    margin-bottom: 4px;
}

/* Стилі для текстових полів */
.container_data input[type="text"] {
    flex: 1 1 calc(100% - 30px);
    padding: 8px;
    font-size: 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #fff;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
    transition: border-color 0.3s ease;
}

.container_data input[type="text"]:focus {
    border-color: #007bff;
    outline: none;
    box-shadow: 0 0 4px rgba(0, 123, 255, 0.3);
}

/* Стилі для кнопки */
.container_data input[type="button"] {
    flex: 1 1 100%;
    padding: 8px 12px;
    font-size: 14px;
    color: #fff;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.container_data input[type="button"]:hover {
    background-color: #0056b3;
}

/* Додаткові стилі для зручності */
.container_data input[type="button"]:active {
    background-color: #003f7f;
}

.container_data input[type="button"]:focus {
    outline: none;
    box-shadow: 0 0 4px rgba(0, 123, 255, 0.5);
}
'''