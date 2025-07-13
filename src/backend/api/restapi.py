# External modules
from fastapi import FastAPI
from fastapi import status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import importlib

# Internal modules
from config import configmodel
from config import configuration
import postmodels.model_table
import responsemodels.model_response
import utils.database.create_transaction_table

importlib.reload(configmodel)
importlib.reload(configuration)
importlib.reload(postmodels.model_table)
importlib.reload(responsemodels.model_response)
importlib.reload(utils.database.create_transaction_table)


REST_API_DESCRIPTION = """
## Functionality


## Security
The API is secured with an API key and entity code combinaton that must be provided in the requests for the endpoints.
"""

# REST API application
app = FastAPI(
    title="WideFork REST API",
    summary="API for manipulation of the WideFork database, query and analyze data.",
    description=REST_API_DESCRIPTION,    
    version="0.1.0",
    contact={
        "name": "Lantos, Attila",
        "email": "lattila.me@gmail.com"
    },
    openapi_tags=[
        {
            "name": "Healthcheck",
            "description": "Checks the status of the API."
        },
        {
            "name": "Database",
            "description": "Endpoints for manipulating WideFork database tables."
        },
        {
            "name": "Data injection",
            "description": "Upload data to the WideFork database."
        },          
    ]
)

# Allow CORS
app.add_middleware (
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]    
)


# ENDPOINTS

## Helathcheck endpoint
@app.get(
    "/api/healthcheck",
    status_code=status.HTTP_200_OK,
    tags=["Healthcheck"],
    summary="Healthcheck endpoint to verify API status",
)
async def helathCheck():

    return responsemodels.model_response.ModelResponse(
        datetime=datetime.now(),
        module="Healthcheck",
        type=responsemodels.model_response.ResponseType.ok,
        message="REST API is up and running."        
    )    


## DATABASE ENDPOINTS

### Create Table Endpoint
@app.post(
    "/api/createtransactiontable",
    status_code=status.HTTP_201_CREATED,
    tags=["Database"],
    summary="Healthcheck endpoint to verify API status",
)
async def createTransactionTable(config: configmodel.ConfigModel, tablemodel: postmodels.model_table.ModelTable):

    # If config is not provided, set to default
    if (config is None):
        config = configuration.Config
    
    res = await utils.database.create_transaction_table.createTransactionTable(
        config=config,
        table=tablemodel        
    )

    return res["json"]