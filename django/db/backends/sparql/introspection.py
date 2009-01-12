"""
Used during introspection to get information needed to build Django models
"""

def get_table_list(cursor):
    "Returns a list of table names in the current database."
    return []

def get_table_description(cursor, table_name):
    "Returns a description of the table, with the DB-API cursor.description interface."
    raise NotImplementedError

def get_relations(cursor, table_name):
    """
    Returns a dictionary of {field_index: (field_index_other_table, other_table)}
    representing all relationships to the given table. Indexes are 0-based.
    """
    raise NotImplementedError

def get_indexes(cursor, table_name):
    """
    Returns a dictionary of fieldname -> infodict for the given table,
    where each infodict is in the format:
        {'primary_key': boolean representing whether it's the primary key,
         'unique': boolean representing whether it's a unique index}
    """
    raise NotImplementedError

# Maps type codes to Django Field types.
DATA_TYPES_REVERSE = {}
