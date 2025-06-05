script_image_func = '''function handleImage(idBtn,idPrevImg,idPrevDiv){
    const textBtn = document.getElementById(idBtn)

    var mediaUploader = wp.media({
        title: 'Select Image',
        button: {
            text: 'Select'
        },
        multiple: false // Тільки один файл
    });

    // Коли вибрано зображення з медіатеки
    mediaUploader.on('select', function() {
        var attachment = mediaUploader.state().get('selection').first().toJSON();
        if (idPrevImg !=='' && idPrevDiv ===''){
            const prevImg = document.getElementById(idPrevImg);
            prevImg.src = attachment.url;
        }

        if (idPrevDiv !=='' && idPrevImg ===''){
            const prevDiv = document.getElementById(idPrevDiv);
            prevDiv.style.backgroundImage= 'url(' + attachment.url + ')';
        }

        textBtn.setAttribute('value',attachment.url);
        textBtn.value = attachment.url;
    });


    mediaUploader.open(); // Відкриваємо медіатеку



}

function loadImage(idValue,idPrevImg,idPrevDiv){
    const textImg = document.getElementById(idValue)

    if (idPrevImg !=='' && idPrevDiv ===''){
        const prevImg = document.getElementById(idPrevImg);
        prevImg.src = textImg.value;
    }

    if (idPrevDiv !=='' && idPrevImg ===''){
        const prevDiv = document.getElementById(idPrevDiv);
        prevDiv.style.backgroundImage= 'url(' + textImg.value + ')';
    }
}'''
script_image_inc = '''\n    document.getElementById('load_image_LWORD').addEventListener('click',function (){
        handleImage('load_image_text_LWORD', 'preview_image_LWORD', '');
    })
    loadImage('load_image_text_LWORD', 'preview_image_LWORD', '');'''

script_svg_func = '''function updateSvgPreviewById(textAreaId, previewDivId) {
    const textArea = document.getElementById(textAreaId);
    const previewDiv = document.getElementById(previewDivId);
    const svgCode = textArea.value.trim();

    // Очистка попереднього контенту
    previewDiv.innerHTML = "";

    // Перевірка, чи поле не порожнє
    if (!svgCode) {
        previewDiv.textContent = "Please enter SVG code.";
        return;
    }

    try {
        // Перевірка, чи це валідний SVG
        const parser = new DOMParser();
        const doc = parser.parseFromString(svgCode, "image/svg+xml");
        const svgElement = doc.documentElement;

        if (svgElement.tagName.toLowerCase() === "svg") {
            // Вставка SVG у div
            previewDiv.appendChild(svgElement);
        } else {
            previewDiv.textContent = "Invalid SVG code.";
        }
    } catch (error) {
        previewDiv.textContent = "Error rendering SVG.";
    }
}

// Функція для ініціалізації слухачів подій
function handleSvgInput(idText, idPrevDiv) {
    const textArea = document.getElementById(idText);
    const previewDiv = document.getElementById(idPrevDiv);

    // Додавання прослуховувача для оновлення SVG при введенні тексту
    textArea.addEventListener("input", () => updateSvgPreviewById(idText, idPrevDiv));
}'''
script_svg_inc ='''\n    handleSvgInput('text_svg_area_LWORD', 'preview_svg_LWORD');
    // Додатково викликаємо функцію після завантаження, якщо поле вже містить SVG
    updateSvgPreviewById('text_svg_area_LWORD', 'preview_svg_LWORD');'''

