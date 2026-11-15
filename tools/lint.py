import re, sys, pathlib
root = pathlib.Path(sys.argv[1]) / "wiki"
pages = {p.stem: p for p in root.rglob("*.md")}
links_in = {k: 0 for k in pages}
broken, uncited = [], []
for name, p in pages.items():
    t = p.read_text(encoding="utf-8")
    for l in re.findall(r"\[\[([^\]]+)\]\]", t):
        if l in pages:
            if l != name: links_in[l] += 1
        else:
            broken.append((name, l))
    if p.parent.name in ("concepts", "sources"):
        body = t.split("---", 2)[-1]
        for i, line in enumerate(body.splitlines(), 1):
            if re.search(r"\d", line) and line.strip().startswith(("-", "|")) and not re.search(r"\(S\d|S\d", line) and "[[" not in line:
                uncited.append((name, i, line.strip()[:70]))
print("頁面數:", len(pages))
print("壞連結:", broken or "無")
print("孤兒頁(無入站連結):", [k for k, v in links_in.items() if v == 0 and k not in ("log",)] or "無")
print("含數字但無來源編號的行:")
for u in uncited: print("  ", u)
