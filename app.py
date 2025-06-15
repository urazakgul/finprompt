import streamlit as st
from finprompt.openai_client import generate_code_from_prompt
from finprompt.code_utils import clean_code_output, run_generated_code, is_valid_python
from finprompt.session import api_key_widget
from finprompt.config import APP_TITLE, DATASOURCE_DISPLAY_NAMES
from finprompt.rate_limit import get_user_ip, check_and_increment_ip_limit, get_ip_limit_reset_seconds, MAX_REQUESTS_PER_IP
from importlib import import_module
from finprompt.logger import log_prompt_supabase
import traceback

def main():
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(APP_TITLE)

    st.caption("⚠️ Beta sürecinde kullanıcı sorguları ve hata mesajları iyileştirme amacıyla anonim bir şekilde kaydedilir.")

    st.write(f"OpenAI API anahtarınızı aşağıdaki alana girdiğinizde tüm özellikleri tam erişimle kullanabilirsiniz. Dilerseniz bu alanı boş bırakıp ücretsiz sürümle (günde {MAX_REQUESTS_PER_IP} sorgu) devam edebilirsiniz.")

    api_key, using_default = api_key_widget()

    datasource_keys = list(DATASOURCE_DISPLAY_NAMES.keys())
    selected_display = st.selectbox("Veri Kaynağı", options=[DATASOURCE_DISPLAY_NAMES[k] for k in datasource_keys])
    display_to_key = {v: k for k, v in DATASOURCE_DISPLAY_NAMES.items()}
    datasource = display_to_key[selected_display]

    ds_module = import_module(f"finprompt.datasources.{datasource}")

    with st.expander("Kullanılabilir Sütunlar"):
        for col, desc in ds_module.COLUMN_DESCRIPTIONS.items():
            st.markdown(f"- **{col}**: {desc}")

    with st.expander("Örnek Sorgular"):
        st.markdown("""
        - 2024 yılı için AKBNK ve THYAO hisselerinin aylık ortalama kapanış verilerini göster
        - SISE'nin Ocak-Mart 2025 kapanış fiyatlarını getir
        - TUPRS hissesinin son 7 iş günündeki en düşük ve en yüksek değerlerini getir
        """)

    user_input = st.text_input("Sorgunuz", help="Örnek: 2025 yılı için AKBNK hissesi kapanış verilerini getir")
    model = "gpt-4o"

    if "generated_code" not in st.session_state:
        st.session_state.generated_code = ""

    kod_ve_sonuc = st.button("Kodu Oluştur ve Sonuçları Getir")

    if kod_ve_sonuc:
        if not user_input:
            st.warning("Lütfen bir sorgu girin.")
            return

        if using_default:
            ip = get_user_ip()
            if not ip:
                st.warning("Kullanıcı IP adresiniz alınamadı. Ücretsiz erişim kapalı. Lütfen kendi OpenAI API anahtarınızı kullanın.")
                log_prompt_supabase(user_input, error_message="IP alınamadı, ücretsiz erişim devre dışı.")
                return
            allowed, remaining = check_and_increment_ip_limit(ip)
            if not allowed:
                reset_sec = get_ip_limit_reset_seconds(ip)
                mins, secs = divmod(reset_sec, 60)
                hours, mins = divmod(mins, 60)
                st.warning(f"Ücretsiz günlük limit aşıldı. {hours} saat {mins} dakika sonra tekrar deneyin veya kendi API anahtarınızı kullanın.")
                log_prompt_supabase(user_input, error_message="Ücretsiz limit aşıldı.")
                return
            else:
                st.info(f"Kalan ücretsiz günlük hakkınız: **{remaining}**")

        try:
            with st.spinner("Kod üretiliyor..."):
                code = generate_code_from_prompt(user_input, api_key, datasource, model)
                code = clean_code_output(code)
                st.session_state.generated_code = code

            log_prompt_supabase(user_input)

            with st.expander("Python kodunu göster"):
                st.code(st.session_state.generated_code, language="python")

            if not is_valid_python(st.session_state.generated_code):
                st.error("Kodda sözdizimi hatası var.")
                log_prompt_supabase(user_input, error_message="Kodda sözdizimi hatası var.")
                return

            with st.spinner("Kod çalıştırılıyor..."):
                run_generated_code(st.session_state.generated_code, user_input)
        except Exception as exc:
            tb_str = traceback.format_exc()
            log_prompt_supabase(user_input, error_message=tb_str)
            st.error(f"Kod çalıştırılırken bir hata oluştu:\n\n{exc}")
            st.info("Bu hata kayıt altına alındı ve incelenecektir.")

if __name__ == "__main__":
    main()