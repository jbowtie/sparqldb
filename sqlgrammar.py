#! /usr/bin/env python
# vi:si:et:sw=4:sts=4:ts=4
# SQL-2003 parser

from pyparsing import *

#reserved words in SQL-2003 standard - parse these as caseless keywords
ADD = CaselessKeyword("ADD")
ALL = CaselessKeyword("ALL")
ALLOCATE = CaselessKeyword("ALLOCATE")
ALTER = CaselessKeyword("ALTER")
AND = CaselessKeyword("AND")
ANY = CaselessKeyword("ANY")
ARE = CaselessKeyword("ARE")
ARRAY = CaselessKeyword("ARRAY")
AS = CaselessKeyword("AS")
ASENSITIVE = CaselessKeyword("ASENSITIVE")
ASYMMETRIC = CaselessKeyword("ASYMMETRIC")
AT = CaselessKeyword("AT")
ATOMIC = CaselessKeyword("ATOMIC")
AUTHORIZATION = CaselessKeyword("AUTHORIZATION")
BEGIN = CaselessKeyword("BEGIN")
BETWEEN = CaselessKeyword("BETWEEN")
BIGINT = CaselessKeyword("BIGINT")
BINARY = CaselessKeyword("BINARY")
BLOB = CaselessKeyword("BLOB")
BOOLEAN = CaselessKeyword("BOOLEAN")
BOTH = CaselessKeyword("BOTH")
BY = CaselessKeyword("BY")
CALL = CaselessKeyword("CALL")
CALLED = CaselessKeyword("CALLED")
CASCADED = CaselessKeyword("CASCADED")
CASE = CaselessKeyword("CASE")
CAST = CaselessKeyword("CAST")
CHAR = CaselessKeyword("CHAR")
CHARACTER = CaselessKeyword("CHARACTER")
CHECK = CaselessKeyword("CHECK")
CLOB = CaselessKeyword("CLOB")
CLOSE = CaselessKeyword("CLOSE")
COLLATE = CaselessKeyword("COLLATE")
COLUMN = CaselessKeyword("COLUMN")
COMMIT = CaselessKeyword("COMMIT")
CONNECT = CaselessKeyword("CONNECT")
CONSTRAINT = CaselessKeyword("CONSTRAINT")
CONTINUE = CaselessKeyword("CONTINUE")
CORRESPONDING = CaselessKeyword("CORRESPONDING")
CREATE = CaselessKeyword("CREATE")
CROSS = CaselessKeyword("CROSS")
CUBE = CaselessKeyword("CUBE")
CURRENT = CaselessKeyword("CURRENT")
CURRENT_DATE = CaselessKeyword("CURRENT_DATE")
CURRENT_DEFAULT_TRANSFORM_GROUP = CaselessKeyword("CURRENT_DEFAULT_TRANSFORM_GROUP")
CURRENT_PATH = CaselessKeyword("CURRENT_PATH")
CURRENT_ROLE = CaselessKeyword("CURRENT_ROLE")
CURRENT_TIME = CaselessKeyword("CURRENT_TIME")
CURRENT_TIMESTAMP = CaselessKeyword("CURRENT_TIMESTAMP")
CURRENT_TRANSFORM_GROUP_FOR_TYPE = CaselessKeyword("CURRENT_TRANSFORM_GROUP_FOR_TYPE")
CURRENT_USER = CaselessKeyword("CURRENT_USER")
CURSOR = CaselessKeyword("CURSOR")
CYCLE = CaselessKeyword("CYCLE")
DATE = CaselessKeyword("DATE")
DAY = CaselessKeyword("DAY")
DEALLOCATE = CaselessKeyword("DEALLOCATE")
DEC = CaselessKeyword("DEC")
DECIMAL = CaselessKeyword("DECIMAL")
DECLARE = CaselessKeyword("DECLARE")
DEFAULT = CaselessKeyword("DEFAULT")
DELETE = CaselessKeyword("DELETE")
DEREF = CaselessKeyword("DEREF")
DESCRIBE = CaselessKeyword("DESCRIBE")
DETERMINISTIC = CaselessKeyword("DETERMINISTIC")
DISCONNECT = CaselessKeyword("DISCONNECT")
DISTINCT = CaselessKeyword("DISTINCT")
DOUBLE = CaselessKeyword("DOUBLE")
DROP = CaselessKeyword("DROP")
DYNAMIC = CaselessKeyword("DYNAMIC")
EACH = CaselessKeyword("EACH")
ELEMENT = CaselessKeyword("ELEMENT")
ELSE = CaselessKeyword("ELSE")
END = CaselessKeyword("END")
END_EXEC = CaselessKeyword("END-EXEC")
ESCAPE = CaselessKeyword("ESCAPE")
EXCEPT = CaselessKeyword("EXCEPT")
EXEC = CaselessKeyword("EXEC")
EXECUTE = CaselessKeyword("EXECUTE")
EXISTS = CaselessKeyword("EXISTS")
EXTERNAL = CaselessKeyword("EXTERNAL")
FALSE = CaselessKeyword("FALSE")
FETCH = CaselessKeyword("FETCH")
FILTER = CaselessKeyword("FILTER")
FLOAT = CaselessKeyword("FLOAT")
FOR = CaselessKeyword("FOR")
FOREIGN = CaselessKeyword("FOREIGN")
FREE = CaselessKeyword("FREE")
FROM = CaselessKeyword("FROM")
FULL = CaselessKeyword("FULL")
FUNCTION = CaselessKeyword("FUNCTION")
GET = CaselessKeyword("GET")
GLOBAL = CaselessKeyword("GLOBAL")
GRANT = CaselessKeyword("GRANT")
GROUP = CaselessKeyword("GROUP")
GROUPING = CaselessKeyword("GROUPING")
HAVING = CaselessKeyword("HAVING")
HOLD = CaselessKeyword("HOLD")
HOUR = CaselessKeyword("HOUR")
IDENTITY = CaselessKeyword("IDENTITY")
IMMEDIATE = CaselessKeyword("IMMEDIATE")
IN = CaselessKeyword("IN")
INDICATOR = CaselessKeyword("INDICATOR")
INNER = CaselessKeyword("INNER")
INOUT = CaselessKeyword("INOUT")
INPUT = CaselessKeyword("INPUT")
INSENSITIVE = CaselessKeyword("INSENSITIVE")
INSERT = CaselessKeyword("INSERT")
INT = CaselessKeyword("INT")
INTEGER = CaselessKeyword("INTEGER")
INTERSECT = CaselessKeyword("INTERSECT")
INTERVAL = CaselessKeyword("INTERVAL")
INTO = CaselessKeyword("INTO")
IS = CaselessKeyword("IS")
ISOLATION = CaselessKeyword("ISOLATION")
JOIN = CaselessKeyword("JOIN")
LANGUAGE = CaselessKeyword("LANGUAGE")
LARGE = CaselessKeyword("LARGE")
LATERAL = CaselessKeyword("LATERAL")
LEADING = CaselessKeyword("LEADING")
LEFT = CaselessKeyword("LEFT")
LIKE = CaselessKeyword("LIKE")
LOCAL = CaselessKeyword("LOCAL")
LOCALTIME = CaselessKeyword("LOCALTIME")
LOCALTIMESTAMP = CaselessKeyword("LOCALTIMESTAMP")
MATCH = CaselessKeyword("MATCH")
MEMBER = CaselessKeyword("MEMBER")
MERGE = CaselessKeyword("MERGE")
METHOD = CaselessKeyword("METHOD")
MINUTE = CaselessKeyword("MINUTE")
MODIFIES = CaselessKeyword("MODIFIES")
MODULE = CaselessKeyword("MODULE")
MONTH = CaselessKeyword("MONTH")
MULTISET = CaselessKeyword("MULTISET")
NATIONAL = CaselessKeyword("NATIONAL")
NATURAL = CaselessKeyword("NATURAL")
NCHAR = CaselessKeyword("NCHAR")
NCLOB = CaselessKeyword("NCLOB")
NEW = CaselessKeyword("NEW")
NO = CaselessKeyword("NO")
NONE = CaselessKeyword("NONE")
NOT = CaselessKeyword("NOT")
NULL = CaselessKeyword("NULL")
NUMERIC = CaselessKeyword("NUMERIC")
OF = CaselessKeyword("OF")
OLD = CaselessKeyword("OLD")
ON = CaselessKeyword("ON")
ONLY = CaselessKeyword("ONLY")
OPEN = CaselessKeyword("OPEN")
OR = CaselessKeyword("OR")
ORDER = CaselessKeyword("ORDER")
OUT = CaselessKeyword("OUT")
OUTER = CaselessKeyword("OUTER")
OUTPUT = CaselessKeyword("OUTPUT")
OVER = CaselessKeyword("OVER")
OVERLAPS = CaselessKeyword("OVERLAPS")
PARAMETER = CaselessKeyword("PARAMETER")
PARTITION = CaselessKeyword("PARTITION")
PRECISION = CaselessKeyword("PRECISION")
PREPARE = CaselessKeyword("PREPARE")
PRIMARY = CaselessKeyword("PRIMARY")
PROCEDURE = CaselessKeyword("PROCEDURE")
RANGE = CaselessKeyword("RANGE")
READS = CaselessKeyword("READS")
REAL = CaselessKeyword("REAL")
RECURSIVE = CaselessKeyword("RECURSIVE")
REF = CaselessKeyword("REF")
REFERENCES = CaselessKeyword("REFERENCES")
REFERENCING = CaselessKeyword("REFERENCING")
RELEASE = CaselessKeyword("RELEASE")
RETURN = CaselessKeyword("RETURN")
RETURNS = CaselessKeyword("RETURNS")
REVOKE = CaselessKeyword("REVOKE")
RIGHT = CaselessKeyword("RIGHT")
ROLLBACK = CaselessKeyword("ROLLBACK")
ROLLUP = CaselessKeyword("ROLLUP")
ROW = CaselessKeyword("ROW")
ROWS = CaselessKeyword("ROWS")
SAVEPOINT = CaselessKeyword("SAVEPOINT")
SCROLL = CaselessKeyword("SCROLL")
SEARCH = CaselessKeyword("SEARCH")
SECOND = CaselessKeyword("SECOND")
SELECT = CaselessKeyword("SELECT")
SENSITIVE = CaselessKeyword("SENSITIVE")
SESSION_USER = CaselessKeyword("SESSION_USER")
SET = CaselessKeyword("SET")
SIMILAR = CaselessKeyword("SIMILAR")
SMALLINT = CaselessKeyword("SMALLINT")
SOME = CaselessKeyword("SOME")
SPECIFIC = CaselessKeyword("SPECIFIC")
SPECIFICTYPE = CaselessKeyword("SPECIFICTYPE")
SQL = CaselessKeyword("SQL")
SQLEXCEPTION = CaselessKeyword("SQLEXCEPTION")
SQLSTATE = CaselessKeyword("SQLSTATE")
SQLWARNING = CaselessKeyword("SQLWARNING")
START = CaselessKeyword("START")
STATIC = CaselessKeyword("STATIC")
SUBMULTISET = CaselessKeyword("SUBMULTISET")
SYMMETRIC = CaselessKeyword("SYMMETRIC")
SYSTEM = CaselessKeyword("SYSTEM")
SYSTEM_USER = CaselessKeyword("SYSTEM_USER")
TABLE = CaselessKeyword("TABLE")
THEN = CaselessKeyword("THEN")
TIME = CaselessKeyword("TIME")
TIMESTAMP = CaselessKeyword("TIMESTAMP")
TIMEZONE_HOUR = CaselessKeyword("TIMEZONE_HOUR")
TIMEZONE_MINUTE = CaselessKeyword("TIMEZONE_MINUTE")
TO = CaselessKeyword("TO")
TRAILING = CaselessKeyword("TRAILING")
TRANSLATION = CaselessKeyword("TRANSLATION")
TREAT = CaselessKeyword("TREAT")
TRIGGER = CaselessKeyword("TRIGGER")
TRUE = CaselessKeyword("TRUE")
UNION = CaselessKeyword("UNION")
UNIQUE = CaselessKeyword("UNIQUE")
UNKNOWN = CaselessKeyword("UNKNOWN")
UNNEST = CaselessKeyword("UNNEST")
UPDATE = CaselessKeyword("UPDATE")
USER = CaselessKeyword("USER")
USING = CaselessKeyword("USING")
VALUE = CaselessKeyword("VALUE")
VALUES = CaselessKeyword("VALUES")
VARCHAR = CaselessKeyword("VARCHAR")
VARYING = CaselessKeyword("VARYING")
WHEN = CaselessKeyword("WHEN")
WHENEVER = CaselessKeyword("WHENEVER")
WHERE = CaselessKeyword("WHERE")
WINDOW = CaselessKeyword("WINDOW")
WITH = CaselessKeyword("WITH")
WITHIN = CaselessKeyword("WITHIN")
WITHOUT = CaselessKeyword("WITHOUT")
YEAR = CaselessKeyword("YEAR")

