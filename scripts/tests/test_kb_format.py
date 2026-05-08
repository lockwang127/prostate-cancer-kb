#!/usr/bin/env python3
"""
前列腺癌知识库格式验证测试
验证所有知识三元组JSON文件格式符合规范
"""

import json
import os
import sys


def load_json(filepath):
    """加载JSON文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_triplet(triplet, source_file="unknown"):
    """验证单个三元组的格式"""
    errors = []
    required_fields = ["head", "relation", "tail", "source", "evidence", "domain", "confidence"]

    # 检查必填字段
    for field in required_fields:
        if field not in triplet:
            errors.append(f"缺少必填字段: {field}")

    # 检查字段类型
    for field in ["head", "relation", "tail", "source", "evidence", "domain"]:
        if field in triplet and not isinstance(triplet[field], str):
            errors.append(f"字段 '{field}' 应为字符串类型")

    # 检查 confidence
    if "confidence" in triplet:
        conf = triplet["confidence"]
        if not isinstance(conf, (int, float)):
            errors.append(f"confidence 应为数字类型")
        elif not (0 <= conf <= 1):
            errors.append(f"confidence 值 {conf} 不在 0-1 范围内")

    # 检查可选字段
    if "pmid" in triplet and not isinstance(triplet.get("pmid"), (str, type(None))):
        errors.append("pmid 应为字符串或 null")

    # 检查空字符串
    for field in ["head", "relation", "tail"]:
        if field in triplet and isinstance(triplet[field], str) and not triplet[field].strip():
            errors.append(f"字段 '{field}' 不应为空字符串")

    return errors


def validate_knowledge_file(filepath):
    """验证单个知识文件"""
    errors = []
    filename = os.path.basename(filepath)

    # 加载JSON
    try:
        data = load_json(filepath)
    except json.JSONDecodeError as e:
        return [f"JSON解析错误: {e}"]

    # 检查顶层字段
    if not isinstance(data, dict):
        return ["文件根元素应为对象"]

    if "triplets" not in data:
        errors.append("缺少 'triplets' 字段")
        return errors

    if not isinstance(data["triplets"], list):
        errors.append("'triplets' 应为数组")
        return errors

    # 验证每个三元组
    triplets = data["triplets"]
    if len(triplets) < 10:
        errors.append(f"三元组数量 {len(triplets)} 少于最低要求 10 条")

    for i, triplet in enumerate(triplets):
        t_errors = validate_triplet(triplet, filename)
        for err in t_errors:
            errors.append(f"三元组 #{i+1}: {err}")

    return errors


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    kg_dir = os.path.join(base_dir, "data", "knowledge-graph")

    all_passed = True
    total_triplets = 0
    total_errors = 0

    json_files = sorted([
        f for f in os.listdir(kg_dir) if f.endswith(".json")
    ])

    if not json_files:
        print("ERROR: 未找到知识图谱JSON文件")
        return 1

    print("=" * 60)
    print("  前列腺癌知识库格式验证")
    print("=" * 60)

    for filename in json_files:
        filepath = os.path.join(kg_dir, filename)
        errors = validate_knowledge_file(filepath)

        if errors:
            all_passed = False
            total_errors += len(errors)
            print(f"\n  [FAIL] {filename}")
            for err in errors:
                print(f"    - {err}")
        else:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            count = len(data["triplets"])
            total_triplets += count
            print(f"  [PASS] {filename} ({count} 条三元组)")

    # 验证构建产物
    print(f"\n{'=' * 60}")
    print("  构建产物验证")
    print(f"{'=' * 60}")

    kb_path = os.path.join(base_dir, "data", "kb.json")
    meta_path = os.path.join(base_dir, "data", "kb_meta.json")

    if os.path.exists(kb_path):
        kb = load_json(kb_path)
        print(f"  [PASS] kb.json 存在 (构建三元组数: {kb.get('total_triplets', 'N/A')})")
    else:
        print(f"  [WARN] kb.json 不存在，请先运行 build_kb.py")
        all_passed = False

    if os.path.exists(meta_path):
        meta = load_json(meta_path)
        print(f"  [PASS] kb_meta.json 存在 (知识域数: {meta.get('total_domains', 'N/A')})")
    else:
        print(f"  [WARN] kb_meta.json 不存在，请先运行 build_kb.py")
        all_passed = False

    # 验证 schema
    schema_path = os.path.join(base_dir, "schemas", "triplet_schema.json")
    if os.path.exists(schema_path):
        print(f"  [PASS] triplet_schema.json 存在")
    else:
        print(f"  [FAIL] triplet_schema.json 不存在")
        all_passed = False

    # 总结
    print(f"\n{'=' * 60}")
    print(f"  验证结果")
    print(f"{'=' * 60}")
    print(f"  总三元组数: {total_triplets}")
    print(f"  总错误数: {total_errors}")
    print(f"  状态: {'全部通过' if all_passed else '存在错误'}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
