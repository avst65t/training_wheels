# from pydantic_settings import BaseSettings
# from pydantic import Field

from dotenv import load_dotenv
import logging
import os
from pymongo import MongoClient

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")
mongo_client = MongoClient(MONGODB_URL) 
db = mongo_client[DATABASE_NAME]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# class Settings(BaseSettings):
#     mongodb_uri: str = Field(..., alias="MONGO_URI")
#     jwt_secret: str = Field(..., alias="JWTSECRET")
#     jwt_algorithm: str = "HS256"

#     class Config:
#         extra = "forbid"
#         populate_by_name = True  # allows use of both alias and field name

# settings = Settings()
