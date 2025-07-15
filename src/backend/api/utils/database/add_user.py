# External modules
import mariadb
import importlib
from datetime import datetime
from fastapi.responses import JSONResponse

# Internal modules
from backend.api.config import configmodel
from backend.api.postmodels import model_table
from backend.api.responsemodels import model_response
importlib.reload(configmodel)
importlib.reload(model_table)
importlib.reload(model_response)


async def addUser(config: configmodel.ConfigModel, table_name: str, username: str, email: str = "", role: str = "V"):
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
    
    SQL_ADD_USER = f"""
        INSERT INTO {config.db_database}.{table_name}
        VALUES ({username}, {email}, {role});
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

        cur.execute(SQL_ADD_USER)

        message = f"User added. Table name: {table_name}, User name: {username}"

        return {
            "result": True,
            "message": message,            
            "json": JSONResponse(
                status_code=201,
                content= (
                    model_response.ModelResponse(
                    datetime=str(datetime.now()),
                    module=UTIL_NAME,
                    type=model_response.ResponseType.ok,
                    message=message,                    
                    ).model_dump()
                )          
            )                        
        }        
    
    except mariadb.Error as e_mariadb:
        print(f"[ERROR] A MariaDB error has occured - Process: [{UTIL_NAME}] | Error: {e_mariadb}")        

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
                    module=UTIL_NAME,
                    type=model_response.ResponseType.mariadb_error,
                    message=f"An error has occured during cration of a table: {table_name}",
                    error=str(e_mariadb)
                    ).model_dump()
                )          
            )                        
        }        

    except Exception as e:        
        print(f"[ERROR] An error has occured - Process: [{UTIL_NAME}] | Error: {e}")        

        return {
            "result": False, 
            "message": e,
            "json": JSONResponse(
                status_code=500,
                content= (
                    model_response.ModelResponse(
                    datetime=str(datetime.now()),
                    module=UTIL_NAME,
                    type=model_response.ResponseType.general_exception,
                    message=f"An error has occured during cration of a table: {table_name}",
                    error=str(e)
                    ).model_dump()
                )          
            )            
        }
    
    finally:
        if (conn is not None) and (conn): conn.close()