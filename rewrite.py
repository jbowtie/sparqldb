#! /usr/bin/env python
# vi:si:et:sw=4:sts=4:ts=4

import re, decimal, base64, itertools, exceptions
from sql import SqlParser, ColumnReference, InsertRow, SelectAnalysis, DeleteAnalysis, UpdateAnalysis
from analysis import TableSchema
from RDF import NS
from pyparsing import ParseException

db = NS("http://www.pongacomputing.net/ontologies/db/")
xsd = NS("http://www.w3.org/2001/XMLSchema#")
FORMAT_TRIPLES = "N3"
FORMAT_SPARQL = "SPARQL"

class SqlSyntaxError(exceptions.StandardError):
	def __init__(self, message, line=None):
	    self.message = message
	    self.line = line

def triple(s,p,o):
    if isinstance(o, int):
        return '<%s> <%s> "%d" .' % (s,p,o)
    return "<%s> <%s> <%s> ." % (s,p,o)

def python_to_sparql(val):
    """
    Convert a built-in Python type to its SPARQL representation.

    >>> python_to_sparql(42)
    '"42"^^<http://www.w3.org/2001/XMLSchema#integer>'
    
    >>> python_to_sparql("'foo'")
    '"foo"'

    >>> python_to_sparql(u"string value")
    '"string value"'
    """
    if isinstance(val, int):
        return python_to_n3(val, datatype=xsd.integer.uri)
    if isinstance(val, (str,unicode)) and val[0] == val[-1] == "'":
        return python_to_n3(val[1:-1])
    if isinstance(val, (str,unicode)) and val[0] == val[-1] == '"':
        return python_to_n3(val[1:-1])
	return python_to_n3(val)


def literal_datatype(node):
    if not node.is_literal():
        return None
    dt = node.literal_value['datatype']
    if dt:
        return unicode(dt)
    return u'http://www.w3.org/2001/XMLSchema#string'

def literal_to_python(node):
    # pass through a null
    if not node: return None
    # we only convert literal nodes
    if not node.is_literal(): return node
    
    # see if datatype is attached
    dt = node.literal_value['datatype']
    val = node.literal_value['string']
    # no datatype, return the string
    if not dt:
        return val
    else:
        conv = SchemaToPython[unicode(dt)][0]
        return conv(val)

def python_to_n3(value, language = '', datatype = ''):
    encoded = unicode(value).encode('unicode-escape')
    if language:
        if datatype:
            return '"%s"@%s^^<%s>' % (encoded, language, datatype)
        else:
            return '"%s"@%s' % (encoded, language)
    else:
        if datatype:
            return '"%s"^^<%s>' % (encoded, datatype)
        else:
            return '"%s"' % encoded

class tripleset(list):
    def n3(self):
        return "\n".join(self) + "\n"

class execution_plan:
    def __init__(self, deleted_query = None, inserted_triples = None, sparql_query = None, lastid = None, new_values = None, update_records_query = None, selected_columns = None, update_schema = False):
        self.deleted_query = deleted_query
        self.inserted_triples = inserted_triples
        self.sparql_query = sparql_query
        self.lastid = lastid
        self.update_records_query = update_records_query
        self.new_values = new_values
        self.selected_columns = selected_columns
        self.update_schema = update_schema

