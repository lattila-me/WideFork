"""
    WideFork POST MODELS - HTTP POST models for REST API Endpoints
"""
__version__ = "0.1.0"
__date__ = "18-07-2025"
__author__ = "Lantos, Attila"

print("WideFork Models imported.")

from .model_response import ModelResponse, ResponseType
from .model_table import MaterDataTableType, ModelMasterDataTable, ModelTransactionTable
from .model_sql import SQLCommandType