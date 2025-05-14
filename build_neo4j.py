from neo4j import GraphDatabase, RoutingControl
import pandas as pd

#neo4j console
def delete_all(driver):
    driver.execute_query('MATCH (n) DETACH DELETE n')  # 删除数据库中所有数据


def create_code(driver, label, label_name, name):
    # 创建节点
    driver.execute_query('MERGE (%s: %s {name: $name})' % (label, label_name),
                         name=name)


def create_code_relastion(driver, start_label_name, start_name, relation, end_label_name,
                          end_name,contact):
    query = 'MERGE (start_label:%s {name: $start_name}) MERGE (end_label:%s {name: $end_name,contact:$contact}) MERGE (start_label)-[:%s]->(end_label)' % (
        start_label_name, end_label_name, relation)
    driver.execute_query(query, start_name=start_name, end_name=end_name,contact=contact)


def create_relastion(driver, start_label_name, start_name, relation, end_label_name, end_name):
    query = 'MATCH (start_label:%s {name:$start_name}),(end_label:%s {name:$end_name})  CREATE (start_label)-[r:%s]->(end_label)' % (
        start_label_name, end_label_name, relation)
    driver.execute_query(query, start_name=start_name, end_name=end_name)


def query_information(label_name, relationship, name,start_name,):
    query = 'MATCH (start_label:%s)-[r:%s]->(end_label:%s) where end_label.name ="%s"  RETURN start_label.name' % (
        label_name, relationship, name,start_name)
    records, _, _ = driver.execute_query(query, database_="neo4j", routing_=RoutingControl.READ)
    return records


def save_text(data,name):
    with open('data/{}.txt'.format(name),'w',encoding='gbk') as w:
        for word in data[name]:
            w.write(str(word))
            w.write('\n')


if __name__ == '__main__':
    uri = 'bolt://127.0.0.1:7687'
    auth = ('neo4j', '123456789')
    driver = GraphDatabase.driver(uri, auth=auth)
    delete_all(driver)  # 删除数据库中所有数据
    data = pd.read_excel('yewu.xlsx')
    print(data)
    for name,money,yewu,contact in zip(data['name'],data['money'],data['yewu'],data['contact']):
        create_code_relastion(driver,'公司',name,'套餐','套餐名称',yewu,contact)
        create_code_relastion(driver, '套餐名称', yewu,'费用','价格',str(money),'无')
        # create_code_relastion(driver, '套餐名称', yewu, '内容', '套餐内容', contact)
    for name in data.columns:
        save_text(data,name)

    # for name in ["Guinevere", "Lancelot", "Merlin"]:
    #     create_code_relastion(driver, 'person', 'Arthur',
    #                           'knows', 'person', name)
    # create_relastion(driver, 'person', 'Guinevere',
    #                  'like', 'person', 'Lancelot')
    records = query_information('套餐名称', '费用', '价格',500)
    for record in records:
        print(record)
        print(record['start_label.name'])
        # print(record['end_label.name'])
        print('~~'*50)
