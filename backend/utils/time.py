from datetime import datetime

def datetime_to_epoch(dt: datetime) -> int:
    # Convert datetime to epoch in seconds (BigInteger)
    return int(dt.timestamp()) 