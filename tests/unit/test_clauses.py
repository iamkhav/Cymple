import pytest
from cymple import QueryBuilder

qb = QueryBuilder()

rendered = {
    '_RESET_': qb.reset(),
    'CALL': qb.reset().call(),
    'CASE WHEN': qb.reset().match().node(ref_name='n').with_('n').case_when({'n.name': 'Bob'}, 'true', 'false', 'my_boolean'),
    'DELETE': qb.reset().match().node(ref_name='n').delete('n'),
    'DETACH DELETE': qb.reset().match().node(ref_name='n').detach_delete('n'),
    'WHERE (single)': qb.reset().match().node(ref_name='n').where('n.name', '=', 'value'),
    'WHERE (multiple)': qb.reset().match().node(ref_name='n').where_multiple({'n.name': 'value', 'n.age': 20}),
    'WHERE (literal)': qb.reset().match().node(ref_name='n').where_literal('NOT exists(n)'),
    'MATCH': qb.reset().match(),
    'MATCH OPTIONAL': qb.reset().match_optional(),
    'MERGE': qb.reset().merge(),
    'NODE': qb.reset().match().node(['label1', 'label2'], 'node', {'name': 'Bob'}),
    'NODE MERGE': qb.reset().merge().node(labels=['label1', 'label2'], ref_name='n', properties={'name': 'Bob'}).related_to().node(ref_name='m'),
    'OPERATOR': qb.reset().call().operator_start('SHORTESTPATH', 'p', '(:A)-[*]-(:B)').operator_end(),
    'RELATION (forward)': qb.reset().match().node().related_to().node(),
    'RELATION (backward)': qb.reset().match().node().related_from().node(),
    'RELATION (unidirectional)': qb.reset().match().node().related().node(),
    'RELATION (variable length)': qb.reset().match().node().related_variable_len(min_hops=1, max_hops=2).node(),
    'RELATION (variable length, empty)': qb.reset().match().node().related_variable_len().node(),
    'RETURN (literal)': qb.reset().match().node(ref_name='n').return_literal('n'),
    'RETURN (mapping)': qb.reset().match().node(ref_name='n').return_mapping(('n.name', 'name')),
    'RETURN (mapping, list)': qb.reset().match().node(ref_name='n').return_mapping([('n.name', 'name'), ('n.age', 'age')]),
    'SET': qb.reset().merge().node(ref_name='n').set({'n.name': 'Alice'}),
    'SET (not escaping)': qb.reset().merge().node(ref_name='n').set({'n.name': 'n.name + "!"'}, escape_values=False),
    'ON CREATE': qb.reset().merge().node(ref_name='n').on_create().set({'n.name': 'Bob'}),
    'ON MATCH': qb.reset().merge().node(ref_name='n').on_match().set({'n.name': 'Bob'}),
    'ON CREATE ON MATCH': qb.reset().merge().node(ref_name='n').on_create().set({'n.name': 'Bob'}).on_match().set({'n.name': 'Alice'}),
    'ON MATCH ON CREATE': qb.reset().merge().node(ref_name='n').on_match().set({'n.name': 'Bob'}).on_create().set({'n.name': 'Alice'}),
    'UNWIND': qb.reset().match().node(ref_name='n').with_('n').unwind('n'),
    'WITH': qb.reset().match().node(ref_name='a').with_('a,b'),
    'YIELD': qb.reset().call().operator_start('SHORTESTPATH', 'p', '(:A)-[*]-(:B)').operator_end().yield_(('length(p)', 'len')),
    'YIELD (list)': qb.reset().call().operator_start('SHORTESTPATH', 'p', '(:A)-[*]-(:B)').operator_end().yield_([('length(p)', 'len'), ('relationships(p)', 'rels')]),
    'LIMIT': qb.reset().match().node(ref_name='n').return_literal('n').limit(1),
    'LIMIT (expression)': qb.reset().match().node(ref_name='n').return_literal('n').limit("1 + toInteger(3 * rand())"),
    'LIMIT (with)': qb.reset().match().node(ref_name='n').with_('n').limit(1),
    'LIMIT (with set)': qb.reset().match().node(ref_name='n').with_('n').limit(1).set({'n.name': 'Bob'}),
    'CYPHER': qb.reset().match().node(ref_name='n').cypher("my cypher").limit(1),
    'SKIP': qb.reset().match().node(ref_name='n').return_literal('n').skip(1),
    'SKIP (expression)': qb.reset().match().node(ref_name='n').return_literal('n').skip("1 + toInteger(3 * rand())"),
    'SKIP (with)': qb.reset().match().node(ref_name='n').with_('n').skip(1),
    'SKIP (with set)': qb.reset().match().node(ref_name='n').with_('n').skip(1).set({'n.name': 'Bob'}),
    'ORDER BY': qb.match().node(ref_name='n').return_literal('n.name, n.age').order_by("elementId(n)"),
    'ORDER BY (List)': qb.match().node(ref_name='n').return_literal('n.name, n.age').order_by(
        ["n.name", "keys(n)"]),
    'ORDER BY (Desc)': qb.match().node(ref_name='n').return_literal('n.name, n.age').order_by("n.name", False),
    'CREATE': qb.reset().create().node(ref_name='n').return_literal('n'),
    'REMOVE': qb.reset().match().node(ref_name='n').remove('n.name').return_literal('n.age, n.name'),
    'REMOVE (list)': qb.reset().match().node(ref_name='n').remove(['n.age', 'n.name']).return_literal('n.age, n.name')

}

