"""Модуль установки настроек проекта."""


from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Класс настроек проекта."""
    # Данные из .env
    app_title: str = 'QRKot'
    description: str = (
        'Приложение для Благотворительного фонда поддержки котиков QRKot'
    )
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'EXTREMELY_SECRET_PHRASE'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    # Данные для подключения к сервисному акканту (из .env)
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None
    # Области применения для google api (из .env)
    spreadsheets_scope: Optional[str] = None
    drive_scope: Optional[str] = None
    # Константы
    FUNDRAISING_TIME_FIELD_NAME: str = 'fundraising_time'

    class Config:
        """Класс конфигурации настроек проекта,
        задается имя файла env."""
        env_file = '.env'

    @property
    def google_api_scopes(self):
        """Возвращает список областей применения для google api."""
        return [self.spreadsheets_scope, self.drive_scope]

    @property
    def google_api_service_account_info(self):
        """Возращает словарь с учётными данными сервисного аккаунта
        google cloud."""
        return {
            'type': self.type,
            'project_id': self.project_id,
            'private_key_id': self.private_key_id,
            'private_key': self.private_key,
            'client_email': self.client_email,
            'client_id': self.client_id,
            'auth_uri': self.auth_uri,
            'token_uri': self.token_uri,
            'auth_provider_x509_cert_url': self.auth_provider_x509_cert_url,
            'client_x509_cert_url': self.client_x509_cert_url,
        }

    @property
    def permissions_body(self):
        """Возвращает словарь разрешений доступа
        для назначения таблице."""
        return {'type': 'user', 'role': 'writer', 'emailAddress': self.email}


settings = Settings()
