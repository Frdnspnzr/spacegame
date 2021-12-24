from gameplay.actor import Actor
from gameplay.equipment import Equipment
from gameplay.data.equipment import get as get_equipment

def get(id: str) -> Actor:

    if id == "template:player":
        actor = Actor()
        actor.equipped.append(get_equipment("shield:shieldgenerator-1"))
        actor.equipped.append(get_equipment("plating:hullplating-1"))
        actor.equipped.append(get_equipment("capsule:capsule-1"))
        actor.equipped.append(get_equipment("engine:basicengine-1"))
        return actor

    raise IndexError