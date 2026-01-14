import streamlit as st
import psycopg2
import pandas as pd
import redis
import time

# --- Configuration ---
st.set_page_config(
    page_title="BidLock Live Monitor",
    page_icon="🔒",
    layout="wide"
)


# --- Connections ---
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="bidlock_db",
        user="admin",
        password="password123"
    )


def get_redis_client():
    return redis.Redis(host='localhost', port=6379, decode_responses=True)


# --- Data Fetching ---
def fetch_data():
    conn = get_db_connection()
    query = "SELECT * FROM accepted_bids ORDER BY processed_at DESC;"
    # Use pandas to read SQL directly into a DataFrame
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def count_active_locks():
    r = get_redis_client()
    # Count keys starting with "lock:"
    return len(r.keys("lock:*"))


# --- Dashboard Layout ---
st.title("🔒 BidLock Ingestion Engine")
st.markdown("### Real-Time Transaction Monitor")

# Create placeholders for live updates
metrics_container = st.empty()
table_container = st.empty()

# --- Live Loop ---
# This loop refreshes the UI every second
while True:
    try:
        # 1. Get Data
        df = fetch_data()
        lock_count = count_active_locks()

        # 2. Render Metrics
        with metrics_container.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("✅ Accepted Bids (Postgres)", len(df))
            col2.metric("🔒 Active Locks (Redis)", lock_count)
            col3.metric("⚡ System Status", "ONLINE", delta_color="normal")

        # 3. Render Table
        with table_container.container():
            st.markdown("#### Latest Accepted Transactions")
            if not df.empty:
                st.dataframe(
                    df,
                    use_container_width=True,
                    column_config={
                        "processed_at": st.column_config.DatetimeColumn(format="D MMM YYYY, h:mm:ss a")
                    }
                )
            else:
                st.info("Waiting for data stream...")

        # 4. Refresh Rate
        time.sleep(1)

    except Exception as e:
        st.error(f"Connection Error: {e}")
        time.sleep(5)