script_hl_func = '''function hlHandleSvgImageById(idPreview,svgText){
    const svgPreview = document.getElementById(idPreview); // Отримуємо контейнер для прев'ю
    const svgCode = svgText

    // Перевіряємо, чи це валідний SVG-код
    if (svgCode.startsWith('<svg') && svgCode.endsWith('</svg>')) {
        svgPreview.innerHTML = svgCode; // Оновлюємо контейнер валідним SVG
    } else {
        svgPreview.innerHTML = '<p style="color: red;">Invalid or incomplete SVG code</p>'; // Повідомлення про помилку
    }
}
function hlHandleSvgImageByClass(svgElement, svgText) {
    // Обрізаємо зайві пробіли перед перевіркою
    const trimmedSvgText = svgText.trim();

    // Перевіряємо, чи це валідний SVG-код
    if (trimmedSvgText.startsWith('<svg') && trimmedSvgText.endsWith('</svg>')) {
        svgElement.innerHTML = trimmedSvgText; // Оновлюємо контейнер валідним SVG
    } else {
        svgElement.innerHTML = '<p style="color: red;">Invalid or incomplete SVG code</p>'; // Повідомлення про помилку
    }
}
function updateSvgPreviewInRealTime(idPreview,idInput) {
    const svgInput = document.getElementById(idInput); // Отримуємо textarea

    // Додаємо слухач події для реального часу
    svgInput.addEventListener('input', function () {
        hlHandleSvgImageById(idPreview,svgInput.value.trim());
    });
}


function resetValue(Array){
    Array.forEach( idElement =>{
        const element = document.getElementById(idElement)
        if (element.id.startsWith('hl_input_')){
            document.getElementById(idElement).value = '';
        }
        if (element.id.startsWith('hl_check_')){
                document.getElementById(idElement).checked = false;

        }
        if (element.id.startsWith('hl_svg_')) {
            document.getElementById(idElement).value='';
            document.getElementById(`preview_${idElement}`).innerHTML='';

        }
        if (element.id.startsWith('hl_image_')){
            document.getElementById(idElement).src = '';
            document.getElementById(idElement).alt = 'photo';

        }
    })
}

function hlHandleImage(elImg,link){
    elImg.src = link;
}

function addValueForRestApi(){
    let data = [];
    const blockItem = document.getElementById('hl_preview_all');
    const items = blockItem.querySelectorAll('.hl_preview_item'); // Отримуємо всі елементи з класом hl_preview_item
    const dataFRA = document.getElementById('save_data_text')

    items.forEach(item => {
    let itemData = {}

        // Проходимо по всіх дочірніх елементах всередині hl_preview_item
        item.querySelectorAll('*').forEach(child => {
            const className = [...child.classList].find(cls =>
                cls.startsWith('hl_input_') ||
                cls.startsWith('hl_check_') ||
                cls.startsWith('hl_svg_') ||
                cls.startsWith('hl_image_')
            );
            if (className) {
                if (child.className.startsWith('hl_input_')) {
                    itemData[child.className] = child.textContent.trim(); // Видаляємо зайві пробіли
                } else if (child.className.startsWith('hl_check_')) {
                    itemData[child.className] = child.textContent === 'on' ? 'on' : 'off'; // Зберігаємо статус чекбокса
                } else if (child.className.startsWith('hl_svg_')) {
                    itemData[child.className] = child.innerHTML.trim(); // Зберігаємо HTML вміст SVG
                } else if (child.className.startsWith('hl_image_')) {
                    const src = child.src;
                    if (src && src.startsWith('http') && !src.includes('wp-admin/post.php')) {
                        itemData[child.className] = src; // Зберігаємо тільки валідний URL
                    } else {
                        itemData[child.className] = 'No valid image source'; // Уникаємо помилкових посилань
                    }
                }
            }
        });

        data.push(itemData); // Додаємо об'єкт з даними у масив
    });

    // console.log(data); // Перевірка результату
    dataFRA.value = JSON.stringify(data);
    dataFRA.setAttribute('value',JSON.stringify(data))
}

function createElement(Array) {
    const container = document.createElement('div')
    const containerParent = document.getElementById('hl_preview_all')
    const manageLabel = document.createElement('div')
    manageLabel.classList.add('manage_label')
    container.classList.add('hl_preview_item')
    Array.forEach( idElement =>{
        const element = document.getElementById(idElement)
        if (element.id.startsWith('hl_input_')){
            const text = document.createElement('p')
            text.classList.add(idElement)
            text.textContent = element.value.trim()
            container.appendChild(text)
        }
        if (element.id.startsWith('hl_check_')){
            const text = document.createElement('p')
            text.classList.add(idElement)
            if (element.checked){
                text.textContent = 'on'
            }else {
                text.textContent = 'off'
            }
            container.appendChild(text)
        }
        if (element.id.startsWith('hl_svg_')) {
            const svg = document.createElement('div');
            svg.classList.add(idElement)
            container.appendChild(svg);  // Додаємо елемент div з класом prev_image в контейнер
            // Тепер передаємо сам елемент (svg), а не клас
            hlHandleSvgImageByClass(svg, element.value);
        }
        if (element.id.startsWith('hl_image_')){
            const img = document.createElement('img');
            img.classList.add(idElement)
            container.appendChild(img);
            hlHandleImage(img,element.src);
        }
    })
    const btnDel = document.createElement('button')
    btnDel.textContent ='Delete';
    btnDel.addEventListener('click',function (){
        event.preventDefault()
        containerParent.removeChild(container)
        addValueForRestApi();
    })
    const btnEdit = document.createElement("button")
    btnEdit.textContent = 'Edit'
    btnEdit.addEventListener('click',function (){
        event.preventDefault()
        container.querySelectorAll('*').forEach(child => {
            const className = [...child.classList].find(cls =>
                cls.startsWith('hl_input_') ||
                cls.startsWith('hl_check_') ||
                cls.startsWith('hl_svg_') ||
                cls.startsWith('hl_image_')
            );
            if (className) {
                if (child.className.startsWith('hl_input_')) {
                    document.getElementById(child.className).value = child.textContent;
                } else if (child.className.startsWith('hl_check_')) {
                    document.getElementById(child.className).checked = child.textContent !== 'off';
                } else if (child.className.startsWith('hl_svg_')) {
                    hlHandleSvgImageByClass(document.getElementById(`preview_${child.className}`), child.innerHTML); // Обробляємо SVG
                    document.getElementById(child.className).value = child.innerHTML.trim();
                    // document.getElementById(child.className).addEventListener('input', function () {
                    // })
                } else if (child.className.startsWith('hl_image_')) {

                    hlHandleImage(document.getElementById(child.className), child.src); // Обробляємо зображення
                }
            }
        });
        containerParent.removeChild(container)
    })
    manageLabel.appendChild(btnDel)
    manageLabel.appendChild(btnEdit)
    container.appendChild(manageLabel)
    containerParent.appendChild(container)
    addValueForRestApi();
}

function uploadImage(btnId,idPrev){
    document.getElementById(btnId).addEventListener('click',function (){
        var mediaUploader = wp.media({
            title: 'Select Image',
            button: {
                text: 'Select'
            },
            multiple: false // Тільки один файл
        });

        // Коли вибрано зображення з медіатеки
        mediaUploader.on('select', function() {
            var attachment = mediaUploader.state().get('selection').first().toJSON();
            // console.log(attachment.url);
            const img = document.getElementById(idPrev)
            hlHandleImage(img,attachment.url)

        });

        mediaUploader.open(); // Відкриваємо медіатеку
    })
}

function uploadElements(){
    let data = [];
    const dataFRA = document.getElementById('save_data_text')
    try {
        data = JSON.parse(dataFRA.value.trim());
        console.log("Parsed Data:", data);
    } catch (error) {
        console.error("JSON parse error:", error);
    }
    const containerParent = document.getElementById('hl_preview_all')
    data.forEach(item => {
        const container = document.createElement('div')
        const manageLabel = document.createElement('div')
        manageLabel.classList.add('manage_label')
        container.classList.add('hl_preview_item')
        for (const key in item) {
            if (Object.hasOwnProperty.call(item, key)) {
                if (key.startsWith('hl_input_')) {
                    const text = document.createElement('p');
                    text.classList.add(key);
                    text.textContent = item[key].trim(); // Використовуємо item[key]
                    container.appendChild(text); // Додаємо текстовий елемент у контейнер
                } else if (key.startsWith('hl_check_')) {
                    const text_c = document.createElement('p');
                    text_c.classList.add(key);
                    text_c.textContent = item[key].trim();
                    container.appendChild(text_c); // Додаємо текстовий елемент у контейнер
                } else if (key.startsWith('hl_svg_')) {
                    const svg = document.createElement('div');
                    svg.classList.add(key);
                    container.appendChild(svg); // Додаємо SVG в контейнер
                    hlHandleSvgImageByClass(svg, item[key].trim()); // Обробляємо SVG
                } else if (key.startsWith('hl_image_')) {
                    const img = document.createElement('img');
                    img.classList.add(key);
                    img.alt='photo';
                    let link = item[key];
                    if (link ==='No valid image source')
                        link = '';
                    container.appendChild(img); // Додаємо зображення в контейнер
                    hlHandleImage(img, link.trim()); // Обробляємо зображення
                }
            }
        }
        const btnDel = document.createElement('button')
        btnDel.textContent ='Delete';
        btnDel.addEventListener('click',function (){
            event.preventDefault()
            containerParent.removeChild(container)
            addValueForRestApi();
        })
        const btnEdit = document.createElement("button")
        btnEdit.textContent = 'Edit'
        btnEdit.addEventListener('click',function (){
            event.preventDefault()
            container.querySelectorAll('*').forEach(child => {
                const className = [...child.classList].find(cls =>
                    cls.startsWith('hl_input_') ||
                    cls.startsWith('hl_check_') ||
                    cls.startsWith('hl_svg_') ||
                    cls.startsWith('hl_image_')
                );
                if (className) {
                    if (child.className.startsWith('hl_input_')) {
                        document.getElementById(child.className).value = child.textContent;
                    } else if (child.className.startsWith('hl_check_')) {
                        document.getElementById(child.className).checked = child.textContent !== 'off';
                    } else if (child.className.startsWith('hl_svg_')) {
                        hlHandleSvgImageByClass(document.getElementById(`preview_${child.className}`), child.innerHTML); // Обробляємо SVG
                        document.getElementById(child.className).value = child.innerHTML.trim();
                        // document.getElementById(child.className).addEventListener('input', function () {
                        // })
                    } else if (child.className.startsWith('hl_image_')) {

                        hlHandleImage(document.getElementById(child.className), child.src); // Обробляємо зображення
                    }
                }
            });
            containerParent.removeChild(container)
        })
        manageLabel.appendChild(btnDel)
        manageLabel.appendChild(btnEdit)
        container.appendChild(manageLabel)
        containerParent.appendChild(container)
    });
}'''

