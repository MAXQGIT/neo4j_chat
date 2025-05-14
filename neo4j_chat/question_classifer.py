import ahocorasick


# pip install pyahocorasick

class QuestionClassifier():

    def __init__(self):
        self.names = [i.strip() for i in open('data/name.txt', 'r')]
        self.moneys = [str(i.strip()) for i in open('data/money.txt')]
        self.yewus = [i.strip() for i in open('data/yewu.txt')]
        self.contacts = [i.strip() for i in open('data/contact.txt')]
        self.words = set(self.names + self.moneys + self.yewus + self.contacts)
        # 可是考虑加入pypinyin 和相似词模型，词嵌入模型也可以考虑
        self.yewu_words = ['业务', '套餐']
        self.money_words = ['钱', '多贵', '多少钱', '几元', '价格']
        self.contact_words = ['内容', '包含', '都有', '包括']
        self.banli_words = ['办理', '购买', '买', '办']

    def build_actree(self, word):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(list(word)):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    def build_wdtype_dict(self):

        wd_dict = dict()
        for wd in self.words:
            wd_dict[wd] = []
            if wd in self.names:
                wd_dict[wd].append('name')
            if wd in self.yewus:
                wd_dict[wd].append('yewu')
            if wd in self.moneys:
                wd_dict[wd].append('money')
            if wd in self.contacts:
                wd_dict[wd].append('contact')
        return wd_dict

    def check_medical(self, question):
        region_tree = self.build_actree(self.words)
        wd_dict = self.build_wdtype_dict()
        region_wds = []
        for i in region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: wd_dict.get(i) for i in final_wds}

        return final_dict

    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False

    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)

        data['args'] = medical_dict
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_types = []
        # 提供套餐
        if self.check_words(self.yewu_words, question) and ('name' in types):
            question_type = 'name_yewu'
            question_types.append(question_type)

        # 业务多少钱
        if self.check_words(self.money_words, question) and ('yewu' in types):
            question_type = 'yewu_money'
            question_types.append(question_type)

        # 套餐内容
        if self.check_words(self.contact_words, question) and ('yewu' in types):
            question_type = 'yewu_contact'
            question_types.append(question_type)

        # 业务办理
        if self.check_words(self.banli_words, question) and ('money' in types):
            question_type = 'money_yewu'
            question_types.append(question_type)

        data['question_type'] = question_types

        return data


if __name__ == '__main__':
    data = QuestionClassifier().classify('500元可以办理什么套餐')
    print(data)
