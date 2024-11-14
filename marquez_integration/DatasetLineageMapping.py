from pymysql.constants.FIELD_TYPE import VARCHAR
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DatasetLineageMapping(Base):
    __tablename__ = 'dataset_lineage_mapping'
    input_dataset = Column(String(255), primary_key=True)
    output_dataset = Column(String(255), primary_key=True)
