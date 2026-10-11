"""
British Airways Flight Delay Analysis - Database Management Module
Creates SQLite relational tables, indexes, populates data, and provides query execution tools.
"""

import os
import sqlite3
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

DB_PATH = 'data/processed/flight_analytics.db'

def get_connection(db_path=DB_PATH):
    """Returns a sqlite3 connection."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)

def get_engine(db_path=DB_PATH):
    """Returns a SQLAlchemy engine."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return create_engine(f'sqlite:///{db_path}')

def initialize_database(features_df_path='data/processed/flight_features.csv', db_path=DB_PATH, verbose=True):
    """
    Builds the relational database schema, ingests flights, airports, routes, and creates indexes.
    """
    if verbose:
        print(f"--- INITIALIZING SQLITE DATABASE: {db_path} ---")
        
    df = pd.read_csv(features_df_path)
    engine = get_engine(db_path)
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # 1. Ingest Main Flights Table
    df.to_sql('flights', engine, if_exists='replace', index=False)
    if verbose:
        print(f"Ingested {len(df):,} records into 'flights' table.")
        
    # 2. Build Airports Dimension Table
    origin_meta = df[['origin_airport', 'origin_city']].drop_duplicates().rename(
        columns={'origin_airport': 'airport_code', 'origin_city': 'city'}
    )
    dest_meta = df[['dest_airport', 'dest_city']].drop_duplicates().rename(
        columns={'dest_airport': 'airport_code', 'dest_city': 'city'}
    )
    airports_dim = pd.concat([origin_meta, dest_meta]).drop_duplicates(subset=['airport_code']).reset_index(drop=True)
    airports_dim['country'] = airports_dim['airport_code'].apply(
        lambda c: 'UK' if c in ['LHR', 'LGW', 'LCY', 'EDI', 'GLA', 'MAN', 'ABZ', 'BFS', 'NCL'] else 'International'
    )
    airports_dim['airport_tier'] = airports_dim['airport_code'].apply(
        lambda c: 'Primary Hub' if c in ['LHR', 'LGW', 'LCY'] else ('Domestic UK' if c in ['EDI', 'GLA', 'MAN', 'ABZ', 'BFS', 'NCL'] else 'International Spoke')
    )
    airports_dim.to_sql('airports', engine, if_exists='replace', index=False)
    if verbose:
        print(f"Ingested {len(airports_dim):,} stations into 'airports' dimension table.")
        
    # 3. Build Routes Dimension Table
    from analysis import compute_route_risk_score
    routes_dim = compute_route_risk_score(df, min_flight_threshold=10)
    routes_dim.to_sql('routes', engine, if_exists='replace', index=False)
    if verbose:
        print(f"Ingested {len(routes_dim):,} route pairs into 'routes' dimension table.")
        
    # 4. Build Delay Root Causes Summary Table
    from analysis import compute_pareto_root_causes
    pareto_dim = compute_pareto_root_causes(df)
    pareto_dim.to_sql('delay_root_causes', engine, if_exists='replace', index=False)
    if verbose:
        print(f"Ingested {len(pareto_dim):,} records into 'delay_root_causes' table.")
        
    # 5. Create Performance Indexes
    index_statements = [
        "CREATE INDEX IF NOT EXISTS idx_flight_date ON flights (flight_date);",
        "CREATE INDEX IF NOT EXISTS idx_flight_number ON flights (flight_number);",
        "CREATE INDEX IF NOT EXISTS idx_origin ON flights (origin_airport);",
        "CREATE INDEX IF NOT EXISTS idx_dest ON flights (dest_airport);",
        "CREATE INDEX IF NOT EXISTS idx_route ON flights (route);",
        "CREATE INDEX IF NOT EXISTS idx_delay_status ON flights (delay_status);",
        "CREATE INDEX IF NOT EXISTS idx_haul_type ON flights (haul_type);",
        "CREATE INDEX IF NOT EXISTS idx_dep_hour ON flights (dep_hour);"
    ]
    for stmt in index_statements:
        cursor.execute(stmt)
    conn.commit()
    conn.close()
    
    if verbose:
        print(f"Database successfully indexed and ready.")
        print(f"--- DATABASE INITIALIZATION COMPLETED ---\n")

def execute_query(sql_query, db_path=DB_PATH):
    """Executes a SQL query and returns results as a pandas DataFrame."""
    conn = get_connection(db_path)
    try:
        df = pd.read_sql_query(sql_query, conn)
        return df
    finally:
        conn.close()

if __name__ == '__main__':
    initialize_database()