#non-reserved words in SQL-2003 standard
#we do these as literals instead of keywords
#I think this is significant, but need to work it out

plus  = Literal( "+" )
minus = Literal( "-" )
mult  = Literal( "*" )
div   = Literal( "/" )
equals = Literal("=")
not_equal = Literal("<>")
lte = Literal("<=")
gte = Literal(">=")
lt = Literal("<")
gt = Literal(">")
lpar  = Literal( "(" ).suppress()
rpar  = Literal( ")" ).suppress()
addop  = plus | minus
multop = mult | div

set_quantifier = DISTINCT | ALL

#numeric literals
E = CaselessLiteral("E")
arithSign = Word("+-",exact=1)
realNumber = Combine( Optional(arithSign) + ( Word( nums ) + "." + Optional( Word(nums) )  | ( "." + Word(nums) ) ) + Optional( E + Optional(arithSign) + Word(nums) ) )
intNumber = Combine( Optional(arithSign) + Word( nums ) + Optional( E + Optional(plus) + Word(nums) ) ).setParseAction( lambda s,l,t: [ int(t[0]) ] )

#operators
comparison_operator = equals | not_equal | lte | gte | lt | gt

#literals
truth_value = TRUE | FALSE | UNKNOWN
general_literal = truth_value | quotedString
unsigned_literal = realNumber | intNumber | general_literal