class rewriter:
    """Rewrites SQL queries as SPARQL queries, using the dbns base uri for anything not explicitly aliased

    >>> sql = rewriter("urn:ponga:example/")
    >>> print sql.pk_uri("Story", 1)
    urn:ponga:example/story/1/
    """
    def __init__(self, dbns_uri, schema = {}):
        self.base_uri = dbns_uri
        self.schema = schema

    def table_uri(self, table_name):
        """
        Convert a table name to a URI that represents that table.
        Tables that are not otherwise aliased become:
            BASE_URI/table

        >>> sql = rewriter("urn:ponga:example/")
        >>> print sql.table_uri("Story")
        urn:ponga:example/story
        """

        return self.base_uri + table_name.lower()

    def column_uri(self, table_name, column_name):
        """
        Convert a table and column name to a URI that represents that column.
        Columns that are not otherwise aliased become:
            BASE_URI/table.column

        >>> sql = rewriter("urn:ponga:example/")
        >>> print sql.column_uri("Story", "title")
        urn:ponga:example/story.title
        """
        return self.table_uri(table_name) + "." + column_name.lower()

    def pk_uri(self, table_name, pk_id):
        """
        Given a table and simple PK, work out the URI
            BASE_URI/table/id/
        """
        return "%s/%s/" % (self.table_uri(table_name), pk_id)

    def rewrite(self, sql):
        try:
            #silently fail index creation; indexes are passe
            if sql.startswith("CREATE INDEX"):
                return None

            self.parser = SqlParser()
            analysis = self.parser.parse(sql)
            if isinstance(analysis, InsertRow):
                return self.rewrite_INSERT(analysis)
            if isinstance(analysis, UpdateAnalysis):
                return self.rewrite_UPDATE(analysis)
            if isinstance(analysis, DeleteAnalysis):
                return self.rewrite_DELETE(analysis)
            if isinstance(analysis, SelectAnalysis):
                return self.rewrite_SELECT(analysis)
            if isinstance(analysis, TableSchema):
                return self.rewrite_CREATE_TABLE(analysis)
        except ParseException, err:
            raise SqlSyntaxError(err.message, line = err.line)
        except Exception:
            print '-' * 20
            print sql
            print '-' * 20
            raise
        raise SqlSyntaxError("Unrecognised or unsupported expression")

    def sparql_variable(self, name):
        return "?" + name

    def get_table_schema(self, tablename):
        #name of pk field
        #last insertID
        table = self.table_uri(tablename)
        if table in self.schema:
            return self.schema[table]
        else:
            return None

    def rewrite_UPDATE(self, analysis):
        #select IDs for matching records (should do double duty and select any cols ref'd on RHS of set clause)
        #for each id:
        #  generate insert triples (id, col.uri, newval)
        #  generate delete triples (id, col.uri, None) <-- model.find_statements will do matching on None
        #  loop through delete triples, generating deletes to exec
        #  exec inserts
        del_plan = self.rewrite_DELETE(analysis)
