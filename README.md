# Генератор базового CPT для WordPress

Цей проєкт створює мінімальний набір файлів для кастомного типу записів (CPT) у WordPress, на основі заданої конфігурації. Ідеально підходить як стартова точка або заготовка.

## 🔧 Основні можливості

1. ✅ **Створення основного PHP-файлу CPT**
   - Автоматично створюється базовий PHP-файл із реєстрацією CPT.

2. ✅ **Підтримка опцій типу `meta_type: options`**
   - Генерується CPT без збереження даних на рівні постів (опціонально).

3. ✅ **Гнучкий контроль над генерацією полів**
   - Підтримуються наступні типи полів *(усі вимкнені за замовчуванням)*:
     - `input_text`
     - `img_link`
     - `img_svg`
     - `check_box`

4. ✅ **Підключення медіа-завантажувача**
   - Автоматичне додавання `wp_enqueue_media()` при потребі.

5. ✅ **Генерація структури проєкту**
   - Створюються базові папки:
     - `inc/` — основний код
     - `inc_css/` — стилі
     - `inc_js/` — скрипти

6. ✅ **Налаштування включення у `functions.php`**
   - Можна увімкнути або вимкнути автоматичне підключення з `functions.php`.

7. ✅ **Контроль перезапису**
   - Якщо файл уже існує — можна увімкнути або вимкнути перезапис.

---

## 🗂️ Конфігурація (`config.json`)

```json
{
  "word": "spirit",
  "meta_type": "options",
  "path": {
    "path_to_main": "D:\\Slash\\Programming\\Language\\PhP\\bilobrov",
    "path_to_inc": "inc",
    "path_to_css": "inc_css",
    "path_to_js": "inc_js"
  },
  "is_create_file": true,
  "include_in_function": false,
  "enqueue_media_uploader": true,
  "create_base_func": {
    "input_text": false,
    "img_link": false,
    "img_svg": false,
    "check_box": false
  },
  "overwrite": true
}
