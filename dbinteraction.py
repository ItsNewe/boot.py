import sqlite3
from sqlite3 import Error
import pprint

def dbexec(query, arg=None, f=True, log=False, db="stor"):
    try:
        conn = sqlite3.connect('{}.db'.format(db))
        c = conn.cursor()
        if arg:
            c.execute(query, arg)

        elif(log is True):
            c.execute(f"SELECT token FROM tokens WHERE name = '{query}'")

        else:
            c.execute(query)
        
        if f:
            az = c.fetchone()
            conn.commit()
            conn.close()
            if az is not None and az[0]:
                return(az[0])
            else:
                return None
        conn.commit()
        conn.close()

    except Error as e:
        print(f"\033[91mUne erreur est survenue pendant la gestion de la requête SQL: {e}\033[0m")
        return "err"