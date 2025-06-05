import os
import shutil


def copy_and_rename_images(source_folder, destination_folder):
    # Перевірка, чи існує папка призначення
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Створено нову папку: {destination_folder}")
    s = 0
    # Список підтримуваних форматів зображень
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    # Перебір всіх підпапок в source_folder
    for master_folder in os.listdir(source_folder):
        master_path = os.path.join(source_folder, master_folder)

        # Перевірка, чи це папка
        if os.path.isdir(master_path):
            print(f"Обробка папки: {master_folder}")
            counter = 1  # Лічильник зображень для поточного майстра

            # Перебір всіх файлів в папці майстра
            for file_name in os.listdir(master_path):
                file_path = os.path.join(master_path, file_name)

                # Перевірка чи файл є зображенням
                if os.path.isfile(file_path) and any(file_name.lower().endswith(ext) for ext in image_extensions):
                    # Створення нового імені для файлу з ім'ям майстра і лічильником
                    ext = os.path.splitext(file_name)[1]  # Отримуємо розширення файлу
                    new_file_name = f"{master_folder}{counter}{ext}"  # Формуємо нове ім'я (включаючи ім'я майстра і номер)
                    dest_file_path = os.path.join(destination_folder, new_file_name)

                    # Копіювання файлу в нову папку з новим ім'ям
                    shutil.copy(file_path, dest_file_path)
                    print(f"Копіюємо {file_name} як {new_file_name}")
                    s+=1

                    # Збільшуємо лічильник для наступного файлу
                    counter += 1

    print("Процес завершено!",s)

# Виклик функції
source_folder = "D:\Download\Data"
destination_folder = "D:\Download\photoAll"
copy_and_rename_images(source_folder, destination_folder)
