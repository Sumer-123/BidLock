import psycopg2
import pandas as pd

def check_data():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="bidlock_db",
            user="admin",
            password="password123"
        )

        print("\n--- 📊 Current Data in 'accepted_bids' Table ---")
        query = "SELECT * FROM accepted_bids;"

        # Use pandas to print it nicely
        df = pd.read_sql(query, conn)
        if df.empty:
            print("⚠️ Table is empty.")
        else:
            print(df.to_string(index=False))
            print("------------------------------------------------")

        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_data()