import os
class BaseConfig:
    BCRYPT_LOG_ROUNDS=13
    #Esto habría que configurarlo por entorno (¿en el fichero .env?)
    SECRET_KEY = os.environ.get("SECRET_KEY","ubu_supersecreto") 
    ACCESS_TOKEN_EXPIRATION = 900  # 15 minutos
    REFRESH_TOKEN_EXPIRATION = 2592000  # 30 días

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/psdb_dev")