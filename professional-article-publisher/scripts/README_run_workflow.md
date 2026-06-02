# Run Workflow 使用说明

## 功能描述

自动化工作流脚本，整合AI图片生成、图片上传和Markdown转HTML三个步骤，一键完成从内容到微信公众号发布的全流程。

## 工作流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                         输入文件                                  │
├─────────────────────────────────────────────────────────────────┤
│  1. Markdown文件 (--md)     │  2. 提示词文件 (--prompt)         │
│     例如: my_article.md      │     例如: prompt.txt              │
│     包含文章正文内容          │     包含AI绘图提示词              │
└──────────────┬──────────────┴──────────────┬───────────────────┘
               │                              │
               ▼                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    步骤1: 生成AI图片                              │
├──────────────────────────────────────────────────────────────────┤
│  • 读取提示词文件内容                                              │
│  • 调用 generate_image.py                                        │
│  • 使用AI模型生成图片                                             │
│  • 保存到输出文件夹: ai_image_YYYYMMDD_HHMMSS.jpg                │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                 步骤2: 上传图片并插入Markdown                      │
├──────────────────────────────────────────────────────────────────┤
│  • 上传图片到七牛云图床                                            │
│  • 获取CDN链接                                                    │
│  • 读取原始Markdown文件                                           │
│  • 将图片插入到第一个标题下方                                      │
│  • 保存为: 原文件名_with_image.md                                 │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                  步骤3: 转换为微信HTML                             │
├──────────────────────────────────────────────────────────────────┤
│  • 读取带图片的Markdown文件                                        │
│  • 调用 md2wechat.py                                             │
│  • 转换为带样式的HTML                                             │
│  • 保存为: 原文件名_wechat.html                                   │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                         输出结果                                  │
├──────────────────────────────────────────────────────────────────┤
│  输出文件夹: workflow_output_YYYYMMDD_HHMMSS/                    │
│  ├── ai_image_YYYYMMDD_HHMMSS.jpg      (AI生成的图片)            │
│  ├── 原文件名_with_image.md             (带图片的Markdown)        │
│  └── 原文件名_wechat.html               (微信公众号HTML)          │
└──────────────────────────────────────────────────────────────────┘
```

## 使用方法

### 基本用法

```bash
python run_workflow.py --md <Markdown文件路径> --prompt <提示词文件路径>
```

**必需参数：**
- `--md`：指定Markdown文件路径（必需）
- `--prompt`：指定提示词文件路径（必需）

### 准备输入文件

#### 1. Markdown文件

包含文章正文的Markdown文件，例如 `my_article.md`：

```markdown
# 文章标题

## 引言

这是文章的引言部分...

## 主要内容

文章的主要内容...

## 结论

