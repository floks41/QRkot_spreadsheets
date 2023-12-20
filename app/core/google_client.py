"""Модуль подключения к google api."""


from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import settings

# Список разрешений.Тест проверяет переменную SCOPES.
SCOPES = settings.google_api_scopes
# Учетные данные сервисного аккаунта. Тест проверяет переменную SCOPES.
INFO = settings.google_api_service_account_info
# Получаем объект учётных данных
creds = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service():
    """Создаёт экземпляр класса Aiogoogle."""
    async with Aiogoogle(service_account_creds=creds) as aiogoogle:
        yield aiogoogle
