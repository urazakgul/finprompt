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
    You are a Python coding assistant. The user will describe a stock data request in natural language.

    Your job:
    1. Extract stock codes (like AKBNK, THYAO) from the prompt.
    2. Detect any date range (e.g. "in 2025", "from January to March 2023") and set:
       - stocks (list of str): stock codes in uppercase
       - startdate (str): start date in DD-MM-YYYY
       - enddate (str): end date in DD-MM-YYYY
    3. For each stock, build the API URL:
       url = f"https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse={{stock}}&startdate={{startdate}}&enddate={{enddate}}.json"
    4. For each URL:
       - Fetch with requests (timeout=10)
       - If error, skip that stock
       - If response is OK, parse the "value" field to a pandas DataFrame
       - Add a "Stock" column indicating the code
    5. Concatenate all DataFrames as df.

    6. If the user requests specific columns, map each to the correct column name using the COLUMN_DESCRIPTIONS dictionary below.
       - Filter df to only those columns.

    7. **Always add the relevant date column for each data type to the DataFrame.**
       - For stock data add HGDG_TARIH
       - For index data add END_TARIH
       - For currency data add DD_TARIH
       - Ensure the date column is present even if not requested by the user.

    8. Do NOT use fuzzy or partial matching. Only map exact or clearly defined expressions from COLUMN_DESCRIPTIONS.

    COLUMN_DESCRIPTIONS = {COLUMN_DESCRIPTIONS}

    Only use standard libraries, requests, and pandas.
    Return ONLY runnable Python code. Do NOT include any comments or explanations.
    """