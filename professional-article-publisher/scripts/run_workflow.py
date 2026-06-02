#!/usr/bin/env python3
"""Workflow script with custom markdown and prompt files"""

import subprocess
import sys
import re
import locale
import argparse
import time
import traceback
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# Logger: 同时写控制台和日志文件
# ---------------------------------------------------------------------------

class WorkflowLogger:
    def __init__(self):
        self._lines = []
        self.log_file = None

    def set_log_file(self, path):
        self.log_file = Path(path)
        # 写入文件头
        self._write_to_file(f"工作流日志 — 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    def log(self, msg=""):
        print(msg)
        self._lines.append(msg)
        if self.log_file:
            self._write_to_file(msg + "\n")

    def _write_to_file(self, text):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(text)
        except Exception:
            pass


_logger = WorkflowLogger()


def log(msg=""):
    _logger.log(msg)


# ---------------------------------------------------------------------------
# fail(): 中断流程，打印失败原因，保存日志
# ---------------------------------------------------------------------------

def fail(step_name, reason, detail=""):
    sep = "=" * 60
    log("")
    log(sep)
    log(f"[失败] 工作流在「{step_name}」环节中断")
    log(f"[原因] {reason}")
    if detail:
        log("[详情]")
        for line in detail.strip().splitlines():
            log(f"       {line}")
    log(sep)
    if _logger.log_file and _logger.log_file.exists():
        log(f"\n失败日志已保存至: {_logger.log_file}")
    sys.exit(1)


# ---------------------------------------------------------------------------
# 命令执行
# ---------------------------------------------------------------------------

def run_command(cmd, step_name, cwd=None):
    """执行命令；失败立即调用 fail()"""
    log(f"\n[执行] {' '.join(str(c) for c in cmd)}")
    enc = locale.getpreferredencoding()
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding=enc)
    if result.stdout:
        log(result.stdout.rstrip())
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "（无详细输出）").strip()
        fail(step_name, f"子进程退出码 {result.returncode}", detail)
    return result


def run_command_tolerant(cmd, cwd=None):
    """执行命令；失败只记录警告，不中断流程"""
    log(f"\n[执行] {' '.join(str(c) for c in cmd)}")
    enc = locale.getpreferredencoding()
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding=enc)
    if result.stdout:
        log(result.stdout.rstrip())
    if result.returncode != 0:
        stderr = (result.stderr or "（无详细输出）").strip()
        log(f"[警告] 命令失败 (退出码 {result.returncode}): {stderr}")
    return result


# ---------------------------------------------------------------------------
# 兜底图片
# ---------------------------------------------------------------------------

