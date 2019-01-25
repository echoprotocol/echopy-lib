# -*- coding: utf-8 -*-
import os
import sqlite3
import logging

from appdirs import user_data_dir

from .interfaces import StoreInterface

log = logging.getLogger(__name__)
timeformat = "%Y%m%d-%H%M%S"


class SQLiteFile:
    """ This class ensures that the user's data is stored in its OS
        preotected user directory:

        **OSX:**

         * `~/Library/Application Support/<AppName>`

        **Windows:**

         * `C:\\Documents and Settings\\<User>\\Application Data\\Local Settings\\<AppAuthor>\\<AppName>`
         * `C:\\Documents and Settings\\<User>\\Application Data\\<AppAuthor>\\<AppName>`

        **Linux:**

         * `~/.local/share/<AppName>`

         Furthermore, it offers an interface to generated backups
         in the `backups/` directory every now and then.

         .. note:: The file name can be overwritten when providing a keyword
            argument ``profile``.
    """

    def __init__(self, *args, **kwargs):
        appauthor = "Fabian Schuh"
        appname = kwargs.get("appname", "graphene")
        data_dir = kwargs.get("data_dir", user_data_dir(appname, appauthor))

        if "profile" in kwargs:
            self.storageDatabase = "{}.sqlite".format(kwargs["profile"])
        else:
            self.storageDatabase = "{}.sqlite".format(appname)

        self.sqlDataBaseFile = os.path.join(data_dir, self.storageDatabase)

        """ Ensure that the directory in which the data is stored
            exists
        """
        if os.path.isdir(data_dir):  # pragma: no cover
            return
        else:  # pragma: no cover
            os.makedirs(data_dir)


class SQLiteStore(SQLiteFile, StoreInterface):
    """ The SQLiteStore deals with the sqlite3 part of storing data into a
        database file.

        .. note:: This module is limited to two columns and merely stores
            key/value pairs into the sqlite database

        On first launch, the database file as well as the tables are created
        automatically.

        When inheriting from this class, the following three class members must
        be defined:

            * ``__tablename__``: Name of the table
            * ``__key__``: Name of the key column
            * ``__value__``: Name of the value column
    """

    #:
    __tablename__ = None
    __key__ = None
    __value__ = None

    def __init__(self, *args, **kwargs):
        #: Storage
        SQLiteFile.__init__(self, *args, **kwargs)
        StoreInterface.__init__(self, *args, **kwargs)
        if self.__tablename__ is None or self.__key__ is None or self.__value__ is None:
            raise ValueError("Values missing for tablename, key, or value!")
        if not self.exists():  # pragma: no cover
            self.create()

    def _haveKey(self, key):
        """ Is the key `key` available?
        """
        query = (
            "SELECT {} FROM {} WHERE {}=?".format(
                self.__value__, self.__tablename__, self.__key__
            ),
            (key,),
        )
        connection = sqlite3.connect(self.sqlDataBaseFile)
        cursor = connection.cursor()
        cursor.execute(*query)
        return True if cursor.fetchone() else False

    def __setitem__(self, key, value):
        """ Sets an item in the store

            :param str key: Key
            :param str value: Value
        """
        if self._haveKey(key):
            query = (
                "UPDATE {} SET {}=? WHERE {}=?".format(
                    self.__tablename__, self.__value__, self.__key__
                ),
                (value, key),
            )
        else:
            query = (
                "INSERT INTO {} ({}, {}) VALUES (?, ?)".format(
                    self.__tablename__, self.__key__, self.__value__
                ),
                (key, value),
            )
        connection = sqlite3.connect(self.sqlDataBaseFile)
        cursor = connection.cursor()
        cursor.execute(*query)
        connection.commit()

    def __getitem__(self, key):
        """ Gets an item from the store as if it was a dictionary

            :param str value: Value
        """
        query = (
            "SELECT {} FROM {} WHERE {}=?".format(
                self.__value__, self.__tablename__, self.__key__
            ),
            (key,),
        )
        connection = sqlite3.connect(self.sqlDataBaseFile)
        cursor = connection.cursor()
        cursor.execute(*query)
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            if key in self.defaults:
                return self.defaults[key]
            else:
                return None

    def __iter__(self):
        """ Iterates through the store
        """
        return iter(self.keys())

    def keys(self):
        query = "SELECT {} from {}".format(self.__key__, self.__tablename__)
        connection = sqlite3.connect(self.sqlDataBaseFile)
        cursor = connection.cursor()
        cursor.execute(query)
        return [x[0] for x in cursor.fetchall()]

    def __len__(self):
        """ return lenght of store
        """
        query = "SELECT id from {}".format(self.__tablename__)
        connection = sqlite3.connect(self.sqlDataBaseFile)
        cursor = connection.cursor()
        cursor.execute(query)
        return len(cursor.fetchall())

    def __contains__(self, key):
        """ Tests if a key is contained in the store.

            May test againsts self.defaults

            :param str value: Value
        """
        if self._haveKey(key) or key in self.defaults:
            return True
        else:
            return False

    def items(self):
        """ returns all items off the store as tuples
        """
        query = "SELECT {}, {} from {}".format(
            self.__key__, self.__value__, self.__tablename__
        )
        connection = sqlite3.connect(self.sqlDataBaseFile)
        cursor = connection.cursor()
        cursor.execute(query)
        r = []
        for key, value in cursor.fetchall():
            r.append((key, value))
        return r

    def get(self, key, default=None):
        """ Return the key if exists or a default value

            :param str value: Value
            :param str default: Default value if key not present
        """
        if key in self:
            return self.__getitem__(key)
        else:
            return default

    # Specific for this library
    def delete(self, key):
        """ Delete a key from the store

            :param str value: Value
        """
        query = (
            "DELETE FROM {} WHERE {}=?".format(self.__tablename__, self.__key__),
            (key,),
        )
        connection = sqlite3.connect(self.sqlDataBaseFile)
        cursor = connection.cursor()
        cursor.execute(*query)
        connection.commit()

    def wipe(self):
        """ Wipe the store
        """
        query = "DELETE FROM {}".format(self.__tablename__)
        connection = sqlite3.connect(self.sqlDataBaseFile)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

    def exists(self):
        """ Check if the database table exists
        """
        query = (
            "SELECT name FROM sqlite_master " + "WHERE type='table' AND name=?",
            (self.__tablename__,),
        )
        connection = sqlite3.connect(self.sqlDataBaseFile)
        cursor = connection.cursor()
        cursor.execute(*query)
        return True if cursor.fetchone() else False

    def create(self):  # pragma: no cover
        """ Create the new table in the SQLite database
        """
        query = (
            """
            CREATE TABLE {} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {} STRING(256),
                {} STRING(256)
            )"""
        ).format(self.__tablename__, self.__key__, self.__value__)
        connection = sqlite3.connect(self.sqlDataBaseFile)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
