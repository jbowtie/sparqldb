"""
SPARQLdb backend for Django
"""

from django.core.exceptions import ImproperlyConfigured
from sparqldb import dbapi

class DatabaseError(Exception):
    pass

try:
    # Only exists in Python 2.4+
    from threading import local
except ImportError:
    # Import copy of _thread_local.py from Python 2.4
    from django.utils._threading_local import local

class FakeCursor(object):
    def execute(self, sql, parameters):
        print "execute:", sql

class DatabaseWrapper(local):
    def __init__(self, **kwargs):
        self.connection = None
        self.queries = []
        self.options = kwargs

    def cursor(self):
        "get a database cursor (init a connection if needed!)"
        from django.conf import settings
        if self.connection is None:
            if settings.DATABASE_NAME == '':
                from django.core.exceptions import ImproperlyConfigured
                raise ImproperlyConfigured, "You need to specify DATABASE_NAME in your Django settings file."
            database_name = '/home/jbowtie/tmp/' + settings.DATABASE_NAME
            self.connection = dbapi.connection("http://example.org/testdb/", database_name)
        return self.connection.cursor()

    def _commit(self):
        "commit a tx"
        #raise NotImplementedError
        pass

    def _rollback(self):
        "rollback the tx"
        raise NotImplementedError

    def close(self):
        "close the connection"
        pass # close()

supports_constraints = False

def quote_name(name):
    "don't currently support quoted identifiers"
    return name

def dictfetchone(cursor):
    "Returns a row from the cursor as a dict"
    raise NotImplementedError

def dictfetchmany(cursor, number):
    "Returns a certain number of rows from a cursor as a dict"
    raise NotImplementedError

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    raise NotImplementedError

def get_last_insert_id(cursor, table_name, pk_name):
    "return most recent id inserted for this table"
    return cursor.lastrowid #most likely, a little TOO trivial

def get_date_extract_sql(lookup_type, table_name):
    # lookup_type is 'year', 'month', 'day'
    # http://www.postgresql.org/docs/8.0/static/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT
    #return "EXTRACT('%s' FROM %s)" % (lookup_type, table_name)
    raise NotImplementedError

def get_date_trunc_sql(lookup_type, field_name):
    # lookup_type is 'year', 'month', 'day'
    # http://www.postgresql.org/docs/8.0/static/functions-datetime.html#FUNCTIONS-DATETIME-TRUNC
    #return "DATE_TRUNC('%s', %s)" % (lookup_type, field_name)
    raise NotImplementedError

def get_limit_offset_sql(limit, offset=None):
    sql = "LIMIT %s" % limit
    if offset and offset != 0:
        sql += " OFFSET %s" % offset
    return sql

def get_random_function_sql():
    #return "RANDOM()"
    raise NotImplementedError

def get_fulltext_search_sql(field_name):
    raise NotImplementedError

def get_deferrable_sql():
    return ""
	
def get_drop_foreignkey_sql():
    #return "DROP CONSTRAINT"
    raise NotImplementedError

def get_pk_default_value():
    #return "DEFAULT"
    raise NotImplementedError

#maps django operators to SQL clauses
OPERATOR_MAPPING = {
    'exact': '= %s',
    'iexact': 'ILIKE %s',
    'contains': 'LIKE %s',
    'icontains': 'ILIKE %s',
    'gt': '> %s',
    'gte': '>= %s',
    'lt': '< %s',
    'lte': '<= %s',
    'startswith': 'LIKE %s',
    'endswith': 'LIKE %s',
    'istartswith': 'ILIKE %s',
    'iendswith': 'ILIKE %s',
}
