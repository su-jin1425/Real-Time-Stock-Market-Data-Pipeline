import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, sum as spark_sum, stddev
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType

# Configuration from environment variables
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
POSTGRES_URL = os.getenv("DATABASE_URL", "jdbc:postgresql://db:5432/stock_market_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")

def write_to_postgres(df, epoch_id):
    """
    Write micro-batch to PostgreSQL table `analytics_metrics`
    """
    # Transform to match table schema
    output_df = df.select(
        col("stock_symbol"),
        col("avg_price").alias("moving_average"),
        col("price_stddev").alias("volatility"),
        col("total_volume").alias("trading_volume"),
        col("window.end").alias("created_at")
    )
    
    output_df.write \
        .format("jdbc") \
        .option("url", POSTGRES_URL) \
        .option("dbtable", "analytics_metrics") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

def main():
    spark = SparkSession.builder \
        .appName("StockMarketRealTimeAnalytics") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,org.postgresql:postgresql:42.6.0") \
        .getOrCreate()
        
    spark.sparkContext.setLogLevel("WARN")

    # Define schema for incoming Kafka JSON data
    schema = StructType([
        StructField("stock_symbol", StringType(), True),
        StructField("price", DoubleType(), True),
        StructField("volume", IntegerType(), True),
        StructField("timestamp", TimestampType(), True)
    ])

    # Read stream from Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", "stock_ticks") \
        .option("startingOffsets", "latest") \
        .load()

    # Parse JSON
    parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

    # Watermark and Aggregations (Tumbling Window of 1 minute)
    aggregated_df = parsed_df \
        .withWatermark("timestamp", "1 minute") \
        .groupBy(
            window(col("timestamp"), "1 minute"),
            col("stock_symbol")
        ) \
        .agg(
            avg("price").alias("avg_price"),
            stddev("price").alias("price_stddev"),
            spark_sum("volume").alias("total_volume")
        )

    # Write output to PostgreSQL
    query = aggregated_df \
        .writeStream \
        .outputMode("append") \
        .foreachBatch(write_to_postgres) \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
