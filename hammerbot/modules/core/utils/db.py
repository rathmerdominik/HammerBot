import sqlite3

from typing import List

from .helpers import load_config

from ..types.module import Module
from ..types.config import Config


def create_db_conn() -> sqlite3.Connection:
    """Creates a database connection and returns the connection.
    Also creates a database with the required "module" table in case it does not exist

    Returns:
        sqlite3.Cursor: The created cursor
    """
    config: Config = load_config()

    conn = sqlite3.connect(config.database_path)

    conn.execute(
        "CREATE TABLE IF NOT EXISTS modules (\
            name TEXT PRIMARY KEY, \
            enabled INTEGER\
        )"
    )

    return conn


def get_module(module: str) -> Module:
    """Find a module by its name

    Args:
        module (str): Name of the module to find

    Returns:
        Module: The found Module
        None: When no Module has been found
    """
    conn = create_db_conn()
    conn.row_factory = sqlite3.Row
    try:
        sql = "SELECT name, enabled FROM modules WHERE name = ?"
        res = conn.execute(sql, (module,))

        return Module(**dict(res.fetchone()))
    except TypeError:
        return None


def get_modules(enabled: bool = None) -> List[Module]:
    """Gets all modules from the database or None if there are no entries

    Args:
        enabled (bool, optional): Specifically search for enabled (True) or disabled (False) plugins. Defaults to None.

    Returns:
        List[Module]: List of modules found
        None: If there are no modules
    """
    conn = create_db_conn()
    conn.row_factory = sqlite3.Row

    sql = "SELECT name, enabled FROM modules"

    modules: List[Module] = []
    try:
        match enabled:
            case None:
                modules = [Module(**module) for module in conn.execute(sql)]
            case True:
                modules = [
                    Module(**module)
                    for module in conn.execute(sql)
                    if module["enabled"] == 1
                ]
            case False:
                modules = [
                    Module(**module)
                    for module in conn.execute(sql)
                    if module["enabled"] == 0
                ]

        return modules
    except TypeError:
        return None


def insert_module(module: str, enabled: bool = True):
    """Inserts and updates a module if it exists

    Args:
        module (str): Module name
        enabled (bool, optional): _description_. Defaults to True.
    """
    conn = create_db_conn()

    with conn:
        try:
            sql = "INSERT INTO modules (name, enabled) VALUES (?, ?)"

            conn.execute(sql, (module, enabled))
            conn.commit()
        except sqlite3.IntegrityError:
            sql = "UPDATE modules SET enabled = ? WHERE name = ?"

            conn.execute(sql, (enabled, module))
            conn.commit()
