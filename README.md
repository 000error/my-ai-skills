# My AI Skills

个人 Claude Code Skill 集合仓库。每个 skill 独立管理，可单独更新、单独说明。

## 现有 Skill

| Skill | 功能 | 路径 |
|---|---|---|
| [professional-article-publisher](./professional-article-publisher) | 文章排版与公众号 HTML 生成 | `professional-article-publisher/` |

## 安装到 Claude Code

将本仓库克隆到本地后，用符号链接映射到 Claude Code 的 skills 目录：

```bash
# Windows (Git Bash)
cd /c/Users/admin/.claude/skills
ln -s /c/Users/admin/my-ai-skills/professional-article-publisher professional-article-publisher
```

## 添加新 Skill

1. 将新 skill 文件夹复制到仓库根目录
2. 在 skill 文件夹内添加 `README.md` 说明
3. 更新本文件的目录表格
4. 提交并推送

## 更新记录

- 2025-06-02: 初始化仓库，上传 `professional-article-publisher`
