class QuestionPaser:

    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    def sql_transfer(self, question_type, entities):
        sql = []
        if question_type == 'name_yewu':
            sql = [
                "MATCH (start_label:公司)-[r:套餐]->(end_label:套餐名称) where start_label.name = '{0}' return start_label.name,r.name,end_label.name".format(
                    i) for i in entities]
        if question_type == 'money_yewu':
            sql = [
                "MATCH (start_label:套餐名称)-[r:费用]->(end_label:价格) where end_label.name='{0}' return start_label.name,r.name,end_label.name".format(
                    i) for i in entities]
        if question_type == 'yewu_contact':
            sql = [
                "MATCH (start_label:套餐名称) where start_label.name='{0}' return start_label".format(i) for i in
                entities]
        if question_type == 'yewu_money':
            sql = [
                "MATCH (start_label:套餐名称)-[r:费用]->(end_label:价格) where start_label.name='{0}' return start_label.name,r.name,end_label.name".format(
                    i) for i in entities]

        return sql

    def parser_main(self, res_classify):
        args = res_classify['args']

        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_type']

        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type

            sql = []
            if question_type == 'name_yewu':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))
            if question_type == 'money_yewu':
                sql = self.sql_transfer(question_type, entity_dict.get('money'))
            if question_type == 'yewu_contact':
                sql = self.sql_transfer(question_type, entity_dict.get('yewu'))
            if question_type == 'yewu_money':
                sql = self.sql_transfer(question_type, entity_dict.get('yewu'))

            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)
        return sqls
