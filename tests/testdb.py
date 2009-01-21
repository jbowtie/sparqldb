import unittest
from sparqldb import dbapi

test_create_table_syntax = """CREATE TABLE survey (
    id serial NOT NULL PRIMARY KEY,
    user_id integer NOT NULL,
    question_id integer NOT NULL,
    freetext_answer varchar(20) NOT NULL
);
"""
test_insert_syntax = "INSERT INTO survey(id, user_id, question_id, freetext_answer) VALUES(1, 4, 9, 'response 1')"
test_insert_syntax2 = "INSERT INTO survey(id, user_id, question_id, freetext_answer) VALUES(2, 5, 8, 'response 2')"
test_insert_syntax3 = "INSERT INTO survey(id, user_id, question_id, freetext_answer) VALUES(3, 6, 7, 'response 3')"

def setup_test_db():
    print "Creating tests"
    conn = dbapi.connect(uri="http://example.org/testdb/", create=True)
    cur = conn.cursor()
    #create a table
    cur.execute(test_create_table_syntax)
    #insert 3 records
    #insert record 2 first to show up any ordering issues!
    cur.execute(test_insert_syntax2)
    cur.execute(test_insert_syntax)
    cur.execute(test_insert_syntax3)
    return conn
        
