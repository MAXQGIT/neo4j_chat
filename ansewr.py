from py2neo import Graph


class AnswerSearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474", auth=('neo4j', '123456'))
        self.num_limit = 20

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'name_yewu':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}提供的套餐有：{1}'.format(subject, '；'.join(list(set(desc))))
        if question_type == 'money_yewu':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的价格是:{1}'.format(subject, ':'.join(list(set(desc))))
        if question_type == 'yewu_contact':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的内容包含:{1}'.format(subject, ':'.join(list(set(desc))))

        if question_type == 'yewu_money':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}可以办理的套餐有:{1}'.format(subject, ','.join(list(set(desc))[:self.num_limit]))

        return final_answer

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']

            answers = []
            for query in queries:
                # print('想要的结果',query)
                ress = self.g.run(query).data()
                answers += ress

            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

# if __name__=='__main__':
