import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
import threading
import base58

RPC_URL = "http://163.172.90.77:5001/rpc"

def send_sell_request(amount, private_key, token_address, slippage_val):
    payload = {
        "jsonrpc": "2.0",
        "method": "sell_token",
        "params": {
            "amount": amount,
            "private_key": private_key,
            "mint": token_address,
            "slippage": slippage_val
        },
        "id": 1
    }

    try:
        response = requests.post(RPC_URL, json=payload, timeout=30)
        result = response.json()
        if "result" in result:
            return f"✅ 成功 / Success:\n{result['result']}\n"
        elif "error" in result:
            return f"❌ 错误 / Error:\n{result['error']['message']}\n"
        else:
            return f"⚠️ 未知响应 / Unknown Response:\n{json.dumps(result, indent=2)}\n"
    except Exception as e:
        return f"🚫 请求失败 / Request Failed:\n{str(e)}\n"

def sell_token_single_thread():
    amount = amount_entry.get().strip()
    private_key = private_key_entry.get().strip()
    token_address = mint_entry.get().strip()
    slippage = slippage_entry.get().strip()

    if not private_key or not token_address:
        messagebox.showerror("错误 / Error", "私钥或代币地址不能为空 / Private key or token address cannot be empty")
        return

    try:
        slippage_val = float(slippage)
    except ValueError:
        messagebox.showerror("错误 / Error", "最大滑点必须是数字 / Slippage must be a number")
        return

    result_text = send_sell_request(amount, private_key, token_address, slippage_val)

    output_text_single.config(state=tk.NORMAL)
    output_text_single.delete("1.0", tk.END)
    output_text_single.insert(tk.END, result_text)
    output_text_single.config(state=tk.DISABLED)

def sell_token_single():
    threading.Thread(target=sell_token_single_thread).start()

def sell_token_batch_thread():
    amount = amount_entry_batch.get().strip()
    private_keys = private_keys_text_batch.get("1.0", tk.END).strip().splitlines()
    token_address = mint_entry_batch.get().strip()
    slippage = slippage_entry_batch.get().strip()

    if not private_keys or not token_address:
        messagebox.showerror("错误 / Error", "私钥或代币地址不能为空 / Private key(s) or token address cannot be empty")
        return

    try:
        slippage_val = float(slippage)
    except ValueError:
        messagebox.showerror("错误 / Error", "最大滑点必须是数字 / Slippage must be a number")
        return

    output_text_batch.config(state=tk.NORMAL)
    output_text_batch.delete("1.0", tk.END)

    for i, key in enumerate(private_keys):
        key = key.strip()
        if not key:
            continue
        output_text_batch.insert(tk.END, f"🔁 正在处理第 {i+1} 个私钥...\n")
        output_text_batch.see(tk.END)
        result_text = send_sell_request(amount, key, token_address, slippage_val)
        output_text_batch.insert(tk.END, result_text + "\n")
        output_text_batch.see(tk.END)

    output_text_batch.config(state=tk.DISABLED)

def sell_token_batch():
    threading.Thread(target=sell_token_batch_thread).start()

# === GUI 主窗口 ===
root = tk.Tk()
root.title("PumpFun - 代币卖出工具 / Token Sell Tool")
screen_width = root.winfo_screenwidth()
root.geometry(f"{screen_width}x600")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

pad_x = 5
pad_y = 5

# === 单个卖出界面 ===
single_sell_frame = tk.Frame(notebook)
notebook.add(single_sell_frame, text="单个卖出 / Single Sell")

tk.Label(single_sell_frame, text="数量 Amount:").grid(row=0, column=0, sticky="w", padx=pad_x, pady=pad_y)
amount_entry = tk.Entry(single_sell_frame, width=20)
amount_entry.insert(0, "all")
amount_entry.grid(row=0, column=1, sticky="w", padx=pad_x, pady=pad_y)
tk.Label(single_sell_frame, text="支持 10%, 25%, 50%, 75%, 100% / Supports partial input").grid(row=0, column=2, sticky="w")

