#!/usr/bin/env python
# vi:si:et:sw=4:sts=4:ts=4
#
# implements Python DBAPI 2.0
# see PEP 249 (http://www.python.org/dev/peps/pep-0249/)
from rewrite import rewriter, FORMAT_TRIPLES, FORMAT_SPARQL, db, literal_to_python, literal_datatype, tripleset, SqlSyntaxError
from sql import LiteralExpression
import RDF
import exceptions
import logging

#logging.basicConfig(level=logging.INFO)

apilevel = '2.0'
paramstyle = 'pyformat' #or 'format' for c-style

#0     Threads may not share the module.
#1     Threads may share the module, but not connections.
#2     Threads may share the module and connections.
#3     Threads may share the module, connections and cursors.
threadstyle = 0 #at least until we test thread safety...

#exception hierarchy defined by PEP
class Error(exceptions.StandardError):
	pass

class Warning(exceptions.StandardError):
	pass

class InterfaceError(Error):
	pass

class DatabaseError(Error):
	pass

class InternalError(DatabaseError):
	pass

class OperationalError(DatabaseError):
	pass

class ProgrammingError(DatabaseError):
	pass

class IntegrityError(DatabaseError):
	pass

class DataError(DatabaseError):
	pass

class NotSupportedError(DatabaseError):
	pass


class dictproxy:
    def __init__(self, attr):
        self.__dict__ = attr

stores = {}

class datastore:
    '''Server-side representation of a database'''
    def __init__(self, storage_name):
        self.uri = None
        self.store = None
        self.is_open = False
        self.name = storage_name
        self.tables = {}
        #read in the URI
        #open the database file

    def create(self, base_uri):
        '''Create a new database with the specified base URI.'''
        self.uri = base_uri
        self.store = RDF.Model(RDF.Storage(storage_name='sqlite', name=self.name, options_string="new='true'"))
        self.tables = {}
        self.is_open = True

    def select(self, query):
        '''Execute a SPARQL query.'''
        #raise exception if store closed!
        q = RDF.SPARQLQuery(query)
        return q.execute(self.store)

	def insert_triples(self, query):
	    '''Insert new triples into the default graph.'''
        #raise exception if store closed!
        p = RDF.NTriplesParser()
        p.parse_string_into_model(self.store, query, self.uri)

    def dump(self):
        for s in self.store:
            print s

    def update(self, query, new_values):
        '''Delete old triples, insert new triples.'''
        ids = self.select(query)
        clauses = tripleset()
        for row in ids:
            rowID = row.values()[0]
            for col in new_values.keys():
                del_query = RDF.Statement(rowID, RDF.Node(uri_string = col), None)
                for s in self.store.find_statements(del_query):
                    del self.store[s]
                clauses.append("<%s> <%s> %s ." % (str(rowID.uri), col, new_values[col]))
        self.insert_triples(clauses.n3())
    
    def delete(self, query):
        '''Delete existing triples for a given URI.'''
        ids = self.select(query)
        for row in ids:
            del_query = RDF.Statement(row.values()[0], None, None)
            for s in self.store.find_statements(del_query):
                del self.store[s]

    def _load_last_val(self, table_uri, pk_uri):
        last_id_query = """SELECT ?lastID
            WHERE {
            ?pk_table <%s> ?lastID .
            } 
            ORDER BY DESC(?lastID) 
            LIMIT 1""" % pk_uri
        results = self.select(last_id_query)
        if len(results) == 0:
            return 0
        else:
            return literal_to_python(results.next()['lastID'])

    def _load_schema(self):
        db_schema = """
        SELECT ?table ?pk
        WHERE{
            ?table <%s> ?pk .
        }
        """ % db.pk.uri

        results = self.select(db_schema)
        
        for dictresult in results:
            table_uri = str(dictresult['table'].uri)
            if table_uri not in self.tables:
                self.tables[table_uri] = dictproxy({'pk': str(dictresult['pk'].uri), 'cols': []})
                self.tables[table_uri].lastID = self._load_last_val(table_uri, str(dictresult['pk'].uri))

    def _load_table_cols(self, tables):
        db_cols = """
        SELECT ?table ?col ?col_alias
        WHERE {
            ?table <%s> ?col .
            OPTIONAL { ?col <%s> ?col_alias }
        }
        """ % (db.col.uri, db.column_name.uri)

        results = self.select(db_cols)
        for dictresult in results:
            table_uri = str(dictresult['table'].uri)
            if dictresult['col_alias']:
                col = (str(dictresult['col'].uri), unicode(dictresult['col_alias']))
            else:
                col = (str(dictresult['col'].uri), unicode(dictresult['col'].uri).split('.')[-1])
            tables[table_uri].cols.append(col)

    def load(self, base_uri):
        # ignore load command when already open
        # see if DBAPI requires us to raise exception
        if self.is_open:
            return

        self.uri = base_uri
        self.store = RDF.Model(RDF.Storage(storage_name='sqlite', name=self.name, options_string=""))
        logging.basicConfig(level=logging.INFO, filename="/home/jbowtie/tmp/%s.log" % self.name.split("/")[-1])
        self.is_open = True
        self._load_schema()
        
    def update_schema(self):
        self._load_schema()

