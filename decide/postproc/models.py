from django.db import models
from enum import Enum

# Create your models here.

class PostprocTypeEnum(Enum):

    IDENTITY = 'IDENTITY'
    DHONDT = 'DHONDT'
    DROOP = 'DROOP'
    BORDA = 'BORDA'
    HARE = 'HARE'
    

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)