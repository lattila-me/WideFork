# External modules
import mariadb
import importlib
from datetime import datetime
from fastapi.responses import JSONResponse
import pandas as pd

# Internal modules
from backend.api.config import configmodel
import backend.api.models as models

importlib.reload(configmodel)
importlib.reload(models)


async def ExecuteSQLCommand(config: configmodel.ConfigModel, util: str, table_name: str, sql_command: str, sql_command_type: models.SQLCommandType) -> dict:
    """
        Executes a pre-defined SQL command.

        Parameters:
            -- config(object): the config object to be used
            -- util(str): the utility name that is calling the SQL command
            -- table_name(str): the table name the SQL command refers to
            -- sql_command(str): the SQL command to be executed            
            -- sql_command_type(Enum): the SQL command type

        Returns:
            -- response(dictionary): a response dictionary with a bool response or with a JSON response object
    """    
    

    # Database connection defaults to None
    conn = None

    try:
        conn = mariadb.connect(
            host=config.db_host,
            port=config.db_port,            
            database=config.db_database,
            user=config.db_user,
            password=config.db_pw        
        )

        if (sql_command_type.value == "data_query"):
            data = pd.read_sql(sql_command, conn)

            message = f"SQL Command executed."
            
            return {
                "result": True,
                "message": message,            
                "json": JSONResponse(
                    status_code=201,
                    sql_command=sql_command,
                    data=data,
                    content= (
                        models.ModelResponse(
                        datetime=str(datetime.now()),
                        module=util,
                        type=models.ResponseType.ok,
                        message=message,                    
                        ).model_dump()
                    )          
                )
            }
        
        else:                            
            cur = conn.cursor()

            cur.execute(sql_command)
            
            conn.commit()

            message = f"SQL Command executed."

            return {
                "result": True,
                "message": message,            
                "json": JSONResponse(
                    status_code=201,
                    sql_command=sql_command,
                    content= (
                        models.ModelResponse(
                        datetime=str(datetime.now()),
                        module=util,
                        type=models.ResponseType.ok,
                        message=message,                    
                        ).model_dump()
                    )          
                )                        
            }        
    
    except mariadb.Error as e_mariadb:
        print(f"[ERROR] A MariaDB error has occured - Process: [{util}] | Error: {e_mariadb}")        

        # Rollback any changes
        if (conn is not None) and (conn): cur.execute("ROLLBACK")        

        return {
            "result": False,
            "message": e_mariadb,             
            "json": JSONResponse(
                status_code=500,
                sql_command=sql_command,
                content= (
                    models.ModelResponse(
                    datetime=str(datetime.now()),
                    module=util,
                    type=models.ResponseType.mariadb_error,
                    message=f"An error has occured during SQL exectuion in table: {table_name}",
                    error=str(e_mariadb)
                    ).model_dump()
                )          
            )                        
        }        

    except Exception as e:        
        print(f"[ERROR] An error has occured - Process: [{util}] | Error: {e}")        

        return {
            "result": False, 
            "message": e,
            "json": JSONResponse(
                status_code=500,
                sql_command=sql_command,
                content= (
                    models.ModelResponse(
                    datetime=str(datetime.now()),
                    module=util,
                    type=models.ResponseType.general_exception,
                    message=f"An error has occured during cration of a table: {table_name}",
                    error=str(e)
                    ).model_dump()
                )          
            )            
        }
    
    finally:
        if (conn is not None) and (conn): conn.close()