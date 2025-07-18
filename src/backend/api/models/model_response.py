# External modules
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class ResponseType(str, Enum):
    ok = "OK"
    mariadb_error = "Mariadb error"
    general_exception = "General exception"
    validation_error = "Validation error"

class ModelResponse(BaseModel):
    datetime: str = Field(description="The date and time of the response", default=str(datetime.now()))
    module: str = Field(description="The utility of module name the response is sent by")
    type: ResponseType = Field(description="The type of the response")
    message: str = Field(description="The response message, if any", default="")
    error: str = Field(description="The error message if any", default="")