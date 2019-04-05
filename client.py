from typing import Any, List, Optional, Tuple

from google.cloud import datastore
from google.cloud.datastore import Entity
from google.cloud.datastore.query import Iterator


def set_key(entity_name: str, key_name: str, **properties: Any) -> None:
    client = datastore.Client()
    key = client.key(entity_name, key_name)

    entity = datastore.Entity(key=key)
    entity.update(properties)

    client.put(entity)


def get_key(entity_name: str, key_name: str) -> Optional[Entity]:
    client = datastore.Client()
    key = client.key(entity_name, key_name)

    return client.get(key)


def query_entity(
    entity_name: str,
    *query_filters: Tuple[str, str, Any],
    projection: List[str]=None,
    limit: Optional[int]=None,
) -> Iterator:
    client = datastore.Client()

    query = client.query(kind=entity_name)

    for query_filter in query_filters:
        query.add_filter(*query_filter)

    if projection is not None:
        query.projection = projection

    return query.fetch(limit=limit)
