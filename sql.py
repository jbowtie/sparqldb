#! /usr/bin/env python
# vi:si:et:sw=4:sts=4:ts=4
# SQL-2003 parser

from sqlgrammar import *
import itertools
import exceptions
from analysis import TableSchema

class ColumnDefinition:
    def __init__(self, name, pk=False):
        self.name = name
        self.pk = pk
        self.uri = None
class InsertRow:
    def __init__(self, table):
        self.table = table
        self.values = {}

class ColumnReference:
    def __init__(self, table, col, alias = None):
        self.table = table
        self.column = col
        self.alias = alias
    def variable_name(self):
        if self.alias:
            return self.alias
        elif self.table:
            return "%s_%s" % (self.table, self.column)
        return self.column.replace(".", "_")
    def evaluate(self, db_vals):
        return db_vals[self.variable_name()]
    def __repr__(self):
        return "COLUMN %s.%s" % (self.table,self.column)

class LiteralExpression:
    def __init__(self, value, alias):
        self.value = value
        self.alias = alias
    def variable_name(self):
        return None
    def evaluate(self, db_vals):
        return self.value
    def __repr__(self):
        return "%s AS %s" % (self.value, self.alias)

class OrTerms:
    def __init__(self, analysis):
        self.value_equivalence = []
        self.analysis = analysis
        self.value_comparison = []
        
class QueryAnalysis:
    def __init__(self):
        self.column_names = []
        self.column_alias = {}
        self.referenced_tables = []
        self.joins = []
        self.value_equivalence = []
        self.value_comparison = []
        self.predicates = []
        self.orTerms = []
        self.columns_to_return = []
        self.column_aliases = {}
        self.order_by = []
        self.limit = None
        self.offset = None
    def determine_table(self, col):
        return self.referenced_tables[0]
    def table_and_col(self, col):
        if "." in col:
            table, column = col.split(".")
        else:
            #consult schema to find out table name
            table, column = self.determine_table(col), col
        return table, column
        
    def build_column_symbols(self, schema):
        pass
        #for each table:
        # tables[table] = TableSchema(schema[table])
        # tables[alias] = tables[table]
        #for each column:
        #  if fully_qualified: table, column = col.split('.')
        #  table, column = disambiguate_column(col)
        # columns[col] = tables[table].columns[column]
        # columns[alias] = columns[col]

    def analyse_predicates(self):
        """
        sort conditions into the following categories:
            - col = literal <-- value equivalence
              col = col <-- explicit inner join
              col < literal <-- filter (<, >, <=, >=) on value
              between <-- 2x filter on value
        """
        for condition in self.predicates:
            # comparisons; just the first 3 at the moment
            if 'comparison_predicate' in condition:
                v1, operator, v2 = condition.comparison_predicate
                v1_type = 'LITERAL'
                v2_type = 'LITERAL'
                if v1 in self.column_names:
                    v1_type = 'COLUMN'
                    t,c = self.table_and_col(v1)
                    v1 = ColumnReference(t,c)
                if v2 in self.column_names:
                    v2_type = 'COLUMN'
                    t,c = self.table_and_col(v2)
                    v2 = ColumnReference(t,c)
                if operator == '=':
                    self.analyse_equivalence(v1,v2,v1_type,v2_type)
                else:
                    self.value_comparison.append((v1, operator, v2))
            elif 'in_predicate' in condition:
                self.analyse_in_pred(condition.in_predicate)                    
            else:
                print 'UNKNOWN', condition
        #print 'JOINS', self.joins
        #print 'VALUE', self.value_equivalence
        #print 'COMP', self.value_comparison
    def analyse_in_pred(self, predicate):
        t,c = self.table_and_col(predicate[0])
        v1 = ColumnReference(t,c)
        negate = False

        if predicate[1] == 'NOT':
            vals = predicate[3:]
            negate = True
        else:
            vals = predicate[2:]
            
        if len(vals) == 1:
            self.analyse_equivalence(v1,vals[0],'COLUMN','LITERAL')
        else:
            terms = OrTerms(self)
            for val in vals:
                terms.value_comparison.append((v1, "=", val))
            self.orTerms.append(terms)

    def analyse_equivalence(self, v1,v2,v1_type,v2_type):
        clause = self.analyse_equivalence_step(v1,v2,v1_type,v2_type)
        if v1_type == 'COLUMN' and v2_type == 'COLUMN':
            self.joins.append(clause)
        else:
            self.value_equivalence.append(clause)

    def analyse_equivalence_step(self, v1,v2,v1_type,v2_type):
        #detect col = col (join)
        if v1_type == 'COLUMN' and v2_type == 'COLUMN':
            return ('QUALIFIED',(v1.table, v1.column),(v2.table, v2.column))
        #detect literal = col (value equiv)
        elif v2_type == 'COLUMN' and v1_type == 'LITERAL':
            return ((v2.table, v2.column),v1)
        #TODO: detect literal = literal
        #assume col = literal
        else:
            return ((v1.table, v1.column),v2)

