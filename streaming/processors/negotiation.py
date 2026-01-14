import psycopg2
from state.locking import acquire_lock


def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="bidlock_db",
        user="admin",
        password="password123"
    )


def process_bid_batch(df, epoch_id):
    bids = df.collect()

    if not bids:
        return

    print(f"--- Processing Batch {epoch_id} with {len(bids)} bids ---")

    # Open DB Connection once per batch
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        for row in bids:
            job_id = row['job_id']
            freelancer = row['freelancer_id']
            amount = row['bid_amount']
            text = row['proposal_text']

            # 1. Try to acquire Redis Lock
            if acquire_lock(job_id, freelancer):
                print(f"[SUCCESS] Lock acquired for {job_id} by {freelancer}. Writing to DB...")

                # 2. If Success, Write to Postgres
                insert_query = """
                    INSERT INTO accepted_bids (job_id, freelancer_id, bid_amount, proposal_text)
                    VALUES (%s, %s, %s, %s)
                """
                cur.execute(insert_query, (job_id, freelancer, amount, text))
                conn.commit()

            else:
                print(f"[REJECTED] Job {job_id} is currently locked. Dropping bid.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"[ERROR] Database Write Failed: {e}")