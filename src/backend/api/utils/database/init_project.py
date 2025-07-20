# External modules
import mariadb
import importlib
from datetime import datetime
from fastapi.responses import JSONResponse

# Internal modules
from backend.api.config import configmodel
import backend.api.models as models
import backend.api.utils as utils

importlib.reload(configmodel)
importlib.reload(models)
importlib.reload(utils)


async def initProjekt(config: configmodel.ConfigModel) -> dict:
    """
        Initializes a WideFork starting project by creating a user, an api_key, a GL entry and a mapping table.

        Parameters:
            -- config(object): the config object to be used            

        Returns:
            -- response(dictionary): a response dictionary with a bool response or with a JSON response object
    """    
    
    UTIL_NAME = "Initialize Project"

    # Database connection defaults to None
    conn = None

    try:

        table_users = models.ModelMasterDataTable(
            table_name = "init",
            table_type = "Users"
        )      

        table_api_keys = models.ModelMasterDataTable(
            table_name = "init",
            table_type = "Api keys"
        )

        table_mapping = models.ModelMasterDataTable(
            table_name = "",
            table_type = "Mapping table"
        )

        await utils.createMasterDataTable(
            config=config,
            table=table_users
        )

        await utils.createMasterDataTable(
            config=config,
            table=table_api_keys
        )

        await utils.addUser(    
            config=config,
            table_name="init",
            username="admin",
            email="test.email@email.com",
            role="A"
        )

        await utils.addAPIKey(    
            config=config,
            table_name="init",
            username="admin"
        )    

        message_success = f"WideFork Project initialized."
        
        return {
            "result": True,
            "message": message_success,            
            "json": JSONResponse(
                status_code=201,                        
                content= (
                    models.ModelResponse(
                    datetime=str(datetime.now()),
                    module=UTIL_NAME,
                    type=models.ResponseType.ok,
                    message=message_success,                    
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
                    models.ModelResponse(
                    datetime=str(datetime.now()),
                    module=UTIL_NAME,
                    type=models.ResponseType.general_exception,
                    message=f"An error has occured during project initialization.",
                    error=str(e)
                    ).model_dump()
                )          
            )            
        }
    
    finally:
        if (conn is not None) and (conn): conn.close()