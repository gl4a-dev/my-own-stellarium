from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str 
    DB_HOST: str
    DB_NAME: str 

    model_config = SettingsConfigDict(env_file="../.env")

    def get_neonsql_link(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}?sslmode=require&channel_binding=require"
    
settings = Settings()

if __name__ == "__main__":
    print(settings.get_neonsql_link())