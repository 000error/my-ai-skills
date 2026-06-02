# AI Image Generator 使用说明

## 功能描述

使用AI模型API生成图片，支持自定义提示词和图片尺寸。

## 配置要求

配置文件 `ai_image_config.json` 必须与脚本在同一目录下。

### 配置文件示例

```json
{
  "api_url": "https://mg.aid.pub/api/v1/images/generations",
  "api_key": "your-api-key-here",
  "model": "Nano-Banana-2",
  "default_size": "3168x1344",
  "output_type": "url",
  "output_format": "jpeg",
  "number_results": 1,
  "available_sizes": {
    "square": "1024x1024",
    "wechat_cover": "1200x896",
    "wechat_post": "1024x1024",
    "wide": "1264x848",
    "ultra_wide": "2048x512"
  }
}
```

## 使用方法

### 基本用法（输出到当前目录）

```bash
python generate_image.py "提示词描述"
```

**说明：** 默认将生成的图片保存到当前工作目录。

### 指定图片尺寸

```bash
python generate_image.py "提示词描述" --size 1264x848
```

### 指定输出目录

```bash
python generate_image.py "提示词描述" --output ./images
```

**说明：** 使用 `--output` 参数可以指定图片保存的目录路径。

### 指定配置文件

```bash
python generate_image.py "提示词描述" --config custom_config.json
```

## 使用示例

### 示例1：生成技术插图

```bash
python generate_image.py "专业的FPGA芯片技术插图，现代科技风格，展示FPGA芯片的内部结构和电路板，蓝色和银色配色，简洁专业的信息图风格，适合技术文档配图，横幅构图" --size 1264x848
```

### 示例2：生成公众号封面

```bash
python generate_image.py "简洁现代的商业科技主题插画，蓝色渐变背景，适合微信公众号封面" --size 1200x896 --output ./covers
```

### 示例3：生成方形配图

```bash
python generate_image.py "扁平化设计风格的数据分析图表，清新配色" --size 1024x1024
```

## 输出说明

- 生成的图片默认保存在**当前工作目录**
- 使用 `--output` 参数可以指定保存目录
- 文件名格式：`ai_image_YYYYMMDD_HHMMSS.jpg`
- 图片格式：JPEG（质量85，已优化）

## 错误处理

如果配置文件不存在，脚本会报错：
```
FileNotFoundError: 配置文件不存在: /path/to/ai_image_config.json
请确保配置文件 'ai_image_config.json' 在脚本同目录下
```

## 注意事项

1. 确保配置文件中的 `api_key` 有效且有足够余额
2. 提示词建议使用中文，描述清晰具体
3. 避免在提示词中包含品牌Logo、真人肖像等可能产生版权问题的内容
4. 不同尺寸适用场景：
   - `1024x1024`：方形配图，适合社交媒体
   - `1200x896`：微信公众号封面推荐尺寸
   - `1264x848`：宽屏配图，适合文档插图
   - `2048x512`：超宽横幅，适合网站banner
