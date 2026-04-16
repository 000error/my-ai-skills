#!/usr/bin/env python3
"""Upload image to image bed and insert into Markdown file"""

import json
import re
import argparse
from pathlib import Path
from abc import ABC, abstractmethod
from qiniu import Auth, put_file
import uuid


class ImageBedUploader(ABC):
    """Abstract base class for image bed uploaders"""

    @abstractmethod
    def upload(self, file_path):
        """Upload file and return URL"""
        pass


class QiniuUploader(ImageBedUploader):
    """Qiniu cloud uploader"""

    def __init__(self, config):
        self.access_key = config['access_key']
        self.secret_key = config['secret_key']
        self.bucket = config['bucket']
        self.domain = config['domain'].rstrip('/')
        self.auth = Auth(self.access_key, self.secret_key)

    def upload(self, file_path):
        """Upload file to Qiniu and return URL"""
        ext = Path(file_path).suffix
        key = f"{uuid.uuid4().hex}{ext}"
        token = self.auth.upload_token(self.bucket, key)
        ret, info = put_file(token, key, file_path)
        if info.status_code != 200:
            raise Exception(f"Upload failed: {info}")
        return f"http://{self.domain}/{key}"


def load_config(config_path='image_bed_config.json'):
    """Load image bed configuration"""
    script_dir = Path(__file__).parent
    config_file = script_dir / config_path if not Path(config_path).is_absolute() else Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_file}\n请确保配置文件 '{config_path}' 在脚本同目录下")
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config


def get_uploader(config):
    """Get uploader instance based on provider"""
    provider = config['provider']
    if provider == 'qiniu':
        return QiniuUploader(config['qiniu'])
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def find_matching_image(marker_name, search_dir):
    """Find image file matching marker name in search directory (recursive)"""
    search_path = Path(search_dir)
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']

    # First try exact match in search_dir directly
    for ext in extensions:
        candidate = search_path / f"{marker_name}{ext}"
        if candidate.exists():
            return candidate
        candidate = search_path / f"{marker_name}{ext.upper()}"
        if candidate.exists():
            return candidate

    # Search recursively in subdirectories
    for ext in extensions:
        for f in search_path.rglob(f"*{ext}"):
            if f.stem == marker_name:
                return f
        for f in search_path.rglob(f"*{ext.upper()}"):
            if f.stem == marker_name:
                return f

    return None


def insert_image_to_markdown(md_file, image_url, output_file=None):
    """Insert image after first heading in Markdown file"""
    md_path = Path(md_file)
    content = md_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    insert_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('#'):
            insert_index = i + 1
            break

    if insert_index == -1:
        insert_index = 0

    image_line = f"\n![封面图]({image_url})\n"
    lines.insert(insert_index, image_line)

    if output_file is None:
        output_file = Path.cwd() / f"{md_path.stem}_with_image{md_path.suffix}"

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    return output_path


def replace_markers_with_images(md_file, images_dir=None, config_path='image_bed_config.json', output_file=None):
    """Replace [*name*] markers in Markdown with uploaded local images"""
    md_path = Path(md_file)
    content = md_path.read_text(encoding='utf-8')

    # Find all markers
    markers = re.findall(r'\[\*(.+?)\*\]', content)
    if not markers:
        print("[信息] 文章中未找到图片标记 [*...*]")
        return None, 0, 0

    # Set images search directory
    search_dir = Path(images_dir) if images_dir else md_path.parent

    # Load config and get uploader
    config = load_config(config_path)
    uploader = get_uploader(config)

    uploaded_count = 0
    skipped_count = 0

    for marker_name in markers:
        matched_file = find_matching_image(marker_name, search_dir)

        if matched_file:
            print(f"[上传中] {matched_file.name} -> 匹配标记 [*{marker_name}*]")
            image_url = uploader.upload(str(matched_file))
            print(f"[成功] 图片URL: {image_url}")
            content = content.replace(f"[*{marker_name}*]", f"![{marker_name}]({image_url})")
            uploaded_count += 1
        else:
            print(f"[跳过] 未找到匹配图片: {marker_name}")
            skipped_count += 1

    if output_file is None:
        output_file = md_path.parent / f"{md_path.stem}_with_image{md_path.suffix}"

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')

    return output_path, uploaded_count, skipped_count


def main():
    parser = argparse.ArgumentParser(description='Upload image and insert into Markdown')
    parser.add_argument('markdown', help='Markdown file path')
    parser.add_argument('--image', help='Image file path (required for upload_insert mode)')
    parser.add_argument('--mode', choices=['upload_insert', 'replace_markers'], default='upload_insert',
                        help='Work mode: upload_insert (upload image and insert after heading) '
                             'or replace_markers (replace [*name*] markers with local images)')
    parser.add_argument('--images-dir', help='Directory to search for image files matching markers '
                                             '(default: same directory as markdown file)')
    parser.add_argument('--config', default='image_bed_config.json', help='Config file path')
    parser.add_argument('--output', help='Output Markdown file path')
    args = parser.parse_args()

    if args.mode == 'replace_markers':
        output_path, uploaded, skipped = replace_markers_with_images(
            args.markdown, args.images_dir, args.config, args.output
        )
        if output_path:
            print(f"[完成] 共上传 {uploaded} 张图片，跳过 {skipped} 个标记")
            print(f"[完成] 新文件: {output_path}")
        else:
            print("[完成] 无图片标记需要替换")
    else:
        if not args.image:
            parser.error("--image is required for upload_insert mode")
        config = load_config(args.config)
        uploader = get_uploader(config)
        print(f"[上传中] {args.image}")
        image_url = uploader.upload(args.image)
        print(f"[成功] 图片URL: {image_url}")
        output_file = insert_image_to_markdown(args.markdown, image_url, args.output)
        print(f"[完成] 新文件: {output_file}")


if __name__ == '__main__':
    main()
