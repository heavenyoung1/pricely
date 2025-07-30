from pydantic_settings import BaseSettings, SettingsConfigDict

class DataBaseSettings(BaseSettings):
    '''Настройки подключения к базе данных'''
    model_config = SettingsConfigDict(
        env_file = '.env', 
        env_prefix='DB_CONFIG_', 
        env_file_encoding = 'utf-8',
        extra="ignore", # Игнорировать лишние переменные

        )

    HOST: str
    PORT: int
    USER: str
    PASS: str
    NAME: str
    CONN: str

    def get_connection_db(self):
        '''Формирует строку подключения для PostgreSQL'''
        connection_str = f'{self.DB_CONN}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        return connection_str
    
