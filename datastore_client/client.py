from contextlib import contextmanager
from typing import Any, List, Optional, Tuple

from google.cloud.datastore import Client, Entity
from google.cloud.datastore.query import Iterator

from datastore_client.utils import chunk_iterable


class BatchManager:
    def __init__(self, datastore_client, overwrite_keys=False):
        self.client = datastore_client
        self.overwrite_keys = overwrite_keys
        self.batch = {}

    def set_key(self, entity_name: str, key_name: str, **properties: Any) -> None:
        key = self.client.key(entity_name, key_name)

        entity = Entity(key=key)
        entity.update(properties)

        self.batch[key] = entity

    def batch_update(self):
        if self.overwrite_keys:
            return self.batch_insert()

        existing_entities = []
        # Get existing entities to preserve unchanged values
        for key_chunk in chunk_iterable(self.batch.keys(), chunk_size=1000):
            key_entities = self.client.get_multi(key_chunk)
            existing_entities.extend(key_entities)

        # Update batch with new properties
        for existing_entity in existing_entities:
            new_entity = self.batch[existing_entity.key]
            existing_entity.update(new_entity)

            self.batch[existing_entity.key] = existing_entity

        # Insert updated entities
        self.batch_insert()

    def batch_insert(self):
        # Max batch size for writes is 500
        for entity_chunk in chunk_iterable(self.batch.values(), chunk_size=500):
            self.client.put_multi(entity_chunk)


class DatastoreClient:
    def __init__(self, namespace: str=None, **kwargs) -> None:
        self.client = Client(namespace=namespace, **kwargs)

    @contextmanager
    def batch_update(self, overwrite_keys=False):
        batch_manager = BatchManager(self.client, overwrite_keys=overwrite_keys)

        yield batch_manager

        batch_manager.batch_update()

    def set_key(self, entity_name: str, key_name: str, **properties: Any) -> None:
        key = self.client.key(entity_name, key_name)

        with self.client.transaction():
            entity = self.client.get(key)

            if entity is None:
                entity = Entity(key=key)

            entity.update(properties)
            self.client.put(entity)

    def get_key(self, entity_name: str, key_name: str) -> Optional[Entity]:
        key = self.client.key(entity_name, key_name)

        return self.client.get(key)

    def query_entity(
        self,
        entity_name: str,
        *query_filters: Tuple[str, str, Any],
        projection: List[str]=None,
        limit: Optional[int]=None,
    ) -> Iterator:
        query = self.client.query(kind=entity_name)

        for query_filter in query_filters:
            query.add_filter(*query_filter)

        if projection is not None:
            query.projection = projection

        return query.fetch(limit=limit)
