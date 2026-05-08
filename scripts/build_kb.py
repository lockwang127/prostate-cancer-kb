#!/usr/bin/env python3
"""
前列腺癌知识库构建脚本
读取 data/knowledge-graph/ 下的所有 JSON 文件，合并生成 kb.json 和 kb_meta.json
"""

import json
import os
import glob
from datetime import datetime


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kg_dir = os.path.join(base_dir, "data", "knowledge-graph")
    schema_path = os.path.join(base_dir, "schemas", "triplet_schema.json")

    # 收集所有三元组
    all_triplets = []
    source_files = []
    domains = set()

    json_files = sorted(glob.glob(os.path.join(kg_dir, "*.json")))

    if not json_files:
        print(f"ERROR: No JSON files found in {kg_dir}")
        return 1

    for filepath in json_files:
        filename = os.path.basename(filepath)
        print(f"  Processing: {filename}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 验证必要字段
        if "triplets" not in data:
            print(f"  WARNING: {filename} missing 'triplets' field, skipping")
            continue

        if "domain" in data:
            domains.add(data["domain"])

        for triplet in data["triplets"]:
            # 验证三元组字段
            required = ["head", "relation", "tail", "source", "evidence", "domain", "confidence"]
            missing = [k for k in required if k not in triplet]
            if missing:
                print(f"  WARNING: Triplet in {filename} missing fields: {missing}, skipping")
                continue

            # 验证 confidence 范围
            conf = triplet["confidence"]
            if not (0 <= conf <= 1):
                print(f"  WARNING: Invalid confidence {conf} in {filename}, skipping triplet")
                continue

            triplet["_source_file"] = filename
            if "domain" in triplet:
                domains.add(triplet["domain"])
            all_triplets.append(triplet)

        source_files.append(filename)

    if not all_triplets:
        print("ERROR: No valid triplets found")
        return 1

    # 生成 kb.json
    kb = {
        "knowledge_base": "prostate-cancer-kb",
        "version": "1.0.0",
        "build_time": datetime.now().isoformat(),
        "total_triplets": len(all_triplets),
        "total_domains": len(domains),
        "source_files": source_files,
        "triplets": all_triplets
    }

    kb_path = os.path.join(base_dir, "data", "kb.json")
    with open(kb_path, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    print(f"\n  Generated: {os.path.relpath(kb_path, base_dir)}")

    # 生成 kb_meta.json
    domain_counts = {}
    for t in all_triplets:
        d = t.get("domain", "未分类")
        domain_counts[d] = domain_counts.get(d, 0) + 1

    kb_meta = {
        "knowledge_base": "prostate-cancer-kb",
        "version": "1.0.0",
        "build_time": datetime.now().isoformat(),
        "total_triplets": len(all_triplets),
        "total_domains": len(domains),
        "domains": sorted(list(domains)),
        "domain_statistics": domain_counts,
        "source_files": source_files,
        "files_triplet_count": {
            os.path.basename(fp): len(json.load(open(fp))["triplets"])
            for fp in json_files
            if "triplets" in json.load(open(fp))
        }
    }

    meta_path = os.path.join(base_dir, "data", "kb_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(kb_meta, f, ensure_ascii=False, indent=2)
    print(f"  Generated: {os.path.relpath(meta_path, base_dir)}")

    # 统计摘要
    print(f"\n  === 构建完成 ===")
    print(f"  总三元组数: {len(all_triplets)}")
    print(f"  知识域数量: {len(domains)}")
    print(f"  源文件数: {len(source_files)}")
    print(f"  知识域明细:")
    for d, c in sorted(domain_counts.items()):
        print(f"    - {d}: {c} 条")

    return 0


if __name__ == "__main__":
    exit(main())