class connection:
    #this assumes an in-memory model
    #need to factor out server; either (global) in-memory server
    # or external daemon we need to talk to over host+port
    def __init__(self, base_uri, dsn="test.dbapi.db", create=False):
        self.base_uri = base_uri

        #if not already open...
        if dsn not in stores:
            stores[dsn] = datastore(dsn)
            #load the existing database
            if not create:
                stores[dsn].load(base_uri)
        #for current tests we need to re-create the databases
        if create:
            stores[dsn].create(base_uri)
        self.store = stores[dsn]

	#DBAPI interface
	def rollback(self):
        raise NotSupportedError("Transactions are not yet implemented on underlying store")
    def commit(self):
        pass
    def close(self):
        pass
    def cursor(self):
        return cursor(self.base_uri, self)

	#custom methods here...
	def insert_triples(self, query):
	    self.store.insert_triples(query)

    def dump(self):
        self.store.dump()

    def select(self, query):
        try:
            return self.store.select(query)
        except:
            logging.error("Failed SPARQL: %s" % query)
            raise

    def update(self, query, new_values):
        self.store.update(query, new_values)
    
    def delete(self, query):
        self.store.delete(query)
    
    def update_schema(self):
        self.store.update_schema()

def connect(**kwargs):
    #print kwargs
	#standard keywords
	#    dsn         Data source name as string
    #    user        User name as string (optional)
    #    password    Password as string (optional)
    #    host        Hostname (optional)
    #    database    Database name (optional)
    #extended keywords
    #    create      Create new database (optional, default False)
    create = False
    if 'create' in kwargs:
        create = kwargs['create']
    if 'dsn' in kwargs:
        return connection(kwargs['uri'], kwargs['dsn'], create = create)
    return connection(kwargs['uri'], create = create)

