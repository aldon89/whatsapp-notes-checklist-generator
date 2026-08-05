import os
import re
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

OLLAMA_MODEL = "deepseek-r1:7b"

SECTION_TITLES = {
    "summary": "**1. 摘要**",
    "todo": "**2. 待辦清單**",
    "follow": "**3. 跟進事項**",
}


def choose_input_file() -> str:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    file_path = filedialog.askopenfilename(
        title="選擇 txt 檔",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    root.destroy()
    return file_path


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"找不到輸入檔案：{path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"輸入檔案是空的：{path}")
    return text


def extract_key_sentences(text: str) -> str:
    kept = []
    keywords = [
        "要", "應該", "需要", "要再", "明天", "星期", "聽日", "今日", "搬", "改",
        "追", "確認", "查看", "丟", "收", "用唔著", "拒收", "合約", "用途", "回收",
        "木碎", "樹皮", "Yard Waste", "AECOM", "CLP", "11kV", "132kV"
    ]

    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue
        if any(tag in s for tag in keywords):
            kept.append(s)
            continue
        if re.search(r"\d", s):
            kept.append(s)
            continue

    return "\n".join(kept) if kept else text.strip()


def build_prompt(text: str) -> str:
    return f"""
你係一個通用文字整理助手。
無論輸入係咩主題，都請根據原文內容，整理成繁體中文。

規則：
1. 只根據輸入文字作答，不加新資訊。
2. 保留原文中的事實、數字、日期、名詞、術語。
3. 如果有唔完整或唔確定嘅地方，寫「未明」。
4. 不要輸出表格。
5. 只輸出以下三部分，且每部分只出現一次：
   **1. 摘要**
   **2. 待辦清單**
   **3. 跟進事項**
6. 不要重複標題。
7. 不要輸出泰文、英文句子或其他語言，除非係原文名詞/型號/專有名詞。
8. 摘要：用 1-4 點簡潔重述原文重點。
9. 待辦清單：只列原文有提到要做的事情。
10. 跟進事項：只列原文提到未完成、未處理、或要再確認的事情。
11. 如果某部分冇內容，寫「未明」。
12. 每個部分請用「-」列點。

原文：
{text}
""".strip()


def run_ollama(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError(f"Ollama 執行失敗：{result.stderr.strip()}")
    output = result.stdout.strip()
    if not output:
        raise RuntimeError("Ollama 冇輸出內容")
    return output


def _clean_item(line: str) -> str | None:
    s = line.strip()
    if not s:
        return None
    s = re.sub(r"^[*\-•\s]+", "", s)
    s = re.sub(r"^\d+[\.)]\s*", "", s)
    s = s.replace("未明。", "未明")
    s = re.sub(r"\s+", "", s) if len(s) < 12 else re.sub(r"\s+", " ", s)
    if s in {"", "未明"}:
        return None
    return s


def normalize_output(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    sections = {"summary": [], "todo": [], "follow": []}
    current = None

    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue

        if "摘要" in s and (s.startswith("**") or s.startswith("#") or s.startswith("1") or current is None):
            current = "summary"
            continue
        if "待辦" in s and (s.startswith("**") or s.startswith("#") or s.startswith("2") or current is not None):
            current = "todo"
            continue
        if "跟進" in s and (s.startswith("**") or s.startswith("#") or s.startswith("3") or current is not None):
            current = "follow"
            continue

        if re.search(r"[A-Za-z]", s) and not any(k in s for k in ["AECOM", "Yard Waste", "CLP", "11kV", "132kV", "PDF", "DeepSeek"]):
            continue

        cleaned = _clean_item(s)
        if cleaned and current:
            sections[current].append(cleaned)

    def render_section(key: str) -> str:
        items = []
        seen = set()
        for item in sections[key]:
            if item not in seen:
                items.append(item)
                seen.add(item)
        if not items:
            items = ["未明"]
        return "\n".join([SECTION_TITLES[key]] + [f"- {x}" for x in items])

    return "\n\n".join([
        render_section("summary"),
        render_section("todo"),
        render_section("follow"),
    ]).strip()


def main():
    try:
        input_path = choose_input_file()
        if not input_path:
            return

        input_file = Path(input_path)
        text = read_text(input_file)
        key_text = extract_key_sentences(text)
        prompt = build_prompt(key_text)
        raw_summary = run_ollama(prompt)
        final_summary = normalize_output(raw_summary)

        output_file = input_file.with_name("summary.txt")
        output_file.write_text(final_summary, encoding="utf-8")

        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("完成", f"已輸出：{output_file}")
        root.destroy()

    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("錯誤", str(e))
        root.destroy()


if __name__ == "__main__":
    main()