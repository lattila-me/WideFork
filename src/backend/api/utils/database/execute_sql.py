# External modules
import mariadb
import importlib
from datetime import datetime
from fastapi.responses import JSONResponse

# Internal modules
from backend.api.config import configmodel
from backend.api.models import model_table
from backend.api.models import model_response
importlib.reload(configmodel)
importlib.reload(model_table)
importlib.reload(model_response)


async def ExecuteSQLCommand(config: configmodel.ConfigModel, util: str, table: str, sql_command: str) -> dict:
    """
        Executes a pre-defined SQL command.

        Parameters:
            -- config(object): the config object to be used
            -- util(str): the utility name that is calling the SQL command
            -- table(str): the table name the SQL command refers to
            -- sql_command(str): the SQL command to be executed            

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
        
        cur = conn.cursor()

        cur.execute(sql_command)
        
        conn.commit()

        message = f"SQL Command executed."

        return {
            "result": True,
            "message": message,            
            "json": JSONResponse(
                status_code=201,
                content= (
                    model_response.ModelResponse(
                    datetime=str(datetime.now()),
                    module=util,
                    type=model_response.ResponseType.ok,
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
                content= (
                    model_response.ModelResponse(
                    datetime=str(datetime.now()),
                    module=util,
                    type=model_response.ResponseType.mariadb_error,
                    message=f"An error has occured during SQL exectuion in table: {table}",
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
                content= (
                    model_response.ModelResponse(
                    datetime=str(datetime.now()),
                    module=util,
                    type=model_response.ResponseType.general_exception,
                    message=f"An error has occured during cration of a table: {table}",
                    error=str(e)
                    ).model_dump()
                )          
            )            
        }
    
    finally:
        if (conn is not None) and (conn): conn.close()