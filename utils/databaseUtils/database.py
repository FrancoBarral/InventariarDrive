import sqlite3
import os

def get_db_connection():
    ''' 
    
    Connection to the database
    
    '''
    db_file = os.getenv('DB_FILE', 'database/drive_inventory.db')
    conn = sqlite3.connect(db_file)

    conn.row_factory = sqlite3.Row

    return conn

def setup_db():
    '''

    Create the tables in the database if not exist in the database.

    '''
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS files (
        id TEXT PRIMARY KEY,
        name TEXT,
        mimeType TEXT,
        owner TEXT,
        visibility TEXT,
        modifiedTime TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS public_files_history (
        id TEXT,
        name TEXT,
        mimeType TEXT,
        owner TEXT,
        visibility TEXT,
        modifiedTime TEXT,
        PRIMARY KEY (id, modifiedTime)
    )''')
    conn.commit()
    cursor.close()
    conn.close()

def insert_or_update_file(file_data):
    '''
    
    Insert o update files in the database. We receive a dict with the data.

    '''
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for file_data in file_data:
        cursor.execute('''INSERT OR REPLACE INTO files (id, name, mimeType, owner, visibility, modifiedTime)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (file_data['id'], file_data['name'], file_data['mimeType'], file_data['owner'], file_data['visibility'], file_data['modifiedTime']))
    
    conn.commit()
    cursor.close()
    conn.close()

def get_data_files():
    '''
    
    We get the data files in the database and return a list of dicts.

    '''
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM files')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    files = []
    columns = [column[0] for column in cursor.description]  # Obtener los nombres de las columnas
    for row in rows:
        file_data = dict(zip(columns, row))
        files.append(file_data)
    
    return files

def get_data_history():
    '''
    
    We get the data history changes files in the database and return a list of dicts.

    '''
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM public_files_history')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    files = []
    columns = [column[0] for column in cursor.description] 
    for row in rows:
        file_data = dict(zip(columns, row))
        files.append(file_data)
    
    return files

def log_public_file(file_data):
    '''
    
    Insert o update files history in the database. We receive a dict with the data.

    '''
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO public_files_history (id, name, mimeType, owner, visibility, modifiedTime)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (file_data['id'], file_data['name'], file_data['mimeType'], file_data['owners'], file_data['visibility'], file_data['modifiedTime']))
    conn.commit()
    cursor.close()
    conn.close()