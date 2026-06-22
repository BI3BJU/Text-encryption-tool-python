import tkinter as tk
import os
import base64
import hashlib
import locale
import sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# =========================
# 🔑 Key Derivation (SHA-256)
# =========================
def text_to_key(key_input: str) -> bytes:
    """Convert any Unicode text to a 32-byte key (using SHA-256)"""
    return hashlib.sha256(key_input.encode("utf-8")).digest()


def get_key(key_input: str) -> bytes:
    """Get key: arbitrary text → SHA-256 → 32 bytes"""
    if not key_input:
        return None
    return text_to_key(key_input)


def generate_random_key() -> str:
    """Generate a random 32-byte key and return it as Base64"""
    key = os.urandom(32)
    return base64.b64encode(key).decode("utf-8")


# =========================
# 🌐 Bilingual Text Manager
# =========================
class I18n:
    _instance = None
    _current_lang = "en"

    _strings = {
        "en": {
            "title": "Text Encryption Tool (AES-256-GCM) v1.0 by BI3BJU",
            "key_label": "Key",
            "generate_key": "Generate Key",
            "plaintext_label": "Plaintext (Unicode)",
            "ciphertext_label": "Ciphertext",
            "encrypt_btn": "Encrypt →",
            "decrypt_btn": "← Decrypt",
            "status_encrypt_success": "Encryption successful, ciphertext copied to clipboard",
            "status_decrypt_success": "Decryption successful, plaintext copied to clipboard",
            "status_key_empty": "Warning: Key cannot be empty",
            "status_plain_empty": "Warning: Plaintext cannot be empty",
            "status_cipher_empty": "Warning: Ciphertext cannot be empty",
            "status_encrypt_error": "Encryption error: {}",
            "status_decrypt_error": "Decryption failed: wrong key or corrupted data",
            "status_invalid_format": "Error: Invalid ciphertext format (needs at least 28 bytes)",
            "status_key_generated": "Random key generated and copied to clipboard",
            "menu_copy": "Copy",
            "menu_paste": "Paste",
            "menu_cut": "Cut",
            "menu_select_all": "Select All",
            "menu_clear": "Clear",
            "key_placeholder": "It is recommended to use a password manager to generate a 32-byte random key (Base64) for maximum security and minimal storage overhead.",
            "output_format": "Output format:",
            "format_base64": "Base64",
            "format_hex": "Hex"
        },
        "zh": {
            "title": "文本加密工具 (AES-256-GCM) v1.0 作者 BI3BJU",
            "key_label": "密钥",
            "generate_key": "生成密钥",
            "plaintext_label": "明文（Unicode）",
            "ciphertext_label": "密文",
            "encrypt_btn": "加密 →",
            "decrypt_btn": "← 解密",
            "status_encrypt_success": "加密成功，密文已复制到剪贴板",
            "status_decrypt_success": "解密成功，明文已复制到剪贴板",
            "status_key_empty": "警告：密钥不能为空",
            "status_plain_empty": "警告：明文不能为空",
            "status_cipher_empty": "警告：密文不能为空",
            "status_encrypt_error": "加密错误: {}",
            "status_decrypt_error": "解密失败：密钥错误或数据损坏",
            "status_invalid_format": "错误：无效的密文格式（至少需要 28 字节）",
            "status_key_generated": "已生成随机密钥并复制到剪贴板",
            "menu_copy": "复制",
            "menu_paste": "粘贴",
            "menu_cut": "剪切",
            "menu_select_all": "全选",
            "menu_clear": "清空",
            "key_placeholder": "建议使用密码管理器生成 32 字节随机密钥（Base64），以获得最高安全性和最小存储开销。",
            "output_format": "输出格式:",
            "format_base64": "Base64",
            "format_hex": "十六进制"
        }
    }

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_text(self, key, **kwargs):
        text = self._strings[self._current_lang].get(key, key)
        if kwargs:
            text = text.format(**kwargs)
        return text

    def set_language(self, lang):
        if lang in self._strings:
            self._current_lang = lang

    def get_language(self):
        return self._current_lang

    def detect_system_language(self):
        try:
            if sys.platform == 'win32':
                try:
                    import ctypes
                    windll = ctypes.windll.kernel32
                    lang_id = windll.GetUserDefaultUILanguage()
                    chinese_lang_ids = [0x0804, 0x0404, 0x0c04, 0x1004, 0x1404, 0x0004]
                    if lang_id in chinese_lang_ids:
                        return 'zh'
                except:
                    pass
            try:
                lang_code = locale.getdefaultlocale()[0]
                if lang_code and lang_code.startswith('zh'):
                    return 'zh'
            except:
                pass
            lang_env = os.environ.get('LANG', '').lower()
            if lang_env.startswith('zh'):
                return 'zh'
        except Exception:
            pass
        return 'en'

    def init_language(self):
        system_lang = self.detect_system_language()
        self.set_language(system_lang)
        print(f"Detected system language: {'Chinese' if system_lang == 'zh' else 'English'}")
        return self._current_lang


