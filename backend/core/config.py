from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): #наследственный класс
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8") #model.. - спец имя которое Pydantic  использует для конфигурации модели

    DATABASE_URL: str  #читаем файлы с .evn
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 #ремя сессии

settings = Settings() #экземпляр класса Settings
#теперь импортруется как backend.core.config import settings