script_points_func = '''function updatePointsForRestApi(idEl) {
    let data =[]
    const mainDiv = document.getElementById(idEl)
    const items = mainDiv.querySelector('div').querySelectorAll('div')
    items.forEach(element =>{
        const text = element.querySelector('p')
        data.push(text.textContent);
    })

    const save_data = mainDiv.querySelector('input')
    save_data.value = JSON.stringify(data)
    save_data.setAttribute('value',JSON.stringify(data))


}

function loadPoints(idData,idPreview) {
    let data = []
    const inpData = document.getElementById(idData)
    const mainDiv = document.getElementById(idPreview)
    data = JSON.parse(inpData.value)
    data.forEach(element =>{
        const containerEl = document.createElement('div')
        containerEl.classList.add('container_preview_points_item')

        const textEl = document.createElement('p')
        textEl.textContent = element;

        const btnDel = document.createElement('button')
        btnDel.textContent='Delete';
        btnDel.addEventListener('click',function (){
            event.preventDefault()
            mainDiv.removeChild(containerEl)
            updatePointsForRestApi(document.getElementById(idPreview).parentElement.id)
        })

        containerEl.appendChild(textEl)
        containerEl.appendChild(btnDel)
        mainDiv.appendChild(containerEl)
    })

}
function createPoints(idInput,idPreview){
    const inpText = document.getElementById(idInput)
    const mainDiv = document.getElementById(idPreview)

    const containerEl = document.createElement('div')
    containerEl.classList.add('container_preview_points_item')

    const textEl = document.createElement('p')
    textEl.textContent = inpText.value;

    const btnDel = document.createElement('button')
    btnDel.textContent='Delete';
    btnDel.addEventListener('click',function (){
        event.preventDefault()
        mainDiv.removeChild(containerEl)
        updatePointsForRestApi(document.getElementById(idPreview).parentElement.id)
    })

    containerEl.appendChild(textEl)
    containerEl.appendChild(btnDel)
    mainDiv.appendChild(containerEl)
}

function addPoints(idMain, idData, idPreview, idInput,idBtn){
    loadPoints(idData,idPreview)

    document.getElementById(idBtn).addEventListener('click',function (){
        if (document.getElementById(idInput).value.trim() !==''){
            createPoints(idInput,idPreview)
            updatePointsForRestApi(idMain)
            document.getElementById(idInput).value='';
        }else {
            document.getElementById(idInput).classList.add('error-inp')
        }

    })

}
'''
script_points_inc = '''\n    addPoints('form_container_points_LWORD','save_data_points_LWORD','preview_points_LWORD','points_LWORD','btn_points_LWORD');
'''