i18n = I18n.get_instance()


# =========================
# 📢 Status message function
# =========================
def show_status(text_key, color="green", **kwargs):
    text = i18n.get_text(text_key, **kwargs)
    status_label.config(text=text, fg=color)
    root.after(3000, lambda: status_label.config(text=""))


# =========================
# 🔐 Decode ciphertext (auto-detect Base64 or Hex)
# =========================
def decode_ciphertext(encoded: str) -> bytes:
    encoded = encoded.strip()
    if not encoded:
        raise ValueError("Empty ciphertext")

    if len(encoded) % 2 == 0 and all(c in '0123456789abcdefABCDEF' for c in encoded):
        try:
            return bytes.fromhex(encoded)
        except ValueError:
            pass

    try:
        missing = len(encoded) % 4
        if missing:
            encoded += '=' * (4 - missing)
        raw = base64.b64decode(encoded, validate=True)
        return raw
    except Exception:
        pass

    raise ValueError("Unrecognized ciphertext format (not Base64 nor Hex)")


# =========================
# 🔐 Encrypt
# =========================
def encrypt_text():
    key_input = key_entry.get().strip()
    
    if not key_input or (hasattr(key_entry, "placeholder") and key_input == key_entry.placeholder):
        show_status("status_key_empty", "red")
        return

    text = plain_text.get("1.0", tk.END).strip()

    key = get_key(key_input)
    if key is None:
        show_status("status_key_empty", "red")
        return

    if not text:
        show_status("status_plain_empty", "red")
        return

    try:
        nonce = os.urandom(12)
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, text.encode("utf-8"), None)
        raw = nonce + ciphertext

        if format_var.get() == "Hex":
            encoded = raw.hex()
        else:  # Base64
            encoded = base64.b64encode(raw).decode("utf-8")

        cipher_text.delete("1.0", tk.END)
        cipher_text.insert(tk.END, encoded)

        root.clipboard_clear()
        root.clipboard_append(encoded)

        show_status("status_encrypt_success", "green")
    except Exception as e:
        show_status("status_encrypt_error", "red", error=str(e))


# =========================
# 🔓 Decrypt
# =========================
def decrypt_text():
    key_input = key_entry.get().strip()

    if not key_input or (hasattr(key_entry, "placeholder") and key_input == key_entry.placeholder):
        show_status("status_key_empty", "red")
        return

    key = get_key(key_input)
    if key is None:
        show_status("status_key_empty", "red")
        return

    try:
        encoded = cipher_text.get("1.0", tk.END).strip()
        if not encoded:
            show_status("status_cipher_empty", "red")
            return

        raw = decode_ciphertext(encoded)

        if len(raw) < 28:
            show_status("status_invalid_format", "red")
            return

        nonce = raw[:12]
        ciphertext = raw[12:]

        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None).decode("utf-8")

        plain_text.delete("1.0", tk.END)
        plain_text.insert(tk.END, plaintext)

        root.clipboard_clear()
        root.clipboard_append(plaintext)

        show_status("status_decrypt_success", "green")
    except ValueError:
        show_status("status_invalid_format", "red")
    except Exception:
        show_status("status_decrypt_error", "red")


