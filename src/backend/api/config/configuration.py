from config import configmodel

import importlib

importlib.reload(configmodel)


# An actual configuration
Config = configmodel.ConfigModel(
    db_host="widefork-mariadb",
    db_port=3310,
    db_user="root",
    db_root_pw="admin"
)