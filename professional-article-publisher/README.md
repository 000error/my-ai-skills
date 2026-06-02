# professional-article-publisher

专业的微信公众号文章发布助手。支持深度研究文章创作和现有文章快速格式化两种模式。

## 功能

- **快速模式**: 用户提供完整文章，自动配图、排版、生成微信公众号 HTML
- **深度模式**: 用户提供话题和资料，自动研究、撰写、配图、输出完整文章
- **AI 配图**: 自动生成配图并上传图床（失败时生成兜底图片）
- **微信公众号 HTML**: 输出带格式的 HTML，直接复制粘贴到公众号编辑器

## 触发方式

- 用户说"转成公众号格式""发布文章""排版"等
- 用户要求将 Markdown 文章转换为微信公众号格式
- 用户要求为文章配图并发布

## 使用方法

### 快速模式
1. 用户提供完整文章内容（Markdown 或纯文本）
2. Skill 自动生成配图提示词、调用 AI 生图
3. 图片上传图床，插入文章
4. 转换为微信公众号 HTML 格式输出

### 深度模式
1. 用户提供话题、资料、链接等
2. Skill 自动搜索补充信息（如平台支持）
3. 撰写 2000-3000 字行业研究文章
4. 配图、排版、输出 HTML

## 输出文件

```
话题文件夹/
├── article_01.md              # 原始 Markdown 文章
├── prompt.txt                 # AI 配图提示词
└── workflow_output_YYYYMMDD_HHMMSS/
    ├── ai_image_YYYYMMDD_HHMMSS.jpg    # AI 生成的配图
    ├── article_with_image.md            # 带图片的 Markdown
    └── article_wechat.html              # 微信公众号 HTML（最终产物）
```

## 依赖配置

### 1. Python 环境
确保已安装 Python 3.x 及依赖：
```bash
cd scripts
pip install -r md2wechat/requirements.txt
```

### 2. AI 图片生成配置
编辑 `scripts/ai_image_generator/ai_image_config.json`：
```json
{
  "api_key": "your-api-key",
  "model": "your-image-model",
  "default_size": "1024x1024"
}
```

### 3. 图床上传配置
编辑 `scripts/image_uploader/image_bed_config.json`：
```json
{
  "access_key": "your-qiniu-access-key",
  "secret_key": "your-qiniu-secret-key",
  "bucket": "your-bucket-name",
  "domain": "your-domain"
}
```

## 样式自定义

默认样式文件：`scripts/md2wechat/styles/default.json`

可修改的参数：
- `p`: 段落样式（字体、行距、间距）
- `h1` / `h2`: 标题样式
- `img`: 图片样式

当前默认配置：
- 正文字体：16px
- 段落间距：2em
- 行高：1.75
- 字间距：2px

## 更新记录

### 2025-06-02
- 调整默认排版：正文字体从 15px 增大到 16px
- 段落间距从 1em 增大到 2em，提升阅读体验

### 2025-04-15
- 初始版本
