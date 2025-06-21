"""Interactive *line-less* wrapper around llama-cli.

Key points
==========
• Starts `llama-cli` once and keeps it hidden in the background.
• Streams the assistant response **character-by-character** (no dependency on
  model newlines).
• Suppresses the model's prologue tokens (everything up to and including the
  custom *IN_SUFFIX*), so you only see the assistant's real words.
• Considers the assistant turn complete after *SILENCE* seconds of inactivity
  **once tokens have started flowing**. Adjust with `--silence`.

This makes the chat feel like a normal REPL even when the model doesn't emit
newlines or custom sentinels.
"""
from __future__ import annotations

import argparse, pathlib, platform, queue, signal, subprocess, sys, threading

# ─── constants ────────────────────────────────────────────────────────────────
REPO_ROOT   = pathlib.Path(__file__).resolve().parent
DEFAULT_GGUF = REPO_ROOT / "model" / "model.gguf"

IN_PREFIX  = "<|begin_of_text|>User:\n"     # wrapped around each user turn
IN_SUFFIX  = "<|end_of_text|>Assistant:\n"  # marks end of user, start of asst

# ─── CLI flags ────────────────────────────────────────────────────────────────
cli = argparse.ArgumentParser(description="Tiny, newline-agnostic chat wrapper for llama-cli")
cli.add_argument("-m", "--model", default=DEFAULT_GGUF, help="GGUF file")
cli.add_argument("-t", "--threads", type=int, default=12)
cli.add_argument("-c", "--ctx-size", type=int, default=4096)
cli.add_argument("-n", "--n-predict", type=int, default=50)
cli.add_argument("--temp", type=float, default=0.5)
cli.add_argument("--silence", type=float, default=0.5, help="seconds of quiet that end an assistant turn")
args = cli.parse_args()

model_path = pathlib.Path(args.model)
if not model_path.is_file():
    sys.exit(f"❌  Model file not found at {model_path}")

exe_name = "llama-cli.exe" if platform.system() == "Windows" else "llama-cli"
exe = REPO_ROOT / "build/bin" / exe_name
if not exe.exists():
    sys.exit(f"❌  llama-cli not found at {exe}")

cmd = [
    str(exe),
    "-m", str(model_path),
    "-t", str(args.threads),
    "-c", str(args.ctx_size),
    "-ngl", "0",
    "-i", "--interactive-first",  # keep stdin open & auto-wrap first prompt
    "--in-prefix",  IN_PREFIX,
    "--in-suffix",  IN_SUFFIX,
    "-n", str(args.n_predict),
    "--temp", str(args.temp),
]

# ─── launch llama-cli ─────────────────────────────────────────────────────────
proc = subprocess.Popen(
    cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,   # flip to None for loader/debug output
    text=True, encoding="utf-8", bufsize=0,  # unbuffered stdout so we see chars ASAP
)
if proc.poll() is not None:
    print(proc.stdout.read())
    sys.exit("💀  llama-cli exited during startup")

# ─── background reader thread (char stream) ───────────────────────────────────
q: "queue.Queue[str | None]" = queue.Queue()

def _reader() -> None:
    """Feed each character from llama-cli stdout into *q* (None on EOF)."""
    while True:
        ch = proc.stdout.read(1)
        if ch == "":   # EOF / model crashed
            q.put(None)
            break
        q.put(ch)

threading.Thread(target=_reader, daemon=True).start()

# ─── graceful Ctrl-C ─────────────────────────────────────────────────────────

def _bye(*_: object) -> None:   # type: ignore[override]
    print("\nBye!")
    proc.kill()
    sys.exit(0)

signal.signal(signal.SIGINT, _bye)

# ─── helper: stream one assistant turn ───────────────────────────────────────

def _stream_assistant() -> None:
    """Print the next assistant response, hiding the model prologue tokens."""
    # 1️⃣  Eat everything up to and including IN_SUFFIX (prologue)
    window: list[str] = []            # rolling buffer of last len(IN_SUFFIX) chars
    while True:
        ch = q.get()
        if ch is None:
            sys.exit("💥  llama-cli closed unexpectedly")
        window.append(ch)
        if len(window) > len(IN_SUFFIX):
            window.pop(0)
        if "".join(window).endswith(IN_SUFFIX):
            break   # prologue over → real assistant text follows

    # 2️⃣  Now print chars until silence gap
    seen_output = False
    while True:
        try:
            ch = q.get(timeout=args.silence)
        except queue.Empty:
            if seen_output:
                print()                # newline after assistant finished
                return
            # else: still thinking before first token
            continue

        if ch is None:
            sys.exit("💥  llama-cli closed unexpectedly")

        print(ch, end="", flush=True)
        seen_output = True

# ─── chat loop ───────────────────────────────────────────────────────────────
print("🤖  Ready — Ctrl-C to quit\n")
while True:
    try:
        user = input("You: ").strip()
    except EOFError:
        _bye()

    if not user:
        continue

    # Send prompt to llama-cli
    proc.stdin.write(user + "\n")
    proc.stdin.flush()

    print("Bot:", end=" ", flush=True)
    _stream_assistant()
