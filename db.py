import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, Integer, JSON
from sqlalchemy.orm import declarative_base

load_dotenv()

PG_USER, PG_PASSWORD, PG_DB = os.getenv('PG_USER'), os.getenv('PG_PASSWORD'), os.getenv('PG_DB')
PG_DSN = f'postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@127.0.0.1:5431/{PG_DB}'

engine = create_async_engine(PG_DSN)
Base = declarative_base()


class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True, autoincrement=True)
    json = Column(JSON, nullable=False)


Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
