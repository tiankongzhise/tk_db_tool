from typing import Type
from .models import SqlAlChemyBase

class BaseCurd(object):
    def __init__(self, model: Type[SqlAlChemyBase]):
        self.model = model
