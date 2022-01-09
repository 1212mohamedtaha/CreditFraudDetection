import json 
import random 
import time 

from kafka import KafkaConsumer
import numpy as np
import pandas as pd
print('start consumer')

import psycopg2
from psycopg2.extras import execute_values

import pickle
from keras.models import load_model


# Constants

TOPIC = 'top1'
BATCH_SIZE = 5

DATABASE_CONFIG = {
"database": "postgres",
"user": "projectdb",
"password": "Azure@1212",
"host": "fraud-project.postgres.database.azure.com",
"port":  5432,
}

    


# Functions

def get_connection():
  
    return psycopg2.connect(
        database=DATABASE_CONFIG.get('database'),
        user=DATABASE_CONFIG.get('user'),
        password=DATABASE_CONFIG.get('password'),
        host=DATABASE_CONFIG.get('host'),
        port=DATABASE_CONFIG.get('port'),
    )

def insert(batch, table_name):
    cols = batch[0].keys()
    values = [[value for value in b.values()] for b in batch]
    
    query = "INSERT INTO {} ({}) VALUES %s".format(table_name, ','.join(cols))
    
    execute_values(cur, query, values)
    conn.commit()
    
 
    
def create_table(table_name):
    CREATE_QUERY ='''CREATE TABLE IF NOT EXISTS {} (
       v1 decimal,
       v2 decimal,
       v3 decimal,
       v4 decimal,
       v5 decimal,
       v6 decimal,
       v7 decimal,
       v8 decimal,
       v9 decimal,
       v10 decimal,
       v11 decimal,
       v12 decimal,
       v13 decimal,
       v14 decimal,
       v15 decimal,
       v16 decimal,
       v17 decimal,
       v18 decimal,
       v19 decimal,
       v20 decimal,
       v21 decimal,
       v22 decimal,
       v23 decimal,
       v24 decimal,
       v25 decimal,
       v26 decimal,
       v27 decimal,
       v28 decimal,
       Log_Amount decimal,
       pred int
       )'''.format(table_name)
    return cur.execute(CREATE_QUERY, table_name)

def predict(msg, record, lst, model_name):
    y_pred = model_name.predict(record)
    m_msg = msg.copy()
    m_msg['pred'] = int(y_pred[0])
    lst.append(m_msg)
    return lst
    




if __name__ == '__main__':
    for i in range(1000):
        print('consumer working')
        time_to_sleep = random.randint(1, 2)
        time.sleep(time_to_sleep)
    # Kafka Consumer 
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )
    
    # models
    encoder = load_model('../models/ae_model.h5')
    rf = pickle.load(open('../models/rf_clf.pkl','rb'))
    cb = pickle.load(open('../models/cb_clf.pkl','rb'))
    clf = pickle.load(open('../models/clf.pkl','rb'))
    lgbm = pickle.load(open('../models/lgbm_clf.pkl','rb'))
    xgb = pickle.load(open('../models/xgb_clf.pkl','rb'))
    
    
    rf_batch = []
    cb_batch = []
    clf_batch = []
    lgbm_batch = []
    xgb_batch = []
    
    
    for message in consumer:
        print(json.loads(message.value))
        m = json.loads(message.value)
        rec =  pd.DataFrame(m, index = [0])
        rec_enc = encoder.predict(rec)
        
        # Models:
        # random forest model
        #rf_y = rf.predict(rec_enc)
        #rf_m = m.copy()
        #rf_m['pred'] = int(y[0])
        #rf_batch.append(rf_m)
        
         # Random Forest Model
        rf_batch = predict(m, rec_enc, rf_batch, rf)
      
        # Cat-Boost Model
        cb_batch = predict(m, rec_enc, cb_batch, cb)
    
        # Logistic Regression Model
        clf_batch = predict(m, rec_enc, clf_batch, clf)
      
        # LGBM Model
        lgbm_batch = predict(m, rec_enc, lgbm_batch, lgbm)
       
        # XGB Model
        xgb_batch = predict(m, rec_enc, xgb_batch, xgb)
        
        

        
        
        if len(xgb_batch) % BATCH_SIZE == 0:
            conn = get_connection()
            cur = conn.cursor()
            # Tables
            create_table('random_forest')
            create_table('cat_boost')
            create_table('logistic_reg')
            create_table('lgbm')
            create_table('xgb')
            conn.commit()
            # Insertion
            insert(rf_batch, 'random_forest')
            insert(cb_batch, 'cat_boost')
            insert(clf_batch, 'logistic_reg')
            insert(lgbm_batch, 'lgbm')
            insert(xgb_batch, 'xgb')
            
            conn.close()
            # Clear batches
            rf_batch[:] = []
            cb_batch[:] = []
            clf_batch[:] = []
            lgbm_batch[:] = []
            xgb_batch[:] = []