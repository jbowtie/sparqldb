#! /usr/bin/env python
import sys, os.path

from sparqldb import dbapi
import unittest, testdb

test_create_user_table = """CREATE TABLE account (
    id serial NOT NULL PRIMARY KEY,
    name varchar(20) NOT NULL
);
"""

test_create_tx_table = """CREATE TABLE tx (
    id serial NOT NULL PRIMARY KEY,
    account integer NOT NULL REFERENCES account(id),
    amount integer NOT NULL
);
"""


test_insert_checking = "INSERT INTO account(id, name) VALUES(1, 'checking')"
test_insert_saving = "INSERT INTO account(id, name) VALUES(2, 'saving')"
test_insert_checking_A = "INSERT INTO tx(id, account, amount) VALUES(1, 1, 100)"
test_insert_checking_B = "INSERT INTO tx(id, account, amount) VALUES(2, 1, 200)"
test_insert_checking_C = "INSERT INTO tx(id, account, amount) VALUES(3, 1, 300)"
test_insert_checking_D = "INSERT INTO tx(id, account, amount) VALUES(5, 1, 400)"
test_insert_saving_A = "INSERT INTO tx(id, account, amount) VALUES(4, 2, 150)"
test_insert_saving_B = "INSERT INTO tx(id, account, amount) VALUES(6, 2, 250)"

test_select_predicate_join = "SELECT name, tx.amount FROM account, tx WHERE tx.account = account.id"

class joinSuite(testdb.dbTestCase):
	def setUp(self):
		#create, insert three records
		self.conn = dbapi.connect(uri="http://example.org/testdb/", create=True)
		cur = self.conn.cursor()
		#create joined tables
		cur.execute(test_create_user_table)
		cur.execute(test_create_tx_table)
		#insert account records
		cur.execute(test_insert_checking)
		cur.execute(test_insert_saving)
		#insert tx records
		cur.execute(test_insert_checking_A)
		cur.execute(test_insert_checking_B)
		cur.execute(test_insert_checking_C)
		cur.execute(test_insert_checking_D)
		cur.execute(test_insert_saving_A)
		cur.execute(test_insert_saving_B)

	def testPredicateJoin(self):
		"""Join in where clause"""
		#self.conn.dump()
		print '+' * 20
		cur = self.conn.cursor()
		cur.execute(test_select_predicate_join)
		print cur.sparql
		results = cur.fetchall()
		print results
		self.assertEqual(6, len(results))

if __name__ == "__main__":
	unittest.main()

