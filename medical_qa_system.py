#!/usr/bin/env python3
# coding: utf-8
# 医疗知识图谱问答系统 - 最终版本

import json
import os
import re

class MedicalQuestionClassifier:
    """医疗问题分类器"""
    def __init__(self):
        # 加载词典
        self.disease_words = self.load_dict('dict/disease.txt')
        self.symptom_words = self.load_dict('dict/symptom.txt')
        self.drug_words = self.load_dict('dict/drug.txt')
        self.food_words = self.load_dict('dict/food.txt')
        self.check_words = self.load_dict('dict/check.txt')
        
        # 疑问词
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现', '有哪些']
        self.cause_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何']
        self.desc_qwds = ['是什么', '介绍', '描述', '说明']
        self.cure_qwds = ['治疗', '怎么治', '如何治', '怎么办', '多久', '周期', '治愈']
        
    def load_dict(self, file_path):
        """加载词典文件"""
        words = []
        try:
            full_path = os.path.join(os.path.dirname(__file__), file_path)
            with open(full_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        words.append(word)
        except Exception as e:
            print(f"加载词典 {file_path} 失败: {e}")
        return words
    
    def classify(self, question):
        """分类问题"""
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        
        data['args'] = medical_dict
        types = list(medical_dict.keys())
        question_types = []
        
        # 症状
        if self.check_words_in_question(self.symptom_qwds, question) and 'disease' in types:
            question_types.append('disease_symptom')
        
        # 原因
        if self.check_words_in_question(self.cause_qwds, question) and 'disease' in types:
            question_types.append('disease_cause')
        
        # 治疗
        if self.check_words_in_question(self.cure_qwds, question) and 'disease' in types:
            question_types.append('disease_cure')
        
        # 描述
        if self.check_words_in_question(self.desc_qwds, question) and 'disease' in types:
            question_types.append('disease_desc')
        
        # 如果没有匹配到特定类型，但有疾病，默认为描述
        if not question_types and 'disease' in types:
            question_types.append('disease_desc')
        
        data['question_types'] = question_types
        return data
    
    def check_medical(self, question):
        """检查问题中的医疗实体"""
        medical_dict = {}
        
        # 检查疾病
        for disease in self.disease_words:
            if disease in question:
                if 'disease' not in medical_dict:
                    medical_dict['disease'] = []
                medical_dict['disease'].append(disease)
        
        # 检查症状
        for symptom in self.symptom_words:
            if symptom in question:
                if 'symptom' not in medical_dict:
                    medical_dict['symptom'] = []
                medical_dict['symptom'].append(symptom)
        
        return medical_dict
    
    def check_words_in_question(self, words, question):
        """检查问题中是否包含特定词汇"""
        for word in words:
            if word in question:
                return True
        return False

class MedicalAnswerSearcher:
    """医疗答案搜索器"""
    def __init__(self):
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
    
    def search_main(self, question_type, disease_name):
        """搜索答案"""
        if disease_name not in self.medical_data:
            return "抱歉，我没有找到相关信息。"
        
        disease_data = self.medical_data[disease_name]
        
        if question_type == 'disease_symptom':
            symptoms = disease_data.get('symptom', [])
            if symptoms:
                return f"{disease_name}的症状包括：{'；'.join(symptoms[:10])}"
            else:
                return f"抱歉，我没有找到{disease_name}的症状信息。"
        
        elif question_type == 'disease_cause':
            cause = disease_data.get('cause', '')
            if cause:
                cause_short = cause[:200] + "..." if len(cause) > 200 else cause
                return f"{disease_name}可能的成因有：{cause_short}"
            else:
                return f"抱歉，我没有找到{disease_name}的病因信息。"
        
        elif question_type == 'disease_cure':
            cure_way = disease_data.get('cure_way', [])
            cure_lasttime = disease_data.get('cure_lasttime', '')
            cured_prob = disease_data.get('cured_prob', '')
            
            result = f"{disease_name}的治疗信息：\n"
            if cure_way:
                result += f"治疗方式：{'；'.join(cure_way)}\n"
            if cure_lasttime:
                result += f"治疗周期：{cure_lasttime}\n"
            if cured_prob:
                result += f"治愈概率：{cured_prob}"
            
            if result == f"{disease_name}的治疗信息：\n":
                return f"抱歉，我没有找到{disease_name}的治疗信息。"
            else:
                return result.strip()
        
        elif question_type == 'disease_desc':
            desc = disease_data.get('desc', '')
            if desc:
                desc_short = desc[:300] + "..." if len(desc) > 300 else desc
                return f"{disease_name}，熟悉一下：{desc_short}"
            else:
                return f"抱歉，我没有找到{disease_name}的详细描述。"
        
        return "抱歉，我暂时无法回答这个问题。"

class MedicalChatBot:
    """医疗聊天机器人"""
    def __init__(self):
        print("正在初始化医疗知识图谱问答系统...")
        self.classifier = MedicalQuestionClassifier()
        self.searcher = MedicalAnswerSearcher()
        print("系统初始化完成！")
    
    def chat_main(self, question):
        """主要聊天函数"""
        # 分类问题
        classify_result = self.classifier.classify(question)
        
        if not classify_result or not classify_result.get('question_types'):
            return "您好，我是小勇医药智能助理，希望可以帮到您。如果没答上来，可联系https://liuhuanyong.github.io/。祝您身体棒棒！"
        
        # 获取疾病名称
        disease_name = None
        if 'disease' in classify_result.get('args', {}):
            disease_name = classify_result['args']['disease'][0]
        
        if not disease_name:
            return "抱歉，我没有识别出您询问的疾病名称。"
        
        # 获取问题类型
        question_type = classify_result['question_types'][0]
        
        # 搜索答案
        answer = self.searcher.search_main(question_type, disease_name)
        return answer

def run_demo():
    """运行演示"""
    handler = MedicalChatBot()
    print("=" * 60)
    print("医疗知识图谱问答系统演示")
    print("=" * 60)
    
    # 演示问题
    demo_questions = [
        "乳腺癌的症状有哪些？",
        "糖尿病",
        "为什么有的人会失眠？",
        "感冒要多久才能好？",
        "高血压怎么治疗？",
        "肺癌的症状是什么？",
        "如何预防心脏病？"
    ]
    
    for question in demo_questions:
        print(f"用户: {question}")
        answer = handler.chat_main(question)
        print(f"小勇: {answer}")
        print("-" * 60)

def run_interactive():
    """运行交互模式"""
    handler = MedicalChatBot()
    print("=" * 60)
    print("医疗知识图谱问答系统")
    print("输入 'quit' 或 'exit' 退出系统")
    print("=" * 60)
    
    while True:
        try:
            question = input('用户: ')
            if question.lower() in ['quit', 'exit', '退出', 'q']:
                print("感谢使用医疗知识图谱问答系统，再见！")
                break
            answer = handler.chat_main(question)
            print(f'小勇: {answer}')
            print("-" * 60)
        except KeyboardInterrupt:
            print("\n\n感谢使用医疗知识图谱问答系统，再见！")
            break
        except EOFError:
            print("\n\n感谢使用医疗知识图谱问答系统，再见！")
            break

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        # 运行演示模式
        run_demo()
    else:
        # 运行交互模式
        run_interactive()
