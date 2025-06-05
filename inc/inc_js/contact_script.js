// This file for script

function handleImage(idBtn,idPrevImg,idPrevDiv){
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
}

function updateSvgPreviewById(textAreaId, previewDivId) {
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
}



document.addEventListener("DOMContentLoaded",function () {
    document.getElementById('load_image').addEventListener('click',function (){
        handleImage('load_image_text', 'preview_image', '');
    })
    loadImage('load_image_text', 'preview_image', '');

handleSvgInput('text_svg_area_photo', 'preview_svg_photo');
    // Додатково викликаємо функцію після завантаження, якщо поле вже містить SVG
    updateSvgPreviewById('text_svg_area_photo', 'preview_svg_photo');
})

