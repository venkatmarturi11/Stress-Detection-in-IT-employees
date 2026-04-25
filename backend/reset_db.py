import psycopg2

conn = psycopg2.connect('postgresql://neondb_owner:npg_cWTw6thyp8kJ@ep-floral-mouse-a8h06nnr.eastus2.azure.neon.tech/neondb?sslmode=require')
conn.autocommit = True
cur = conn.cursor()

# Get ALL tables including those we might have missed
cur.execute("""
    SELECT tablename FROM pg_tables 
    WHERE schemaname = 'public'
    UNION
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'public';
""")
tables = cur.fetchall()
print(f"Found {len(tables)} items to drop:")

for (t,) in tables:
    try:
        cur.execute(f'DROP TABLE IF EXISTS "{t}" CASCADE;')
        print(f"  Dropped: {t}")
    except Exception as e:
        print(f"  Skip {t}: {e}")

# Also drop any sequences
cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
print("Schema reset complete!")

cur.close()
conn.close()
print('SUCCESS: Database is completely clean.')
