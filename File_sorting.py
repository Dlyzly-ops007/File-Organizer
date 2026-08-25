import os
import shutil
import threading
import tkinter as tk
from tkinter import ttk, filedialog

# categories
cm = {
    "Images":      [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos":      [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv"],
    "Music":       [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Documents":   [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".md"],
    "Archives":    [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code":        [".py", ".cpp", ".c", ".js", ".ts", ".html", ".css",
                    ".java", ".cs", ".go", ".rs", ".json", ".yaml", ".sh"],
    "Slides":      [".pptx", ".ppt"],
    "Spreadsheets":[".csv", ".ods"],
    "Executables": [".exe", ".msi", ".dmg"],
}

# colors
bg   = "#0f0f11"
bg2  = "#1a1a20"
bg3  = "#222228"
acc  = "#e8ff48"
grn  = "#4fffb0"
red  = "#ff4f6b"
txt  = "#e8e8ec"
dim  = "#555560"
brdr = "#2e2e38"
fn   = ("Courier New", 10)
fnb  = ("Courier New", 10, "bold")


def get_cat(ext):
    for cat, exts in cm.items():
        if ext in exts:
            return cat
    return "Others"


def run(path, mode, preview, skip_sub, log, bar, status, btn):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    if not skip_sub:
        for item in os.listdir(path):
            sub = os.path.join(path, item)
            if os.path.isdir(sub):
                for f in os.listdir(sub):
                    if os.path.isfile(os.path.join(sub, f)):
                        files.append(os.path.join(item, f))

    if not files:
        log("no files found", dim)
        btn.config(state="normal")
        return

    cats = {}
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        cats.setdefault(get_cat(ext), []).append(f)

    total = sum(len(v) for v in cats.values())
    bar["maximum"] = total
    done = 0

    for cat, lst in cats.items():
        dest_dir = os.path.join(path, cat)
        for f in lst:
            src  = os.path.join(path, f)
            fname = os.path.basename(f)
            dest = os.path.join(dest_dir, fname)
            if os.path.exists(dest):
                name, ext2 = os.path.splitext(fname)
                dest = os.path.join(dest_dir, f"{name}_copy{ext2}")
            try:
                if not preview:
                    os.makedirs(dest_dir, exist_ok=True)
                    if mode == "move":
                        shutil.move(src, dest)
                    else:
                        shutil.copy2(src, dest)
                sym = "?" if preview else ("→" if mode == "move" else "+")
                log(f"  {sym} {fname}  ({cat})", dim if preview else grn)
            except Exception as e:
                log(f"  error: {fname} — {e}", red)
            done += 1
            bar["value"] = done
            status.config(text=f"{done}/{total}")
            bar.update_idletasks()

    label = "preview done" if preview else "done"
    log(f"\n{label} — {done} files, {len(cats)} folders", acc)
    status.config(text=label)
    btn.config(state="normal")


def browse(var):
    p = filedialog.askdirectory()
    if p:
        var.set(p)


def start(path_var, mode_var, preview_var, skip_var, log, bar, status, btn):
    p = path_var.get().strip().strip('"')
    if not os.path.isdir(p):
        log("invalid path", red)
        return
    btn.config(state="disabled")
    pre = preview_var.get()
    log(f"\n{'[preview] ' if pre else ''}running on: {p}  [{mode_var.get()}]\n", acc)
    threading.Thread(target=run, args=(p, mode_var.get(), pre, skip_var.get(), log, bar, status, btn), daemon=True).start()


def mk_log(widget):
    widget.tag_config("grn", foreground=grn)
    widget.tag_config("red", foreground=red)
    widget.tag_config("acc", foreground=acc)
    widget.tag_config("dim", foreground=dim)
    colors = {"grn": grn, "red": red, "acc": acc, "dim": dim}
    def write(msg, color=txt):
        tag = next((k for k, v in colors.items() if v == color), "")
        widget.config(state="normal")
        widget.insert("end", msg + "\n", tag if tag else ())
        widget.see("end")
        widget.config(state="disabled")
    return write


# window
root = tk.Tk()
root.title("file sorter")
root.geometry("700x520")
root.configure(bg=bg)
root.resizable(True, True)

# style
sty = ttk.Style()
sty.theme_use("default")
sty.configure("bar.Horizontal.TProgressbar", troughcolor=bg3, background=acc, thickness=4, borderwidth=0)
sty.configure("TScrollbar", background=bg3, troughcolor=bg3, borderwidth=0, arrowcolor=dim)

path_var    = tk.StringVar()
mode_var    = tk.StringVar(value="move")
preview_var = tk.BooleanVar(value=False)
skip_var    = tk.BooleanVar(value=True)

# title
tk.Label(root, text="file sorter", font=("Courier New", 18, "bold"), bg=bg, fg=acc).pack(anchor="w", padx=20, pady=(18, 4))
tk.Frame(root, bg=brdr, height=1).pack(fill="x", padx=20)

# path row
fr = tk.Frame(root, bg=bg, pady=10)
fr.pack(fill="x", padx=20)
tk.Label(fr, text="folder", font=fn, bg=bg, fg=dim).pack(anchor="w")
row = tk.Frame(fr, bg=bg)
row.pack(fill="x", pady=(4,0))
tk.Entry(row, textvariable=path_var, font=fn, bg=bg3, fg=txt, insertbackground=acc,
         relief="flat", highlightthickness=1, highlightbackground=brdr, highlightcolor=acc
         ).pack(side="left", fill="x", expand=True, ipady=6)
tk.Button(row, text="browse", font=fnb, bg=acc, fg=bg, relief="flat", cursor="hand2",
          activebackground="#d0e830", command=lambda: browse(path_var)
          ).pack(side="left", padx=(8,0), ipady=4, ipadx=8)

# options
opts = tk.Frame(root, bg=bg)
opts.pack(fill="x", padx=20, pady=(0, 8))
for label, val in [("move", "move"), ("copy", "copy")]:
    tk.Radiobutton(opts, text=label, variable=mode_var, value=val, font=fn,
                   bg=bg, fg=txt, selectcolor=bg, activebackground=bg,
                   activeforeground=acc, indicatoron=False, relief="flat",
                   padx=10, pady=3, cursor="hand2").pack(side="left", padx=(0,6))

tk.Frame(opts, bg=brdr, width=1).pack(side="left", fill="y", padx=10)

for label, var in [("skip subfolders", skip_var), ("preview only", preview_var)]:
    tk.Checkbutton(opts, text=label, variable=var, font=fn,
                   bg=bg, fg=dim, selectcolor=bg, activebackground=bg,
                   activeforeground=txt, cursor="hand2").pack(side="left", padx=(0, 10))

# run + status
br = tk.Frame(root, bg=bg)
br.pack(fill="x", padx=20, pady=(0,8))
btn = tk.Button(br, text="run", font=fnb, bg=acc, fg=bg, relief="flat",
                cursor="hand2", padx=20, pady=6, activebackground="#d0e830")
btn.pack(side="left")
status = tk.Label(br, text="", font=fn, bg=bg, fg=dim)
status.pack(side="left", padx=12)

bar = ttk.Progressbar(root, style="bar.Horizontal.TProgressbar")
bar.pack(fill="x", padx=20, pady=(0, 8))

# log
tk.Frame(root, bg=brdr, height=1).pack(fill="x", padx=20)
log_frame = tk.Frame(root, bg=bg3)
log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))
log_box = tk.Text(log_frame, bg=bg3, fg=txt, font=("Courier New", 9),
                  relief="flat", wrap="none", state="disabled",
                  selectbackground=bg2, insertbackground=acc)
sb = ttk.Scrollbar(log_frame, command=log_box.yview)
log_box.config(yscrollcommand=sb.set)
sb.pack(side="right", fill="y")
log_box.pack(fill="both", expand=True, padx=8, pady=8)

log = mk_log(log_box)
btn.config(command=lambda: start(path_var, mode_var, preview_var, skip_var, log, bar, status, btn))

root.mainloop()