#        table = self.get_table_schema(analysis.target_table)
#        print table.name
        
        #triples of new values to be inserted
        values = dict([(self.column_uri(analysis.target_table, col), python_to_sparql(val)) for col, val in analysis.set_clauses])
            
        return execution_plan(new_values = values, update_records_query = del_plan.deleted_query)

    def rewrite_DELETE(self, analysis):
        delete_selection = analysis.select_rows
        table = self.get_table_schema(delete_selection.referenced_tables[0])
        pk_col = table.pk.split("/")[-1]
        
        #delete_selection.columns_to_return = [pk_col]
        delete_selection.column_names.append(pk_col)
        delete_selection.analyse_predicates()
        sel_plan = self.rewrite_SELECT(delete_selection, for_deletion_records = True)
        return execution_plan(deleted_query = sel_plan.sparql_query)

    def rewrite_INSERT(self, newRow):
        #print sql
        clauses = tripleset()
        table = self.get_table_schema(newRow.table)
        values = dict([(self.column_uri(newRow.table, col), val) for col, val in newRow.values.iteritems()])
        pk = 0
        if table:
        #need to query:
        # table.pk, table.lastID
            if table.pk in values and values[table.pk] != None:
                pk = values[table.pk]
                del values[table.pk]
            else:
                pk = table.lastID + 1
            table.lastID += 1
        else:
            print 'schema', self.schema
        newID = self.pk_uri(newRow.table, pk)
        pktriple = "<%s> <%s> %s ." % (newID, table.pk, python_to_sparql(pk))
        clauses.append(pktriple)
        for col, val in values.iteritems():
            #print newID, col, python_to_sparql(val)
            clauses.append("<%s> <%s> %s ." % (newID, col, python_to_sparql(val)))
        return execution_plan(inserted_triples = clauses.n3(), lastid = pk)

    def rewrite_CREATE_TABLE(self, table):
        """
        Returns a set of triples that describe the table using Ponga's db ontology.
        """
        clauses = []
        #define a table
        tableURI = self.table_uri(table.name)
        clauses.append(triple(self.base_uri, db.table.uri, tableURI))
        for col in table.columns.values():
            if col.name[0] == "<":
                columnURI = col.name[1:-1]
            else:
                columnURI = self.column_uri(table.name, col.name)
            clauses.append(triple(tableURI, db.col.uri, columnURI))
            if(col.is_pk):
                clauses.append(triple(tableURI, db.pk.uri, columnURI))
        return execution_plan(inserted_triples = "\n".join(clauses) + "\n", update_schema = True)

    def table_and_col(self, analysis, col):
        #if isinstance(col, ColumnReference):
        #    table, column = col.table, col.column
        #    if not table:
        #        return self.table_and_col(self, analysis, column)
        if "." in col:
            table, column = col.split(".")
        else:
            #consult schema to find out table name
            table, column = analysis.determine_table(col), col
        return table, column

    def is_bound_pk(self, col_val):
        table, col, val = col_val[0][0], col_val[0][1], col_val[1]
        table_schema = self.get_table_schema(table)
        return self.column_uri(table, col) == table_schema.pk

    def determine_columns_to_query(self, analysis, variable_names):
        # for (table not specified) columns we need schema
        selected_columns = []
        for col in analysis.columns_to_return:
            if isinstance(col, ColumnReference):
                variable_name = self.sparql_variable(col.variable_name())
                col_info = (col.column, col.alias, variable_name)
                selected_columns.append(col_info)
                variable_names[col.alias or col.column] = variable_name
        return selected_columns

    def variable_for_column(self, analysis, col, variable_names, column_aliases):
        table, column = self.table_and_col(analysis, col)
        if col in variable_names:
            return variable_names[col]
        elif col in column_aliases:
            return variable_names[column_aliases[col]]
        else:
            candidate_variable = "?query_%s_%s" % (table.lower(), column.lower())
            variable_names[col] = candidate_variable
            return candidate_variable
    
    def rewrite_SELECT(self, analysis, for_deletion_records = False):
        """
        Rewrites the SQL statement as a SPARQL query
        """
        sparql = ""

        #the variable names are used when building where clauses
        variable_names = {}
        #first, figure out names and aliases of returned columns
        returned_columns = self.determine_columns_to_query(analysis, variable_names)
        column_aliases = dict([(c[0], c[1]) for c in returned_columns if c[1]])

        #second, generate bound variables to represent tables
        # technically we want them to represent ID
        # tables["TABLE"] = "?x"
        tables = {}
        for table in analysis.referenced_tables:
            variable_name = "?pk_" + table.lower()
            tables[table] = variable_name
            if for_deletion_records:
                returned_columns.append((None, None, variable_name))

        #find bound primary key values
        for col, val in itertools.ifilter(self.is_bound_pk, analysis.value_equivalence):
            table, column = col
            tables[table] = "<%s>" % self.pk_uri(table, val)

        #we use a set to avoid duplicate clauses arising from different analysis steps
        where_clauses = set()
        for col in analysis.column_names:
            table, column = self.table_and_col(analysis, col)
            #candidate_variable = self.variable_for_col(analysis, col, variable_names, column_aliases)
            if col in variable_names:
                candidate_variable = variable_names[col]
            elif col in column_aliases:
                candidate_variable = variable_names[column_aliases[col]]
            else:
                candidate_variable = "?query_%s_%s" % (table.lower(), column.lower())
                variable_names[col] = candidate_variable
                if col not in [col for col, sort in analysis.order_by]:
                    continue
            where_cond = "%s <%s> %s ." % (tables[table], self.column_uri(table, column), candidate_variable)
            where_clauses.add(where_cond)

        #now build where clause
        # col = val
        for col, val in analysis.value_equivalence:
            table, column = col
            table_schema = self.get_table_schema(table)
            if for_deletion_records and self.column_uri(table, column) == table_schema.pk:
                where_filter = "%s <%s> %s ." % (returned_columns[0][-1], self.column_uri(table, column), python_to_sparql(val))
                where_clauses.add(where_filter)
            if not self.column_uri(table, column) == table_schema.pk:
                where_filter = "%s <%s> %s ." % (tables[table], self.column_uri(table, column), python_to_sparql(val))
                where_clauses.add(where_filter)
        
        # col <, >, <=, >= val
        for v1, op, v2 in analysis.value_comparison:
            if isinstance(v1, ColumnReference):
                where_cond = "%s <%s> %s ." % (tables[v1.table], self.column_uri(v1.table, v1.column), variable_names[v1.column])
                where_clauses.add(where_cond)
                v1 = variable_names[v1.column]
            #print v1, op, v2
            where_filter = "FILTER (%s %s %s) ." % (v1, op, v2)
            where_clauses.add(where_filter)

        # predicate joins
        # Case 1> Following standard FK relationship
        # Case 2> Unrelated value constraints...
        for join_type, sideA, sideB in analysis.joins:
            if join_type == "QUALIFIED":
                v1 = ColumnReference(sideA[0], sideA[1])
                v2 = ColumnReference(sideB[0], sideB[1])
                #this is correct, but inserts need to be fixed first!
                #where_cond = "%s <%s> %s ." % (tables[v1.table], self.column_uri(v1.table, v1.column), tables[v2.table])
                #where_clauses.add(where_cond)
                where_cond = "FILTER ( %s = %s ) ." % (tables[v1.table], tables[v2.table])
                where_clauses.add(where_cond)
        # table joins
        # for using/natural joins we need schema
        
        # process OR terms
        # currently handles only IN(x,y,z)
        # we need to deal with explicit or, nesting of parenthetical expressions
        # FILTER(a=x || a=y || a=z)
        for or_term in analysis.orTerms:
            subclauses = set()
            for v1, op, v2 in or_term.value_comparison:
                if isinstance(v1, ColumnReference):
                    where_cond = "%s <%s> %s ." % (tables[v1.table], self.column_uri(v1.table, v1.column), variable_names[v1.column])
                    where_clauses.add(where_cond)
                    v1 = variable_names[v1.column]
                #print v1, op, v2
                where_filter = "%s %s %s" % (v1, op, v2)
                subclauses.add(where_filter)
            or_filter = "FILTER (%s) ." % " || ".join(subclauses)
            where_clauses.add(or_filter)

        #order by
        order_by_clauses = []
        for sort_key, sort_dir in analysis.order_by:
            order_by_clauses.append("%s(%s)" % (sort_dir.upper(), variable_names[sort_key]))

        # no return columns? probably existence check. Select the pk value
        existence_variable_name = "?pk_val"
        if not returned_columns:
            if tables and not for_deletion_records:
                table_var = tables.values()[0]
                if table_var.startswith("?"):
                    existence_variable_name = table_var
            returned_columns.append((None, None, existence_variable_name))

        #if no where clause by this point, try for primary key value
        if for_deletion_records and len(where_clauses) == 0:
            deletion_pk = self.get_table_schema(analysis.referenced_tables[0]).pk
            where_cond = "%s <%s> %s ." % (returned_columns[0][-1], deletion_pk, existence_variable_name)
            where_clauses.add(where_cond)
            
        # no where clauses
    	if not where_clauses and not for_deletion_records:
    	    row_id = ""
            for col, val in itertools.ifilter(self.is_bound_pk, analysis.value_equivalence):
                table, column = col
                row_id = "<%s>" % self.pk_uri(table, val)
            row_pk = self.get_table_schema(analysis.referenced_tables[0]).pk
            where_cond = "%s <%s> %s ." % (row_id, row_pk, existence_variable_name)
            where_clauses.add(where_cond)

        sparql = self._generate_select_sparql(returned_columns, where_clauses, order_by_clauses, analysis.limit, analysis.offset)
        return execution_plan(sparql_query = sparql, selected_columns = analysis.columns_to_return)

    def _generate_select_sparql(self, returned_columns, where_clauses, order_by_clauses, limit, offset):
        """Pull all the various pieces together for the final SPARQL text"""
        if not where_clauses:
            return None

        select_list = " ".join([col[-1] for col in returned_columns])
        where_clause = "\n\t".join(where_clauses)
        sparql = "PREFIX xsd:    <http://www.w3.org/2001/XMLSchema#>\nSELECT %s \nWHERE\n{\n\t%s\n}\n" % (select_list, where_clause)
        if order_by_clauses:
            sparql += "ORDER BY %s\n" % " ".join(order_by_clauses)
        if limit:
            sparql += "LIMIT %s\n" % limit
        if offset:
            sparql += "OFFSET %s\n" % offset
        return sparql        

