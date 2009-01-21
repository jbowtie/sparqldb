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

test_insert_1 = "INSERT INTO survey(id, user_id, question_id, freetext_answer) VALUES(1, 4, 9, 'foo')"
test_insert_2 = "INSERT INTO survey(id, user_id, question_id, freetext_answer) VALUES(2, 5, 8, 'foo')"
test_insert_3 = "INSERT INTO survey(id, user_id, question_id, freetext_answer) VALUES(3, 6, 9, 'response 3')"

test_delete_single_record = "DELETE FROM survey WHERE id = 1"
test_delete_multiple_records = "DELETE FROM survey WHERE freetext_answer = 'foo'"
test_delete_all_records = "DELETE FROM survey"

class deleteSuite(unittest.TestCase):
	def setUp(self):
		#create, insert three records
		self.conn = dbapi.connect(uri="http://example.org/testdb/", create=True)
		cur = self.conn.cursor()
		#create a table
		cur.execute(test_create_table_syntax)
		cur.execute(test_insert_1)
		cur.execute(test_insert_2)
		cur.execute(test_insert_3)

	def testDeleteSingleRecord(self):
		cur = self.conn.cursor()
		cur.execute(test_delete_single_record)
		cur.execute("SELECT id, user_id FROM survey ORDER BY id")
		rows = cur.fetchall()
		self.assertEqual(2, len(rows))
		self.assertEqual(2, rows[0][0])
		self.assertEqual(5, rows[0][1])
		self.assertEqual(3, rows[1][0])
		self.assertEqual(6, rows[1][1])

	def testDeleteMultiRecords(self):
		cur = self.conn.cursor()
		cur.execute(test_delete_multiple_records)
		cur.execute("SELECT id, user_id FROM survey ORDER BY id")
		rows = cur.fetchall()
		self.assertEqual(1, len(rows))
		self.assertEqual(3, rows[0][0])
		self.assertEqual(6, rows[0][1])

	def testDeleteAllRecords(self):
		cur = self.conn.cursor()
		cur.execute(test_delete_all_records)
		cur.execute("SELECT id, user_id FROM survey ORDER BY id")
		rows = cur.fetchall()
		self.assertEqual(0, len(rows))
if __name__ == "__main__":
	unittest.main()

