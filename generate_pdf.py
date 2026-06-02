from pathlib import Path
from markdown import markdown
from playwright.sync_api import sync_playwright

md_path = Path(__file__).parent / "Test_Strategy_Peviitor.ro.md"
pdf_path = Path(__file__).parent / f"Test_Strategy_Peviitor.ro_v{{}}.pdf"

tpl = '<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
tpl += '@page{margin:18mm 20mm;size:A4}'
tpl += '*{box-sizing:border-box}'
tpl += 'body{font-family:Segoe UI,Calibri,Arial,sans-serif;font-size:10.5pt;line-height:1.45;color:#1a1a1a;margin:0;padding:0}'
tpl += 'h1{font-size:16pt;color:#1a1a1a;margin-top:0}'
tpl += 'h2{font-size:13pt;color:#2c5f8a;border-bottom:1.5px solid #2c5f8a;padding-bottom:2pt;margin:14pt 0 6pt 0}'
tpl += 'h3{font-size:11pt;color:#333;margin:10pt 0 4pt 0}'
tpl += 'h4{font-size:10.5pt;color:#444;margin:8pt 0 3pt 0}'
tpl += 'p{margin:3pt 0}ul{margin:3pt 0;padding-left:18pt}'
tpl += 'li{margin-bottom:1.5pt}'
tpl += 'table{width:100%;border-collapse:collapse;margin:6pt 0;font-size:9pt}'
tpl += 'th,td{border:1px solid #ccc;padding:3pt 5pt;text-align:left}'
tpl += 'th{background:#eef3f8;color:#2c5f8a;font-weight:600}'
tpl += 'strong{color:#2c5f8a}'
tpl += 'hr{border:none;border-top:1px solid #ddd;margin:10pt 0}'
tpl += 'code{background:#f4f4f4;padding:1pt 3pt;border-radius:2pt;font-size:9pt}'
tpl += 'blockquote{border-left:3px solid #2c5f8a;margin:6pt 0;padding:4pt 10pt;background:#f9fafb;font-style:italic;color:#555}'
tpl += 'pre{white-space:pre-wrap;word-wrap:break-word;background:#f9fafb;border:1px solid #ddd;padding:10pt;font-size:9pt;border-radius:3pt}'
tpl += '</style></head><body>{c}</body></html>'

text = md_path.read_text(encoding="utf-8")
content = markdown(text, extensions=["extra", "codehilite", "tables", "nl2br"])
html = tpl.replace("{c}", content)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.set_content(html, wait_until="networkidle")
    # determine next version from existing PDFs
    existing = sorted(p.parent.glob("Test_Strategy_Peviitor.ro_v*.pdf"))
    if existing:
        import re
        m = re.search(r'_v(\d+)\.pdf$', existing[-1].name)
        ver = int(m.group(1)) + 1 if m else 1
    else:
        ver = 1
    out = Path(str(pdf_path).format(ver))
    pg.pdf(path=str(out), format="A4", print_background=True)
    b.close()

print(f"PDF generat: {out.name}")
