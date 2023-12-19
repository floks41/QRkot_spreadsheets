"""Модуль класса CharitySheetsSettings."""


import string
from datetime import datetime

from app.core.frequently_used_values import FrequentlyUsedValues as number


class CharitySheetsSettings:
    """Класс настроек таблицы google sheets для записи данных
    о закрытых проектах и времени сбора средств.
    Содержит атрибуты с данными о наименовании и версии
    api google sheets, api google drive для сохранения таблицы,
    структуры данных и методы их подготовки для создания таблицы
    и измнения данных ячеек.
    """
    # Приватные константы
    __TABLE_UPDATE_BODY_TEMPLATE = {
        'majorDimension': 'ROWS',
        'values': [],
    }
    __TABLE_HEADER_TEMPLATE = [
        ['Отчёт от', ''],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
    ]
    # Приватные аттрибуты
    __table_row_count = number.THOUSAND
    __table_column_count = number.THREE
    # Константы
    DATE_TIME_FORMAT: str = '%Y/%m/%d %H:%M:%S'
    SHEETS_API: dict = {
        'api_name': 'sheets',
        'api_version': 'v4',
    }
    DRIVE_API: dict = {
        'api_name': 'drive',
        'api_version': 'v3',
    }
    VALUE_INPUT_OPTION: str = 'USER_ENTERED'

    def __get_now_date_time(self) -> str:
        """Возвращает строковое значение текущих даты и времени."""
        return datetime.now().strftime(self.DATE_TIME_FORMAT)

    @property
    def table_header(self):
        """Возвращает заголовок для таблицы
        с данными о закрытых проектах."""
        header = self.__TABLE_HEADER_TEMPLATE
        header[number.ZERO][number.ONE] = self.__get_now_date_time()
        return header

    @property
    def spreadsheet_body(self) -> dict:
        """Возвращает словарь настроек для создания таблицы с данными
        о закрытых проектах."""
        return {
            'properties': {
                'title': f'Отчёт от {self.__get_now_date_time()}',
                'locale': 'ru_RU',
            },
            'sheets': [
                {
                    'properties': {
                        'sheetType': 'GRID',
                        'sheetId': number.ZERO,
                        'title': 'Лист1',
                        'gridProperties': {
                            'rowCount': self.table_row_count,
                            'columnCount': self.table_column_count,
                        },
                    }
                }
            ],
        }

    @property
    def table_range(self) -> str:
        """Формирует строку диапазона ячеек в формате A1:B2."""
        column_letter = dict(enumerate(string.ascii_uppercase, 1)).get(
            self.table_column_count
        )
        return f'A1:{column_letter}{self.table_row_count}'

    def set_table_row_count(self, table_data_row_count: int) -> None:
        """Устанавливает количество строк для таблицы с данными
        о закрытых проектах. К количеству строк данных (передается
        в аргументе table_data_row_count) прибавляется количество
        строк в шаблоке заголовка таблицы."""
        self.__table_row_count = (
            len(self.__TABLE_HEADER_TEMPLATE) + table_data_row_count
        )

    @property
    def table_row_count(self) -> int:
        """Возвращает количество строк для таблицы."""
        return self.__table_row_count

    @property
    def table_column_count(self) -> int:
        """Возвращает количество колонок для таблицы."""
        return self.__table_column_count

    @property
    def table_update_body_template(self) -> dict:
        """Возвращает словарь - шаблон с настройками для обновления
        данных в таблице."""
        return self.__TABLE_UPDATE_BODY_TEMPLATE


sheets_settings = CharitySheetsSettings()
