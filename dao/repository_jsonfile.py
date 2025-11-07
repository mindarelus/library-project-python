import json
import os
from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import TypeVar, Type, Generic, Set, Dict

from dao.id_generator import IdGenerator
from dao.repository import Repository

T = TypeVar('T')

class RepositoryJsonFile(Repository, Generic[T]):
    def __init__(self, filename: str, id_generator: IdGenerator, entity_classes: Set[Type]):
        self.filename = filename
        self.id_generator = id_generator
        self._entities = {}
        self._entity_classes = {cls.__name__: cls for cls in entity_classes}
        self.load_from_file()

    def __contains__(self, item: T) -> bool:
        self.load_from_file()
        return item in set(self._entities.values())

    def __iter__(self):
        self.load_from_file()
        return iter(self._entities.values())

    def __len__(self) -> int:
        self.load_from_file()
        return len(self._entities)

    def add(self, entity: T):
        self.load_from_file()
        entity.id = self.id_generator.generate_id()
        self._entities[entity.id] = entity
        self.save_to_file()
        return entity

    def edit(self, entity: T):
        self.load_from_file()
        self._entities[entity.id] = entity
        self.save_to_file()
        return entity

    def delete(self, entity_id):
        self.load_from_file()
        old = self.find_by_id(entity_id)
        if old:
            del self._entities[entity_id]
            self.save_to_file()
        return old

    def find_by_id(self, entity_id):
        self.load_from_file()
        return self._entities.get(entity_id)

    def find_all(self):
        self.load_from_file()
        return list(self._entities.values())

    def load_from_file(self):
        if not os.path.exists(self.filename):
            self._entities = {}
            return

        def _object_hook_factory(entity_cls: Dict[str, Type]):
            def object_hook(obj):
                class_name = obj.get('__class')
                if not class_name:
                    return obj

                cls = entity_cls.get(class_name)
                if cls is None:
                    if class_name == "UUID":
                        return UUID(obj['value'])
                    if class_name == "datetime":
                        return datetime.fromisoformat(obj['value'])
                    return obj

                if issubclass(cls, Enum):
                    return cls[obj['value']]

                del obj['__class']
                return cls(**obj)

            return object_hook

        with open(self.filename, "r", encoding="utf-8") as f:
            try:
                items = json.load(f, object_hook=_object_hook_factory(self._entity_classes))
                self._entities = {entity.id: entity for entity in items if hasattr(entity, 'id')}
            except json.JSONDecodeError:
                self._entities = {}

    def save_to_file(self):
        def _dumper(obj):
            if isinstance(obj, (datetime, UUID)):
                return {"__class": obj.__class__.__name__, "value": str(obj)}
            elif isinstance(obj, Enum):
                return {"__class": obj.__class__.__name__, "value": obj.name}
            
            result = dict(obj.__dict__)
            result.update({"__class": obj.__class__.__name__})
            return result

        dirname = os.path.dirname(self.filename)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        with open(self.filename, 'w', encoding="utf-8") as f:
            json.dump(list(self._entities.values()), f, indent=4, default=_dumper)
