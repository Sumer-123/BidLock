from fastapi import APIRouter, HTTPException
from ingestion.schemas.models import Bid
from confluent_kafka import Producer
import json

router = APIRouter()

# Kafka Configuration
conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)


def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


@router.post("/place_bid")
def place_bid(bid: Bid):
    try:
        # Convert bid to JSON string
        bid_data = bid.model_dump_json()

        # Send to Kafka topic 'bids'
        # We use job_id as the key to ensure ordering per job
        producer.produce(
            'bids',
            key=bid.job_id,
            value=bid_data,
            callback=delivery_report
        )
        producer.poll(0)  # Trigger the callback

        return {"status": "success", "message": "Bid placed successfully", "data": bid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))