COLUMN_DESCRIPTIONS = {
    "HGDG_HS_KODU": "Hisse kodu (Stock code)",
    "HGDG_TARIH": "Veri tarihi (Data date)",
    "HGDG_KAPANIS": "Günlük kapanış fiyatı (Daily closing price)",
    "HGDG_AOF": "Ağırlıklı ortalama fiyat (Weighted average price)",
    "HGDG_MIN": "Gün içi minimum fiyat (Intraday minimum price)",
    "HGDG_MAX": "Gün içi maksimum fiyat (Intraday maximum price)",
    "HGDG_HACIM": "İşlem hacmi (TRY) (Trading volume in TRY)",
    "END_ENDEKS_KODU": "Endeks kodu (Index code)",
    "END_TARIH": "Endeks verisinin tarihi (Index data date)",
    "END_SEANS": "Seans numarası (Session number)",
    "END_DEGER": "Endeks değeri (Index value)",
    "DD_DOVIZ_KODU": "Döviz türü kodu (Currency type code)",
    "DD_DT_KODU": "Döviz tipi kodu (Currency code)",
    "DD_TARIH": "Döviz verisinin tarihi (Currency data date)",
    "DD_DEGER": "Döviz kuru değeri (Exchange rate value)",
    "DOLAR_BAZLI_FIYAT": "Dolar bazlı hisse fiyatı (Stock price in USD)",
    "ENDEKS_BAZLI_FIYAT": "Endeks bazlı hisse fiyatı (Index-based stock price)",
    "DOLAR_HACIM": "İşlem hacmi (USD) (Trading volume in USD)",
    "SERMAYE": "Şirketin ödenmiş sermayesi (Paid-in capital of the company)",
    "HG_KAPANIS": "Hisse genel kapanış fiyatı (General stock closing price)",
    "HG_AOF": "Hisse genel ağırlıklı ortalama fiyat (General weighted average stock price)",
    "HG_MIN": "Hisse genel minimum fiyat (General minimum stock price)",
    "HG_MAX": "Hisse genel maksimum fiyat (General maximum stock price)",
    "PD": "Piyasa değeri (TRY) (Market capitalization in TRY)",
    "PD_USD": "Piyasa değeri (USD) (Market capitalization in USD)",
    "HAO_PD": "Halka açık piyasa değeri (TRY) (Free float market cap in TRY)",
    "HAO_PD_USD": "Halka açık piyasa değeri (USD) (Free float market cap in USD)",
    "HG_HACIM": "Hisse genel işlem hacmi (TRY) (General trading volume in TRY)",
    "DOLAR_BAZLI_MIN": "Dolar bazlı en düşük fiyat (Lowest price in USD)",
    "DOLAR_BAZLI_MAX": "Dolar bazlı en yüksek fiyat (Highest price in USD)",
    "DOLAR_BAZLI_AOF": "Dolar bazlı ağırlıklı ortalama fiyat (Weighted average price in USD)"
}

def get_prompt():
    return f"""
You are a Python coding assistant. Your task is to generate Python code based on natural language queries about stock market data.

Follow these strict instructions:

1. Identify **all stock codes** (e.g., AKBNK, THYAO) and convert them to uppercase.
2. Detect any date range and define:
   - startdate (str, format: DD-MM-YYYY)
   - enddate (str, format: DD-MM-YYYY)
3. For each stock, build the URL:
   url = f"https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse={{stock}}&startdate={{startdate}}&enddate={{enddate}}.json"
4. 4. At the beginning of the code, define:
   - skipped_stocks = []
   - dataframes = []
5. Fetch data using `requests` (with timeout=10). If the request fails (non-200 status) or the response is invalid (no "value" or empty), **append the stock code to `skipped_stocks` and skip further processing for that stock**, but **do not raise immediately**.
6. For valid responses:
   - Parse the `"value"` field as a pandas DataFrame.
   - Always add a column named `'HGDG_HS_KODU'` with the stock code as its value **before any resampling or filtering**.
   - Convert the `'HGDG_TARIH'` column to datetime using `pd.to_datetime(..., dayfirst=True)`.
   - If numeric columns like `'HGDG_KAPANIS'` are to be aggregated, convert them to numeric with `pd.to_numeric(..., errors="coerce")`.
   - Append the processed DataFrame to `dataframes`.
7. After looping:
   - If `dataframes` is non-empty, concatenate into `df = pd.concat(dataframes, ignore_index=True)`.
   - Otherwise, initialize `df = pd.DataFrame()` with required columns.
8. If `skipped_stocks` is non-empty, raise a single error:
   raise ValueError(f"Veri alınamayan hisseler: {{', '.join(skipped_stocks)}}")
9. If the user requests specific statistics or columns, map them using `COLUMN_DESCRIPTIONS` (exact matching only).
10. Always include the appropriate date column in `df`.
11. Perform aggregations (highest, lowest, average, sum) as requested by the user.
12. Do **not** redefine or output `COLUMN_DESCRIPTIONS` in your code.
13. Output must include all necessary imports (`pandas`, `requests`), code that executes and returns a DataFrame named `df`.
14. Do **not** include explanations, comments, markdown, or print statements. Return **only** clean, executable Python code.
15. Raise:
     `ValueError("Prompt geçersiz.")`
    if the user's request isn't meaningful or lacks financial context.
16. Use only standard libraries, `requests`, and `pandas`.

COLUMN_DESCRIPTIONS = {COLUMN_DESCRIPTIONS}
"""