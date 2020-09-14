# import simulation


class Component:

    def __init__(self):
        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)
        entity.components.append(entity)
