# External modules
from pydantic import BaseModel, Field
from enum import Enum

class TransactionTableType(str, Enum):
    gl = "General Ledger table"
    tax = "Tax balance or transactions table"
    ap = "Accounts Payable"
    ar = "Accounts Receivable"
    inventory = "Inventory and transactions"
    fa = "Intangible and Fixed Assets"

class MaterDataTableType(str, Enum):    
    users = "Users"
    api_keys = "Api keys"
    entities = "Reporting entities"
    gl_master = "General ledger master table"
    mapping = "Mapping table"


class ModelTransactionTable(BaseModel):
    table_name: str = Field(description="The name of the table", max_length=100)
    table_type: TransactionTableType = Field(description="Type of the table")

class ModelMasterDataTable(BaseModel):
    table_name: str = Field(description="The name of the table", max_length=100)
    table_type: MaterDataTableType = Field(description="Type of the table")