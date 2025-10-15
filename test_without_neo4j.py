#!/usr/bin/env python3
# coding: utf-8
# 测试版本 - 不使用Neo4j数据库

import json
import os
from question_classifier import QuestionClassifier
from question_parser import QuestionPaser

class MockAnswerSearcher:
    """模拟答案搜索器，用于测试"""
    def __init__(self):
        self.num_limit = 20
        # 加载医疗数据
        self.medical_data = self.load_medical_data()
    
    def load_medical_data(self):
        """加载医疗数据"""
        data_path = os.path.join(os.path.dirname(__file__), 'data/medical.json')
        medical_data = {}
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        disease_data = json.loads(line)
                        medical_data[disease_data['name']] = disease_data
        except Exception as e:
            print(f"加载医疗数据失败: {e}")
        return medical_data
    
    def search_main(self, sqls):
        """模拟搜索主函数"""
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            
            # 从医疗数据中查找答案
            for query in queries:
                # 简单的字符串匹配来查找疾病
                disease_name = self.extract_disease_name_from_query(query)
                if disease_name and disease_name in self.medical_data:
                    disease_data = self.medical_data[disease_name]
                    answers.append(self.format_disease_data(disease_data, question_type))
            
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers
    
    def extract_disease_name_from_query(self, query):
        """从查询中提取疾病名称"""
        # 简单的字符串匹配
        if "m.name = '" in query:
            start = query.find("m.name = '") + 10
            end = query.find("'", start)
            return query[start:end]
        return None
    
    def format_disease_data(self, disease_data, question_type):
        """格式化疾病数据"""
        if question_type == 'disease_symptom':
            return {
                'm.name': disease_data['name'],
                'n.name': disease_data.get('symptom', [])
            }
        elif question_type == 'disease_cause':
            return {
                'm.name': disease_data['name'],
                'm.cause': disease_data.get('cause', '')
            }
        elif question_type == 'disease_desc':
            return {
                'm.name': disease_data['name'],
                'm.desc': disease_data.get('desc', '')
            }
        else:
            return {
                'm.name': disease_data['name'],
                'm.desc': disease_data.get('desc', '')
            }
    
    def answer_prettify(self, question_type, answers):
        """美化答案格式"""
        if not answers:
            return ''
        
        if question_type == 'disease_symptom':
            if answers and 'n.name' in answers[0]:
                symptoms = answers[0]['n.name']
                if isinstance(symptoms, list):
                    subject = answers[0]['m.name']
                    return f'{subject}的症状包括：{"；".join(symptoms[:self.num_limit])}'
        
        elif question_type == 'disease_cause':
            if answers and 'm.cause' in answers[0]:
                cause = answers[0]['m.cause']
                subject = answers[0]['m.name']
                return f'{subject}可能的成因有：{cause}'
        
        elif question_type == 'disease_desc':
            if answers and 'm.desc' in answers[0]:
                desc = answers[0]['m.desc']
                subject = answers[0]['m.name']
                return f'{subject},熟悉一下：{desc}'
        
        return '抱歉，我暂时无法回答这个问题。'

class MockChatBotGraph:
    """模拟聊天机器人"""
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = MockAnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是小勇医药智能助理，希望可以帮到您。如果没答上来，可联系https://liuhuanyong.github.io/。祝您身体棒棒！'
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
    print("正在初始化医疗知识图谱问答系统...")
    handler = MockChatBotGraph()
    print("系统初始化完成！")
    print("=" * 50)
    
    # 测试问题
    test_questions = [
        "乳腺癌的症状有哪些？",
        "糖尿病",
        "为什么有的人会失眠？",
        "感冒要多久才能好？"
    ]
    
    for question in test_questions:
        print(f"用户: {question}")
        answer = handler.chat_main(question)
        print(f"小勇: {answer}")
        print("=" * 50)
    
    # 交互式问答
    print("现在您可以开始提问了（输入'quit'退出）:")
    while True:
        question = input('用户: ')
        if question.lower() in ['quit', 'exit', '退出']:
            break
        answer = handler.chat_main(question)
        print(f'小勇: {answer}')
        print("=" * 50)

