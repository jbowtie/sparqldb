# SPARQLdb should support all SQL-2003 standard types
# note the following conventions:
#  "boolean", not "bool"
#  "clob", not "text"
#  "timestamp", not "datetime" (TODO: verify this by reading section 6.1 of the standard!)
DATA_TYPES = {
#    'AutoField':                    'integer GENERATED ALWAYS AS IDENTITY', #correct, but need to update parser
    'AutoField':                    'integer', #will do until parser handles correct syntax
    'BooleanField':                 'boolean',
    'CharField':                    'varchar(%(maxlength)s)',
    'CommaSeparatedIntegerField':   'varchar(%(maxlength)s)',
    'DateField':                    'date',
    'DateTimeField':                'timestamp',
    'FileField':                    'varchar(100)',
    'FilePathField':                'varchar(100)',
    'FloatField':                   'numeric(%(max_digits)s, %(decimal_places)s)',
    'ImageField':                   'varchar(100)',
    'IntegerField':                 'integer',
    'IPAddressField':               'char(15)',
    'ManyToManyField':              None,
    'NullBooleanField':             'boolean',
    'OneToOneField':                'integer',
    'PhoneNumberField':             'varchar(20)',
    'PositiveIntegerField':         'integer unsigned',
    'PositiveSmallIntegerField':    'smallint unsigned',
    'SlugField':                    'varchar(%(maxlength)s)',
    'SmallIntegerField':            'smallint',
    'TextField':                    'clob',
    'TimeField':                    'time',
    'USStateField':                 'varchar(2)',
}
