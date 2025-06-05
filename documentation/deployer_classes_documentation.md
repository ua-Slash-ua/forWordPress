
# 📘 Документація до класів деплойменту WordPress

---

## 🧱 `BaseDeployer`

### 🔹 Опис:
Базовий клас для розгортання WordPress, від якого наслідуються всі специфічні реалізації (наприклад, розгортання в кастомне середовище або в OpenServer).

### 📌 Конструктор
```python
def __init__(self, main_settings, wp_settings, CustomLogging)
```
- `main_settings` *(dict)* — словник із загальними конфігураційними параметрами.
- `wp_settings` *(dict)* — словник із налаштуваннями для конкретного розгортання WP.
- `CustomLogging` *(class/obj)* — кастомний логер для виведення інформації, помилок, успішних повідомлень.

### 📌 Методи

#### `copy_wp(folder_path: str, folder_name: str) -> str`
- **Опис**: копіює шаблон WordPress у зазначену директорію з новою назвою папки.
- **Параметри**:
  - `folder_path` — шлях до директорії, куди буде копіюватися WordPress.
  - `folder_name` — ім’я нової папки WordPress у цьому шляху.
- **Повертає**: повний шлях до створеної папки WordPress.

#### `info_log(status: str, message: str)`
- **Опис**: логування інформаційного повідомлення через `CustomLogging`.

#### `error_log(message: str)`
- **Опис**: логування помилки через `CustomLogging`.

---

## 🧩 `CustomDeployer(BaseDeployer)`

### 🔹 Опис:
Клас для розгортання WordPress в кастомне середовище (наприклад, фізично окрема директорія для кожного клієнта чи проєкту).

### 📌 Метод

#### `deploy_wp()`
- **Опис**:
  - Фільтрує всі середовища в `main_settings`, у яких поле `'name'` починається з `'Custom_'` **та** активоване (`'active' == True`).
  - Для кожного такого середовища копіює WordPress через `copy_wp()`.
  - Логує результат або помилку.

- **Використані функції** (ззовні):
  - `get_value_on_other_value()` — фільтрація словників за певною парою ключ-значення.

- **Локальні змінні**:
  - `folder_path` — куди копіювати.
  - `folder_name` — назва папки, береться з `wp_settings['environment_name']`.
  - `path_to_folder_environment` — фактичний шлях до створеної WP-папки.

---

## 🧩 `OpenServerDeployer(BaseDeployer)`

### 🔹 Опис:
Клас для розгортання WordPress в OpenServer + додаткове створення `.osp/project.ini` файлу та перезапуск OpenServer після розгортання.

### 📌 Конструктор
```python
def __init__(self, main_settings, wp_settings, CustomLogging)
```
- Крім стандартного ініціалізатора, ініціалізує ще змінну:
  - `self.path_to_template_osp` — шлях до шаблону `project.ini` (`osp` файл).

---

### 📌 Метод

#### `deploy_wp()`
- **Опис**:
  - Фільтрує середовища, у яких `'name' == 'OpenServer'` і `'active' == True`.
  - Копіює WordPress.
  - Створює директорію `.osp`, читає шаблон `project.ini`, замінює `'NAME'` на ім’я проєкту і зберігає його в `.osp/project.ini`.
  - Перезапускає OpenServer (`reload_program()`).
  - Логує всі етапи.

- **Додаткові функції**:
  - `read_txt_file(path)` — читає файл.
  - `write_txt_file(path, content)` — записує файл.

---

### 📌 Метод

#### `reload_program()`
- **Опис**:
  - Завершує процес OpenServer, якщо він уже працює, та запускає заново.
- **Використані функції**:
  - `get_value_in_dict()` — витягує шлях до exe OpenServer.
  - `is_program_running()` — перевірка, чи працює програма.
  - `kill_program()` — завершення процесу.

- **Змінні**:
  - `program_path` — повний шлях до EXE-файлу OpenServer.
  - `program_name` — тільки ім’я EXE-файлу (наприклад, `'Open Server.exe'`).

---

## 🔠 Зовнішні утиліти та функції (які часто викликаються)

| Функція | Опис |
|--------|------|
| `get_value_on_other_value(data, key, value)` | Фільтрує список словників `data`, де `key == value` |
| `get_value_in_dict(dict_obj, key)` | Безпечно витягує значення за ключем |
| `read_txt_file(path)` | Читає текстовий файл |
| `write_txt_file(path, content)` | Записує текстовий файл |
| `is_program_running(name)` | Перевіряє, чи запущена програма з таким ім'ям |
| `kill_program(name)` | Завершує процес з таким ім'ям |

