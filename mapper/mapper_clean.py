#!/usr/bin/env python3
"""
Hadoop Streaming Mapper for NYC Taxi Trip Data
Validates, cleans, and deduplicates records
"""

import sys
import hashlib
from datetime import datetime

# ============ CONFIGURATION ============
HEADER_PREFIX = "VendorID"
EXPECTED_FIELDS = 20
CRITICAL_FIELDS = [1, 2, 3, 4, 10]  # pickup, dropoff, passengers, distance, fare

# Validation thresholds
PASSENGER_MIN, PASSENGER_MAX = 1, 6
DISTANCE_MIN, DISTANCE_MAX = 0.1, 100
FARE_MIN, FARE_MAX = 0.01, 500
DURATION_MIN, DURATION_MAX = 0.5, 300

# ============ HELPER FUNCTIONS ============
def counter(group, name, amount=1):
    """Emit Hadoop counter for monitoring"""
    sys.stderr.write(f"reporter:counter:{group},{name},{amount}\n")

def is_header(line):
    """Check if line is a CSV header"""
    return not line or line.startswith(HEADER_PREFIX)

def parse_fields(line):
    """Parse CSV line into fields"""
    fields = line.split(",")
    
    if len(fields) != EXPECTED_FIELDS:
        counter("Anomalies", "MalformedRow")
        return None
    
    # Check for missing critical values
    if any(fields[i].strip() == "" for i in CRITICAL_FIELDS):
        counter("Anomalies", "MissingValue")
        return None
    
    return fields

def extract_metrics(fields):
    """Extract and validate core metrics from fields"""
    try:
        metrics = {
            'passenger_count': float(fields[3]),
            'trip_distance': float(fields[4]),
            'pickup_dt': datetime.strptime(fields[1], "%Y-%m-%d %H:%M:%S"),
            'dropoff_dt': datetime.strptime(fields[2], "%Y-%m-%d %H:%M:%S"),
            'fare_amount': float(fields[10])
        }
        
        # Calculate duration
        metrics['duration_min'] = (
            metrics['dropoff_dt'] - metrics['pickup_dt']
        ).total_seconds() / 60.0
        
        return metrics, None
        
    except (ValueError, IndexError) as e:
        return None, str(e)

def validate_metrics(metrics):
    """Validate all business rules"""
    errors = []
    
    # Passenger count
    if not (PASSENGER_MIN <= metrics['passenger_count'] <= PASSENGER_MAX):
        errors.append("InvalidPassengerCount")
    
    # Trip distance
    if not (DISTANCE_MIN <= metrics['trip_distance'] <= DISTANCE_MAX):
        errors.append("InvalidDistance")
    
    # Fare amount
    if not (FARE_MIN <= metrics['fare_amount'] <= FARE_MAX):
        errors.append("InvalidFare")
    
    # Duration
    if not (DURATION_MIN <= metrics['duration_min'] <= DURATION_MAX):
        errors.append("InvalidDuration")
    
    # Timestamp order
    if metrics['dropoff_dt'] <= metrics['pickup_dt']:
        errors.append("BadTimestampOrder")
    
    return errors

def process_record(line):
    """
    Process a single record line
    Returns: (is_valid, output_line, error_type)
    """
    # Skip empty lines and headers
    if is_header(line):
        return False, None, "Header"
    
    # Parse fields
    fields = parse_fields(line)
    if fields is None:
        return False, None, "ParseError"
    
    # Extract metrics
    metrics, error = extract_metrics(fields)
    if metrics is None:
        counter("Anomalies", "ParseError")
        return False, None, "ParseError"
    
    # Validate metrics
    errors = validate_metrics(metrics)
    
    # Track processing
    counter("Records", "TotalProcessed")
    
    # Handle invalid records
    if errors:
        for error in errors:
            counter("Anomalies", error)
        counter("Records", "TotalInvalid")
        return False, None, errors[0]
    
    # Generate deduplication hash
    row_hash = hashlib.sha256(line.encode()).hexdigest()[:16]
    output = f"{row_hash}\t{line}"
    
    return True, output, None

# ============ MAIN EXECUTION ============
def main():
    """Main mapper function"""
    processed = 0
    valid = 0
    invalid = 0
    
    for line in sys.stdin:
        line = line.strip()
        is_valid, output, error = process_record(line)
        
        if is_valid:
            print(output)
            valid += 1
        elif error not in ["Header"]:
            invalid += 1
        
        processed += 1
    
    # Emit final statistics
    sys.stderr.write(f"Processed: {processed} | Valid: {valid} | Invalid: {invalid}\n")

if __name__ == "__main__":
    main()
