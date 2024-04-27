#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    print("Reinitializing DB")
    storage = DBStorage()
    print(storage)
    print("DB reinitialized")
else:
    from models.engine.file_storage import FileStorage
    print("Reinitializing file storage")
    storage = FileStorage()
storage.reload()
