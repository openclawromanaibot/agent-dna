#!/usr/bin/env python3
"""PR gate for a PUBLIC repo of agent instructions. Fails closed, stdlib only.

Checks every commit of the PR (not only the final tree): a secret added and
removed later is still public in the PR history.
"""
import os
import re
import subprocess
import sys

L0_BUDGET = 3072  # bytes, core + local per agent
MAX_FILE = 65536
AGENTS = ("openclaw", "hermes")

ALLOWED_PATHS = [
    r"L0-core\.md",
    r"broadcast\.md",
    r"(?:openclaw|hermes)/L0-local\.md",
    r"(?:common|openclaw|hermes)/instructions/[A-Za-z0-9._/-]+\.md",
    r"common/tasks/[A-Za-z0-9._/-]+\.md",
    r"README\.md",
    r"\.gitignore",
    r"\.github/CODEOWNERS",
    r"\.github/workflows/gate\.yml",
    r"\.github/scripts/gate\.py",
    r"tests/test_gate\.py",
]
# Gate sources and tests must contain sample patterns; they are owner-reviewed.
CONTENT_EXEMPT = (".github/scripts/", "tests/")

SECRET_PATTERNS = [
    ("github token", r"\bgh[pousr]_[A-Za-z0-9]{30,}"),
    ("github fine-grained token", r"\bgithub_pat_[A-Za-z0-9_]{30,}"),
    ("api key (sk-)", r"\bsk-[A-Za-z0-9_-]{20,}"),
    ("slack token", r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    ("aws key id", r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    ("telegram bot token", r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b"),
    ("private key block", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("bearer value", r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    ("credential in url", r"x-access-token:|://[^/\s:@]+:[^/\s@]+@"),
    ("assigned secret", r"(?i)\b(?:password|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*['\"]?[A-Za-z0-9/+_.-]{12,}"),
]
PRIVATE_PATTERNS = [
    ("ipv4 address", r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    ("email address", r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    ("windows user path", r"(?i)\b[a-z]:\\+users\\+(?!<)[^\\\s<]+"),
    ("unix home path", r"/home/(?!<)[A-Za-z0-9._-]+"),
    ("telegram chat id", r"(?<![\w.])-100\d{8,}\b"),
    ("phone number", r"\+\d[\d\s().-]{8,}\d"),
]
INJECTION_PATTERNS = [
    ("html comment (hidden text)", r"<!--"),
    ("remote execution", r"(?i)\b(?:curl|wget)\b[^\n|]*\|\s*(?:ba)?sh\b|\bInvoke-Expression\b|base64\s+-d"),
    ("override phrase", r"(?i)ignore\s+(?:all\s+|any\s+)?(?:previous|prior|above)\s+instructions"),
]
SAFE_IPS = {"0.0.0.0", "127.0.0.1"}
# zero-width, bidi controls, BOM, tag characters: hidden text for a reader model
HIDDEN_CHARS = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff\U000e0000-\U000e007f]")


def checkPath(path):
    """Return a reason string if the path is not allowed, else None."""
    parts = path.split("/")
    if ".." in parts or "" in parts or any(p.startswith(".") and p not in (".github", ".gitignore") for p in parts):
        return "unsafe path segment"
    if not any(re.fullmatch(p, path) for p in ALLOWED_PATHS):
        return "path not in allowlist"
    return None


def checkMode(mode):
    """Reject symlinks, submodules and executables."""
    if mode in ("120000", "160000"):
        return "symlink or submodule"
    if mode == "100755":
        return "executable bit"
    return None


def scanLine(path, line):
    """Return a list of reasons a single text line must not be published."""
    reasons = []
    if HIDDEN_CHARS.search(line):
        reasons.append("hidden unicode")
    if path.startswith(CONTENT_EXEMPT):
        return reasons
    for name, pat in SECRET_PATTERNS + INJECTION_PATTERNS:
        if re.search(pat, line):
            reasons.append(name)
    for name, pat in PRIVATE_PATTERNS:
        for m in re.finditer(pat, line):
            if name == "ipv4 address" and m.group(0) in SAFE_IPS:
                continue
            reasons.append(name)
            break
    return reasons


def checkL0Size(coreBytes, localBytes):
    """Return a reason if core + local exceeds the L0 budget."""
    total = coreBytes + localBytes
    if total > L0_BUDGET:
        return f"L0 {total} B exceeds budget {L0_BUDGET} B"
    return None


def git(*args):
    """Run git and return stdout bytes; fail closed on error."""
    return subprocess.run(["git", *args], check=True, capture_output=True).stdout


def historyFindings(base, head):
    """Scan paths, modes and added lines of every commit in base..head."""
    out = []
    raw = git("log", "--raw", "--no-renames", "--format=", "-z", f"{base}..{head}").decode("utf-8", "replace")
    for rec in filter(None, raw.split("\0")):
        if rec.startswith(":"):
            meta = rec.split()
            mode, status = meta[1], meta[4]
            continue
        if status != "D":
            why = checkPath(rec) or checkMode(mode)
            if why:
                out.append(f"{rec}: {why}")
    patch = git("log", "-p", "-U0", "--no-color", "--no-renames", "--format=", f"{base}..{head}").decode("utf-8", "replace")
    path = ""
    for line in patch.splitlines():
        if line.startswith("+++ b/"):
            path = line[6:]
        elif line.startswith("+") and not line.startswith("+++"):
            for why in scanLine(path, line[1:]):
                out.append(f"{path}: {why} (in commit history)")
    return out


def treeFindings():
    """Scan the final tree: encoding, size, content, L0 budget."""
    out = []
    sizes = {}
    for path in git("ls-files", "-z").decode().split("\0"):
        if not path.endswith(".md"):
            continue
        if os.path.islink(path):
            continue  # never follow links out of the repo; checkMode reports them
        data = open(path, "rb").read()
        sizes[path] = len(data)
        if len(data) > MAX_FILE:
            out.append(f"{path}: larger than {MAX_FILE} B")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            out.append(f"{path}: not valid UTF-8")
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for why in scanLine(path, line):
                out.append(f"{path}:{n}: {why}")
    for agent in AGENTS:
        core, local = sizes.get("L0-core.md"), sizes.get(f"{agent}/L0-local.md")
        if core is not None and local is not None:
            why = checkL0Size(core, local)
            if why:
                out.append(f"{agent}: {why}")
    return out


def main():
    """Entry point: exit 1 on any finding."""
    base, head = os.environ["BASE_SHA"], os.environ["HEAD_SHA"]
    findings = historyFindings(base, head) + treeFindings()
    for f in findings:
        print(f"❌ {f}")
    if findings:
        print(f"🛑 gate failed: {len(findings)} finding(s)")
        return 1
    print("✅ gate passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
