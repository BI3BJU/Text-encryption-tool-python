# AES-256-GCM 文本加密工具 / Text Encryption Tool

[English](#english) | [中文](#chinese)

## <a id="chinese"></a>中文

### 📖 简介

**AES-256-GCM 文本加密工具** 是一款基于 Python + Tkinter 的轻量级桌面应用，用于对任意 Unicode 文本进行安全加密与解密。  
它采用行业标准的 **AES-256-GCM** 认证加密算法，同时支持 **Base64** 和 **十六进制** 两种密文输出格式，并自动检测输入密文的编码方式，极大提升易用性。

项目由 **BI3BJU** 开发，代码完全开源，适合个人隐私保护、密码管理辅助等场景。

### ✨ 功能特性

- ✅ **AES-256-GCM 加密** – 提供机密性、完整性和真实性保护
- 🔑 **灵活密钥输入** – 支持任意文本（经 SHA-256 派生）或 32 字节 Base64 随机密钥（推荐）
- 🎲 **一键生成随机密钥** – 使用系统安全随机数生成器，并自动复制到剪贴板
- 📋 **自动剪贴板操作** – 加密/解密成功后，结果自动复制，方便粘贴使用
- 🔄 **自动识别密文格式** – 粘贴密文后无需手动选择 Base64 或 Hex，程序自动解码
- 🌐 **中英文双语界面** – 根据系统语言自动切换（Windows / Linux / macOS）
- 🖱️ **右键上下文菜单** – 支持复制、粘贴、剪切、全选、清空，提升编辑效率
- 🎨 **简洁直观的 UI** – 清晰的布局，状态栏实时反馈操作结果

### 🚀 快速开始

#### 环境要求
- Python 3.6+
- 依赖库：cryptography（Tkinter 为 Python 标准库，无需额外安装）

#### 安装依赖
执行命令：pip install -r requirements.txt

#### 运行程序
执行命令：python main.py

提示：若需要图标文件 logo.png，请放置于同目录下（非必需，加载失败不影响使用）。

### 🧩 使用说明

1. **密钥（Key）**  
   - 可直接输入任意文本（如口令），程序会自动 SHA-256 哈希为 32 字节密钥。  
   - 推荐点击 “生成密钥” 按钮获得高熵随机密钥（Base64 编码），并妥善保存。

2. **加密**  
   - 在“明文”区域输入要加密的文本。  
   - 选择输出格式（Base64 或 Hex）。  
   - 点击 “加密 →”，密文将显示在“密文”区域并自动复制到剪贴板。

3. **解密**  
   - 在“密文”区域粘贴待解密的字符串（支持 Base64 或 Hex）。  
   - 确保密钥正确。  
   - 点击 “← 解密”，成功解密后明文会显示并自动复制。

4. **右键菜单**  
   - 在任意文本框内右键（或触控板双指点击）可调出上下文菜单，快速执行复制、粘贴等操作。

### 🔒 安全说明

- **加密算法**：AES-256-GCM（Galois/Counter Mode），提供认证加密，可同时检测篡改和密钥错误。  
- **随机数**：每加密一次生成全新的 12 字节 nonce（使用 os.urandom），确保相同明文产生不同密文。  
- **密钥派生**：使用 SHA-256 将任意输入哈希为 32 字节。强烈建议使用“生成密钥”功能获得的高熵 Base64 密钥，而非简单口令，以抵御字典攻击。  
- **数据保护**：密钥仅存在于内存中，程序不保存任何数据至磁盘（除非用户手动复制保存）。  
- **错误处理**：解密失败统一提示“密钥错误或数据损坏”，避免泄露内部状态。

### 🛠️ 技术栈

- **前端**：Tkinter（Python 内置 GUI 库）  
- **加密库**：cryptography 的 AESGCM 实现  
- **编码处理**：Base64 / Hex 自动识别与转换  
- **国际化**：基于系统 locale 检测，自建 I18n 单例管理器

### 📁 项目结构

.
├── main.py          # 主程序（需用户自行添加）
├── logo.png         # 可选图标（需用户自行添加）
├── requirements.txt # Python 依赖
├── build.bat        # Windows 打包脚本
├── build.sh         # Linux/macOS 打包脚本
├── LICENSE          # MIT 许可证
├── .gitignore       # Git 忽略规则
└── README.md        # 说明文档

### 📝 更新日志

- v1.0 (2026-06) – 首个正式版本，支持基础加密/解密、中英文界面、剪贴板联动。

### 👤 作者

BI3BJU – 业余无线电爱好者 & 开源开发者

### 📄 许可证

本项目采用 MIT 许可证，详情请见 LICENSE 文件。

---

## <a id="english"></a>English

### 📖 Introduction

**AES-256-GCM Text Encryption Tool** is a lightweight desktop application built with Python and Tkinter, designed to securely encrypt and decrypt arbitrary Unicode text.  
It uses the industry-standard AES-256-GCM authenticated encryption algorithm, supports both Base64 and Hex output formats, and automatically detects the encoding of input ciphertext – making it extremely easy to use.

Developed by BI3BJU, this open‑source project is ideal for personal privacy protection, password management assistance, and more.

### ✨ Features

- ✅ AES-256-GCM encryption – ensures confidentiality, integrity, and authenticity
- 🔑 Flexible key input – accepts any text (derived via SHA‑256) or a 32‑byte Base64 random key (recommended)
- 🎲 One‑click random key generation – uses system‑secure RNG and auto‑copies to clipboard
- 📋 Automatic clipboard integration – results are copied to clipboard after encryption/decryption
- 🔄 Auto‑detection of ciphertext format – no need to select Base64 or Hex manually when pasting; the program decodes it automatically
- 🌐 Bilingual UI (English/Chinese) – switches based on system language (Windows / Linux / macOS)
- 🖱️ Right‑click context menu – supports copy, paste, cut, select all, clear for efficient editing
- 🎨 Clean and intuitive UI – clear layout with a status bar giving real‑time feedback

### 🚀 Quick Start

#### Requirements
- Python 3.6+
- Dependency: cryptography (Tkinter is built‑in with Python)

#### Install dependency
Run command: pip install -r requirements.txt

#### Run the program
Run command: python main.py

Note: An optional logo.png file placed in the same directory will be used as the window icon (if missing, the program still runs fine).

### 🧩 Usage Guide

1. **Key**  
   - You may enter any arbitrary text (e.g., a passphrase); the program will hash it with SHA‑256 to derive a 32‑byte key.  
   - It is highly recommended to click the “Generate Key” button to obtain a high‑entropy Base64 random key and store it securely.

2. **Encryption**  
   - Type your plaintext in the “Plaintext” area.  
   - Choose output format (Base64 or Hex).  
   - Click “Encrypt →” – the ciphertext will appear in the “Ciphertext” area and be automatically copied to your clipboard.

3. **Decryption**  
   - Paste the ciphertext (Base64 or Hex) into the “Ciphertext” area.  
   - Ensure the correct key is entered.  
   - Click “← Decrypt” – upon success, the plaintext is displayed and copied to clipboard.

4. **Context Menu**  
   - Right‑click (or two‑finger tap on touchpad) inside any text box to open a context menu for copy, paste, cut, select all, and clear.

### 🔒 Security Notes

- Algorithm: AES‑256‑GCM (Galois/Counter Mode) – an authenticated encryption mode that detects tampering and wrong keys.  
- Nonce: A fresh 12‑byte nonce is generated for each encryption (using os.urandom), ensuring that identical plaintexts yield different ciphertexts.  
- Key derivation: SHA‑256 is used to hash any input into a 32‑byte key. Strongly recommended: use the high‑entropy Base64 key generated by the “Generate Key” button, rather than a simple password, to resist dictionary attacks.  
- Data safety: The key exists only in memory; the program does not save any data to disk (unless you manually copy it out).  
- Error handling: Decryption failures show a generic “wrong key or corrupted data” message, avoiding internal state leakage.

### 🛠️ Technology Stack

- Frontend: Tkinter (Python built‑in GUI library)  
- Cryptography: AESGCM from the cryptography library  
- Encoding: Automatic Base64 / Hex detection and conversion  
- Internationalisation: System locale detection with a custom I18n singleton manager

### 📁 Project Structure

.
├── main.py          # Main program (you need to add this)
├── logo.png         # Optional icon (you need to add this)
├── requirements.txt # Python dependencies
├── build.bat        # Windows build script
├── build.sh         # Linux/macOS build script
├── LICENSE          # MIT License
├── .gitignore       # Git ignore rules
└── README.md        # This documentation

### 📝 Changelog

- v1.0 (2026-06) – First stable release with basic encryption/decryption, bilingual UI, and clipboard integration.

### 👤 Author

BI3BJU – Amateur radio enthusiast & open‑source developer

### 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.