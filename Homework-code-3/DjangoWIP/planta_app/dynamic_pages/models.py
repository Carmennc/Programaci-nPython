from django.db import models

# Create your models here.

class Material:
    # **kwargs Materials(name= , descrition= ..... )
    def __init__(self,dic):
        self.name= dic["name"]
        self.description= dic["description"]
        self.price_starting= dic["price_starting"]
        self.planta_types= dic["planta_types"]
        
        
def create_materials(dic):
    return list(map( lambda e: Material(e), dic) )

MATERIALS = create_materials([
    {
        "name": "Fertilizante Orgánico", 
        "description": "Mezcla rica en nutrientes para crecimiento",
        "price_starting": 15000, 
        "planta_types": "Rosa, Girasol, Orquídea"
    },
    {
        "name": "Maceta de Cerámica",
        "description": "Con sistema de drenaje incluido", 
        "price_starting": 25000, 
        "planta_types": "Aloe vera, Cactus, Orquídea"
    },
    {
        "name": "Kit de Riego por Goteo",
        "description": "Sistema automático programable", 
        "price_starting": 45000, 
        "planta_types": "Rosa, Girasol, Aloe vera"
    },
    {
        "name": "Sustrato Premium",
        "description": "Mezcla especial con perlita y turba", 
        "price_starting": 18000, 
        "planta_types": "Orquídea, Cactus, Rosa"
    }
])

