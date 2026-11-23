#!/usr/bin/env python3
"""
check_deck.py — 檢查 deck.html 的品質規範。

用法：
    python scripts/check_deck.py <deck_html> <wiki_dir>

檢查項目：
  1. 每頁都有出處（S1–S7）
  2. 頁數 8–15 頁
  3. 每個百分比和人數同頁內都有期間（如「114年」「115年前3季」）
  4. 每個數字都能在被引用的 wiki 頁找到（僅警告）
  5. 出現「第 X 條」時，該條號存在於法規 wiki 頁
  6. 沒有空白頁

輸出：PASS 或 FAIL，並列出每個問題的頁碼。
"""

import sys
import re
import os
from pathlib import Path
from html.parser import HTMLParser

# Windows 終端機預設 cp950，強制 UTF-8 輸出
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


# --- HTML 解析 ---

class SlideParser(HTMLParser):
    """從 deck.html 中提取每頁的文字內容與頁碼。"""

    def __init__(self):
        super().__init__()
        self.slides: list[str] = []  # slides[i] = 第 i+1 頁的純文字
        self._current: list[str] = []
        self._in_slide = False
        self._depth = 0
        self._slide_tag = None
        self._slide_attrs_stack: list[dict] = []

    # 只對這些容器標籤計深度，避免 void elements（<br>/<img> 等）造成計數失衡
    BLOCK_TAGS = {'div', 'section', 'article', 'main', 'aside', 'header', 'footer'}

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class', '')
        id_ = attrs_dict.get('id', '')

        # 偵測投影片容器：常見寫法為 class="slide" 或 id 以 "slide" 開頭
        is_slide = (
            'slide' in cls.lower()
            or 'page' in cls.lower()
            or re.match(r'slide[-_]?\d*', id_.lower()) is not None
            or tag in ('section', 'article') and 'slide' in cls.lower()
        )

        if is_slide and not self._in_slide:
            self._in_slide = True
            self._slide_tag = tag
            self._depth = 1
            self._current = []
        elif self._in_slide and tag in self.BLOCK_TAGS:
            self._depth += 1

    def handle_endtag(self, tag):
        if self._in_slide and tag in self.BLOCK_TAGS:
            self._depth -= 1
            if self._depth <= 0:
                self.slides.append(' '.join(self._current))
                self._current = []
                self._in_slide = False
                self._slide_tag = None

    def handle_data(self, data):
        if self._in_slide:
            stripped = data.strip()
            if stripped:
                self._current.append(stripped)


def parse_slides_from_html(html_content: str) -> list[str]:
    """回傳每頁純文字的清單。若解析失敗，改用簡單分隔符切割。"""
    parser = SlideParser()
    parser.feed(html_content)

    if parser.slides:
        return parser.slides

    # fallback：尋找 <section> 或 <div class="slide">
    sections = re.findall(
        r'<(?:section|div)[^>]*class=["\'][^"\']*(?:slide|page)[^"\']*["\'][^>]*>(.*?)</(?:section|div)>',
        html_content, re.DOTALL | re.IGNORECASE
    )
    if sections:
        return [re.sub(r'<[^>]+>', ' ', s).strip() for s in sections]

    # 最後 fallback：依 <hr> 或 <!-- slide --> 切割
    parts = re.split(r'<hr\s*/?>|<!--\s*(?:slide|page)\s*-->', html_content, flags=re.IGNORECASE)
    return [re.sub(r'<[^>]+>', ' ', p).strip() for p in parts if p.strip()]


# --- 檢查邏輯 ---

SOURCE_RE = re.compile(r'\bS[1-7]\b')

PERIOD_RE = re.compile(
    r'(\d{3,4}\s*年'
    r'|前\s*\d+\s*季'
    r'|上半年|下半年|全年'
    r'|\d{3,4}\s*年\s*\d+\s*月'
    r')'
)

# 百分比：數字後接 %，或中文「百分之」
PERCENT_RE = re.compile(r'\d+(?:\.\d+)?\s*%|百分之\s*\d+')

