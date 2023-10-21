
from py2neo import Graph
g = Graph("http://localhost:7474", auth=('neo4j', '123456'))
b = "MATCH (m:yewu)-[r:money_yewu]->(n:money) where n.name='500' return m.name,r.name,n.name"
# b = "MATCH (m:yewu)-[r:yewu_contact]->(n:contact) where m.name='话费业务' return m.name,r.name,n.name"
data = g.run(b).data()
desc = [i['m.name'] for i in data]
subject = data[1]['n.name']
final_answer = '{0}可以办理的套餐有:{1}'.format(subject, ','.join(list(set(desc))))
print(data)
print(final_answer)