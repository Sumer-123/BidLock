# 🔒 BidLock - Real-Time Auction Ingestion Engine

**BidLock** is a high-concurrency real-time data engineering pipeline designed to ingest, process, and visualize auction bids. It utilizes **Apache Kafka** for high-throughput buffering, **Apache Spark Structured Streaming** for processing, and **Redis** for distributed locking to prevent race conditions (e.g., double-booking or simultaneous wins)

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Spark](https://img.shields.io/badge/Apache_Spark-3.5.0-orange)
![Kafka](https://img.shields.io/badge/Apache_Kafka-7.4.0-black)

## 🏗️ Architecture

The pipeline follows a standard streaming architecture:

1.  **Ingestion Layer:** A **FastAPI** service receives JSON bid payloads from users/clients.
2.  **Message Broker:** Validated bids are pushed to an **Apache Kafka** topic (`bids`) for decoupling and buffering.
3.  **Processing Engine:** **Spark Structured Streaming** consumes the Kafka stream.
    * It checks **Redis** to ensure the specific Job ID is not already "locked" or taken.
    * If valid, it writes the bid to **PostgreSQL**.
4.  **Presentation Layer:** A **Streamlit** dashboard provides a real-time view of accepted bids and system status.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Containerization:** Docker & Docker Compose
* **Ingestion:** FastAPI, Uvicorn
* **Streaming:** Apache Kafka, Zookeeper
* **Processing:** PySpark (Structured Streaming)
* **State Management:** Redis (for distributed locking)
* **Storage:** PostgreSQL
* **Visualization:** Streamlit

## 📂 Project Structure

```text
BidLock/
├── dashboard/          # Streamlit real-time monitoring app
├── docker/             # Docker Compose infrastructure (Kafka, Redis, Postgres)
├── ingestion/          # FastAPI app for receiving bids
├── streaming/          # Spark Structured Streaming logic
├── airflow/            # (Optional) DAGs for batch maintenance
└── requirements.txt    # Python dependencies

