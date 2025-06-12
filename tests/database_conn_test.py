# import psycopg2
# import os
# from dotenv import load_dotenv

# # Ladda .env om du har DATABASE_URL där
# load_dotenv()

# # Läs DATABASE_URL (ex: postgresql://user:password@host:port/database)
# DATABASE_URL = os.getenv("DATABASE_URL")

# try:
#     # Öppna connection
#     conn = psycopg2.connect(DATABASE_URL)
#     cur = conn.cursor()
    
#     # Kör en enkel fråga
#     cur.execute("SELECT version();")
#     db_version = cur.fetchone()
#     print(f"✅ Connected! Database version: {db_version}")
    
#     # Stäng
#     cur.close()
#     conn.close()

# except Exception as e:
#     print(f"❌ Connection failed: {e}")
