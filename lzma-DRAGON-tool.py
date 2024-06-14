import tkinter as tk
from tkinter import filedialog, messagebox
import lzma
import os
import binascii

def browse_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, filepath)

def compress_file():
    filepath = entry_file_path.get()
    if not filepath:
        messagebox.showerror("Error", "Please select a file first.")
        return
    
    lc = int(entry_lc.get())
    lp = int(entry_lp.get())
    pb = int(entry_pb.get())
    
    output_path = filepath + '.lzma'
    with open(filepath, 'rb') as f:
        data = f.read()
    
    options = {
        'format': lzma.FORMAT_ALONE,
        'filters': [{
            'id': lzma.FILTER_LZMA1,
            'lc': lc,
            'lp': lp,
            'pb': pb,
        }]
    }
    
    with lzma.open(output_path, 'wb', **options) as compressed_file:
        compressed_file.write(data)
    
    messagebox.showinfo("Success", f"File compressed to {output_path}")

def decompress_file():
    filepath = entry_file_path.get()
    if not filepath.endswith('.lzma'):
        messagebox.showerror("Error", "Please select a .lzma file first.")
        return

    output_path = filepath.replace('.lzma', '_decompressed')
    with lzma.open(filepath, 'rb') as f:
        data = f.read()
    
    with open(output_path, 'wb') as decompressed_file:
        decompressed_file.write(data)
    
    file_info = get_file_info(filepath)
    display_file_info(file_info)
    messagebox.showinfo("Success", f"File decompressed to {output_path}")

def get_file_info(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    
    crc32 = binascii.crc32(data)
    file_info = {
        'path': filepath,
        'size': os.path.getsize(filepath),
        'crc32': format(crc32, '08x'),
        'magic_bytes': data[:4].hex(),
    }
    
    return file_info

def display_file_info(file_info):
    info_text.delete('1.0', tk.END)
    for key, value in file_info.items():
        info_text.insert(tk.END, f"{key.capitalize()}: {value}\n")

root = tk.Tk()
root.title("LZMA DragonNoir-Dz_Tool")
root.geometry("500x400")
root.resizable(False, False)

frame_path = tk.Frame(root)
frame_path.pack(pady=10)

label_file_path = tk.Label(frame_path, text="File Path:")
label_file_path.pack(side=tk.LEFT, padx=5)

entry_file_path = tk.Entry(frame_path, width=50)
entry_file_path.pack(side=tk.LEFT, padx=5)

button_browse = tk.Button(frame_path, text="Browse", command=browse_file)
button_browse.pack(side=tk.LEFT, padx=5)

frame_params = tk.Frame(root)
frame_params.pack(pady=10)

label_lc = tk.Label(frame_params, text="lc:")
label_lc.pack(side=tk.LEFT, padx=5)
entry_lc = tk.Entry(frame_params, width=5)
entry_lc.pack(side=tk.LEFT, padx=5)
entry_lc.insert(0, "3")

label_lp = tk.Label(frame_params, text="lp:")
label_lp.pack(side=tk.LEFT, padx=5)
entry_lp = tk.Entry(frame_params, width=5)
entry_lp.pack(side=tk.LEFT, padx=5)
entry_lp.insert(0, "0")

label_pb = tk.Label(frame_params, text="pb:")
label_pb.pack(side=tk.LEFT, padx=5)
entry_pb = tk.Entry(frame_params, width=5)
entry_pb.pack(side=tk.LEFT, padx=5)
entry_pb.insert(0, "2")

frame_results = tk.LabelFrame(root, text="File Info", padx=10, pady=10)
frame_results.pack(pady=10, fill="both", expand=True)

info_text = tk.Text(frame_results, width=60, height=10)
info_text.pack()

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

button_decompress = tk.Button(frame_buttons, text="Decompress", command=decompress_file, width=15)
button_decompress.pack(side=tk.LEFT, padx=5)

button_compress = tk.Button(frame_buttons, text="Compress", command=compress_file, width=15)
button_compress.pack(side=tk.LEFT, padx=5)

root.mainloop()
