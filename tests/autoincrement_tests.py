#! /usr/bin/env python
import sys, os.path

from sparqldb import dbapi
import unittest

test_create_table_syntax = """CREATE TABLE survey (
    id serial NOT NULL PRIMARY KEY,
    user_id integer NOT NULL,
    question_id integer NOT NULL,
    freetext_answer varchar(20) NOT NULL
);
"""

test_autoinsert_syntax = "INSERT INTO survey(user_id, question_id, freetext_answer) VALUES(4, 9, 'response 1')"
test_autoinsert_syntax2 = "INSERT INTO survey(user_id, question_id, freetext_answer) VALUES(5, 8, 'response 1')"

class autoincrementSuite(unittest.TestCase):
	def setUp(self):
		#create, insert three records
		self.conn = dbapi.connect(uri="http://example.org/testdb/", create=True)
		cur = self.conn.cursor()
		#create a table
		cur.execute(test_create_table_syntax)

	def testLastRowID(self):
		cur = self.conn.cursor()
		cur.execute(test_autoinsert_syntax)
		self.assertEqual(1, cur.lastrowid)
		cur.execute(test_autoinsert_syntax2)
		self.assertEqual(2, cur.lastrowid)

	def testSelectFirstInserted(self):
		cur = self.conn.cursor()
		cur.execute(test_autoinsert_syntax)
		cur.execute("SELECT id, user_id FROM survey WHERE id = 1")
		row = cur.fetchone()
		self.assertEqual(1, row[0])
		self.assertEqual(4, row[1])
		
	def testSelectLastInserted(self):
		cur = self.conn.cursor()
		cur.execute(test_autoinsert_syntax2)
		cur.execute(test_autoinsert_syntax)
		cur.execute("SELECT id, user_id FROM survey WHERE id = %s" % cur.lastrowid)
		row = cur.fetchone()
		self.assertEqual(2, row[0])
		self.assertEqual(4, row[1])

if __name__ == "__main__":
	unittest.main()