#basic identifier (valid column/table names)
#TODO:
# we'll need to extend this definition in two ways:
#   allow for quoted identifiers (is this *really* needed?)
#   allow for URI identifiers (for use with O/R mappers that recognise this backend)
#extended_uri_id = Literal("<") + Word(alphas, alphanums + ":/$_-.") + Literal(">")
extended_uri_id = QuotedString("<",  endQuoteChar=">") 
_standard_identifier = Word( alphas, alphanums + "_$" )
_sql_identifier = _standard_identifier | extended_uri_id
identifier = _sql_identifier.setName("identifier") #| extended_uri_id
identifier_chain = delimitedList(identifier, ".", combine=True)
column_reference = identifier_chain.setName("column_reference")

#value expressions
value_expression = Forward()
general_value_spec = USER | VALUE #|SYSTEM_USER|...
unsigned_value_spec = (unsigned_literal | general_value_spec).setResultsName("literal_value")
value_expression_primary_nopara = unsigned_value_spec | column_reference #|scalar|case|cast|...
value_expression_primary = (lpar + value_expression + rpar) | value_expression_primary_nopara
row_value_expression = value_expression_primary_nopara
boolean_value_expression = Forward()
numeric_value_expression = Forward()
common_value_expression = numeric_value_expression #|string_value_expression....
value_expression << common_value_expression | boolean_value_expression | row_value_expression

