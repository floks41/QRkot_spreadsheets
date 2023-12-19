"""Модуль функций для работы с api google drive и google sheets."""


from datetime import timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.charity_sheets import sheets_settings
from app.core.frequently_used_values import FrequentlyUsedValues as word


def get_table_update_body(table_values: list) -> dict:
    """Формирует словарь c настройками и данными для обновления таблицы.
    Шаблон настроек хранится в
    app.core.app.core.charity_sheets.sheets_settings.
    Аргумент table_values: list - список строк (списков по ячейкам)
    данных для записи."""
    table_update_body = sheets_settings.table_update_body_template
    table_update_body[word.VALUES] = table_values
    return table_update_body


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создает пустую таблицу google sheets на google drive.
    Использует настройки из app.core.app.core.charity_sheets.sheets_settings.
    """
    service = await wrapper_services.discover(**sheets_settings.SHEETS_API)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=sheets_settings.spreadsheet_body)
    )
    spreadsheet_id = response[word.SPREADSHEET_ID]
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    """Назначение прав доступа таблице на гугл-диске."""
    service = await wrapper_services.discover(**sheets_settings.DRIVE_API)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=settings.permissions_body,
            fields=word.ID,
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str, projects: list, wrapper_services: Aiogoogle
) -> None:
    """Заполняет таблицу spreadsheet_id данными из списка projects,
    формирует время сбора средст для каждого проекта."""
    service = await wrapper_services.discover(**sheets_settings.SHEETS_API)
    table_values = sheets_settings.table_header

    for project in projects:
        new_row = [
            str(project[word.NAME]),
            str(
                timedelta(
                    seconds=project[settings.FUNDRAISING_TIME_FIELD_NAME]
                )
            ),
            str(project[word.DESCRIPTION]),
        ]
        table_values.append(new_row)

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=sheets_settings.table_range,
            valueInputOption=sheets_settings.VALUE_INPUT_OPTION,
            json=get_table_update_body(table_values),
        )
    )
