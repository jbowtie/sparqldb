#! /usr/bin/env python

import RDF

test_data = """
<http://example.org/testdb/project/1/> <http://example.org/testdb/project_title> "Ponga.SPARQLDB" .
<http://example.org/testdb/project/2/> <http://example.org/testdb/project_title> "ShouldNotAppear" .
<http://example.org/testdb/story/1/> <http://example.org/testdb/story_project> <http://example.org/testdb/project/1/>.
<http://example.org/testdb/story/2/> <http://example.org/testdb/story_project> <http://example.org/testdb/project/1/>.
<http://example.org/testdb/story/1/> <http://example.org/testdb/story_title> "Testing" .
<http://example.org/testdb/story/1/> <http://example.org/testdb/story_desc> "This is the testing desc" .
<http://example.org/testdb/story/2/> <http://example.org/testdb/story_title> "Sample Story" .
<http://example.org/testdb/story/2/> <http://example.org/testdb/story_desc> "This is the sample story desc" .
<http://example.org/testdb/story/1/> <http://example.org/testdb/story_id> "1"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://example.org/testdb/story/2/> <http://example.org/testdb/story_id> "2" .
"""

test_query = """
PREFIX xsd:    <http://www.w3.org/2001/XMLSchema#>

SELECT ?desc, ?title, ?project_title
WHERE
{
        ?XXX <http://example.org/testdb/story_desc> ?desc.
        ?XXX <http://example.org/testdb/story_title> ?title.
        ?XXX <http://example.org/testdb/story_project> ?project.
        ?project <http://example.org/testdb/project_title> ?project_title.
        ?XXX <http://example.org/testdb/story_id> ?id.
        FILTER( ?id = xsd:integer("1") || ?id = "2" )
}
"""

test_construct = """
CONSTRUCT
{
        ?XXX <http://example.org/testdb/story_desc> ?desc.
        ?XXX <http://example.org/testdb/story_title> ?title.
        ?project <http://example.org/testdb/project_title> ?project_title.
}
WHERE
{
        ?XXX <http://example.org/testdb/story_project> ?project.
}
"""

test_construct_fake = """
SELECT ?XXX ?desc ?title ?project_title
WHERE
{
        ?XXX <http://example.org/testdb/story_desc> ?desc.
        ?XXX <http://example.org/testdb/story_title> ?title.
        ?XXX <http://example.org/testdb/story_project> ?project.
}
"""
# load test data into storage
s = RDF.MemoryStorage()
model = RDF.Model(s)
p = RDF.NTriplesParser()
p.parse_string_into_model(model, test_data, "http://example.org/testdb/")
#ser = RDF.NTriplesSerializer()
#ser.serialize_model_to_file('test.n3', model)

#sample delete
#story_2 = RDF.Statement(RDF.Node(uri_string='http://example.org/testdb/story/2/'), None, None)
#for s in model.find_statements(story_2):
#	del model[s]
q = RDF.SPARQLQuery(test_query)
results = q.execute(model)

print 'title \t\tdesc\t\t\t\tproject'
for dictresult in results:
    print dictresult['title'], '\t', dictresult['desc'], '\t', dictresult['project_title']

#q = RDF.SPARQLQuery(test_construct_fake)
#results = q.execute(model)
#print '=' * 20
#print 'title \t\tdesc\t\t\t\tproject'
#for dictresult in results:
#    print dictresult['XXX'], '\t', dictresult['title'], '\t', dictresult['desc'], '\t', dictresult['project_title']

