from numbers import Number
from typing import Any, Dict, Iterator, List, Optional, Tuple


class MockDatastoreClient:
    """Functionally equivalent to the real DatatstoreClient - used for testing"""
    data: Dict[str, Any] = {}

    def __init__(self, namespace: str = None, **kwargs) -> None:
        pass

    @classmethod
    def set_key(cls, entity_name: str, key_name: str, **properties: Any) -> None:
        if entity_name not in cls.data:
            cls.data[entity_name] = {}

        if key_name not in cls.data[entity_name]:
            cls.data[entity_name][key_name] = {}

        cls.data[entity_name][key_name].update(properties)

    @classmethod
    def get_key(cls, entity_name: str, key_name: str) -> Optional[Dict[str, Any]]:
        return cls.data.get(entity_name, {}).get(key_name)

    @classmethod
    def query_entity(
        cls,
        entity_name: str,
        *query_filters: Tuple[str, str, Any],
        projection: List[str] = None,
        limit: Optional[int] = None,
    ) -> Iterator:
        entities = cls.data.get(entity_name, [])

        def _get_entity(entity_list, filters, fields):
            counter = 0

            for entity_id, entity in entity_list.items():
                if limit and counter >= limit:
                    return

                for key, operator, value in filters:
                    if operator == '=':
                        entity_value = entity[key]
                        if isinstance(entity_value, Number):
                            if value != entity_value:
                                break
                        elif value not in entity_value:
                            break
                else:
                    # This is done if the loop didn't break
                    yield {
                        entity_key: entity_value
                        for entity_key, entity_value in entity.items()
                        if fields and entity_key in fields
                    }
                    counter += 1

        return _get_entity(entities, query_filters, projection)