tk.Label(single_sell_frame, text="私钥（完整）Private Key (Full):").grid(row=1, column=0, sticky="w", padx=pad_x, pady=pad_y)
private_key_entry = tk.Entry(single_sell_frame, width=100)
private_key_entry.grid(row=1, column=1, columnspan=2, sticky="w", padx=pad_x, pady=pad_y)

tk.Label(single_sell_frame, text="代币地址 Token Address:").grid(row=2, column=0, sticky="w", padx=pad_x, pady=pad_y)
mint_entry = tk.Entry(single_sell_frame, width=60)
mint_entry.grid(row=2, column=1, columnspan=2, sticky="w", padx=pad_x, pady=pad_y)

tk.Label(single_sell_frame, text="最大滑点 Slippage:").grid(row=3, column=0, sticky="w", padx=pad_x, pady=pad_y)
slippage_entry = tk.Entry(single_sell_frame, width=10)
slippage_entry.insert(0, "0.25")
slippage_entry.grid(row=3, column=1, sticky="w", padx=pad_x, pady=pad_y)
tk.Label(single_sell_frame, text="例如: 0.25 = 25% / Example: 0.25 = 25%").grid(row=3, column=2, sticky="w")

tk.Button(single_sell_frame, text="卖出 / Sell", width=20, command=sell_token_single).grid(row=4, column=0, columnspan=3, pady=10)