SchemaToPython = {  #  (schema->python, python->schema)  Does not validate.
    'http://www.w3.org/2001/XMLSchema#string': (unicode, unicode),
    'http://www.w3.org/2001/XMLSchema#normalizedString': (unicode, unicode),
    'http://www.w3.org/2001/XMLSchema#token': (unicode, unicode),
    'http://www.w3.org/2001/XMLSchema#language': (unicode, unicode),
    'http://www.w3.org/2001/XMLSchema#boolean': (bool, lambda i:unicode(i).lower()),
    'http://www.w3.org/2001/XMLSchema#decimal': (decimal.Decimal, unicode), 
    'http://www.w3.org/2001/XMLSchema#integer': (int, unicode), 
    'http://www.w3.org/2001/XMLSchema#nonPositiveInteger': (int, unicode),
    'http://www.w3.org/2001/XMLSchema#long': (long, unicode),
    'http://www.w3.org/2001/XMLSchema#nonNegativeInteger': (int, unicode),
    'http://www.w3.org/2001/XMLSchema#negativeInteger': (int, unicode),
    'http://www.w3.org/2001/XMLSchema#int': (int, unicode),
    'http://www.w3.org/2001/XMLSchema#unsignedLong': (long, unicode),
    'http://www.w3.org/2001/XMLSchema#positiveInteger': (int, unicode),
    'http://www.w3.org/2001/XMLSchema#short': (int, unicode),
    'http://www.w3.org/2001/XMLSchema#unsignedInt': (long, unicode),
    'http://www.w3.org/2001/XMLSchema#byte': (int, unicode),
    'http://www.w3.org/2001/XMLSchema#unsignedShort': (int, unicode),
    'http://www.w3.org/2001/XMLSchema#unsignedByte': (int, unicode),
    'http://www.w3.org/2001/XMLSchema#float': (float, unicode),
    'http://www.w3.org/2001/XMLSchema#double': (float, unicode),  # doesn't do the whole range
#    duration
#    dateTime
#    time
#    date
#    gYearMonth
#    gYear
#    gMonthDay
#    gDay
#    gMonth
#    hexBinary
    'http://www.w3.org/2001/XMLSchema#base64Binary': (base64.decodestring, lambda i:base64.encodestring(i)[:-1]),
    'http://www.w3.org/2001/XMLSchema#anyURI': (str, str),
}

if __name__ == "__main__":
    import doctest
    doctest.testmod()

