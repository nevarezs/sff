"""Smartphone Framework Forensics
    Functions to interact with sqlite databases.
    Copyright (C) 2017  Sergio A. Nevarez

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# DB-API 2.0 interface for SQLite databases
# https://docs.python.org/2/library/sqlite3.html
import sqlite3

def _connect(db_path):
    """Connect to sqlite database.

    Args:
      db_path: Path to the sqlite database.
    """
    conn = sqlite3.connect(db_path)
    return conn

def _disconnect(conn):
    """Disconnect from sqlite database."""
    conn.close()

def query(db_path, q, params = None):
    """Run a query on a sqlite database and return the results.

    Args:
      db_path: Path to the sqlite database.
      q: Query to run.
    """
    conn = _connect(db_path)
    c = conn.cursor()
    if (params is None):
        c.execute(q)
    else:
        c.execute(q, params)
    rows = c.fetchall()
    _disconnect(conn)
    return rows
