from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from streaming.processors.negotiation import process_bid_batch

# Define Schema
schema = StructType([
    StructField("job_id", StringType()),
    StructField("freelancer_id", StringType()),
    StructField("bid_amount", FloatType()),
    StructField("proposal_text", StringType())
])

def run_spark_job():
    spark = SparkSession.builder \
        .appName("BidLock Streaming") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")
    print(">>> BidLock Engine Started. Waiting for bids...")

    # Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "bids") \
        .option("startingOffsets", "latest") \
        .load()

    # Parse JSON
    parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

    # Use foreachBatch to apply our Custom Logic (Redis Locking)
    query = parsed_df.writeStream \
        .outputMode("append") \
        .foreachBatch(process_bid_batch) \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    run_spark_job()