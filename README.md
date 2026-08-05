[README_bilingual (1).md](https://github.com/user-attachments/files/30728134/README_bilingual.1.md)
# WhatsApp 摘要工具 / WhatsApp Summary Tool

呢個工具可以令你雙擊執行檔，揀一個 `.txt` 聊天記錄檔，然後自動產生中文摘要，輸出成同名資料夾入面嘅 `summary.txt`。

This tool lets you double-click an executable, choose a `.txt` chat export file, and automatically generate a Chinese summary as `summary.txt` in the same folder as the input file.

---

## 功能 / Features

- 雙擊開啟程式。 / Open the app by double-clicking it.
- 用檔案選擇視窗揀 `.txt` 檔。 / Choose a `.txt` file using a file picker.
- 讀取 WhatsApp 聊天內容。 / Read WhatsApp chat content.
- 抽出較重要嘅句子。 / Extract the most relevant lines.
- 交俾本機 Ollama 模型整理。 / Send it to a local Ollama model for summarization.
- 將結果輸出成 `summary.txt`。 / Save the result as `summary.txt`.

---

## 輸出格式 / Output Format

輸出會分成三部分： / The output is split into three sections:

- `1. 摘要` / `1. Summary`
- `2. 待辦清單` / `2. To-do List`
- `3. 跟進事項` / `3. Follow-ups`

---

## 系統需求 / Requirements

- Windows 10 / 11。 / Windows 10 / 11.
- Python 3.10 或以上。 / Python 3.10 or newer.
- Ollama。 / Ollama.
- 一個已下載到本機嘅 Ollama 模型，例如 `deepseek-r1:7b`。 / A local Ollama model, for example `deepseek-r1:7b`.

---

## 安裝 Python / Install Python

### 1. 下載 Python / Download Python

去 Python 官方網站下載安裝程式： / Download the installer from the official Python website:

- [Python 下載頁](https://www.python.org/downloads/)

建議安裝最新版 Python 3。 / It is recommended to install the latest Python 3 release.

### 2. 安裝 Python / Install Python

執行安裝程式時，記得勾選： / When running the installer, make sure to check:

- **Add Python to PATH**

呢個步驟好重要，因為之後你先可以喺 PowerShell / CMD 入面直接用 `python`。 / This step is important because it lets you run `python` directly from PowerShell / CMD.

### 3. 檢查安裝是否成功 / Verify Installation

打開 PowerShell，輸入： / Open PowerShell and run:

```powershell
python --version
```

如果見到版本號，例如 `Python 3.12.x`，即係安裝成功。 / If you see a version number such as `Python 3.12.x`, the installation was successful.

---

## 安裝 Ollama / Install Ollama

### 1. 下載 Ollama / Download Ollama

去 Ollama 官方網站下載並安裝： / Download and install Ollama from the official website:

- [Ollama 官網](https://ollama.com/)

### 2. 確認安裝成功 / Verify Installation

安裝完成後，打開 PowerShell，輸入： / After installation, open PowerShell and run:

```powershell
ollama --version
```

如果有版本號輸出，就代表安裝成功。 / If a version number appears, Ollama is installed correctly.

### 3. 下載模型 / Pull a Model

你可以下載我哋程式預設使用嘅模型： / You can pull the model used by default in this project:

```powershell
ollama pull deepseek-r1:7b
```

如果你想用其他模型，可以改 Python 檔入面嘅 `OLLAMA_MODEL`。 / If you want to use another model, change `OLLAMA_MODEL` in the Python file.

### 4. 測試模型 / Test the Model

你可以試下： / You can test it with:

```powershell
ollama run deepseek-r1:7b
```

入面輸入一句話試下，確認模型可以正常回應。 / Type a sentence and confirm that the model responds normally.

---

## 安裝套件 / Install Tools

如果你要直接喺 Python 跑，先安裝 PyInstaller（如果你之後要打包成 exe）： / If you want to package the app into an exe later, install PyInstaller first:

```powershell
python -m pip install pyinstaller
```

如果你只係想用 Python 跑程式，而未打包 exe，基本上唔需要額外套件，因為程式用到嘅 `tkinter`、`subprocess`、`pathlib` 都係 Python 內置。 / If you only want to run the script in Python and not build an exe, you do not need extra packages because `tkinter`, `subprocess`, and `pathlib` are built in.

---

## 使用方法 / How to Use

### 方法一：直接用 Python 跑 / Option 1: Run with Python

1. 將 `whatsapp_summary.py` 放喺一個資料夾。 / Put `whatsapp_summary.py` in a folder.
2. 用 PowerShell 去到嗰個資料夾。 / Open PowerShell and go to that folder.
3. 執行： / Run:

```powershell
python whatsapp_summary.py
```

4. 揀你想處理嘅 `.txt` 檔。 / Choose the `.txt` file you want to process.
5. 程式會喺同一個資料夾輸出 `summary.txt`。 / The program will output `summary.txt` in the same folder.

### 方法二：打包成 EXE / Option 2: Build an EXE

1. 安裝 PyInstaller： / Install PyInstaller:

```powershell
python -m pip install pyinstaller
```

2. 打包： / Build:

```powershell
python -m PyInstaller --clean --onefile --noconsole whatsapp_summary.py
```

3. 打包完成後，去 `dist` 資料夾搵： / After building, find the executable in the `dist` folder:

```text
dist\whatsapp_summary.exe
```

4. 雙擊 `whatsapp_summary.exe`。 / Double-click `whatsapp_summary.exe`.
5. 選擇 `.txt` 檔。 / Choose a `.txt` file.
6. 等佢完成，之後睇返同一個資料夾入面嘅 `summary.txt`。 / Wait for it to finish, then open the `summary.txt` in the same folder.

---

## 檔案位置規則 / File Location Rules

- **輸入檔**：你揀嘅 `.txt`。 / **Input file**: the `.txt` file you choose.
- **輸出檔**：固定叫 `summary.txt`。 / **Output file**: always named `summary.txt`.
- **輸出位置**：同輸入檔同一個資料夾。 / **Output location**: the same folder as the input file.

---

## 常見問題 / Troubleshooting

### `python` 搵唔到 / `python` not found

如果你輸入： / If you run:

```powershell
python --version
```

但出現錯誤，通常係 Python 未加入 PATH。你可以： / and it fails, Python is probably not added to PATH. You can:

- 重新安裝 Python。 / Reinstall Python.
- 勾選 **Add Python to PATH**。 / Check **Add Python to PATH**.
- 或者重開 PowerShell 再試。 / Or restart PowerShell and try again.

### `ollama` 搵唔到 / `ollama` not found

如果你輸入： / If you run:

```powershell
ollama --version
```

但搵唔到命令，代表 Ollama 未裝好，或者未加 PATH。請重新安裝 Ollama。 / If the command is not found, Ollama is not installed correctly or is not on PATH. Reinstall Ollama.

### `pyinstaller` 搵唔到 / `pyinstaller` not found

如果你輸入： / If you run:

```powershell
pyinstaller --clean --onefile --noconsole whatsapp_summary.py
```

但出錯，改用： / and it fails, use:

```powershell
python -m PyInstaller --clean --onefile --noconsole whatsapp_summary.py
```

### 冇生成 `summary.txt` / `summary.txt` not created

請檢查： / Please check:

- 你有冇成功揀到 `.txt` 檔。 / Whether you selected a valid `.txt` file.
- Ollama 有冇正常運作。 / Whether Ollama is running normally.
- 模型名有冇同程式一致。 / Whether the model name matches the script.
- 你嘅輸入檔係咪 UTF-8 編碼。 / Whether the input file is UTF-8 encoded.

---

## 可修改項目 / Things You Can Customize

你可以自行改以下位置： / You can modify these parts:

- `OLLAMA_MODEL`：改成你想用嘅模型。 / `OLLAMA_MODEL`: change to another model.
- `extract_key_sentences()`：改抽句規則。 / `extract_key_sentences()`: adjust line filtering.
- `build_prompt()`：改摘要格式同語氣。 / `build_prompt()`: change the summary prompt and tone.

---

## 建議流程 / Recommended Workflow

1. 先安裝 Python。 / Install Python first.
2. 再安裝 Ollama。 / Then install Ollama.
3. 下載模型。 / Pull the model.
4. 用 Python 直接測試 script。 / Test the script with Python directly.
5. 確認正常後再打包成 EXE。 / After it works, package it into an EXE.

---

## 備註 / Notes

呢個工具主要係針對 WhatsApp 聊天輸出設計，所以 prompt 同過濾規則都係朝呢個方向調整。你可以按自己需要再修改。 / This tool is mainly designed for WhatsApp chat exports, so the prompt and filtering rules are tuned for that use case. You can adjust them as needed.
