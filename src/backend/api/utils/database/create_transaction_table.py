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


async def createTransactionTable(config: configmodel.ConfigModel, table: model_table.ModelTransactionTable) -> dict:
    """
        Creates a WideFork transaction table (GL, Tax, AP, AR, Inventory).

        Parameters:
            -- config(object): the config object to be used
            -- table(object): the table model to be used

        Returns:
            -- response(dictionary): a response dictionary with a bool response or with a JSON response object
    """

    UTIL_NAME = "Create Database table"

    table_type = table.table_type.name
    table_name = f"{table_type}_{table.table_name}"
    
    SQL_GL = f"""        
        CREATE TABLE {config.db_database}.{table_name} (
            -- Input fields            
            Id INT NOT NULL AUTO_INCREMENT,
            Entity VARCHAR(255) NOT NULL COMMENT "The business unit/entity name",
            Date DATETIME NOT NULL COMMENT "The date of the transaction",
            VAT_date DATETIME COMMENT "The VAT fulfillment/effective date if differs from the date of the transaction",            
            Due_date DATETIME COMMENT "The due date of the transaction/invoice if any",
            Partner VARCHAR(255) COMMENT "Partner name, if any",
            Description VARCHAR (255) COMMENT "A textual description of the transaction",
            Journal VARCHAR (255) COMMENT "The code/name of the journal the transaction is booked into",
            GL_account VARCHAR(100) NOT NULL COMMENT "The GL account number/code the transacation is affected by",
            Counter_GL_account VARCHAR(100) COMMENT "The counter GL account number/code the transacation is affected by",
            VAT_code VARCHAR(100) COMMENT "VAT identification for the transaction, if any",
            Currency_ISO VARCHAR(3) COMMENT "Currency ISO code. If blank, the default currency will be used",
            Credit FLOAT COMMENT "Credit value of the transaction",
            Debit FLOAT COMMENT "Debit value of the transaction",            
            Amount FLOAT NOT NULL COMMENT "The transaction's value",
            VAT_amount FLOAT COMMENT "The VAT amount, if any",            
            Marker1 VARCHAR(100) COMMENT "Custom marking like cost center or business unit etc.",
            Marker2 VARCHAR(100) COMMENT "Custom marking like cost center or business unit etc.",
            Marker3 VARCHAR(100) COMMENT "Custom marking like cost center or business unit etc.",
            Marker4 VARCHAR(100) COMMENT "Custom marking like cost center or business unit etc.",            
            -- Calculated fields
            Amount_abs FLOAT COMMENT "The absolute value of the transaction. It serves risk assessment",            
            Z_point FLOAT CHECK (Z_point >= 0) COMMENT "The Z-score of the given transaction. It serves anomaly detection purposes.",
            -- Constrains
            primary key(Id)
        ) COMMENT = "A table for GL transactions";
    """

    SQL_TAX = f"""         
        CREATE TABLE {config.db_database}.{table_name} (
            -- Input fields
            Id INT NOT NULL auto_increment,
            Entity VARCHAR (255) NOT NULL COMMENT "The business unit/entity name",
            Date DATETIME NOT NULL COMMENT "The date of the transaction/balance",
            Tax_name VARCHAR(255) NOT NULL COMMENT "The description, type etc. of the tax",
            Description VARCHAR (255) COMMENT "A textual description of the transaction",
            Currency_ISO VARCHAR(3) COMMENT "Currency ISO code. If blank, the default currency will be used",
            Amount FLOAT NOT NULL COMMENT "The transaction's value",
            Marker1 VARCHAR(100) COMMENT "Custom marking like cost center or business unit etc.",
            Marker2 VARCHAR(100) COMMENT "Custom marking like cost center or business unit etc.",
            Marker3 VARCHAR(100) COMMENT "Custom marking like cost center or business unit etc.",
            Marker4 VARCHAR(100) COMMENT "Custom marking like cost center or business unit etc.",            
            -- Constrains
            CONSTRAINT PK_ID PRIMARY KEY (ID)
        ) COMMENT = "A table for keeping track of tax balances and/or tax transacations";
    """

    # Select the appropriate SQL command
    if (table_type == "gl"):
        SQL_COMMAND = SQL_GL
    elif (table_type == "tax"):
        SQL_COMMAND = SQL_TAX

    res = await execute_sql.ExecuteSQLCommand(
        config=config,
        util=UTIL_NAME,
        table=table_name,
        sql_command=SQL_COMMAND
    )

    return res