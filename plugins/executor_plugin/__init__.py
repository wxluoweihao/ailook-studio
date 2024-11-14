# from lib.query_executor.base_executor import QueryExecutorBaseClass
from lib.query_executor.executors.hive import HiveQueryExecutor
from lib.query_executor.executors.sqlalchemy import SqlAlchemyQueryExecutor, GenericSqlAlchemyQueryExecutor
from lib.query_executor.executors.trino import TrinoQueryExecutor

ALL_PLUGIN_EXECUTORS = [
    HiveQueryExecutor,
    TrinoQueryExecutor,
    GenericSqlAlchemyQueryExecutor
]