rvp = value_expression_primary_nopara #| row_value_constructor_predicand

#column names
column_alias = identifier.setResultsName("column_alias")
column_name = identifier.setResultsName("column_name")
derived_column = Group(Combine(value_expression) + Optional( Suppress(AS) + column_alias ))
select_sublist = derived_column #| qualified_asterisk

#tables names
table_name = identifier
table_alias = identifier
table_reference = Forward()
only_spec = ONLY + lpar + table_name + rpar
derived_column_list = lpar + delimitedList(column_name) + rpar
joined_table = Forward()
table_primary = table_name  + Optional( Group(AS + table_alias) ) | only_spec | lpar + joined_table + rpar #|derived_table
join_type = INNER | (oneOf("LEFT RIGHT FULL") + Optional(OUTER))
join_spec = ON + boolean_value_expression# | USING (...)
cross_joinr = CROSS + JOIN + table_primary
qualified_joinr = Optional(join_type) + JOIN + table_reference + join_spec
natural_joinr = NATURAL + Optional(join_type) + JOIN + table_primary
union_joinr = UNION + JOIN + table_primary
cross_join = table_reference + cross_joinr
qualified_join = table_reference + qualified_joinr
natural_join = table_reference + natural_joinr
union_join = table_reference + union_joinr

joined_table << (cross_join | qualified_join | natural_join | union_join)
table_primary_or_join = table_primary + ZeroOrMore( cross_joinr | qualified_joinr | natural_joinr | union_joinr )
sample_method = Keyword("BERNOULLI") | Keyword("SYSTEM")
repeat_argument = numeric_value_expression
sample_percentage = numeric_value_expression
repeatable_clause = Keyword("REPEATABLE") + lpar + repeat_argument + rpar
sample_clause = Keyword("TABLESAMPLE") + sample_method + lpar + sample_percentage + rpar + Optional(repeatable_clause)
table_reference << table_primary_or_join #+ Optional(sample_clause)
from_clause = FROM + Group(delimitedList(table_reference)).setResultsName("tables")

