from pydantic import BaseModel, Field

class ConfigModel(BaseModel):
    """
        The config model for WideFork. By creating different class instances, you may use multiple configurations.
    """

    # Language. Default = English
    lang: str = Field(description="Language", default="en", max_length=2)

    # MariaDB/MySQL server configuration
    db_host: str = Field(description="Database host IP", default="localhost")
    db_port: int = Field(description="Database server port", default=3306)
    db_database: str = Field(description="Database name", default="widefork")    
    db_user: str = Field(description="Database user name", default="root")
    db_pw: str = Field(description="Database password", default="admin")    