class SelectAnalysis(QueryAnalysis):
    pass

class UpdateAnalysis(QueryAnalysis):
    def __init__(self, select_rows, target_table):
        self.select_rows = select_rows
        self.target_table = target_table
        self.set_clauses = []

class DeleteAnalysis(QueryAnalysis):
    def __init__(self, select_rows):
        self.select_rows = select_rows

class SqlParser:
    def __init__(self):
        self.analysis = SelectAnalysis()
        self.joins = []

    def add_col_reference(self, s, loc, col):
        self.analysis.column_names.append(col[0])

    def add_col_alias(self, s, loc, cols):
        col = cols[0]
        if len(col) > 1:
            self.analysis.column_alias[col[1]] = col[0]

    def add_calc_expression(self, s, loc, tokens):
        if isinstance(tokens[0], int):
            print tokens

    def add_table_reference(self, s, loc, col):
        self.analysis.referenced_tables.append(col[0])

    def add_join(self, s, loc, col):
        self.joins.append(col)

    def add_condition(self, s, loc, col):
        self.analysis.predicates.append(col)


    def handle_insert(self):
        #print "parsing INSERT INTO"
        newRow = InsertRow(self.tokens.insert_statement.table_name)
        for col, val in itertools.izip(self.tokens.insert_statement.column_names, self.tokens.insert_statement.column_values):
            newRow.values[col] = val
        return newRow
        
    def handle_create_table(self):
        #print "parsing CREATE TABLE"
        table = TableSchema(self.tokens.create_table_statement.table_name)
        for col in self.tokens.create_table_statement.column_defs:
            if 'defined_column_name' in col:
                table.add_column(col.defined_column_name, is_pk = bool(col.primary_key));
                if 'foreign_key' in col:
                    table.columns[col.defined_column_name].reference = col.foreign_key
        return table

    def handle_select(self):
        query = self.tokens.query_statement

        for c in query.select_list:
            alias = None
            col = None
            if 'column_alias' in c:
                alias = c.column_alias
            if 'literal_value' in c:
                col = LiteralExpression(c.literal_value, alias)
            else:
                col = ColumnReference(None, c[0], alias)
            self.analysis.columns_to_return.append(col) #= [c[-1] for c in query.select_list if 'literal_value' not in c]
        self.analysis.column_aliases = dict([(c[1],c[0]) for c in query.select_list if len(c) == 2])
        self.analysis.analyse_predicates()
        if 'order_by_list' in self.tokens:
            for sort_spec in self.tokens.order_by_list:
                self.analysis.order_by.append((sort_spec.sort_key, sort_spec.ordering_spec or 'ASC'))
        if 'cursor_limit' in self.tokens:
            self.analysis.limit = self.tokens.cursor_limit
        if 'cursor_offset' in self.tokens:
            self.analysis.offset = self.tokens.cursor_offset
        return self.analysis

    def handle_delete(self):
        delete = self.tokens.delete_statement
        self.analysis.referenced_tables.append(delete.target_table)
        return DeleteAnalysis(select_rows = self.analysis)

    def handle_update(self):
        update = self.tokens.update_statement
        self.analysis.referenced_tables.append(update.target_table)
        updater = UpdateAnalysis(select_rows = self.analysis, target_table = update.target_table)
        updater.set_clauses = [(clause[0], clause[1]) for clause in update.set_clauses]
        return updater

    def parse(self, sql):
        self.analysis = SelectAnalysis()
        column_reference.setParseAction(self.add_col_reference)
        #derived_column.setParseAction(self.add_col_alias)
        table_name.setParseAction(self.add_table_reference)
        natural_joinr.setParseAction(self.add_join)
        qualified_joinr.setParseAction(self.add_join)
        boolean_primary.setParseAction(self.add_condition)
        #numeric_value_expression.setParseAction(self.add_calc_expression)
        try:
            self.tokens = sql_statement.parseString(sql)
        except ParseException, e:
            print "BAD SQL"
            print e.message
            print "-" * 30
            print sql
            raise
        if 'query_statement' in self.tokens:
            return self.handle_select()
        elif 'insert_statement' in self.tokens:
            return self.handle_insert()
        elif 'create_table_statement' in self.tokens:
            return self.handle_create_table()
        elif 'update_statement' in self.tokens:
            return self.handle_update()
        elif 'delete_statement' in self.tokens:
            return self.handle_delete()
        else:
            raise exceptions.StandardError("No handler for statement type!")

