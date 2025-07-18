# External modules
from enum import Enum

class SQLCommandType(str, Enum):
    data_query = "SELECT type SQL command"
    data_manipulation = "UPDATE, INSERT, DELETE and CREATE type SQL commands"    