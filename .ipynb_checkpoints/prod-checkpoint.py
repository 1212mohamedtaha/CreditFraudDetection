import time 
import string 
import json 
import random 
from datetime import datetime
from kafka import KafkaProducer
import pandas as pd
import numpy as np


TOPIC = 'top1'



# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

def generate_message(df) -> dict:
    return {
        'V1': df['V1'],
        'V2': df['V2'],
        'V3': df['V3'],
        'V4': df['V4'],
        'V5': df['V5'],
        'V6': df['V6'],
        'V7': df['V7'],
        'V8': df['V8'],
        'V9': df['V9'],
        'V10': df['V10'],
        'V11': df['V11'],
        'V12': df['V12'],
        'V13': df['V13'],
        'V14': df['V14'],
        'V15': df['V15'],
        'V16': df['V16'],
        'V17': df['V17'],
        'V18': df['V18'],
        'V19': df['V19'],
        'V20': df['V20'],
        'V21': df['V21'],
        'V22': df['V22'],
        'V23': df['V23'],
        'V24': df['V24'],
        'V25': df['V25'],
        'V26': df['V26'],
        'V27': df['V27'],
        'V28': df['V28'],
        'Log_Amount': df['Log_Amount'],
}

if __name__ == '__main__':
    df = pd.read_csv('/data/test.csv')
    X = df.drop(columns=['Class'])
    # while True:
        
    for i in range(len(X)):
            
        message = generate_message(X.iloc[i, :])
        print(f'Producing message @ {datetime.now()} | Message = {str(message)}')
        
        producer.send(TOPIC, message)
        # Sleep for a random number of seconds
        time_to_sleep = random.randint(1, 2)
        time.sleep(time_to_sleep)