from neo4j import GraphDatabase, RoutingControl

# def query_information(label_name, relationship, name,start_name,):
#     query = 'MATCH (start_label:%s)-[r:%s]->(end_label:%s) where start_label.name ="%s"  RETURN end_label.name' % (
#         label_name, relationship, name,start_name)
#     records, _, _ = driver.execute_query(query, database_="neo4j", routing_=RoutingControl.READ)
#     return records

class AnswerSearcher:
    def __init__(self):
        uri = 'bolt://127.0.0.1:7687'
        auth = ('neo4j', '123456789')
        self.driver = GraphDatabase.driver(uri, auth=auth)
        self.num_limit = 20

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'name_yewu':
            desc = [i['end_label.name'] for i in answers]
            subject = answers[0]['start_label.name']
            final_answer = '{0}提供的套餐有：{1}'.format(subject, '；'.join(list(set(desc))))
        if question_type == 'money_yewu':#####
            desc = [i['start_label.name'] for i in answers]
            subject = answers[0]['end_label.name']
            final_answer = '{0}元可以办理的套餐:{1}'.format(subject, ':'.join(list(set(desc))))
        if question_type == 'yewu_contact':
            desc = [i['start_label']['contact'] for i in answers]
            subject = answers[0]['start_label']['name']
            final_answer = '{0}的内容包含:{1}'.format(subject, ':'.join(list(set(desc))))

        if question_type == 'yewu_money':
            desc = [i['end_label.name'] for i in answers]
            subject = answers[0]['start_label.name']
            final_answer = '{0}套餐价格是:{1}元'.format(subject, ','.join(list(set(desc))[:self.num_limit]))

        return final_answer

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']

            answers = []
            for query in queries:
                # print('想要的结果',query)
                records, _, _ = self.driver.execute_query(query, database_="neo4j", routing_=RoutingControl.READ)
                answers += records

            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

# if __name__=='__main__':
