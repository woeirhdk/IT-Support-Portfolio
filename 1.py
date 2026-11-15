import re
import sys
from pathlib import Path

IMAGE_RE = re.compile(r'^\s*!\[[^\]]*\]\([^)]*\)\s*$')
FENCE_RE = re.compile(r'^\s*(```+|~~~+)')

def fix_blank_lines_around_images(text: str) -> str:
    lines = text.splitlines()
    result = []
    in_fence = False
    fence_marker = None

    for line in lines:
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker[0] == fence_marker[0] and len(marker) >= len(fence_marker):
                in_fence = False
            result.append(line)
            continue

        if in_fence:
            result.append(line)
            continue

        if IMAGE_RE.match(line):
            # 确保图片前有空行
            if result and result[-1].strip() != "":
                result.append("")
            result.append(line)
            # 确保图片后有空行（先放一个占位，下一行处理）
            result.append("")
        else:
            result.append(line)

    # 清理：去掉因连续图片或尾部造成的多余空行，合并连续空行
    cleaned = []
    for line in result:
        if line.strip() == "" and cleaned and cleaned[-1].strip() == "":
            continue
        cleaned.append(line)

    # 确保文件末尾只有一个换行
    while cleaned and cleaned[-1].strip() == "":
        cleaned.pop()
    return "\n".join(cleaned) + "\n"


def process_file(path: Path, check_only: bool = False):
    original = path.read_text(encoding="utf-8")
    fixed = fix_blank_lines_around_images(original)
    if fixed == original:
        return False
    if check_only:
        print(f"[需要修改] {path}")
    else:
        path.write_text(fixed, encoding="utf-8")
        print(f"[已修复] {path}")
    return True


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    check = "--check" in sys.argv
    count = 0
    for md in root.rglob("*.md"):
        if process_file(md, check_only=check):
            count += 1
    print(f"\n完成。{'需要修改' if check else '已修复'} {count} 个文件。")