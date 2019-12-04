from contextlib import contextmanager
from typing import Any, List, Optional, Tuple

from google.cloud.datastore import Client, Entity
from google.cloud.datastore.query import Iterator

from datastore_client.utils import chunk_iterable


class DatastoreClient:
    def __init__(self, namespace: str=None, **kwargs) -> None:
        self.client = Client(namespace=namespace, **kwargs)
        self._batched_update_entities = None

    @contextmanager
    def batch_update(self):
        self._batched_update_entities = []

        yield

        # Max batch size for writes is 500
        for entity_chunk in chunk_iterable(self._batched_update_entities, chunk_size=500):
            self.client.put_multi(entity_chunk)

        self._batched_update_entities = None

    def set_key(self, entity_name: str, key_name: str, **properties: Any) -> None:
        key = self.client.key(entity_name, key_name)

        entity = Entity(key=key)
        entity.update(properties)

        if self._batched_update_entities is not None:
            self._batched_update_entities.append(entity)
        else:
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
