# Markdown to WeChat HTML Converter 使用说明

## 功能描述

将Markdown文件转换为带有微信公众号样式的HTML文件，可直接复制粘贴到微信公众号编辑器。

## 配置要求

样式文件 `styles/default.json` 应与脚本在同一目录结构下。

### 样式文件结构

```
md2wechat/
├── md2wechat.py
└── styles/
    └── default.json
```

## 使用方法

### 基本用法（输出到当前目录）

```bash
python md2wechat.py <Markdown文件路径>
```

**说明：** 默认将生成的HTML文件保存到当前工作目录，文件名为 `原文件名_wechat.html`。

### 指定输出文件

```bash
python md2wechat.py <Markdown文件路径> --output <输出HTML文件路径>
```

**说明：** 使用 `--output` 参数可以指定输出文件的完整路径（包括文件名）。

### 指定样式文件

```bash
python md2wechat.py <Markdown文件路径> --style styles/custom.json
```

## 使用示例

### 示例1：转换单个文件（输出到当前目录）

```bash
python md2wechat.py ./article.md
```

**执行结果：**
- 在**当前工作目录**生成 `article_wechat.html` 文件
- 文件包含完整的HTML结构和内联样式
- 可在浏览器中预览效果

### 示例2：指定输出路径

```bash
python md2wechat.py ./article.md --output ./output/final.html
```

**执行结果：**
- 在指定路径生成HTML文件
- 自动创建不存在的目录

### 示例3：使用自定义样式

```bash
python md2wechat.py ./article.md --style styles/tech.json
```

**执行结果：**
- 使用 `tech.json` 中定义的样式
- 生成带有自定义样式的HTML文件到当前目录

### 示例4：批量转换

```bash
# 转换多个文章到当前目录
python md2wechat.py ./articles/article1.md
python md2wechat.py ./articles/article2.md
python md2wechat.py ./articles/article3.md
```

## 输出说明

### 默认输出文件命名

如果不指定 `--output` 参数，输出文件将保存到**当前工作目录**，文件名格式为：
```
原文件名_wechat.html
```

例如：`article.md` → `article_wechat.html`（保存在当前目录）

### 指定输出路径

使用 `--output` 参数可以指定完整的输出路径：
```bash
python md2wechat.py article.md --output ./html/final.html
```

脚本会自动创建不存在的目录。

### 使用生成的HTML

1. 用浏览器打开生成的HTML文件
2. 全选内容（Ctrl+A 或 Cmd+A）
3. 复制内容（Ctrl+C 或 Cmd+C）
4. 粘贴到微信公众号编辑器（Ctrl+V 或 Cmd+V）

## 支持的Markdown语法

### 基本语法

- **标题**：`# H1`, `## H2`, `### H3` 等
- **段落**：普通文本段落
- **粗体**：`**粗体文本**`
- **斜体**：`*斜体文本*`
- **链接**：`[链接文本](URL)`
- **图片**：`![图片描述](图片URL)`

### 扩展语法

- **表格**：支持Markdown表格语法
- **代码块**：支持围栏式代码块
- **行内代码**：`` `代码` ``
- **换行**：自动处理换行

## 示例Markdown文件

```markdown
# 技术文章标题

![封面图](https://example.com/cover.jpg)

## 引言

这是一篇关于技术的文章，包含**重要内容**和*强调文本*。

## 主要内容

### 代码示例

​```python
def hello_world():
    print("Hello, World!")
​```

### 数据表格

| 项目 | 数值 | 说明 |
|------|------|------|
| A    | 100  | 示例 |
| B    | 200  | 示例 |

## 结论

更多信息请访问[官方网站](https://example.com)。
```

## 样式定制

### 创建自定义样式文件

在 `styles/` 目录下创建新的JSON文件，例如 `custom.json`：

```json
{
  "h1": "font-size: 24px; font-weight: bold; color: #2c3e50; margin: 20px 0 10px;",
  "h2": "font-size: 20px; font-weight: bold; color: #34495e; margin: 18px 0 8px;",
  "h3": "font-size: 18px; font-weight: bold; color: #7f8c8d; margin: 16px 0 6px;",
  "p": "margin: 10px 0; line-height: 1.75;",
  "a": "color: #3498db; text-decoration: none;",
  "strong": "font-weight: bold; color: #e74c3c;",
  "code": "background-color: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: monospace;",
  "blockquote": "border-left: 4px solid #3498db; padding-left: 16px; color: #7f8c8d; margin: 16px 0;"
}
```

### 使用自定义样式

```bash
python md2wechat.py article.md --style styles/custom.json
```

## 注意事项

1. **图片链接**：确保Markdown中的图片链接是公网可访问的URL
2. **样式限制**：微信公众号编辑器只支持内联样式，不支持外部CSS
3. **字体**：使用系统默认字体，确保在不同设备上显示一致
4. **预览**：建议先在浏览器中预览效果，再粘贴到公众号
5. **编码**：文件必须使用UTF-8编码

## 常见问题

### Q: 粘贴到公众号后样式丢失？

A: 确保使用"全选+复制"方式，而不是直接复制HTML代码。

### Q: 图片无法显示？

A: 检查图片URL是否可公网访问，微信不支持本地图片路径。

### Q: 代码块格式不正确？

A: 确保使用围栏式代码块（三个反引号），并指定语言类型。

### Q: 表格显示异常？

A: 检查Markdown表格语法是否正确，确保每列对齐。

## 依赖安装

```bash
pip install markdown
```

## 完整工作流示例

```bash
# 1. 生成AI配图
cd ai_image_generator
python generate_image.py "文章主题配图" --size 1200x896 --output ../images

# 2. 上传图片并插入Markdown
cd ../image_uploader
python upload_image.py ../images/ai_image_*.jpg ../article.md --output ../merged/article_with_image.md

# 3. 转换为微信HTML
cd ../md2wechat
python md2wechat.py ../merged/article_with_image.md

# 4. 打开生成的HTML文件，复制粘贴到微信公众号
```
