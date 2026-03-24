<div align="center">

# MedGraph-QA

<p>
  <img src="https://img.shields.io/badge/Domain-Medical%20Knowledge%20Graph-2F5D62?style=flat-square" />
  <img src="https://img.shields.io/badge/Task-Knowledge%20Construction%20%26%20Question%20Answering-4C6A92?style=flat-square" />
  <img src="https://img.shields.io/badge/Backend-Python-3B7EA1?style=flat-square" />
  <img src="https://img.shields.io/badge/Database-Neo4j-0E5A8A?style=flat-square" />
  <img src="https://img.shields.io/badge/Method-Rule--based%20QA-5B7C99?style=flat-square" />
</p>

<p>面向疾病中心组织的医药知识图谱构建与自动问答系统</p>

</div>

---

## 项目简介

本项目围绕疾病这一核心实体，构建医药领域知识图谱，并在此基础上实现面向自然语言问题的自动问答服务。系统以垂直领域网页中的结构化与半结构化信息为基础，完成知识抽取、图谱建模、图数据库存储与问答查询等流程。

项目目标包括：

- 构建具有清晰医学语义结构的领域知识图谱
- 建立从原始数据到图数据库入库的完整流程
- 基于图谱查询实现可解释的自动问答服务
- 为后续医学信息组织、知识检索与分析任务提供基础框架

---

## 方法概览

### 1. 知识图谱构建

知识图谱以疾病为中心，组织疾病、症状、药品、食物、检查项目、科室等实体，并建模它们之间的医学语义关系，如症状关联、推荐用药、饮食建议、检查需求及并发关系等。

整体流程包括：

- 医药垂直网站数据采集
- 文本与字段清洗
- 实体与关系抽取
- 图谱 schema 设计
- Neo4j 图数据库入库

### 2. 自动问答

问答模块采用基于规则与模板的实现方式，将用户自然语言问题映射为图谱查询语句，并对查询结果进行组织与返回。该方法具有结构清晰、可解释性较强、部署成本较低等特点。

整体流程包括：

- 问句类型识别
- 关键实体识别
- 查询语句生成
- 图谱检索
- 答案生成与返回

---

## 知识模式

### 实体类型

- Disease
- Symptom
- Drug
- Food
- Check
- Department
- Producer

### 关系类型

- 疾病与症状
- 疾病与药品
- 疾病与食物
- 疾病与检查
- 疾病与科室
- 疾病与并发症
- 药品与生产信息

### 主要属性

- `name`
- `desc`
- `cause`
- `prevent`
- `cure_lasttime`
- `cure_way`
- `cured_prob`
- `easy_get`

---

## 支持的问答任务

系统支持以下典型问答类型：

- 疾病的症状
- 已知症状反推可能疾病
- 疾病病因
- 疾病并发症
- 疾病宜吃与忌吃食物
- 疾病相关药品
- 药品对应疾病
- 疾病相关检查
- 检查对应疾病
- 疾病预防措施
- 疾病治疗周期
- 疾病治疗方式
- 疾病治愈概率
- 疾病易感人群
- 疾病基础描述

---

## 项目结构

```text
.
├── build_medicalgraph.py
├── chatbot_graph.py
├── question_classifier.py
├── question_parser.py
└── prepare_data/
    ├── dataspider.py
    └── max_cut.py