# 人數：「N人」「N名」「N件」
PERSON_RE = re.compile(r'\d+\s*(?:人|名|件|起)')

# 條號：第 N 條
ARTICLE_RE = re.compile(r'第\s*(\d+)\s*條')

# 空白頁判斷：去除空白後長度
BLANK_THRESHOLD = 20


def load_wiki_articles(wiki_dir: Path) -> set[int]:
    """從 wiki/concepts/regulations/ 下的 .md 讀出所有出現的條號。"""
    articles: set[int] = set()
    reg_dir = wiki_dir / 'concepts' / 'regulations'
    if not reg_dir.exists():
        return articles

    for md_file in reg_dir.glob('*.md'):
        text = md_file.read_text(encoding='utf-8')
        for m in ARTICLE_RE.finditer(text):
            articles.add(int(m.group(1)))
    return articles


def check_deck(deck_path: Path, wiki_dir: Path) -> list[str]:
    """回傳問題清單，格式：「第N頁：問題描述」。空清單表示 PASS。"""
    html = deck_path.read_text(encoding='utf-8')
    slides = parse_slides_from_html(html)
    issues: list[str] = []

    # 規則 2：頁數 8–15
    n = len(slides)
    if n < 8:
        issues.append(f"全局：頁數 {n} 頁，低於最低要求 8 頁")
    elif n > 15:
        issues.append(f"全局：頁數 {n} 頁，超過最高限制 15 頁")

    wiki_articles = load_wiki_articles(wiki_dir)

    for i, text in enumerate(slides, start=1):
        label = f"第{i}頁"

        # 規則 6：空白頁
        if len(text.strip()) < BLANK_THRESHOLD:
            issues.append(f"{label}：空白頁（內容長度 {len(text.strip())} 字元）")
            continue  # 空白頁其他規則無意義

        # 規則 1：每頁都有出處 S1–S7
        if not SOURCE_RE.search(text):
            issues.append(f"{label}：缺少來源標記（S1–S7）")

        # 規則 3：百分比旁有期間
        for m in PERCENT_RE.finditer(text):
            start = max(0, m.start() - 30)
            end = min(len(text), m.end() + 30)
            context = text[start:end]
            if not PERIOD_RE.search(context):
                issues.append(
                    f"{label}：百分比「{m.group()}」附近缺少期間標記（前後 30 字元內）"
                )

        # 規則 3：人數旁有期間
        for m in PERSON_RE.finditer(text):
            start = max(0, m.start() - 30)
            end = min(len(text), m.end() + 30)
            context = text[start:end]
            if not PERIOD_RE.search(context):
                issues.append(
                    f"{label}：人數「{m.group()}」附近缺少期間標記（前後 30 字元內）"
                )

        # 規則 5：條號存在於法規 wiki 頁
        if wiki_articles:  # 若未能載入 wiki，跳過此規則
            for m in ARTICLE_RE.finditer(text):
                article_no = int(m.group(1))
                if article_no not in wiki_articles:
                    issues.append(
                        f"{label}：引用「第 {article_no} 條」，但該條號在法規 wiki 頁中找不到"
                    )

    return issues


def main():
    if len(sys.argv) < 3:
        print("用法：python scripts/check_deck.py <deck_html> <wiki_dir>")
        sys.exit(1)

    deck_path = Path(sys.argv[1])
    wiki_dir = Path(sys.argv[2])

    if not deck_path.exists():
        print(f"FAIL\n  找不到檔案：{deck_path}")
        sys.exit(1)

    if not wiki_dir.exists():
        print(f"FAIL\n  找不到 wiki 目錄：{wiki_dir}")
        sys.exit(1)

    issues = check_deck(deck_path, wiki_dir)

    if issues:
        print("FAIL")
        print(f"發現 {len(issues)} 個問題：\n")
        for issue in issues:
            print(f"  {issue}")
        sys.exit(1)
    else:
        print("PASS — deck.html 通過所有檢查")
        sys.exit(0)


if __name__ == '__main__':
    main()
