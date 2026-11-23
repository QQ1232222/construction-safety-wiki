#!/usr/bin/env python3
"""
check_cards.py — 檢查 cards/ 下每張證據卡的數字是否附有期間與來源。

用法：
    python scripts/check_cards.py <cards_dir>

輸出：PASS 或 FAIL，並列出每個問題的檔案名稱與行號。
"""

import sys
import re
import os
from pathlib import Path

# Windows 終端機預設 cp950，強制 UTF-8 輸出
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# 匹配「實質數字」的正則：含數字且不是純頁碼標記、條號、日期格式
# 要求：至少一個阿拉伯數字
NUMBER_RE = re.compile(r'\d+')

# 期間模式：年度、季度、上半年、全年、前N季等
PERIOD_RE = re.compile(
    r'(\d{3,4}\s*年'           # 如「114年」「115年」
    r'|前\s*\d+\s*季'          # 如「前3季」
    r'|上半年|下半年|全年'
    r'|\d+\s*年\s*\d+\s*月'    # 如「115年8月」
    r'|\d+\s*月\s*\d+\s*日'    # 如「11月3日」
    r')'
)

# 來源模式：S1–S7 加頁碼，或 S6 第 X 條
SOURCE_RE = re.compile(r'S[1-7]')

# 純粹是條號（第 X 條）、頁碼標記（p.N）、日期（YYYY-MM-DD）的行可以豁免
EXEMPT_RE = re.compile(
    r'^\s*\|?\s*第\s*\d+\s*條'              # 表格中條號列
    r'|\bp\.\d+'                             # 頁碼標記
    r'|\d{4}-\d{2}-\d{2}'                   # ISO 日期
    r'|\d+年\d+月\d+日'                      # 中文日期
    r'|民國\s*\d+\s*年'                      # 民國年份
    r'|^\s*\|?(?:\s*:?-+:?\s*\|?)+\s*$'    # Markdown 表格分隔列（---|---|）
    r'|^\s*$'                                # 空白行
    r'|^\s*#'                                # 標題行
    r'|^\s*\|?\s*來源\s*wiki'               # 表頭「來源 wiki」
    r'|^\s*\|[^\|]*數據描述'                 # 表格欄位標題列
    r'|XX'                                   # 範本佔位符
)


def check_card(filepath: Path) -> list[str]:
    """回傳問題清單，空清單表示 PASS。"""
    issues = []
    lines = filepath.read_text(encoding='utf-8').splitlines()

    in_data_table = False

    for lineno, line in enumerate(lines, start=1):
        # 偵測是否在「數據摘錄」表格內
        if '## 數據摘錄' in line or '## 數據' in line:
            in_data_table = True
            continue
        if line.startswith('## ') and '數據' not in line:
            in_data_table = False

        # 豁免行
        if EXEMPT_RE.search(line):
            continue

        # 只檢查含數字的行
        if not NUMBER_RE.search(line):
            continue

        # 表格資料行（含 | 且有數字）
        if '|' in line or in_data_table:
            has_period = bool(PERIOD_RE.search(line))
            has_source = bool(SOURCE_RE.search(line))

            # 允許數值欄位在同一表格列中有期間與來源
            if not has_period:
                issues.append(
                    f"  {filepath.name}:{lineno} — 數字缺少期間標記：{line.strip()[:80]}"
                )
            if not has_source:
                issues.append(
                    f"  {filepath.name}:{lineno} — 數字缺少來源標記（S[N]）：{line.strip()[:80]}"
                )

    return issues


def main():
    if len(sys.argv) < 2:
        print("用法：python scripts/check_cards.py <cards_dir>")
        sys.exit(1)

    cards_dir = Path(sys.argv[1])
    if not cards_dir.exists():
        print(f"FAIL\n  目錄不存在：{cards_dir}")
        sys.exit(1)

    md_files = sorted(cards_dir.glob('*.md'))
    if not md_files:
        print(f"FAIL\n  cards/ 目錄下沒有任何 .md 檔案：{cards_dir}")
        sys.exit(1)

    all_issues = []
    for md_file in md_files:
        issues = check_card(md_file)
        all_issues.extend(issues)

    if all_issues:
        print("FAIL")
        print(f"發現 {len(all_issues)} 個問題：\n")
        for issue in all_issues:
            print(issue)
        sys.exit(1)
    else:
        print(f"PASS — 檢查了 {len(md_files)} 張證據卡，全部符合規範")
        sys.exit(0)


if __name__ == '__main__':
    main()
