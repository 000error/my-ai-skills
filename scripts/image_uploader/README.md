# Image Uploader 使用说明

## 功能描述

将图片上传到图床（如七牛云），并自动插入到Markdown文件的标题下方。

## 配置要求

配置文件 `image_bed_config.json` 必须与脚本在同一目录下。

### 配置文件示例

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

## 使用方法

### 基本用法（输出到当前目录）

```bash
python upload_image.py <图片文件路径> <Markdown文件路径>
```

**说明：** 默认将生成的Markdown文件保存到当前工作目录，文件名为 `原文件名_with_image.md`。

### 指定输出文件

```bash
python upload_image.py <图片文件路径> <Markdown文件路径> --output <输出文件路径>
```

**说明：** 使用 `--output` 参数可以指定输出文件的完整路径（包括文件名）。

### 指定配置文件

```bash
python upload_image.py <图片文件路径> <Markdown文件路径> --config custom_config.json
```

## 使用示例

### 示例1：上传图片并插入Markdown（输出到当前目录）

```bash
python upload_image.py ./images/cover.jpg ./article.md
```

**执行结果：**
- 图片上传到七牛云，获得CDN链接
- 在**当前工作目录**生成 `article_with_image.md`
- 图片插入到第一个标题下方

### 示例2：指定输出文件

```bash
python upload_image.py ./images/cover.jpg ./article.md --output ./merged/final_article.md
```

**执行结果：**
- 图片上传到七牛云
- 生成指定路径的输出文件 `./merged/final_article.md`

### 示例3：批量处理

```bash
# 处理多个文章
python upload_image.py ./images/cover1.jpg ./articles/article1.md --output ./output/article1.md
python upload_image.py ./images/cover2.jpg ./articles/article2.md --output ./output/article2.md
```

## 输出说明

### 默认输出文件命名

如果不指定 `--output` 参数，输出文件将保存到**当前工作目录**，文件名格式为：
```
原文件名_with_image.md
```

例如：`article.md` → `article_with_image.md`（保存在当前目录）

### 指定输出路径

使用 `--output` 参数可以指定完整的输出路径：
```bash
python upload_image.py image.jpg article.md --output ./output/final.md
```

脚本会自动创建不存在的目录。

### 图片插入位置

脚本会在Markdown文件中查找第一个标题（以 `#` 开头的行），并在标题下方插入图片：

```markdown
# 文章标题

![封面图](https://cdn.example.com/xxxxx.jpg)

文章正文内容...
```

如果文件中没有标题，图片会插入到文件开头。

## 错误处理

### 配置文件不存在

```
FileNotFoundError: 配置文件不存在: /path/to/image_bed_config.json
请确保配置文件 'image_bed_config.json' 在脚本同目录下
```

### 上传失败

```
Exception: Upload failed: <错误信息>
```

常见原因：
- API密钥错误
- 存储空间不存在
- 网络连接问题
- 存储空间已满

## 注意事项

1. 确保配置文件中的七牛云凭证正确且有效
2. 确保存储空间（bucket）已创建并绑定CDN域名
3. 图片文件必须存在且可读
4. Markdown文件必须存在且可读
5. 输出目录必须存在或脚本有权限创建
6. 上传的图片会生成唯一的UUID文件名，避免重复

## 依赖安装

```bash
pip install qiniu
```

## 支持的图床

当前版本支持：
- 七牛云（Qiniu）

未来可扩展支持：
- 阿里云OSS
- 腾讯云COS
- 又拍云
- 其他兼容S3协议的对象存储
