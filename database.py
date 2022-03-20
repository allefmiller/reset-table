from os import system
import pymssql

settings = open('settings.txt', 'r', encoding='utf8')

system_params = [param[param.index('=')+1:].rstrip('\n') for param in settings.readlines()]
host,database,username,password,TABLE_ONE,TABLE_TWO = system_params

def connect_database():
    conn = pymssql.connect(server=host, user=username, password=password, database=database)
    cursor = conn.cursor()
    return cursor,conn

def close_connection(cursor,conn):
    cursor.close()
    conn.close()

def execute_sql(query):
    try: 
        cursor,conn = connect_database()
        cursor.execute(query)
        row_affected = cursor.rowcount
        conn.commit()
        return {"status": 0 , "message": row_affected}
    except Exception as error:
        return {"status":-1 , "message": str(error)}
    finally:
        close_connection(cursor,conn)

def verify_table_exists(table):
    try: 
        cursor,conn = connect_database()
        query = f"""
            IF OBJECT_ID (N'{table}', N'U') IS NOT NULL
            BEGIN
                SELECT 1 AS result;
            END 
            ELSE
            BEGIN 
                SELECT 0 AS result;
            END
        """
        cursor.execute(query)
        records = cursor.fetchall()
        results = list()
        columns_name = [column[0] for column in cursor.description]
        for record in records:
            results.append( dict( zip( columns_name , record ) ) )

        if results[0]['result'] == 1:
            return {"status":1, "message": "Tabela existe em banco"}
        elif results[0]['result'] == 0:
            return {"status":0, "message": "Tabela não existe em banco"}

    except Exception as error:
        return {"status":-1 , "message": str(error)}
    finally:
        close_connection(cursor,conn)
