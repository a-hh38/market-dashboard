from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:Athharva@localhost:5432/market_dashboard"

engine = create_engine(DB_URL)