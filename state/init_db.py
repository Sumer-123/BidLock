import psycopg2


def init_postgres():
    try:
        # Connect to Postgres
        conn = psycopg2.connect(
            host="localhost",
            database="bidlock_db",
            user="admin",
            password="password123"
        )
        cur = conn.cursor()

        # Create Table
        create_query = """
        CREATE TABLE IF NOT EXISTS accepted_bids (
            id SERIAL PRIMARY KEY,
            job_id VARCHAR(50),
            freelancer_id VARCHAR(50),
            bid_amount FLOAT,
            proposal_text TEXT,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(create_query)
        conn.commit()
        print("[SUCCESS] Database initialized! Table 'accepted_bids' created.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"[ERROR] initializing DB: {e}")


if __name__ == "__main__":
    init_postgres()