expected = {
    '_RESET_': '',
    'CALL': 'CALL',
    'CASE WHEN': 'MATCH (n) WITH n CASE WHEN n.name = "Bob" THEN true ELSE false END as my_boolean',
    'DELETE': 'MATCH (n) DELETE n',
    'DETACH DELETE': 'MATCH (n) DETACH DELETE n',
    'WHERE (single)': 'MATCH (n) WHERE n.name = "value"',
    'WHERE (multiple)': 'MATCH (n) WHERE n.name = "value" AND n.age = 20',
    'WHERE (literal)': 'MATCH (n) WHERE NOT exists(n)',
    'MATCH': 'MATCH',
    'MATCH OPTIONAL': 'OPTIONAL MATCH',
    'MERGE': 'MERGE',
    'NODE': 'MATCH (node: label1: label2 {name : "Bob"})',
    'NODE MERGE': 'MERGE (n: label1: label2 {name : "Bob"})-->(m)',
    'OPERATOR': 'CALL p = SHORTESTPATH( (:A)-[*]-(:B) )',
    'RELATION (forward)': 'MATCH ()-->()',
    'RELATION (backward)': 'MATCH ()<--()',
    'RELATION (unidirectional)': 'MATCH ()--()',
    'RELATION (variable length)': 'MATCH ()-[*1..2]-()',
    'RELATION (variable length, empty)': 'MATCH ()-[*]-()',
    'RETURN (literal)': 'MATCH (n) RETURN n',
    'RETURN (mapping)': 'MATCH (n) RETURN n.name as name',
    'RETURN (mapping, list)': 'MATCH (n) RETURN n.name as name, n.age as age',
    'SET': 'MERGE (n) SET n.name = "Alice"',
    'SET (not escaping)': 'MERGE (n) SET n.name = n.name + "!"',
    'ON CREATE': 'MERGE (n) ON CREATE SET n.name = "Bob"',
    'ON MATCH': 'MERGE (n) ON MATCH SET n.name = "Bob"',
    'ON CREATE ON MATCH': 'MERGE (n) ON CREATE SET n.name = "Bob" ON MATCH SET n.name = "Alice"',
    'ON MATCH ON CREATE': 'MERGE (n) ON MATCH SET n.name = "Bob" ON CREATE SET n.name = "Alice"',
    'UNWIND': 'MATCH (n) WITH n UNWIND n',
    'WITH': 'MATCH (a) WITH a,b',
    'YIELD': 'CALL p = SHORTESTPATH( (:A)-[*]-(:B) ) YIELD length(p) as len',
    'YIELD (list)': 'CALL p = SHORTESTPATH( (:A)-[*]-(:B) ) YIELD length(p) as len, relationships(p) as rels',
    'LIMIT': 'MATCH (n) RETURN n LIMIT 1',
    'LIMIT (expression)': 'MATCH (n) RETURN n LIMIT 1 + toInteger(3 * rand())',
    'LIMIT (with)': 'MATCH (n) WITH n LIMIT 1',
    'LIMIT (with set)': 'MATCH (n) WITH n LIMIT 1 SET n.name = "Bob"',
    'CYPHER': 'MATCH (n) my cypher LIMIT 1',
    'SKIP': 'MATCH (n) RETURN n SKIP 1',
    'SKIP (expression)': 'MATCH (n) RETURN n SKIP 1 + toInteger(3 * rand())',
    'SKIP (with)': 'MATCH (n) WITH n SKIP 1',
    'SKIP (with set)': 'MATCH (n) WITH n SKIP 1 SET n.name = "Bob"',
    'ORDER BY': 'MATCH (n) RETURN n.name, n.age ORDER BY elementId(n) ASC',
    'ORDER BY (List)': 'MATCH (n) RETURN n.name, n.age ORDER BY n.name, keys(n) ASC',
    'ORDER BY (Desc)': 'MATCH (n) RETURN n.name, n.age ORDER BY n.name DESC',
    'CREATE': 'CREATE (n) RETURN n',
    'REMOVE': 'MATCH (n) REMOVE n.name RETURN n.age, n.name',
    'REMOVE (list)': 'MATCH (n) REMOVE n.age, n.name RETURN n.age, n.name'
}


@pytest.mark.parametrize('clause', expected)
def test_case(clause: str):
    assert str(rendered[clause]) == expected[clause]