# =========================
# 🔑 Generate random key
# =========================
def generate_key():
    new_key = generate_random_key()
    
    if hasattr(key_entry, "default_fg"):
        key_entry.config(fg=key_entry.default_fg)
        
    key_entry.delete(0, tk.END)
    key_entry.insert(0, new_key)
    root.clipboard_clear()
    root.clipboard_append(new_key)
    show_status("status_key_generated", "green")


# =========================
# 🌟 Placeholder for Entry
# =========================
def add_placeholder(entry, placeholder):
    entry.placeholder = placeholder
    entry.default_fg = entry.cget("fg")
    if not entry.get():
        entry.insert(0, placeholder)
        entry.config(fg="gray")
    def on_focus_in(e):
        if entry.get() == entry.placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=entry.default_fg)
    def on_focus_out(e):
        if not entry.get():
            entry.insert(0, entry.placeholder)
            entry.config(fg="gray")
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


def update_placeholder_language():
    """Update placeholder text when language changes"""
    new_placeholder = i18n.get_text("key_placeholder")
    if hasattr(key_entry, "placeholder"):
        old_placeholder = key_entry.placeholder
        if key_entry.get() == old_placeholder:
            key_entry.delete(0, tk.END)
            key_entry.insert(0, new_placeholder)
        key_entry.placeholder = new_placeholder


# =========================
# 🖱️ Right-click context menu (Cross-platform)
# =========================
def create_context_menu(widget):
    m = tk.Menu(root, tearoff=0)
    def update_menu_language():
        m.delete(0, tk.END)
        m.add_command(label=i18n.get_text("menu_copy"), command=lambda: copy_text(widget))
        m.add_command(label=i18n.get_text("menu_paste"), command=lambda: paste_text(widget))
        m.add_command(label=i18n.get_text("menu_cut"), command=lambda: cut_text(widget))
        m.add_separator()
        m.add_command(label=i18n.get_text("menu_select_all"), command=lambda: select_all(widget))
        m.add_command(label=i18n.get_text("menu_clear"), command=lambda: clear_text(widget))
    def copy_text(widget):
        try: widget.event_generate("<<Copy>>")
        except: pass
    def paste_text(widget):
        try: widget.event_generate("<<Paste>>")
        except: pass
    def cut_text(widget):
        try: widget.event_generate("<<Cut>>")
        except: pass
    def select_all(widget):
        try:
            if isinstance(widget, tk.Text):
                widget.tag_add("sel", "1.0", "end")
                widget.mark_set("insert", "end")
            else:
                widget.select_range(0, tk.END)
        except: pass
    def clear_text(widget):
        try:
            if isinstance(widget, tk.Text):
                widget.delete("1.0", "end")
            else:
                widget.delete(0, tk.END)
        except: pass
    def show_menu(e):
        update_menu_language()
        m.tk_popup(e.x_root, e.y_root)
    
    # 💻 跨平台安全修复：使用 Tkinter 专用的虚拟事件识别右键行为
    widget.bind("<<ContextMenu>>", show_menu)


# =========================
# 🖥 GUI Layout
# =========================
root = tk.Tk()
root.title(i18n.get_text("title"))
root.geometry("750x680+100+100")
root.minsize(750, 680)
root.grid_columnconfigure(0, weight=1)

format_var = tk.StringVar(value="Base64")

# Key area
frame1 = tk.Frame(root)
frame1.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
frame1.grid_columnconfigure(1, weight=1)

key_label = tk.Label(frame1, text=i18n.get_text("key_label"))
key_label.grid(row=0, column=0, padx=(0,5))

key_entry = tk.Entry(frame1)
key_entry.grid(row=0, column=1, sticky="ew", padx=10)

# 🔧 修改生成密钥按钮样式
generate_key_btn = tk.Button(frame1, text=i18n.get_text("generate_key"), command=generate_key,
                             bg="#90CAF9", fg="#1C1C1C", relief="groove", width=12)
generate_key_btn.grid(row=0, column=2, padx=(5,0), sticky="e")

create_context_menu(key_entry)

placeholder_text = i18n.get_text("key_placeholder")
add_placeholder(key_entry, placeholder_text)