def generate_fallback_image(prompt_text, output_folder):
    """两次 AI 生图均失败后，生成蓝底白字兜底图片"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        fail("步骤1 生成图片", "兜底图片生成失败：Pillow (PIL) 未安装，请执行 pip install Pillow")

    try:
        img = Image.new("RGB", (1280, 640), color=(30, 80, 160))
        draw = ImageDraw.Draw(img)
        title = prompt_text[:50]
        font = None
        for fp in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/arial.ttf"]:
            try:
                font = ImageFont.truetype(fp, 40)
                break
            except Exception:
                continue
        if font is None:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), title, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((1280 - w) // 2, (640 - h) // 2), title, fill="white", font=font)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = output_folder / f"ai_image_{ts}.jpg"
        img.save(img_path, "JPEG", quality=85)
        log(f"[兜底] 蓝底白字兜底图片已生成: {img_path}")
        return img_path
    except Exception as e:
        fail("步骤1 生成图片", "兜底图片生成失败", traceback.format_exc())


# ---------------------------------------------------------------------------
# 图片标记检测
# ---------------------------------------------------------------------------

def find_marker_images(md_file, images_dir=None):
    """检测Markdown文件中的[*...*]图片标记，并查找匹配的本地图片"""
    content = Path(md_file).read_text(encoding="utf-8")
    markers = re.findall(r'\[\*(.+?)\*\]', content)
    if not markers:
        return [], []

    search_dir = Path(images_dir) if images_dir else Path(md_file).parent
    matched = []
    for marker_name in markers:
        matched_file = None
        # Search in directory directly
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp',
                    '.JPG', '.JPEG', '.PNG', '.GIF', '.WEBP', '.BMP']:
            candidate = search_dir / f"{marker_name}{ext}"
            if candidate.exists():
                matched_file = candidate
                break
        # Recursive search in subdirectories
        if not matched_file:
            for ext_pattern in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp', '*.bmp',
                                '*.JPG', '*.JPEG', '*.PNG', '*.GIF', '*.WEBP', '*.BMP']:
                for f in search_dir.rglob(ext_pattern):
                    if f.stem == marker_name:
                        matched_file = f
                        break
                if matched_file:
                    break
        if matched_file:
            matched.append((marker_name, matched_file))

    return markers, matched


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="运行完整工作流：生成图片、上传、转换HTML")
    parser.add_argument("--md",         required=True, help="Markdown文件路径（必需）")
    parser.add_argument("--prompt",     default=None,  help="提示词文件路径（AI生图模式必需）")
    parser.add_argument("--images-dir", default=None,  help="图片搜索目录（用于[*图片*]标记匹配，默认为文章所在目录）")
    args = parser.parse_args()

    md_file = Path(args.md)

    # ── 输入验证 ──────────────────────────────────────────────────────────
    if not md_file.exists():
        fail("输入验证", f"Markdown 文件不存在: {md_file}")

    # ── 检测图片标记 ─────────────────────────────────────────────────────
    markers, matched_images = find_marker_images(md_file, args.images_dir)

    # ── 建立输出文件夹 & 日志文件 ─────────────────────────────────────────
    project_root  = Path(__file__).parent
    timestamp     = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = md_file.resolve().parent / f"workflow_output_{timestamp}"
    output_folder.mkdir(exist_ok=True)

    log_file = output_folder / "workflow_log.txt"
    _logger.set_log_file(log_file)   # 从这行起，所有 log() 同步写入文件

    log(f"[输入] Markdown文件  : {md_file.resolve()}")
    log(f"[输出] 目标文件夹    : {output_folder}")
    log(f"[日志] 日志文件      : {log_file}")

    md_with_image = output_folder / f"{md_file.stem}_with_image.md"

    if matched_images:
        # ══════════════════════════════════════════════════════════════════
        # 本地图片替换模式：检测到 [*...*] 标记且有对应本地图片
        # ══════════════════════════════════════════════════════════════════
        log(f"\n=== 检测到 {len(markers)} 个图片标记，其中 {len(matched_images)} 个有对应本地图片 ===")
        log("[模式] 使用本地图片替换模式，跳过AI生图")
        for name, path in matched_images:
            log(f"  [*{name}*] -> {path}")

        search_dir = Path(args.images_dir) if args.images_dir else md_file.parent
        upload_script = project_root / "image_uploader" / "upload_image.py"
        run_command(
            [sys.executable, str(upload_script), str(md_file),
             "--mode", "replace_markers",
             "--images-dir", str(search_dir),
             "--output", str(md_with_image)],
            step_name="本地图片上传并替换标记",
        )
        log(f"[完成] 带图 Markdown: {md_with_image}")

    else:
        # ══════════════════════════════════════════════════════════════════
        # AI 生图模式：无图片标记或无匹配本地图片
        # ══════════════════════════════════════════════════════════════════
        if not args.prompt:
            fail("输入验证", "未检测到可替换的图片标记，且未提供 --prompt 参数，无法继续")
        prompt_file = Path(args.prompt)
        if not prompt_file.exists():
            fail("输入验证", f"提示词文件不存在: {prompt_file}")

        prompt = prompt_file.read_text(encoding="utf-8").strip()
        if not prompt:
            fail("输入验证", f"提示词文件为空: {prompt_file}")

        log(f"[输入] 提示词文件    : {prompt_file.resolve()}")
        log(f"[提示词] {prompt}")

        # ── 步骤 1：生成图片（含重试 + 兜底）──────────────────────────────
        log("\n=== 步骤1: 生成图片 ===")
        gen_script = project_root / "ai_image_generator" / "generate_image.py"
        img_cmd    = [sys.executable, str(gen_script), prompt, "--output", str(output_folder)]
        run_command_tolerant(img_cmd)
        image_files = list(output_folder.glob("ai_image_*.jpg"))

        if not image_files:
            log("[重试] 第一次生成失败，等待 2 秒后重试...")
            time.sleep(2)
            run_command_tolerant(img_cmd)
            image_files = list(output_folder.glob("ai_image_*.jpg"))

        if not image_files:
            log("[兜底] 两次生成均失败，启用蓝底白字兜底图片...")
            image_files = [generate_fallback_image(prompt, output_folder)]

        generated_image = image_files[0]
        log(f"[完成] 图片已就绪: {generated_image}")

        # ── 步骤 2：上传图片并插入 Markdown ───────────────────────────────
        log("\n=== 步骤2: 上传图片并插入Markdown ===")
        upload_script = project_root / "image_uploader" / "upload_image.py"
        run_command(
            [sys.executable, str(upload_script), str(md_file),
             "--image", str(generated_image),
             "--output", str(md_with_image)],
            step_name="步骤2 上传图片并插入Markdown",
        )
        log(f"[完成] 带图 Markdown: {md_with_image}")

    # ── 步骤 3：转换为微信 HTML（两种模式共用）───────────────────────────
    log("\n=== 步骤3: 转换为微信HTML ===")
    md2wechat_script = project_root / "md2wechat" / "md2wechat.py"
    html_output      = output_folder / f"{md_file.stem}_wechat.html"
    run_command(
        [sys.executable, str(md2wechat_script), str(md_with_image), "--output", str(html_output)],
        step_name="步骤3 转换微信HTML",
    )
    log(f"[完成] 微信HTML: {html_output}")

    # ── 完成 ───────────────────────────────────────────────────────────────
    log(f"\n{'='*60}")
    log(f"[成功] 工作流全部完成！输出目录: {output_folder}")
    log(f"{'='*60}")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        log(f"\n[异常] 发生未预期错误:")
        log(traceback.format_exc())
        sys.exit(1)