output_text_single = scrolledtext.ScrolledText(single_sell_frame, height=8, width=screen_width // 10, wrap=tk.WORD)
output_text_single.grid(row=5, column=0, columnspan=3, padx=pad_x, pady=pad_y)
output_text_single.config(state=tk.DISABLED)

# === 批量卖出界面 ===
batch_sell_frame = tk.Frame(notebook)
notebook.add(batch_sell_frame, text="批量卖出 / Batch Sell")

tk.Label(batch_sell_frame, text="数量 Amount:").grid(row=0, column=0, sticky="w", padx=pad_x, pady=pad_y)
amount_entry_batch = tk.Entry(batch_sell_frame, width=20)
amount_entry_batch.insert(0, "all")
amount_entry_batch.grid(row=0, column=1, sticky="w", padx=pad_x, pady=pad_y)
tk.Label(batch_sell_frame, text="支持 10%, 25%, 50%, 75%, 100% / Supports partial input").grid(row=0, column=2, sticky="w")

tk.Label(batch_sell_frame, text="私钥（多行）Private Keys (Multi-line):").grid(row=1, column=0, sticky="nw", padx=pad_x, pady=pad_y)
private_keys_text_batch = scrolledtext.ScrolledText(batch_sell_frame, width=100, height=4)
private_keys_text_batch.grid(row=1, column=1, columnspan=2, sticky="w", padx=pad_x, pady=pad_y)

tk.Label(batch_sell_frame, text="代币地址 Token Address:").grid(row=2, column=0, sticky="w", padx=pad_x, pady=pad_y)
mint_entry_batch = tk.Entry(batch_sell_frame, width=60)
mint_entry_batch.grid(row=2, column=1, columnspan=2, sticky="w", padx=pad_x, pady=pad_y)

tk.Label(batch_sell_frame, text="最大滑点 Slippage:").grid(row=3, column=0, sticky="w", padx=pad_x, pady=pad_y)
slippage_entry_batch = tk.Entry(batch_sell_frame, width=10)
slippage_entry_batch.insert(0, "0.25")
slippage_entry_batch.grid(row=3, column=1, sticky="w", padx=pad_x, pady=pad_y)
tk.Label(batch_sell_frame, text="例如: 0.25 = 25% / Example: 0.25 = 25%").grid(row=3, column=2, sticky="w")

tk.Button(batch_sell_frame, text="批量卖出 / Batch Sell", width=20, command=sell_token_batch).grid(row=4, column=0, columnspan=3, pady=10)

output_text_batch = scrolledtext.ScrolledText(batch_sell_frame, height=10, width=screen_width // 10, wrap=tk.WORD)
output_text_batch.grid(row=5, column=0, columnspan=3, padx=pad_x, pady=pad_y)
output_text_batch.config(state=tk.DISABLED)

# === 转换到私钥界面 ===
convert_frame = tk.Frame(notebook)
notebook.add(convert_frame, text="转换到私钥 / Convert to Private Key")

tk.Label(convert_frame, text="输入 Byte 数组（例如: [1, 2, ...]）/ Input Byte Array:").grid(row=0, column=0, sticky="nw", padx=pad_x, pady=pad_y)

byte_array_text = scrolledtext.ScrolledText(convert_frame, width=100, height=8)
byte_array_text.grid(row=1, column=0, columnspan=2, sticky="w", padx=pad_x, pady=pad_y)
byte_array_text.insert(tk.END, "[152, 78, 203, 213, 0, 112, 232, 100, 154, 4, 97, 87, 52, 111, 61, 172,\n205, 238, 175, 119, 92, 78, 246, 183, 54, 244, 244, 208, 137, 233, 251, 4,\n7, 90, 205, 48, 51, 55, 111, 233, 230, 75, 173, 212, 120, 229, 18, 248,\n157, 2, 123, 143, 150, 24, 135, 13, 187, 175, 11, 150, 10, 202, 54, 238]")

def clear_byte_array():
    byte_array_text.delete("1.0", tk.END)

tk.Button(convert_frame, text="清空 / Clear", command=clear_byte_array).grid(row=1, column=2, padx=pad_x, pady=pad_y, sticky="ne")

def convert_to_private_key():
    raw_text = byte_array_text.get("1.0", tk.END).strip()
    try:
        parsed = eval(raw_text)
        if not isinstance(parsed, list) or not all(isinstance(i, int) and 0 <= i <= 255 for i in parsed):
            raise ValueError("输入必须是 0-255 之间的整数列表")
        byte_data = bytes(parsed)
        b58_key = base58.b58encode(byte_data).decode()
        private_key_output.config(state=tk.NORMAL)
        private_key_output.delete("1.0", tk.END)
        private_key_output.insert(tk.END, b58_key)
        private_key_output.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("错误 / Error", f"转换失败: {str(e)}")

tk.Button(convert_frame, text="转换 / Convert", width=20, command=convert_to_private_key).grid(row=2, column=0, columnspan=2, pady=10)

tk.Label(convert_frame, text="Base58 私钥 / Base58 Private Key:").grid(row=3, column=0, sticky="w", padx=pad_x, pady=pad_y)

private_key_output = scrolledtext.ScrolledText(convert_frame, width=100, height=2, wrap=tk.WORD)
private_key_output.grid(row=4, column=0, columnspan=2, padx=pad_x, pady=pad_y)
private_key_output.config(state=tk.DISABLED)

def clear_private_key():
    private_key_output.config(state=tk.NORMAL)
    private_key_output.delete("1.0", tk.END)
    private_key_output.config(state=tk.DISABLED)

def copy_private_key():
    private_key_output.config(state=tk.NORMAL)
    text = private_key_output.get("1.0", tk.END).strip()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    private_key_output.config(state=tk.DISABLED)
    messagebox.showinfo("提示 / Info", "私钥已复制到剪贴板！")

button_frame = tk.Frame(convert_frame)
button_frame.grid(row=4, column=2, sticky="n", padx=pad_x, pady=pad_y)

tk.Button(button_frame, text="清空 / Clear", command=clear_private_key).pack(fill="x", pady=2)
tk.Button(button_frame, text="复制 / Copy", command=copy_private_key).pack(fill="x", pady=2)

# === 启动 GUI ===
root.mainloop()
