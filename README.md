# Simple DataStore Client

A simple Google DataStore client that exposes 3 functions.

```python
def set_key(entity_name: str, key_name: str, **properties: Any) -> None:
    ...
```

```python
def get_key(entity_name: str, key_name: str) -> Optional[Entity]:
    ...
```

```python
def query_entity(
    entity_name: str,
    *query_filters: Tuple[str, str, Any],
    projection: List[str]=None,
    limit: Optional[int]=None,
) -> Iterator:
    ...
```

## Examples

### `set_key`

```python
set_key(
    entity_name=RECHARGE_NOTES_ENTITY, 
    key_name=note_key, 
    username=username, 
    reference=reference, 
    note=notes,
)
```

### `get_key`

```python
get_key(LOGIN_ENTITY, username)
```

### `query_entity`

```python
product_list = list(query_entity(
    PRODUCT_ENTITY,
    ('network', '=', network_name),
    ('product_type', '=', product_code),
    ('bundle_size', '=', denomination),
    projection=['id'],
    limit=1,
))

print(product_list[0]['id'])
```
