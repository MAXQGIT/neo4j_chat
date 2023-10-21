from py2neo import Graph, Node
import pandas as pd


class MedicalGraph:
    def __init__(self, data_path):
        self.data_path = data_path
        self.graph = Graph("http://localhost:7474", auth=('neo4j', '123456'))
        self.graph.delete_all()

    def read_nodes(self):
        data = pd.read_excel(self.data_path)
        names = data.name.values.tolist()
        moneys = [str(i) for i in data.money.values.tolist()]
        yewus = data.yewu.values.tolist()
        contacts = data.contact.values.tolist()

        name_yewu = []
        yewu_money = []
        yewu_contact = []

        liantong_infos = []
        for name, money, yewu, contact in zip(names, moneys, yewus, contacts):
            liantong = {}
            liantong['name'] = name
            liantong['money'] = money
            liantong['yewu'] = yewu
            liantong['contact'] = contact
            name_yewu.append([name, yewu])
            yewu_money.append([yewu, money])
            yewu_contact.append([yewu, contact])
            liantong_infos.append(liantong)

        return set(names), set(moneys), set(yewus), set(contacts), name_yewu, yewu_money, yewu_contact, liantong_infos

    def create_nodes(self, label, nodes):
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.graph.create(node)
        return

    def create_liantong_nodes(self, liantong_infos):

        for liantong_info in liantong_infos:
            node = Node('业务介绍', name=liantong_info['name'], yewu=liantong_info['yewu'],
                        money=liantong_info['money'], contact=liantong_info['contact'])
            self.graph.create(node)
        return

    def create_graph_nodes(self):
        names, moneys, yewus, contacts, name_yewu, yewu_money, yewu_contact, liantong_infos = self.read_nodes()
        self.create_liantong_nodes(liantong_infos)
        self.create_nodes('name', names)
        self.create_nodes('yewu', yewus)
        self.create_nodes('money', moneys)
        self.create_nodes('contact', contacts)

    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name = '%s' and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            self.graph.run(query)
        return

    def create_graphrels(self):
        names, moneys, yewus, contacts, name_yewu, yewu_money, yewu_contact, liantong_infos = self.read_nodes()

        self.create_relationship('yewu', 'money', yewu_money, 'money_yewu', '业务资费')
        self.create_relationship('name', 'yewu', name_yewu, 'name_yewu', '提供套餐')
        self.create_relationship('yewu', 'contact', yewu_contact, 'yewu_contact', '业务介绍')


    def save_data(self):
        names, moneys, yewus, contacts, name_yewu, yewu_money, yewu_contact, liantong_infos = self.read_nodes()

        f_name = open('data/name.txt', 'w+')
        f_yewu = open('data/yewu.txt', 'w+')
        f_money = open('data/money.txt', 'w+')
        f_contact = open('data/contact.txt', 'w+')

        f_name.write('\n'.join(names))
        f_yewu.write('\n'.join(yewus))
        f_money.write('\n'.join(moneys))
        f_contact.write('\n'.join(contacts))

        f_name.close()
        f_yewu.close()
        f_money.close()
        f_contact.close()


if __name__ == '__main__':
    data_path = 'yewu.xlsx'
    handler = MedicalGraph(data_path)
    handler.save_data()
    handler.create_graph_nodes()
    handler.create_graphrels()
