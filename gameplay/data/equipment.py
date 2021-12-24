from gameplay.attribute import Attribute
from ..equipment import Equipment

def get(id: str) -> Equipment:

    if id == "shield:shieldgenerator-1":
        eq = Equipment()
        eq.name = "Shield Generator V1"
        eq.attributes[Attribute.MAX_SHIELD] = 30
        return eq

    if id == "plating:hullplating-1":
        eq = Equipment()
        eq.name = "Hull Plating Mark I"
        eq.attributes[Attribute.MAX_HULL] = 30
        return eq

    if id == "capsule:capsule-1":
        eq = Equipment()
        eq.name = "Light Capsule"
        eq.attributes[Attribute.MAX_CORE] = 10
        return eq

    if id == "engine:basicengine-1":
        eq = Equipment()
        eq.name = "Basic Engine"
        eq.attributes[Attribute.MAX_ACCELERATION] = 0.001
        return eq

    raise IndexError