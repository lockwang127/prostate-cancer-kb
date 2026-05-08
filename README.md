# 前列腺癌知识库 (Prostate Cancer Knowledge Base)

基于知识三元组（Head-Relation-Tail）结构的前列腺癌领域结构化知识图谱，适用于RAG/LLM/AI应用集成。

## 知识库概览

| 指标 | 数值 |
|------|------|
| 知识域 | 12个 |
| 三元组 | 53条 |
| 数据文件 | 4个 |
| 指南版本 | CSCO 2024 |
| 流行病学数据 | GLOBOCAN 2022 |

## 覆盖知识域

- **流行病学**: 中国及全球发病/死亡数据、趋势、危险因素
- **病理评估**: Gleason评分、ISUP分级系统
- **筛查诊断**: PSA、PSAD、free PSA、前列腺穿刺、mpMRI
- **分期系统**: TNM分期、危险分层(低/中/高危)
- **治疗指南**: CSCO 2024各分期推荐方案
- **药物治疗**: ADT、NHA(阿比特龙/恩扎卢胺/阿帕他胺/达罗他胺)
- **手术治疗**: 根治性前列腺切除术(RARP)
- **放射治疗**: EBRT、近距离放疗
- **化学治疗**: 多西他赛、卡巴他赛
- **靶向治疗**: PARP抑制剂
- **免疫治疗**: Sipuleucel-T
- **内分泌治疗**: ADT方式与不良反应

## 仓库结构

```
prostate-cancer-kb/
├── data/
│   ├── knowledge-graph/        # 原始知识三元组
│   │   ├── epidemiology.json   # 流行病学数据 (12条)
│   │   ├── csco_2024.json      # CSCO 2024指南推荐 (14条)
│   │   ├── biomarkers.json     # 生物标志物与分期评估 (13条)
│   │   └── treatment.json      # 治疗方案 (14条)
│   ├── kb.json                 # 合并后的知识库（构建产物）
│   └── kb_meta.json            # 知识库元数据（构建产物）
├── scripts/
│   ├── build_kb.py             # 知识库构建脚本
│   ├── sync_to_github.py       # GitHub同步脚本
│   └── tests/
│       └── test_kb_format.py   # 格式验证测试
├── schemas/
│   └── triplet_schema.json     # 三元组JSON Schema
├── docs/
│   └── domain_guide.md         # 领域指南
├── README.md                   # 本文件
├── UPDATE_POLICY.md            # 更新策略
├── CHANGELOG.md                # 变更日志
└── DEPLOY.md                   # 部署指南
```

## 快速开始

### 构建知识库

```bash
python3 scripts/build_kb.py
```

### 运行测试

```bash
python3 scripts/tests/test_kb_format.py
```

### 数据格式

每条知识三元组包含以下字段：

```json
{
  "head": "前列腺癌",
  "relation": "2022年中国新发病例数",
  "tail": "13.42万例",
  "source": "GLOBOCAN 2022 / 国家癌症中心",
  "evidence": "2022年中国前列腺癌新发病例约13.42万",
  "domain": "流行病学",
  "confidence": 0.95,
  "pmid": "38433564"
}
```

## 数据来源

- GLOBOCAN 2022 (IARC)
- 国家癌症中心年度统计
- CSCO前列腺癌诊疗指南2024版
- NCCN前列腺癌临床实践指南
- ISUP 2014 Gleason分级共识
- AJCC第8版TNM分期
- PubMed文献 (PMID引用)

## 许可证

MIT License
