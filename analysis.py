#! /usr/bin/env python
# vi:si:et:sw=4:sts=4:ts=4
# SQL-2003 parser
class TableSchema:
    def __init__(self, name):
        self.name = name
        self.pk = None
        self.columns = {}
        self.constraints = []
    def __repr__(self):
        return self.name
    def add_column(self, name, **kwargs):
        col = ColumnSchema(self.name, name)
        for kw, val in kwargs.iteritems():
            setattr(col, kw, val)
        self.columns[col.name] = col
    def __getitem__(self, key):
        return self.columns[key]
    def __contains__(self, key):
        return key in self.columns

class ColumnSchema:
	def __init__(self, table, name):
		self.table = table
		self.name = name
		self.is_pk = False
		self.reference = None
		self.rdf_type = None
    def __repr__(self):
        return "%s.%s" % (self.table, self.name)
    def references(self, fk):
        return self.reference == fk
		
class QueryAnalysis:
    def __init__(self, schema=[]):
        #self.schema = schema #list of TableSchema instances
        self.schema = dict([(s.name, s) for s in schema])
        self.tables = {} #map table_string: TableSchema
        self.columns = {} #map column_string: ColumnSchema
        self.joins = set()

    def resolveTableReferences(self, tableRefs):
        #first, the actual table name
        for ref in tableRefs:
            if isinstance(ref, tuple):
                name, alias = ref
            else:
                name, alias = ref, None
            if name in self.schema:
                self.tables[name] = self.schema[name]
                if alias:
                    self.tables[alias] = self.schema[name]

    def resolveColumnReferences(self, columns):
        for colname in columns:
            if isinstance(colname, tuple):
                col, alias = colname
            else:
                col, alias = colname, None
            if "." in col:
                tablename, column = col.split(".")
                table = self.tables[tablename]
            else:
                #loop through tables in schema....
                for t in set(self.tables.values()):
                    if col in t:
                        table = t
                        break
                column = col
            self.columns[col] = table[column]
            if alias:
                self.columns[alias] = table[column]

    def analyseComparisonPredicates(self, preds):
        for v1, pred, v2 in preds:
            v1 = self.columns[v1]
            v2 = self.columns[v2]
            if v1.references(v2):
                self.joins.add((v1.table, v1, v2.table))
            elif v2.references(v1):
                self.joins.add((v2.table, v2, v1.table))
            else:
                print v1, pred, v2, 'not a join'
            
def test():
	account = TableSchema('account')
	account.add_column('id', is_pk = True, rdf_type = "db.autoincrement")
	account.add_column('name', rdf_type = "xsd.string")
	
	tx = TableSchema('tx')
	tx.add_column('id', is_pk = True, rdf_type = 'db.autoincrement')
	tx.add_column('account', reference = account['id'])
	tx.add_column('amount', rdf_type = 'xsd.integer')
	
	schema = [account, tx]
	
	a = QueryAnalysis(schema)

	#select = "select name, amount as val from account a, tx where tx.account = a.id"
	tables = [('account', 'a'), 'tx']
	columns = ['name', ('amount', 'val'), 'tx.account', 'a.id']
	a.resolveTableReferences(tables)
	a.resolveColumnReferences(columns)
	print a.tables #= {'account': account, 'a': account, 'tx': tx}
	print a.columns #= {'name': account.name, 'amount': tx.amount, 'val': tx.amount, 'tx.account': tx.account, 'a.id': account.id}
	
	preds = [('tx.account', '=', 'a.id'), ('name', '=', 'amount')]
	a.analyseComparisonPredicates(preds)
	print a.joins
	
if __name__=="__main__":
    test()