# some TODO/implementation notes:
# .connection is supposed to be read-only
# .lastrowid returns ROWID of last INSERT statement
class cursor:
    def __init__(self, base_uri, connection):
        self.arraysize = 1
        self.rowcount = -1
        self.rewriter = rewriter(base_uri)
        self._connection = connection
        self.sql = None
        self.sparql = None
		self.results = None
		self.lastrowid = 0
    
    def _desc(self):
		#(name, type_code, display_size, internal_size, precision, scale, null_ok)
		#first two are required, supply None for optional values
		if not self.results:
			return None

		if len(self.results) == 0:
			return None

        desc = []
		cols = [self.results.get_binding_name(i) for i in range(self.results.get_bindings_count())]
		for col in cols:
			desc_col = (col, literal_datatype(self.results.get_binding_value_by_name(col)), None, None, None, None, None)
			desc.append(desc_col)
		return desc

		#if no return values, or nothing executed
        return None
    description = property(_desc)

    def close(self):
        pass

	def _escape_param(self, param):
		if isinstance(param, (str, unicode)):
			return '"%s"' % param
		return unicode(param)

	def escape_params(self, parameters):
		#for dict, return dict
		if isinstance(parameters, dict):
			params = {}
			for k,v in parameters.iteritems():
				params[k] = self._escape_param(v)
			return params
		#for sequence, return tuple
		params = []
		for p in parameters:
			params.append(self._escape_param(p))
		return tuple(params)

	def execute(self, operation, parameters=None):
		#TODO: support parameters as dictionary (code assumes tuples!)
		#catch param substitution error, raise ProgrammingError
        if parameters:
			params = self.escape_params(parameters)
            sql = operation % params
        else:
            sql = operation
        self.sql = sql
        self.rewriter.schema = self._connection.store.tables
        try:
    		plan = self.rewriter.rewrite(sql)
    		logging.info(sql)
    	except SqlSyntaxError, err:
    	    logging.error("Syntax Error:  " + sql)
    	    raise ProgrammingError(err.message, line = err.line)
		if plan:
            self.sparql = plan.sparql_query
            self.results = self._exec(plan)
            self.result_columns = plan.selected_columns
    		if plan.lastid:
    			self.lastrowid = plan.lastid

    def _exec(self, plan):
        if plan == None: #resolves to a no-op if this happens
            return

        # we resolve deletions, inserts, and selects, in that order.
        # updates are deletes followed by inserts, so they go between delete and insert            
        # first, delete any records indicated by the plan
        if plan.deleted_query:
            self._connection.delete(plan.deleted_query)
        # second, update values as indicated
        if plan.new_values:
            self._connection.update(plan.update_records_query, plan.new_values)
        # third, insert any records
        if plan.inserted_triples:
            self._connection.insert_triples(plan.inserted_triples)
        #forth, update the cached schema
        if plan.update_schema:
            self._connection.update_schema()
        #finally, execute any query
        if plan.sparql_query:
            return self._connection.select(plan.sparql_query)

    def execute_sparql_directly(self, sparql):
        self.sparql = sparql
        self.results = self._connection.select(sparql)

    def executemany(self, operation, seq_of_parameters):
        pass
        
    def _yieldresult(self):
        db_cols = [self.results.get_binding_name(i) for i in range(self.results.get_bindings_count())]
        for r in self.results:
            db_vals = dict([(key, literal_to_python(r[key])) for key in db_cols])
            cols = []
            for c in self.result_columns:
                cols.append(c.evaluate(db_vals))
            yield tuple(cols)
    
    def fetchone(self):
        if not self.results:
            return []
        return self._yieldresult().next()

    def fetchmany(self, size=None):
        if not self.results:
            return []
		#TODO: use array size in when size == None
		if size==None:
            return self.fetchall()
        rows = []
        try:
            for i in range(size):
                rows.append(self._yieldresult().next())
        except StopIteration:
            pass
        return rows

    def fetchall(self):
		if not self.results:
			return []

        cols = [self.results.get_binding_name(i) for i in range(self.results.get_bindings_count())]
        rows = []
        for r in self._yieldresult():
            rows.append(r)
        return rows
    def dictfetchone(self):
		if not self.results:
            return None
		return self.results[0]
    def nextset(self):
        return None

    def setinputsizes(self):
        pass
    def setoutputsize(self, size, column=None):
        pass


#singleton type objects are used for parameters
# typeobject.__cmp__ will be passed the type-code from cursor.description
# in our case, we're going to getting the rdf:type URI
# generally expecting xsd types
#STRING
#BINARY
#NUMBER
#DATETIME
#ROWID

#following constructors required
#Date(year, month, day)
#Time(hour,minute,second)
#Timestamp(...)
#DateFromTicks(ticks) / Time.. / Timestamp...
#Binary(string)

