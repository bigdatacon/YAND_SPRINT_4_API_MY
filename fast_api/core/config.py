import os
from logging import config as logging_config

# importing sys
import sys

# adding Folder_2/subfolder to the system path
sys.path.insert(0, '/Users/Пользователь/PycharmProjects/2.2.YAND_SPRINT_2_NEW_MODELS/fast_api/core')

# from core.logger import LOGGING
from core.logger import LOGGING
# from ..core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

# Настройки Redis
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Настройки Elasticsearch
ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