# Plaintext area
plain_header = tk.Frame(root)
plain_header.grid(row=1, column=0, sticky="ew", padx=10, pady=(10,0))
plain_header.grid_columnconfigure(0, weight=0)  # plain_label 不扩展
plain_header.grid_columnconfigure(1, weight=1)  # 中间列扩展，用于居中格式选项
plain_header.grid_columnconfigure(2, weight=0)  # 加密按钮不扩展

plain_label = tk.Label(plain_header, text=i18n.get_text("plaintext_label"))
plain_label.grid(row=0, column=0, sticky="w")

# 格式选项框架（用于居中）
format_frame = tk.Frame(plain_header)
format_frame.grid(row=0, column=1, sticky='ew')  # 填充中间列宽度

# 内部容器，用于实际居中
inner_format_frame = tk.Frame(format_frame)
inner_format_frame.pack(anchor='center')  # 水平居中

format_label = tk.Label(inner_format_frame, text=i18n.get_text("output_format"))
format_label.pack(side=tk.LEFT, padx=(0, 5))

rb_base64 = tk.Radiobutton(inner_format_frame, text=i18n.get_text("format_base64"), variable=format_var, value="Base64")
rb_base64.pack(side=tk.LEFT, padx=2)

rb_hex = tk.Radiobutton(inner_format_frame, text=i18n.get_text("format_hex"), variable=format_var, value="Hex")
rb_hex.pack(side=tk.LEFT, padx=2)

# 加密按钮
encrypt_btn = tk.Button(plain_header, text=i18n.get_text("encrypt_btn"), command=encrypt_text,
                        width=12, bg="#E57373", fg="#1C1C1C", activebackground="#EF5350", relief="groove")
encrypt_btn.grid(row=0, column=2, sticky="e", padx=(10, 0))

plain_text = tk.Text(root, height=10)
plain_text.grid(row=2, column=0, sticky="nsew", padx=10)
create_context_menu(plain_text)

# Ciphertext area
cipher_header = tk.Frame(root)
cipher_header.grid(row=3, column=0, sticky="ew", padx=10, pady=(10,0))
cipher_header.grid_columnconfigure(0, weight=1)
cipher_label = tk.Label(cipher_header, text=i18n.get_text("ciphertext_label"))
cipher_label.grid(row=0, column=0, sticky="w")

# 🎨 视觉美化提示：采用莫兰迪低饱和度淡绿/鼠尾草绿
decrypt_btn = tk.Button(cipher_header, text=i18n.get_text("decrypt_btn"), command=decrypt_text,
                        width=12, bg="#81C784", fg="#1C1C1C", activebackground="#66BB6A", relief="groove")
decrypt_btn.grid(row=0, column=1, sticky="e")

cipher_text = tk.Text(root, height=10)
cipher_text.grid(row=4, column=0, sticky="nsew", padx=10)
create_context_menu(cipher_text)

# Status bar
status_frame = tk.Frame(root)
status_frame.grid(row=5, column=0, sticky="ew", padx=10, pady=10)
status_frame.grid_columnconfigure(0, weight=1)
status_label = tk.Label(status_frame, text="", font=("Arial", 10, "bold"))
status_label.grid(row=0, column=0, sticky="w")

root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(4, weight=1)


# =========================
# UI Text Refresh
# =========================
def refresh_ui_texts():
    root.title(i18n.get_text("title"))
    key_label.config(text=i18n.get_text("key_label"))
    generate_key_btn.config(text=i18n.get_text("generate_key"))
    plain_label.config(text=i18n.get_text("plaintext_label"))
    cipher_label.config(text=i18n.get_text("ciphertext_label"))
    encrypt_btn.config(text=i18n.get_text("encrypt_btn"))
    decrypt_btn.config(text=i18n.get_text("decrypt_btn"))
    update_placeholder_language()
    format_label.config(text=i18n.get_text("output_format"))
    rb_base64.config(text=i18n.get_text("format_base64"))
    rb_hex.config(text=i18n.get_text("format_hex"))


# Initialize language and start application loop
i18n.init_language()
refresh_ui_texts()

root.mainloop()