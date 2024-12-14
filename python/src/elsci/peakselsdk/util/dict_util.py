def entity_to_dict(entity: any, field_renames: dict[str, str]):
    fields: dict[str, any] = entity.__dict__
    fields_to_delete = []
    for old_name, new_name in field_renames.items():
        if new_name in fields:
            raise Exception(f"Field '{new_name}' already exists, you don't want to override it with the value from '{old_name}', right?")
        fields[new_name] = fields[old_name]
        fields_to_delete.append(old_name)
    for old_name in fields_to_delete:
        del fields[old_name]
    return fields