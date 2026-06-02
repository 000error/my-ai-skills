#!/usr/bin/env python3
"""AI Image Generator - Generate images using AI models"""

import requests
import json
import base64
import argparse
from pathlib import Path
from datetime import datetime
from PIL import Image
from io import BytesIO


def load_config(config_path='ai_image_config.json'):
    """Load AI image generation configuration"""
    script_dir = Path(__file__).parent
    config_file = script_dir / config_path if not Path(config_path).is_absolute() else Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_file}\n请确保配置文件 '{config_path}' 在脚本同目录下")

    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_image(prompt, config, size=None):
    """Generate image using AI model API"""
    url = config['api_url']
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }

    data = {
        "output_type": config['output_type'],
        "number_results": config['number_results'],
        "model": config['model'],
        "prompt": prompt,
        "size": size or config['default_size']
    }

    # Add output_format if specified in config
    if 'output_format' in config:
        data['output_format'] = config['output_format']

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            error_info = response.json() if response.text else {}
            error_msg = error_info.get('error', {}).get('message', response.text)
            print(f"[错误] 生成失败 (状态码: {response.status_code})")
            print(f"[错误] 详细信息: {error_msg}")
            return None

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[错误] 网络请求失败: {e}")
        return None


def save_image_from_base64(base64_data, output_dir='.', convert_to_jpeg=True):
    """Save base64 image to file, optionally convert to JPEG"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Handle potential base64 prefix
    if isinstance(base64_data, str):
        if base64_data.startswith('data:'):
            base64_data = base64_data.split(',', 1)[1]
        # Remove whitespace
        base64_data = base64_data.strip().replace('\n', '').replace('\r', '').replace(' ', '')
        # Fix padding if needed
        missing_padding = len(base64_data) % 4
        if missing_padding:
            base64_data += '=' * (4 - missing_padding)

    try:
        # Use validate=False for more lenient decoding
        image_data = base64.b64decode(base64_data, validate=False)

        # Convert to JPEG if requested
        if convert_to_jpeg:
            img = Image.open(BytesIO(image_data))
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"ai_image_{timestamp}.jpg"
            filepath = output_path / filename

            img.save(filepath, 'JPEG', quality=85, optimize=True)
            return filepath
        else:
            # Detect image format from header
            if image_data.startswith(b'\x89PNG'):
                ext = 'png'
            elif image_data.startswith(b'\xff\xd8\xff'):
                ext = 'jpg'
            else:
                ext = 'jpg'

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"ai_image_{timestamp}.{ext}"
            filepath = output_path / filename

            filepath.write_bytes(image_data)
            return filepath
    except Exception as e:
        print(f"[错误] 图片处理失败: {e}")
        raise


def save_image_from_url(url, output_dir='.', convert_to_jpeg=True):
    """Download and save image from URL, optionally convert to JPEG"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()

    if convert_to_jpeg:
        img = Image.open(BytesIO(response.content))
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ai_image_{timestamp}.jpg"
        filepath = output_path / filename

        img.save(filepath, 'JPEG', quality=85, optimize=True)
        return filepath
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ai_image_{timestamp}.jpg"
        filepath = output_path / filename

        filepath.write_bytes(response.content)
        return filepath


def main():
    parser = argparse.ArgumentParser(description='Generate images using AI')
    parser.add_argument('prompt', help='Image generation prompt')
    parser.add_argument('--size', help='Image size (e.g., 1024x1024)')
    parser.add_argument('--config', default='ai_image_config.json', help='Config file')
    parser.add_argument('--output', default='.', help='Output directory')
    args = parser.parse_args()

    config = load_config(args.config)

    print(f"[生成中] 提示词: {args.prompt}")
    result = generate_image(args.prompt, config, args.size)

    if result is None:
        print("[失败] 图片生成失败，请检查配置和账户余额")
        return

    if 'data' in result and len(result['data']) > 0:
        for idx, item in enumerate(result['data']):
            if 'b64_json' in item:
                filepath = save_image_from_base64(item['b64_json'], args.output)
                print(f"[完成] 图片已保存: {filepath}")
            elif 'content' in item:
                filepath = save_image_from_base64(item['content'], args.output)
                print(f"[完成] 图片已保存: {filepath}")
            elif 'url' in item:
                filepath = save_image_from_url(item['url'], args.output)
                print(f"[完成] 图片已保存: {filepath}")
            else:
                print(f"[错误] 返回数据格式不支持")
    else:
        print(f"[错误] 未生成图片")


if __name__ == '__main__':
    main()
