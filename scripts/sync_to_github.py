#!/usr/bin/env python3
"""
前列腺癌知识库 GitHub 同步脚本
将本地知识库变更推送到 GitHub 远程仓库
"""

import subprocess
import os
import sys


def run_cmd(cmd, check=True):
    """执行shell命令"""
    print(f"  > {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print(f"    {result.stdout.strip()}")
    if result.stderr.strip():
        print(f"    {result.stderr.strip()}")
    if check and result.returncode != 0:
        print(f"  ERROR: Command failed with exit code {result.returncode}")
        sys.exit(1)
    return result


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)

    # Step 1: 检查 git 状态
    print("Step 1: 检查仓库状态")
    result = run_cmd("git status --porcelain", check=False)
    if not result.stdout.strip():
        print("  没有待提交的变更")
        return 0

    # Step 2: 重新构建知识库
    print("\nStep 2: 构建知识库")
    run_cmd("python3 scripts/build_kb.py")

    # Step 3: 运行测试
    print("\nStep 3: 运行格式验证")
    test_result = run_cmd("python3 scripts/tests/test_kb_format.py", check=False)
    if test_result.returncode != 0:
        print("  WARNING: 测试未全部通过，请检查后再提交")

    # Step 4: 添加变更
    print("\nStep 4: 暂存变更")
    run_cmd("git add .")

    # Step 5: 提交
    print("\nStep 5: 提交变更")
    run_cmd('git commit -m "Update knowledge base: $(date +%Y-%m-%d)"')

    # Step 6: 推送
    print("\nStep 6: 推送到远程仓库")
    remote_result = run_cmd("git remote get-url origin", check=False)
    if remote_result.returncode != 0 or not remote_result.stdout.strip():
        print("  WARNING: 未配置远程仓库，请参考 DEPLOY.md 配置")
        return 1

    run_cmd("git push")

    print("\n  同步完成!")
    return 0


if __name__ == "__main__":
    exit(main())
