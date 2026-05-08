# 变更日志

## [1.0.0] - 2026-05-08

### 新增
- 初始化前列腺癌知识库仓库
- 流行病学数据 (epidemiology.json): 12条三元组
  - 2022年中国发病/死亡数据
  - 发病趋势与驱动因素
  - 全球对比数据
- CSCO 2024指南推荐 (csco_2024.json): 14条三元组
  - 低/中/高危前列腺癌治疗方案
  - mCRPC治疗方案
  - 新型内分泌药物(阿比特龙、恩扎卢胺、阿帕他胺、达罗他胺)
  - mHSPC标准治疗
- 生物标志物与分期评估 (biomarkers.json): 13条三元组
  - Gleason评分/ISUP分级
  - PSA/PSAD/free PSA
  - TNM分期系统
  - 危险分层标准
  - 前列腺穿刺与MRI评估
- 治疗方案 (treatment.json): 14条三元组
  - 根治性前列腺切除术(RARP)
  - 近距离放疗
  - ADT方式与不良反应
  - 化疗方案(多西他赛/卡巴他赛)
  - PARP抑制剂靶向治疗
  - 免疫治疗现状

### 基础设施
- 知识库构建脚本 (build_kb.py)
- 格式验证测试 (test_kb_format.py)
- JSON Schema定义 (triplet_schema.json)
- 领域指南文档 (domain_guide.md)
- 部署指南 (DEPLOY.md)
- 更新策略 (UPDATE_POLICY.md)

### 统计
- 总三元组数: 53条
- 知识域: 12个
- 覆盖数据文件: 4个
