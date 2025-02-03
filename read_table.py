import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import env


def edit_date_str(date):
    date_day, date_month = date.split('.')
    if date_day[0] == '0':
        date_day = date_day[1:]
    if date_month[0] == '0':
        date_month = date_month[1:]
    return f'{date_day}.{date_month}'


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
    today = edit_date_str(today)
    for row in data:
        table_date = edit_date_str(str(row['ДР']))
        if table_date == today:
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
