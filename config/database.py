import psycopg2
from psycopg2.extras import Json

DB_CONFIG = {
    "host": "localhost",
    "dbname": "NextMove",
    "user": "postgres",
    "password": "Bhuvi@2024",
    "port": 5432
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    
    # Create tables if they don't exist
    with conn.cursor() as cursor:
        # Drop existing tables to ensure clean schema
        cursor.execute("""
            DROP TABLE IF EXISTS actions CASCADE;
            DROP TABLE IF EXISTS user_actions CASCADE;
        """)
        
        # Table for storing action sequences with user_id
        cursor.execute("""
            CREATE TABLE actions (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                action_name VARCHAR(255) NOT NULL,
                next_action_name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT unique_sequence UNIQUE (user_id, action_name, next_action_name)
            )
        """)
        
        # Table for storing individual user actions
        cursor.execute("""
            CREATE TABLE user_actions (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                action_name VARCHAR(255) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSONB,
                CONSTRAINT unique_user_action UNIQUE (user_id, action_name, timestamp)
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("""
            CREATE INDEX idx_actions_user_action ON actions(user_id, action_name);
            CREATE INDEX idx_user_actions_user ON user_actions(user_id);
            CREATE INDEX idx_user_actions_timestamp ON user_actions(timestamp DESC);
        """)
        
        conn.commit()
    
    return conn