#predicates (where expressions)
comparison_predicate = (rvp + comparison_operator + rvp).setResultsName("comparison_predicate")
between_predicate = ( rvp + Optional(NOT) + BETWEEN + rvp + AND + rvp).setResultsName("between_predicate")
in_predicate = ( rvp + Optional(NOT) + IN + lpar + delimitedList(row_value_expression) + rpar).setResultsName("in_predicate")
predicate = comparison_predicate | between_predicate | in_predicate #| like | similar | null | quant_comp | exists | unique | normalised | match | overlaps | distinct | member | submultiset | set | type

#numeric expressions
numeric_primary = value_expression_primary_nopara #|numeric_value_function
numeric_factor = Optional(arithSign) + numeric_primary
numeric_term = numeric_factor + ZeroOrMore( ( multop + numeric_factor ) )
numeric_value_expression << numeric_term + ZeroOrMore( ( addop + numeric_term ))

#boolean expressions
boolean_primary = predicate | lpar + boolean_value_expression + rpar
boolean_test = boolean_primary + Optional(IS + Optional(NOT) + truth_value)
boolean_factor = Optional(NOT) + boolean_test
boolean_term = delimitedList(boolean_factor, AND)
boolean_value_expression << delimitedList(boolean_term, OR)

#sort specification
ordering_specification = (CaselessKeyword("ASC") | CaselessKeyword("DESC")).setResultsName("ordering_spec")
sort_specification = Group(value_expression.setResultsName("sort_key") + Optional(ordering_specification)).setResultsName("sort_spec")
sort_specification_list = delimitedList(sort_specification).setResultsName("order_by_list")

#select subclauses
where_clause = WHERE + boolean_value_expression.setResultsName("where_clause")
group_by_clause = GROUP + BY #TODO - what follows??
having_clause = HAVING + boolean_value_expression
window_clause = CaselessKeyword("WINDOW")
order_by_clause = ORDER + BY + sort_specification_list
#updatability_clause = CaselessKeyword("FOR") + (Literal("READ ONLY") | (CaselessKeyword("UPDATE") + Optional(CaselessKeyword("OF") + column_name_list)))

#LIMIT and OFFSET are not part of SQL-2003
nonstandard_limit_clause = CaselessKeyword("LIMIT") + intNumber.setResultsName("cursor_limit")
nonstandard_offset_clause = CaselessKeyword("OFFSET") + intNumber.setResultsName("cursor_offset")

