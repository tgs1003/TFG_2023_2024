import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True) # read local .env file

class BaseConfig:
    BCRYPT_LOG_ROUNDS=13
    #Esto habría que configurarlo por entorno (¿en el fichero .env?)
    SECRET_KEY = os.environ.get("SECRET_KEY","ubu_supersecreto") 
    ACCESS_TOKEN_EXPIRATION = 900  # 15 minutos
    REFRESH_TOKEN_EXPIRATION = 2592000  # 30 días
    USE_AUTHORIZATION = True

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/psdb_dev")

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/psdb_test")
    ACCESS_TOKEN_EXPIRATION = 3
    REFRESH_TOKEN_EXPIRATION = 3
    USE_AUTHORIZATION = False

    
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/psdb_prod")