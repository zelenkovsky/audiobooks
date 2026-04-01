#!/usr/bin/env python3
"""Parse /workspace/index.md and generate books.json for the AudioBooks section."""

import json
import re

INPUT = "/workspace/index.md"
OUTPUT = "/workspace/Projects/index/books.json"

SEPARATOR_RE = re.compile(r"\s+[-–—]\s+")

CONJUNCTIONS = {"и", "да", "де", "ван", "фон", "ди", "ле", "ла", "аль"}

GENRE_PREFIXES = {
    "Сказка",
    "Сказки",
    "Повесть",
    "Рассказ",
    "Рассказы",
    "Композиция",
    "Постановка",
    "Инсценировка",
    "Радиоспектакль",
    "Мюзикл",
    "Музыкальная",
    "Музыкальный",
    "Музыкальня",
    "Литературное",
    "Журнал",
    "Серия",
}

NOT_AUTHOR_START = {
    "Книга",
    "Сказка",
    "Сказки",
    "Повесть",
    "Рассказ",
    "Рассказы",
    "Музыкальная",
    "Музыкальный",
    "Музыкальня",
    "Постановка",
    "Инсценировка",
    "Басни",
    "Стихи",
    "Стихотворения",
    "Песни",
    "Запись",
    "Композиция",
    "Радиоспектакль",
    "Журнал",
    "Новогодний",
    "Восточные",
    "Русские",
    "Детские",
    "Колыбельные",
}


def _all_significant_words_uppercase(s):
    for m in re.finditer(r"[А-ЯЁA-Zа-яёa-zёЁ]+", s):
        word = m.group()
        if word.lower() in CONJUNCTIONS:
            continue
        if word[0].islower():
            return False
    return True


def _is_name_like(candidate):
    candidate = candidate.strip()
    if not candidate:
        return False
    if len(candidate) < 2:
        return False
    if re.match(r"^[0-9]", candidate):
        return False
    return _all_significant_words_uppercase(candidate)


def extract_author(title):
    # 1. "Author - Title" — first space-surrounded dash
    m = SEPARATOR_RE.search(title)
    if m:
        candidate = title[: m.start()].strip()
        if candidate and _is_name_like(candidate):
            first_word = re.match(r"[А-ЯЁа-яёA-Za-z]+", candidate)
            if first_word and first_word.group() not in NOT_AUTHOR_START:
                return candidate

    # 2. "YYYY - Author - Title" or "YYYY - Attribution" (vinyl records)
    m = re.match(r"^\d{4}\s+[-–—]\s+(.+)$", title)
    if m:
        rest = m.group(1)
        m2 = SEPARATOR_RE.search(rest)
        if m2:
            return rest[: m2.start()].strip()
        return rest.strip()

    # 3. Role-based: "Читает Author", "Исполняет Author"
    m = re.search(r"(?:читает|исполняет)\s+(.+)$", title, re.IGNORECASE)
    if m:
        result = m.group(1).strip()
        # Split at sentence boundaries (period + space + uppercase)
        # but don't split after single-letter initials (e.g., "Э. Успенский")
        parts = re.split(r"\.\s+(?=[А-ЯЁA-Z])", result)
        if len(parts) > 1 and len(parts[0]) > 2:
            result = parts[0]
        return result

    # 4. "Title. [Genre word] Author" or "Title. Author"
    last_dot = title.rfind(". ")
    if last_dot >= 0:
        after = title[last_dot + 2 :].strip().strip('"\u201c\u201d')
        words = after.split()
        if words:
            start = 0
            while start < len(words) and words[start] in GENRE_PREFIXES:
                start += 1
            if start < len(words):
                candidate = " ".join(words[start:])
                if _is_name_like(candidate):
                    return candidate

    return ""


def parse_line(line):
    line = line.strip()
    if not line.startswith("- "):
        return None

    line = line[2:]

    parts = line.split("|")
    if len(parts) != 3:
        return None

    raw_title = parts[0].strip()
    raw_meta = parts[1].strip()
    raw_path = parts[2].strip().strip("`")

    title = raw_title
    author = extract_author(title)

    files = 0
    fmt = ""
    meta_match = re.match(r"(\d+)\s+(.+)", raw_meta)
    if meta_match:
        files = int(meta_match.group(1))
        fmt = meta_match.group(2).strip()
    elif re.match(r"^(\d+)$", raw_meta.strip()):
        files = int(raw_meta.strip())

    return {
        "title": title,
        "author": author,
        "path": raw_path,
        "files": files,
        "format": fmt,
    }


def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    in_audiobooks = False

    for line in lines:
        stripped = line.strip()

        if stripped == "## AudioBooks/":
            in_audiobooks = True
            continue

        if stripped.startswith("## Music/"):
            break

        if stripped == "---" and in_audiobooks:
            continue

        if not in_audiobooks:
            continue

        entry = parse_line(line)
        if entry:
            entries.append(entry)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"Generated {OUTPUT} with {len(entries)} entries")


if __name__ == "__main__":
    main()
