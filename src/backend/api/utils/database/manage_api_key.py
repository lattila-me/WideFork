# External modules
import mariadb
import importlib
from datetime import datetime
from fastapi.responses import JSONResponse
import secrets
import hashlib
from datetime import datetime

# Internal modules
from backend.api.config import configmodel
from backend.api.postmodels import model_table
from backend.api.responsemodels import model_response
from backend.api.utils.database import execute_sql

importlib.reload(configmodel)
importlib.reload(model_table)
importlib.reload(model_response)
importlib.reload(execute_sql)   


async def addAPIKey(config: configmodel.ConfigModel, table_name: str, username: str) -> dict:
    """
        Creates an API key for a given user.

        Parameters:
            -- config(object): the config object to be used
            -- table_name(str): the name of the api key table
            -- username(str): the user's name who will have the api key

        Returns:
            -- response(dictionary): a response dictionary with a bool response or with a JSON response object
    """

    UTIL_NAME = "Add apy key"

    table_name = f"api_keys_{table_name}"

    now = str(datetime.now())
    api_key = hashlib.md5(str(secrets.token_hex(10) + now).encode())
    api_key = api_key.hexdigest()
    
    SQL_ADD_API_KEY = f"""
        INSERT INTO {config.db_database}.{table_name}
        VALUES ("{username}", "{api_key}", 1);
    """

    res = await execute_sql.ExecuteSQLCommand(
        config=config,
        util=UTIL_NAME,
        table=table_name,
        sql_command=SQL_ADD_API_KEY
    )

    return res