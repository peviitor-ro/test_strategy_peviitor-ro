# generate_pdf.py — Dependencies

Scriptul care face conversia: **`generate_pdf.py`**

## Required Python packages

```powershell
pip install markdown playwright
```

## Playwright browser

After installing the `playwright` package, install the Chromium browser:

```powershell
python -m playwright install chromium
```

## Test it

```powershell
python generate_pdf.py
```

The script reads `Test_Strategy_Peviitor.ro.md` from the same folder and outputs a new PDF with an auto-incremented version number (e.g. `Test_Strategy_Peviitor.ro_v20.pdf`).
