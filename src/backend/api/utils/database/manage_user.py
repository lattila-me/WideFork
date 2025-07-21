# External modules
import mariadb
import importlib
from datetime import datetime
from fastapi.responses import JSONResponse

# Internal modules
from backend.api.config import configmodel
from backend.api.models import model_table
from backend.api.models import model_response
from backend.api.utils.database import execute_sql

importlib.reload(configmodel)
importlib.reload(model_table)
importlib.reload(model_response)
importlib.reload(execute_sql)


async def addUser(config: configmodel.ConfigModel, table_name: str, username: str, email: str = "", role: str = "V") -> dict:
    """
        Adds a user to the given User table.

        Parameters:
            -- config(object): the config object to be used
            -- table(str): the name of the user table
            -- username(str): the user's name to be added
            -- email(str): the email of the user
            -- role(str): the role of the user (A, V)

        Returns:
            -- response(dictionary): a response dictionary with a bool response or with a JSON response object
    """

    UTIL_NAME = "Add user"

    table_name = f"users_{table_name}"
    
    SQL_ADD_USER = f"""
        INSERT INTO {config.db_database}.{table_name}
        VALUES ("{username}", "{email}", "{role}", 1);
    """   

    res = await execute_sql.ExecuteSQLCommand(
        config=config,
        util=UTIL_NAME,
        table_name=table_name,
        sql_command=SQL_ADD_USER,
        sql_command_type="data_manipulation"  
    )

    return res


async def deactivateUser(config: configmodel.ConfigModel, table_name: str, username: str):
    """
        Makes the given user inactive.

        Parameters:
            -- config(object): the config object to be used
            -- table(str): the name of the user table
            -- username(str): the user's name to be deactivated
        
        Returns:
            -- response(dictionary): a response dictionary with a bool response or with a JSON response object
    """
    UTIL_NAME = "Deactivate user"

    table_name = f"users_{table_name}"
    
    SQL_DEACTIVATE_USER = f"""
        UPDATE {config.db_database}.{table_name}
        SET Active = 0
        WHERE Username = "{username}";
    """   

    res = await execute_sql.ExecuteSQLCommand(
        config=config,
        util=UTIL_NAME,
        table_name=table_name,
        sql_command=SQL_DEACTIVATE_USER,
        sql_command_type="data_manipulation"
    )

    return res