#select query
table_expression = from_clause + Optional(where_clause) + Optional(group_by_clause) + Optional(having_clause) + Optional(window_clause)
select_list = Group(delimitedList(select_sublist)).setResultsName("select_list")
query_statement = Group(SELECT + Optional(set_quantifier) + select_list + table_expression).setResultsName('query_statement')
cursor_specification = query_statement + Optional(order_by_clause) + Optional(nonstandard_limit_clause) + Optional(nonstandard_offset_clause)#+ Optional(updatability_clause)

#create table query
numeric_type = (INTEGER | INT | SMALLINT | BIGINT | CaselessKeyword("serial")) + Optional(CaselessKeyword("UNSIGNED")) ##FIXME: see if unsigned in spec
character_string_type_keyword = (CHARACTER + VARYING) | (CHAR + VARYING) | VARCHAR | CHAR | CHARACTER
character_long_string_type = CLOB | CaselessKeyword("CHAR LARGE OBJECT") | CaselessKeyword("CHARACTER LARGE OBJECT")
character_string_type = character_string_type_keyword + Literal("(") + Word(nums).setResultsName("length") + Literal(")")
boolean_type = BOOLEAN
datetime_type = DATE | TIME | TIMESTAMP
predefined_type = character_long_string_type | character_string_type | numeric_type |boolean_type |datetime_type #|interval
data_type = predefined_type #|row_type...
unique_specification = UNIQUE | (PRIMARY + CaselessLiteral("KEY")).setResultsName("primary_key")
references_specification = REFERENCES + (table_name + lpar + delimitedList(column_name) + rpar).setResultsName("foreign_key")
column_constraint_definition = NULL | (NOT + NULL) | unique_specification | references_specification
column_definition = Group(column_name.setResultsName("defined_column_name") + Optional(data_type) + ZeroOrMore(column_constraint_definition))
unique_constraint_definition = UNIQUE + lpar + delimitedList(column_name) + rpar
table_constraint = unique_constraint_definition
table_element = table_constraint.setResultsName("table_constraint") | column_definition
table_definition = table_name.setResultsName("table_name") + lpar + delimitedList(table_element).setResultsName("column_defs") + rpar
create_table_statement = Group(CREATE + TABLE + table_definition).setResultsName('create_table_statement')

#insert statement
from_constructor = Optional(lpar + delimitedList(column_name).setResultsName("column_names") + rpar) + VALUES + lpar + delimitedList(row_value_expression).setResultsName("column_values") + rpar
insert_columns_and_source = from_constructor# |from subquery | from default
insert_statement = Group(INSERT + INTO + table_name.setResultsName("table_name") + insert_columns_and_source).setResultsName('insert_statement')

#update statement
target_table = table_name.setResultsName("target_table")
update_source = value_expression
update_target = column_name
set_clause = Group(update_target + equals.suppress() + update_source)
update_statement = Group(UPDATE + target_table + SET + delimitedList(set_clause).setResultsName("set_clauses") + Optional(where_clause)).setResultsName('update_statement')

#delete statement
delete_statement = Group(DELETE + FROM + target_table + Optional(where_clause)).setResultsName("delete_statement")

#all supported statements
sql_statement = (cursor_specification | create_table_statement | insert_statement | update_statement | delete_statement) + Optional(Suppress(";"))


if __name__=="__main__":
    print identifier.parseString("foo")
    print identifier.parseString("<http://foo.com>")
    print table_name.parseString("foo")
    print target_table.parseString("foo")
    print target_table.parseString("<http://foo.com>")
    print delete_statement.parseString("DELETE FROM foo")
    print create_table_statement.parseString("CREATE TABLE foo (bar)")
    print insert_statement.parseString("INSERT INTO survey (id, user_id, question_id, freetext_answer) VALUES (1, 4, 9, 'foo')")
    print sql_statement.parseString("insert into foo (bar) values (1);")
    print sql_statement.parseString("select survey.user_id, survey.freetext_answer as answer from survey order by user_id limit 1")