script_table_func = '''
function updateTableForRestApi(idTableBody) {
    let data = []
    let infoCell = []
    const tableBody = document.getElementById(idTableBody)
    const allTableHead = tableBody.parentElement.querySelector('thead').querySelector('tr') .querySelectorAll('th')    // Отримуємо всі рядки таблиці
    const tableHead = Array.from(allTableHead).slice(1,-1);
    tableHead.forEach(textCell =>{
        infoCell.push(textCell.textContent)
    })

    const tableLines = Array.from(tableBody.querySelectorAll('tr'));
    tableLines.forEach(child =>{
        const thTable = Array.from(child.querySelectorAll('th')).slice(1, -1);
        let num = 0
        let dataLine = {}
        thTable.forEach( element =>{
            dataLine[infoCell[num].toLowerCase()] = element.textContent;
            num++;
            }
        )
        data.push(dataLine)
    })
    // console.log(data)
    const tableForm = document.getElementById('table_data')
    tableForm.value = JSON.stringify(data)
    tableForm.setAttribute('value',JSON.stringify(data))
}

function updateEnumerationTable(idTableBody) {
    let num = 1
    const tableBody = document.getElementById(idTableBody)
    const tableLine = tableBody.querySelectorAll('tr')
    tableLine.forEach( child =>{
        const cellChild = child.querySelectorAll('th')[0]
        // console.log('Before:',cellChild.textContent)
        cellChild.textContent = String(num);
        // console.log('After :',num)
        num++;
    })
}

function createTableLine(idTableBody, dataValue) {
    const tableBody = document.getElementById(idTableBody)
    const tableLine = document.createElement('tr')
    const tableCellNum = document.createElement('th')
    let num = 0
    const rows = tableBody.querySelectorAll('tr')


    if (rows.length > 0) {
        const lastRow = rows[rows.length - 1]; // Остання комірка

        num=1+Number(lastRow.querySelectorAll('th')[0].textContent); // Збільшуємо номер для нового рядка
    } else {
        num = 1; // Якщо таблиця порожня, починаємо з 1
    }
    tableCellNum.textContent = String(num);
    tableLine.appendChild(tableCellNum)
    dataValue.forEach(text=>{
        const tableCell = document.createElement('th')
        tableCell.textContent = text;
        tableLine.appendChild(tableCell)
    })

    const tableCellAction = document.createElement('th')

    const btnDel = document.createElement('button')
    btnDel.textContent = 'Delete'
    btnDel.addEventListener('click',function (){
        event.preventDefault();
        tableBody.removeChild(tableLine)
        updateEnumerationTable(idTableBody)
        updateTableForRestApi(idTableBody)
    })


    tableCellAction.appendChild(btnDel)

    tableLine.appendChild(tableCellAction)
    tableBody.appendChild(tableLine)
    updateTableForRestApi(idTableBody)
}

function loadTableData(idTableBody, idDataTable) {
    const dataTable = document.getElementById(idDataTable)
    const tableBody = document.getElementById(idTableBody)
    let data = JSON.parse(dataTable.value)
    // console.log(data)
    data.forEach( dict =>{

        const tableLine = document.createElement('tr')
        const tableCellNum = document.createElement('th')
        let num = 0
        const rows = tableBody.querySelectorAll('tr')


        if (rows.length > 0) {
            const lastRow = rows[rows.length - 1]; // Остання комірка

            num=1+Number(lastRow.querySelectorAll('th')[0].textContent); // Збільшуємо номер для нового рядка
        } else {
            num = 1; // Якщо таблиця порожня, починаємо з 1
        }
        tableCellNum.textContent = String(num);
        tableLine.appendChild(tableCellNum)
        // Додаємо дані з об'єкта
        Object.keys(dict).forEach(key => {
            const tableCell = document.createElement('th');
            tableCell.textContent = dict[key];
            tableLine.appendChild(tableCell);
        });

        const tableCellAction = document.createElement('th')

        const btnDel = document.createElement('button')
        btnDel.textContent = 'Delete'
        btnDel.addEventListener('click',function (){
            event.preventDefault();
            tableBody.removeChild(tableLine)
            updateEnumerationTable(idTableBody)
            updateTableForRestApi(idTableBody)
        })


        tableCellAction.appendChild(btnDel)

        tableLine.appendChild(tableCellAction)
        tableBody.appendChild(tableLine)
        })


}

function enableDragAndDrop(tbodyId) {
    const tbody = document.getElementById(tbodyId);

    if (!tbody) {
        console.error(`Element with id "${tbodyId}" not found.`);
        return;
    }

    let draggedRow = null;

    // Додаємо події для кожного рядка
    tbody.querySelectorAll('tr').forEach(row => {
        row.setAttribute('draggable', true); // Робимо рядок перетаскуваним

        // Подія, коли починається перетягування
        row.addEventListener('dragstart', (e) => {
            draggedRow = row;
            row.classList.add('dragging');


        });

        // Подія, коли перетягування закінчується
        row.addEventListener('dragend', () => {
            row.classList.remove('dragging');
            draggedRow = null;
            updateEnumerationTable(tbodyId)
            updateTableForRestApi(tbodyId)
        });

        // Дозволяємо перетягування над іншим рядком
        row.addEventListener('dragover', (e) => {
            e.preventDefault();
            row.classList.add('dragover');
        });

        // Виконуємо заміну рядків
        row.addEventListener('drop', (e) => {
            e.preventDefault();
            row.classList.remove('dragover');
            if (draggedRow && draggedRow !== row) {
                const parent = tbody;
                const draggedIndex = Array.from(parent.children).indexOf(draggedRow);
                const targetIndex = Array.from(parent.children).indexOf(row);

                if (draggedIndex < targetIndex) {
                    parent.insertBefore(draggedRow, row.nextSibling);
                } else {
                    parent.insertBefore(draggedRow, row);
                }
            }
        });
    });
}

function create_table(idTableBody,idTableData,idTableBtn, data) {
    loadTableData(idTableBody,idTableData)
    // Виклик функції для таблиці з ID "body_table"
    enableDragAndDrop(idTableBody);
    document.getElementById(idTableBtn).addEventListener('click',function (){
        let dataId = data
        let dataValue = []
        dataId.forEach(idElement =>{
            const text = document.getElementById(idElement).value
            dataValue.push(text)
        })

        createTableLine(idTableBody,dataValue)
        // Виклик функції для таблиці з ID "body_table"
        enableDragAndDrop(idTableBody);

        dataId.forEach(idElement =>{
            const text = document.getElementById(idElement)
            text.value = ''
        })
    })
}'''
script_table_inc = '''\n    create_table('body_table','table_data','btn_table_add',[DATA_WORD])
'''