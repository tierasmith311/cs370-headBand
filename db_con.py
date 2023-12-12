#Needed for postgres
#import psycopg2 

#Use sqllite
import sqlite3



def get_db():
    #Postgres
    #return psycopg2.connect(host="localhost", dbname="authme" , user="loki", password="4prez")
    return sqlite3.connect("local_data_base")

def get_db_instance():  
    db  = get_db()
    cur  = db.cursor( )

    return db, cur 


def create_accounts_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            firstName TEXT,
            lastName TEXT,
            username TEXT,
            email TEXT,
            password TEXT
        )
    ''')
    conn.commit()


if __name__ == "__main__":
    db, cur = get_db_instance()

    cur.execute("select * from users")
    for r in cur.fetchall():
        print(r)

    cur.execute("create table music ( song_name varchar(255), rating int);")
    db.commit()

