# Simple DataStore Client

A simple Google DataStore client that exposes 3 functions on the `DatastoreClient` class.

```python
class DatastoreClient:
    def __init__(self, namespace: str=None, **kwargs) -> None:
        self.client = Client(namespace=namespace, **kwargs)

    def set_key(
        self,
        entity_name: str,
        key_name: str,
        **properties: Any,
    ) -> None:
        ...

    def get_key(
        self,
        entity_name: str,
        key_name: str,
    ) -> Optional[Entity]:
        ...

    def query_entity(
        self,
        entity_name: str,
        *query_filters: Tuple[str, str, Any],
        projection: List[str]=None,
        limit: Optional[int]=None,
    ) -> Iterator:
        ...
```

## Examples

### Changing the `namespace`
You can set the `namespace` for the client by passing it in to the constructor
```python
from datastore_client.client import DatastoreClient

client = DatastoreClient(namespace='namespace_A')
```

The following will change the namespace for all subsequent function calls.

```python
from datastore_client.client import DatastoreClient

client = DatastoreClient()
client.client.namespace = 'specific_namespace'
```

### `set_key`

```python
from datastore_client.client import DatastoreClient

client = DatastoreClient()
client.set_key(
    entity_name=RECHARGE_NOTES_ENTITY, 
    key_name=note_key, 
    username=username, 
    reference=reference, 
    note=notes,
)

# This can also be used in batch mode
with client.batch_update():
    client.set_key(...)
    client.set_key(...)

# Both key updates will be done when the with block exits
```

### `get_key`

```python
from datastore_client.client import DatastoreClient

client = DatastoreClient()
client.get_key(LOGIN_ENTITY, username)
```

### `query_entity`

```python
from datastore_client.client import DatastoreClient

client = DatastoreClient()
product_list = list(client.query_entity(
    PRODUCT_ENTITY,
    ('network', '=', network_name),
    ('product_type', '=', product_code),
    ('bundle_size', '=', denomination),
    projection=['id'],
    limit=1,
))

print(product_list[0]['id'])
```
