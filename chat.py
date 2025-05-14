from question_classifer import *
from question_parser import *
from answer import *

class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '对不起，您问的问题，小机器人没学会，会尽快联系工程师让我学习的'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()

    question = '包年不限宽带多少钱'#input('咨询:')
    answer = handler.chat_main(question)
    print(answer)