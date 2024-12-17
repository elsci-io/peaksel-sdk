def entity_to_dict(entity: any, field_renames: dict[str, str] = None):
    """
    Puts the fields of the entity into a dict, and optionally renames the keys.
    """
    renames = merged_dicts(field_renames)
    fields: dict[str, any] = dict(entity.__dict__)
    fields_to_delete = []
    for old_name, new_name in renames.items():
        if new_name in fields:
            raise Exception(f"Field '{new_name}' already exists, you don't want to override it with the value from '{old_name}', right?")
        fields[new_name] = fields[old_name]
        fields_to_delete.append(old_name)
    for old_name in fields_to_delete:
        del fields[old_name]
    return fields

def merged_dicts(d1: dict[str, any] | None, d2: dict[str, any] | None = None) -> dict[str, any]:
    """
    Is used either to combine multiple dicts into one or to replace None dicts with empty ones.
    """
    result: dict[str, any] = {}
    if d1:
        result.update(d1)
    if d2:
        result.update(d2)
    return result

def pass_if_defined(val, func):
    if val is not None:
        return func(val)
    return None