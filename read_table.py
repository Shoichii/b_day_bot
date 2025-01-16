import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import env


def get_msg():
    '''Получение сообщения для поздравления'''

    # установка соединения с гугл
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        env.JSON_FILE, scope)
    client = gspread.authorize(credentials)

    # открываем таблицу
    spreadsheet = client.open_by_url(env.SPREADSHEET_URL)
    sheet = spreadsheet.sheet1  # первый лист

    # получаем все данные
    data = sheet.get_all_records()

    # получаем сегодняшнюю дату
    today = datetime.now().strftime('%d.%m')  # Формат, как в таблице (ДД.ММ)

    # проверяем строки на совпадение дат
    # и заполняем список для поздравления
    birthdays_data = []
    for row in data:
        if str(row['ДР']) == today:
            birthdays_data.append(row)

    # если нет совпадений, возвращаем False
    if not birthdays_data:
        return False

    # формирование сообщения
    msg = f'✨🎉 Сегодня Свой день рождения отмечает'
    if len(birthdays_data) > 1:
        msg = msg[:-2] + 'ют'

    # доделываем сообщение
    for person in birthdays_data:
        name = person['ФИО']
        position = person['Должность']
        msg += f'\n\n{position}\n{name}🎂'

    return msg
