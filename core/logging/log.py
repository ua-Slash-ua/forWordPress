import datetime
import traceback


class ErrorAndInitLogging:
    def __init__(self, path_to_debug, path_to_info):
        self.path_to_debug = path_to_debug
        self.path_to_info = path_to_info
        self.write_debug('-'*50)
        self.write_info('new','-'*50)

    def write_debug(self, msg):
        if isinstance(msg, Exception):
            # Отримуємо повідомлення про помилку та трасування
            msg = f"Exception: {str(msg)}\nTraceback:\n{traceback.format_exc()}"
        now = f'[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] '
        line_message = now + msg + '\n'
        with open(self.path_to_debug,'a+', encoding = 'utf-8') as file:
            file.write(line_message)

    def write_info(self, status, msg):
        # Дозволені статуси та кольори
        allowed_statuses = {
            'success': ['SUCCESS', 'green'],
            'already': ['ALREADY EXIST', 'yellow'],
            'error': ['ERROR', 'red'],
            'info': ['INFO', 'cyan'],
            'new': ['NEW', 'black']
        }
        if isinstance(msg, Exception):
            # Отримуємо повідомлення про помилку та трасування
            msg = f"Exception: {str(msg)}\nTraceback:\n{traceback.format_exc()}"

        max_length = max(len(allowed_statuses[a][0]) for a in allowed_statuses)

        # Отримуємо поточний час
        now = f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] '

        # Перевірка статусу і вибір кольору
        if status.lower() in allowed_statuses:
            line_message = now + f"[<span style='color:{allowed_statuses[status.lower()][1]}'>" + \
                           allowed_statuses[status.lower()][0] + f"</span>] {'_'*(max_length-len(allowed_statuses[status.lower()][0])+2)}-" + msg + '<br>\n'
        else:
            # Якщо статус не знайдено, буде використовувати синій колір
            line_message = now + f"[<span style='color:blue'>UNKNOWN STATUS</span>] -{msg}<br>\n"

        # Записуємо повідомлення в файл
        with open(self.path_to_info, 'a+', encoding='utf-8') as file:
            file.write(line_message)


# Використання:
if __name__ == '__main__':
    path_to_debug = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\debug.log'
    path_to_info = r'D:\Slash\Programming\Project\ForWordPress\for_WP_3_0\logs\info.md'
    errorlog = ErrorAndInitLogging(path_to_debug,path_to_info)
    # errorlog.write_info('success','Успішно')
    # errorlog.write_info('already','Уже зроблено')
    # errorlog.write_info('error','Помилка')
    # errorlog.write_info('asfd','Хз')
