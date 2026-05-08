# 部署指南

## 前置条件

1. GitHub账号: `lockwang127`
2. Git已安装并配置SSH密钥
3. Python 3.6+

## 部署步骤

### 第1步: 在GitHub创建远程仓库

1. 访问 https://github.com/new
2. 仓库名称: `prostate-cancer-kb`
3. 描述: `前列腺癌知识库 - 基于知识三元组的结构化医学知识图谱`
4. 可见性: **Public**
5. **不要**勾选 "Add a README file"、"Add .gitignore"、"Choose a license"
6. 点击 "Create repository"

### 第2步: 配置远程仓库地址

```bash
cd /Users/wangxiaodong/WorkBuddy/prostate-cancer-kb
git remote set-url origin git@github.com:lockwang127/prostate-cancer-kb.git
```

### 第3步: 推送代码

```bash
git push -u origin main
```

### 第4步: 验证

访问 https://github.com/lockwang127/prostate-cancer-kb 确认文件已上传。

## 后续更新

修改知识库内容后，执行以下命令同步到GitHub：

```bash
python3 scripts/build_kb.py
python3 scripts/tests/test_kb_format.py
git add .
git commit -m "更新描述"
git push
```
