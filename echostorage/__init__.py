# -*- coding: utf-8 -*-
# Load modules from other classes
from .base import (
    InRamConfigurationStore,
    InRamPlainKeyStore,
    InRamEncryptedKeyStore,
    SqliteConfigurationStore,
    SqlitePlainKeyStore,
    SqliteEncryptedKeyStore,
)
from .sqlite import SQLiteFile

__all__ = ["interfaces", "masterpassword", "base", "sqlite", "ram"]

url = "ws://195.201.164.54:6311/"
InRamConfigurationStore.setdefault("node", url)
SqliteConfigurationStore.setdefault("node", url)


def get_default_config_store(*args, **kwargs):
    """ This method returns the default **configuration** store
        that uses an SQLite database internally.

        :params str appname: The appname that is used internally to distinguish
            different SQLite files
    """
    kwargs["appname"] = kwargs.get("appname", "echo")
    return SqliteConfigurationStore(*args, **kwargs)


def get_default_key_store(config, *args, **kwargs):
    """ This method returns the default **key** store
        that uses an SQLite database internally.

        :params str appname: The appname that is used internally to distinguish
            different SQLite files
    """
    kwargs["appname"] = kwargs.get("appname", "echo")
    return SqliteEncryptedKeyStore(config=config, **kwargs)
