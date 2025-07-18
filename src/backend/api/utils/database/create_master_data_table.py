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


async def createMasterDataTable(config: configmodel.ConfigModel, table: model_table.ModelMasterDataTable) -> dict:
    """
        Creates a WideFork master data table (users, api_keys, mapping etc.).

        Parameters:
            -- config(object): the config object to be used
            -- table(object): the table model to be used

        Returns:
            -- response(dictionary): a response dictionary with a bool response or with a JSON response object
    """

    UTIL_NAME = "Create Mastertable"

    table_type = table.table_type.name
    table_name = f"{table_type}_{table.table_name}"
    
    SQL_USERS = f"""        
        CREATE TABLE {config.db_database}.{table_name} (
            -- Input fields                        
            Username VARCHAR(255) NOT NULL UNIQUE COMMENT "The user's name",
            Email VARCHAR(255) COMMENT "The user's email",
            Role VARCHAR(1) COMMENT "User's role: (A)dmin, (V)iewer",
            Active BOOL COMMENT "Whether the user is active or not",
            -- Constrains
            primary key(Username)
        ) COMMENT = "A table for keeping track of users";
    """

    SQL_ENTITIES = f"""        
        CREATE TABLE {config.db_database}.{table_name} (
            -- Input fields                        
            Entity_code VARCHAR(255) NOT NULL UNIQUE COMMENT "Reporting entity's code",
            Entity_name VARCHAR(255) NOT NULL UNIQUE COMMENT "Reporting entity's code",
            Country VARCHAR(100) COMMENT "The country of origin/official seat",
            City VARCHAR(100) COMMENT "City address",
            Street VARCHAR(255) COMMENT "Street address",
            Zip VARCHAR(100) COMMENT "Zip code",
            Tax_number VARCHAR(100) COMMENT "Tax number of the reporting entity",            
            Comment LONGTEXT COMMENT "Comments for the reporting entity",
            -- Constrains
            primary key(Entity_code)
        ) COMMENT = "A table for keeping track of reporting entities.";
    """

    SQL_API_KEYS = f"""        
        CREATE TABLE {config.db_database}.{table_name} (
            -- Input fields                        
            Username VARCHAR(255) NOT NULL COMMENT "The user's name",
            Api_key VARCHAR(32) NOT NULL UNIQUE COMMENT "API key",
            Valid BOOL COMMENT "Whether the API key is valid or not"          
        ) COMMENT = "A table for keeping track of API keys.";
    """

    # Select the appropriate SQL command
    if (table_type == "users"):
        SQL_COMMAND = SQL_USERS
    elif (table_type == "entities"):
        SQL_COMMAND = SQL_ENTITIES
    elif (table_type == "api_keys"):
        SQL_COMMAND = SQL_API_KEYS

    res = await execute_sql.ExecuteSQLCommand(
        config=config,
        util=UTIL_NAME,
        table=table_name,
        sql_command=SQL_COMMAND
    )

    return res