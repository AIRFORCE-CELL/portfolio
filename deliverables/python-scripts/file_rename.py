#!/usr/bin/env python3
"""
文件批量重命名工具
支持：替换文字、添加前缀/后缀、序号命名
"""
import argparse
import os
import re


def rename_files(folder: str, pattern: str, replace: str = "",
                 prefix: str = "", suffix: str = "",
                 numbering: bool = False, dry_run: bool = True):
    """批量重命名"""
    files = sorted(os.listdir(folder))
    renamed = 0

    for i, old_name in enumerate(files, 1):
        old_path = os.path.join(folder, old_name)
        if os.path.isdir(old_path):
            continue

        name, ext = os.path.splitext(old_name)

        if numbering:
            new_name = f"{i:03d}{ext}"
        else:
            new_name = name
            if pattern:
                new_name = re.sub(pattern, replace, new_name)
            if prefix:
                new_name = prefix + new_name
            if suffix:
                new_name = new_name + suffix
            new_name += ext

        if new_name == old_name:
            continue

        new_path = os.path.join(folder, new_name)
        if dry_run:
            print(f"  {old_name}  →  {new_name}")
        else:
            os.rename(old_path, new_path)
            print(f"✅ {old_name}  →  {new_name}")
        renamed += 1

    action = "预览" if dry_run else "完成"
    print(f"\n{action}: {renamed} 个文件")


def main():
    parser = argparse.ArgumentParser(description="批量重命名文件")
    parser.add_argument("folder", help="目标文件夹")
    parser.add_argument("-p", "--pattern", help="要替换的文字（正则）")
    parser.add_argument("-r", "--replace", default="", help="替换为")
    parser.add_argument("--prefix", default="", help="添加前缀")
    parser.add_argument("--suffix", default="", help="添加后缀")
    parser.add_argument("--numbering", action="store_true", help="改为 001/002/003 序号")
    parser.add_argument("--go", action="store_true", help="真正执行（不加 --go 只预览）")
    args = parser.parse_args()

    if not any([args.pattern, args.prefix, args.suffix, args.numbering]):
        parser.print_help()
        print("\n💡 示例:")
        print("  预览:   python file_rename.py ./图片 --prefix 旅行_")
        print("  执行:   python file_rename.py ./图片 --prefix 旅行_ --go")
        print("  序号:   python file_rename.py ./图片 --numbering --go")
        return

    rename_files(args.folder, args.pattern, args.replace,
                 args.prefix, args.suffix, args.numbering,
                 dry_run=not args.go)


if __name__ == "__main__":
    main()
