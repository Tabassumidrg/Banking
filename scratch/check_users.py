import psycopg2
from psycopg2.extras import RealDictCursor
db_url = 'postgresql://neondb_owner:npg_8BTDxaX0Ynfh@ep-falling-art-akb1ael9-pooler.c-3.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
conn = psycopg2.connect(db_url)
cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("SELECT email, role FROM users")
users = cur.fetchall()
for u in users:
    print(u)
conn.close()
