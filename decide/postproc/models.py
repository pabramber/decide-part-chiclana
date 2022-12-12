from django.db import models
from enum import Enum

# Create your models here.

class PostprocTypeEnum(Enum):

    IDENTITY = 'IDENTITY'
    DHONDT = 'DHONDT'
    DROOP = 'DROOP'
    IMPERIALI = 'IMPERIALI'
    BORDA = 'BORDA'
    HARE = 'HARE'
    REINFORCED_IMPERIAL = 'REINFORCED_IMPERIAL'
    HAGENBACH_BISCHOFF = 'HAGENBACH_BISCHOFF'
    SAINTE_LAGUE = 'SAINTE_LAGUE'
    MODIFIED_SAINTE_LAGUE = 'MODIFIED_SAINTE_LAGUE'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)