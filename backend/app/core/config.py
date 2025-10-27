from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    class Config:
        # Renamed 'env_file' to 'case_sensitive' which is required in V2 settings
        # and 'env_file' argument is moved to settings_config.
        # However, for simple use with BaseSettings, keeping env_file usually works,
        # but let's use the explicit V2 configuration method.

        # The correct V2 way to configure the settings environment:
        settings_config = {'env_file': '.env'}
        
        # If your model also serves as an ORM model representation, add this:
        from_attributes = True # This replaces the old 'orm_mode = True'
        
        # NOTE: If your code uses a legacy template, the simplest fix for the warning
        # is often just ensuring `from_attributes = True` is present.
        
# For maximum compatibility and clarity in a modern project:
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    model_config = {
        "env_file": ".env",
        "from_attributes": True  # Equivalent of orm_mode for Pydantic V2
    }

settings = Settings()