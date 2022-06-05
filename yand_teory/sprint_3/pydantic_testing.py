from typing import Optional, List
from pydantic import BaseModel
import json

data = {
  "film_work_pg": {
    "dsn": {
      "dbname": "movies_database",
      "user": "postgres",
      "password": 1234,
      "host": "127.0.0.1",
      "port": 5432
    },
    "state_file_path": None,
    "fetch_delay": 0.1,
    "limit": 100,
    "order_field": ["updated_at"],
    "state_field": ["updated_at"],
    "sql_query": "SELECT id, updated_at\n\tFROM content.film_work"
  }
}



with open('config.json', 'w') as outfile:
  json.dump(data, outfile)

print(data['film_work_pg']['dsn']['user'])


class DSNSettings(BaseModel):
    host: str
    port: int
    dbname: str
    password: str
    user: str


class PostgresSettings(BaseModel):
    dsn: DSNSettings
    limit: Optional[int]
    order_field: List[str]
    state_field: List[str]
    fetch_delay: Optional[float]
    state_file_path: Optional[str]
    sql_query: str


class Config(BaseModel):
    film_work_pg: PostgresSettings


config = Config.parse_file('config.json')
# config = Config.parse_file(data)

print(config.film_work_pg.dsn.user)