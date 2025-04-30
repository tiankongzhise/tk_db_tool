from typing import Type
from .models import SqlAlChemyBase
from .message import message
from .datebase import get_session,init_db
from sqlalchemy.orm import Session

class BaseCurd(object):
    def __init__(self):
        init_db()


    def bluck_insert(self, data: list, model: Type[SqlAlChemyBase],chunk_size: int = 1000):
        """批量插入数据
        :param data: 插入的数据
        :param model: 插入的数据对应的model
        当数据出现重复时报错
        :return: 插入的数据条数
        """
        with get_session() as session:
                for i in range(0, len(data), chunk_size):
                    chunk_objects = [model(**data) for data in data[i:i+chunk_size]] # If MyTable is your ORM class
                    if chunk_objects:
                        session.add_all(chunk_objects)
                        session.flush() # Flushes the current batch to DB
                        message.info(f"Flushed batch {i//chunk_size + 1}")