文章的结论部分...
```

#### 2. 提示词文件

包含AI绘图提示词的文本文件，例如 `prompt.txt`：

```
专业的芯片结构图，现代科技风格，蓝色和银色配色，简洁的信息图风格，适合技术文档配图
```

**提示词编写建议：**
- 描述清晰具体
- 包含风格要求（如"简洁现代""专业科技风格"）
- 包含配色建议（如"蓝色渐变""暖色调"）
- 说明用途（如"适合公众号封面""适合技术文档"）
- 避免品牌Logo、真人肖像等版权敏感内容

## 使用示例

### 示例1：基本使用

```bash
python run_workflow.py --md ./article.md --prompt ./prompt.txt
```

**执行结果：**
- 创建输出文件夹：`workflow_output_20260306_095559/`
- 生成AI图片：`ai_image_20260306_095559.jpg`
- 生成带图Markdown：`article_with_image.md`
- 生成微信HTML：`article_wechat.html`

### 示例2：技术文章

**prompt.txt 内容：**
```
现代化的数据中心服务器机房，整齐排列的服务器机柜，蓝色LED灯光，科技感强，适合技术博客配图
```

**执行命令：**
```bash
python run_workflow.py --md ./tech_article.md --prompt ./prompt.txt
```

### 示例3：商业文章

**prompt.txt 内容：**
```
简洁的商业办公场景插画，现代办公室，团队协作氛围，扁平化设计风格，温暖配色，适合企业公众号
```

**执行命令：**
```bash
python run_workflow.py --md ./business_article.md --prompt ./prompt.txt
```

## 输出说明

### 输出文件夹

脚本会自动创建带时间戳的输出文件夹：
```
workflow_output_YYYYMMDD_HHMMSS/
```

例如：`workflow_output_20260306_095559/`

### 输出文件

1. **AI生成的图片**
   - 文件名：`ai_image_YYYYMMDD_HHMMSS.jpg`
   - 格式：JPEG
   - 质量：85（已优化）

2. **带图片的Markdown文件**
   - 文件名：`原文件名_with_image.md`
   - 图片已插入到第一个标题下方
   - 图片使用CDN链接（七牛云）

3. **微信公众号HTML文件**
   - 文件名：`原文件名_wechat.html`
   - 包含完整HTML结构和内联样式
   - 可直接复制粘贴到微信公众号编辑器

### 使用生成的HTML

1. 用浏览器打开 `原文件名_wechat.html`
2. 全选内容（Ctrl+A 或 Cmd+A）
3. 复制内容（Ctrl+C 或 Cmd+C）
4. 粘贴到微信公众号编辑器（Ctrl+V 或 Cmd+V）

## 错误处理

### 缺少必需参数

```bash
python run_workflow.py --md ./article.md
```

**错误信息：**
```
usage: run_workflow.py [-h] --md MD --prompt PROMPT
run_workflow.py: error: the following arguments are required: --prompt
```

### Markdown文件不存在

```bash
python run_workflow.py --md ./not_exist.md --prompt ./prompt.txt
```

**错误信息：**
```
[错误] Markdown文件不存在: not_exist.md
```

### 提示词文件不存在

```bash
python run_workflow.py --md ./article.md --prompt ./not_exist.txt
```

**错误信息：**
```
[错误] 提示词文件不存在: not_exist.txt
```

### 提示词文件为空

```bash
python run_workflow.py --md ./article.md --prompt ./empty.txt
```

**错误信息：**
```
[错误] 提示词文件为空: empty.txt
```

## 依赖配置

### 1. AI图片生成配置

确保 `ai_image_generator/ai_image_config.json` 配置正确：
```json
{
  "api_url": "https://mg.aid.pub/api/v1/images/generations",
  "api_key": "your-api-key",
  "model": "Nano-Banana-2",
  "default_size": "3168x1344",
  "output_type": "url",
  "output_format": "jpeg",
  "number_results": 1
}
```

### 2. 图床上传配置

确保 `image_uploader/image_bed_config.json` 配置正确：
```json
{
  "provider": "qiniu",
  "qiniu": {
    "access_key": "your-access-key",
    "secret_key": "your-secret-key",
    "bucket": "your-bucket-name",
    "domain": "https://your-cdn-domain.com"
  }
}
```

## 注意事项

1. **文件编码**：确保Markdown和提示词文件使用UTF-8编码
2. **网络连接**：需要稳定的网络连接以访问AI API和图床服务
3. **API配额**：确保AI API和图床服务有足够的配额
4. **提示词质量**：提示词越详细具体，生成的图片质量越好
5. **Markdown格式**：确保Markdown文件格式正确，至少包含一个标题

## 完整示例

### 准备文件

**1. 创建 article.md**
```markdown
# 人工智能的未来发展

## 引言

人工智能技术正在快速发展，改变着我们的生活方式。

## 主要趋势

1. 大模型技术的突破
2. AI应用的普及
3. 伦理和监管的完善

## 结论

人工智能将继续深刻影响人类社会的发展。
```

**2. 创建 prompt.txt**
```
未来科技感的人工智能概念图，神经网络可视化，蓝色和紫色渐变，现代简洁风格，适合科技文章配图
```

### 执行命令

```bash
python run_workflow.py --md ./article.md --prompt ./prompt.txt
```

### 查看结果

```bash
cd workflow_output_20260306_095559
ls -lh
```

输出：
```
ai_image_20260306_095559.jpg      (AI生成的图片)
article_with_image.md             (带图片的Markdown)
article_wechat.html               (微信公众号HTML)
```

## 相关脚本

- `generate_image.py` - AI图片生成工具
- `upload_image.py` - 图片上传和Markdown插入工具
- `md2wechat.py` - Markdown转微信HTML工具
- `test_workflow.py` - 自动化测试脚本（使用内置测试数据）

## 常见问题

### Q: 可以批量处理多篇文章吗？

A: 可以，使用shell脚本循环调用：
```bash
for md in articles/*.md; do
    python run_workflow.py --md "$md" --prompt ./prompt.txt
done
```

### Q: 可以使用不同的提示词吗？

A: 可以，为每篇文章准备对应的提示词文件：
```bash
python run_workflow.py --md ./article1.md --prompt ./prompt1.txt
python run_workflow.py --md ./article2.md --prompt ./prompt2.txt
```

### Q: 生成的图片可以自定义尺寸吗？

A: 目前使用配置文件中的默认尺寸。如需自定义，可以修改 `ai_image_config.json` 中的 `default_size` 参数。

### Q: 输出文件夹可以自定义吗？

A: 目前输出文件夹自动生成带时间戳的名称。如需自定义，可以在脚本执行后手动重命名文件夹。
