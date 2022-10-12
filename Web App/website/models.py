from . import get_db_conn
from flask_login import UserMixin

conn = get_db_conn()
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                'username varchar (50) NOT NULL,'
                                'password varchar (50) NOT NULL);'
)

cur.execute('INSERT INTO users (username, password)'
            'VALUES (%s, %s)',
            ('DKULIS','258369147')
)

conn.commit()

cur.close()
conn.close()




