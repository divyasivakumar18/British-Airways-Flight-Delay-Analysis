"""
Unit tests for SQLite database schema and analytical queries.
"""
import pytest
import sqlite3
import pandas as pd
from src.database import DB_PATH, execute_query

def test_database_tables_exist():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    assert 'flights' in tables
    assert 'airports' in tables
    assert 'routes' in tables
    assert 'delay_root_causes' in tables

def test_sql_query_execution():
    with open('sql/flight_analysis.sql', 'r', encoding='utf-8') as f:
        sql_text = f.read()
        
    raw_blocks = [b.strip() for b in sql_text.split(';') if b.strip()]
    valid_queries = []
    for b in raw_blocks:
        lines = [l for l in b.split('\n') if not l.strip().startswith('--')]
        query_body = '\n'.join(lines).strip()
        if query_body:
            valid_queries.append(query_body)
            
    assert len(valid_queries) >= 10
    
    for i, q in enumerate(valid_queries):
        df_res = execute_query(q)
        assert isinstance(df_res, pd.DataFrame)
        assert len(df_res) > 0, f"Query {i+1} returned empty result"
