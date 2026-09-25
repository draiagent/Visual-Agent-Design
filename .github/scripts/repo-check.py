#!/usr/bin/env python3
"""repo 一致性檢查：名稱、授權、版本、徽章、tag。用法見 --help。"""
import io, os
import argparse, re, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

LIC_PATTERNS = [
    ("CC-BY-SA", r"Attribution-ShareAlike 4\.0"),
    ("CC-BY-NC", r"Attribution-NonCommercial 4\.0"),
    ("CC-BY", r"Creative Commons Attribution 4\.0|Attribution 4\.0 International"),
    ("OFL", r"SIL OPEN FONT LICENSE"),
    ("MIT", r"Permission is hereby granted, free of charge"),
    ("RESERVED", r"All rights reserved|保留所有權利|保留權利"),
]
README_LIC = [
    ("CC-BY-SA", r"CC[ -]BY[- ]SA"),
    ("CC-BY-NC", r"CC[ -]BY[- ]NC"),
    ("MIT", r"\bMIT\b"),
    ("OFL", r"OFL|Open Font"),
    ("RESERVED", r"保留(所有)?權利|All rights reserved|未授予開源授權"),
    ("CC-BY", r"CC[ -]BY[ -]?4"),
]


def read(p):
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def norm(v):
    v = v.strip().lstrip("vV").strip("[]`* ")
    parts = v.split("-", 1)
    nums = parts[0].split(".")
    while len(nums) < 3:
        nums.append("0")
    return ".".join(nums) + ("-" + parts[1] if len(parts) > 1 else "")


def lic_types(text):
    return {name for name, pat in LIC_PATTERNS if re.search(pat, text, re.I)}


def check(path, name, check_tags):
    errs, warns = [], []
    root = Path(path)
    readme = read(root / "README.md")
    lic_file = next((root / f for f in ("LICENSE", "LICENSE.md", "LICENSE.txt") if (root / f).exists()), None)
    lic_text = read(lic_file) if lic_file else ""
    skill = read(root / "SKILL.md")

    # 1. LICENSE 存在
    if not lic_file:
        errs.append("缺少 LICENSE 檔")
    actual = lic_types(lic_text) if lic_file else set()
    if lic_file and not actual:
        warns.append("LICENSE 無法辨識授權類型")

    # 2. SKILL.md 指向 LICENSE
    if re.search(r"repository LICENSE", skill, re.I) and not lic_file:
        errs.append("SKILL.md 指向 repository LICENSE，但 repo 沒有 LICENSE")

    # 3. README 授權宣稱 vs LICENSE
    claimed = set()
    sec = re.search(r"^#+\s*(?:\d+\.\s*)?(?:授權|License|開源授權)[^\n]*\n+([^#]{0,300})", readme, re.M | re.I)
    badges = " ".join(x for t in re.findall(r"(?:License|授權)-([A-Za-z0-9%._-]+?)-\w+\.svg|badge/(?:code|docs[^/]*)-([A-Za-z0-9%._-]+?)-", readme) for x in t if x)
    scope = badges.replace("%20", " ").replace("--", "-") + " " + (sec.group(1) if sec else "")
    for n, pat in README_LIC:
        if re.search(pat, scope, re.I):
            claimed.add(n)
    if actual and claimed and not (claimed & actual) and not ("CC-BY" in claimed and actual & {"CC-BY-SA", "CC-BY-NC"}):
        errs.append(f"README 宣稱授權 {sorted(claimed)}，但 LICENSE 是 {sorted(actual)}")


    # 4. README 專案結構第一行資料夾名
    m = re.search(r"^#+\s*(?:\d+\.\s*)?(專案結構|檔案結構|目錄結構|Project Structure|Repository Structure)[^\n]*\n+```[^\n]*\n([^\n]+)\r?\n(?=[├└│|])", readme, re.M | re.I)
    if m:
        top = m.group(2).strip()
        if top.endswith("/") and top.rstrip("/") != name and "." != top.rstrip("/"):
            errs.append(f"專案結構資料夾 `{top}` 與 repo 名稱 `{name}` 不一致")

    # 5. 版本來源
    vers = {}
    if (root / "VERSION").exists():
        vers["VERSION"] = norm(read(root / "VERSION").splitlines()[0])
    cl = read(root / "CHANGELOG.md")
    m = re.search(r"^##\s*\[?v?(\d+\.\d+(?:\.\d+)?(?:-[\w.]+)?)\]?", cl, re.M)
    if m:
        vers["CHANGELOG"] = norm(m.group(1))
    m = re.search(r"^version:\s*['\"]?([\w.\-]+)", skill, re.M)
    if m:
        vers["SKILL.md"] = norm(m.group(1))
    pj = read(root / "package.json")
    m = re.search(r'"version":\s*"([^"]+)"', pj)
    if m:
        vers["package.json"] = norm(m.group(1))
    m = re.search(r"badge/[Vv]ersion-(\d+\.\d+(?:\.\d+)?(?:--[\w.]+)?)", readme)
    if m:
        vers["README徽章"] = norm(m.group(1).replace("--", "-"))
    m = re.search(r"(?:版本|Version)[:：*\s`]*v?(\d+\.\d+(?:\.\d+)?(?:-[\w.]+)?)", readme)
    if m:
        vers["README版本"] = norm(m.group(1))
    if len(set(vers.values())) > 1:
        errs.append("版本不一致：" + "、".join(f"{k}={v}" for k, v in vers.items()))
    if not vers:
        warns.append("沒有任何版本來源（VERSION / CHANGELOG）")

    # 6. tag
    if check_tags and vers:
        ver = vers.get("VERSION") or vers.get("CHANGELOG") or next(iter(vers.values()))
        tags = subprocess.run(["git", "-C", path, "tag"], capture_output=True, text=True).stdout.split()
        if not any(norm(t) == ver for t in tags):
            warns.append(f"沒有對應 v{ver} 的 git tag")
    return errs, warns


def main():
    ap = argparse.ArgumentParser(description="repo 名稱／授權／版本／徽章／tag 一致性檢查")
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--name", help="repo 名稱（預設用資料夾名）")
    ap.add_argument("--tags", action="store_true", help="檢查 git tag")
    a = ap.parse_args()
    name = a.name or Path(a.path).resolve().name
    errs, warns = check(a.path, name, a.tags)
    for e in errs:
        print(f"  [錯誤] {e}")
    for w in warns:
        print(f"  [警告] {w}")
    print(f"{'PASS' if not errs else 'FAIL'} {name}（{len(errs)} 錯誤、{len(warns)} 警告）")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
