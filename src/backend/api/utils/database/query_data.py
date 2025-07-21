# External modules
import importlib

# Internal modules
from backend.api.config import configmodel
from backend.api.models import model_table
from backend.api.models import model_response
from backend.api.utils.database import execute_sql

importlib.reload(configmodel)
importlib.reload(model_table)
importlib.reload(model_response)
importlib.reload(execute_sql)


async def queryData(config: configmodel.ConfigModel, table_name: str) -> object:
    """
        Queries a WideFork Transaction or Master table.

        Parameters:
            -- config(object): the config object to be used
            -- table_name(str): the table name to be queried

        Returns:
            -- response(pandas dataframe): a response dictionary with a bool response or with a JSON response object
    """

    UTIL_NAME = "Query Database table"    
    
    SQL_COMMAND = f"""        
        SELECT * FROM {config.db_database}.{table_name};        
    """    

    res = await execute_sql.ExecuteSQLCommand(
        config=config,
        util=UTIL_NAME,
        table_name=table_name,
        sql_command=SQL_COMMAND,
        sql_command_type="data_query"
    )

    return res