from .configmodel import ConfigModel

import importlib

importlib.reload(ConfigModel)


# An actual configuration
Config = ConfigModel(
    db_host="widefork-mariadb",
    db_port=3310,
    db_user="root",
    db_root_pw="admin"
)