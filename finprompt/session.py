import streamlit as st
from finprompt.config import OPENAI_API_KEY

def get_active_api_key():
    user_key = st.session_state.get("user_api_key", "")
    use_default = not bool(user_key)

    if use_default:
        api_key = OPENAI_API_KEY
    else:
        api_key = user_key

    return api_key, use_default

def api_key_widget():
    if "user_api_key" not in st.session_state:
        st.session_state.user_api_key = ""

    api_key, using_default = get_active_api_key()

    if not using_default:
        st.success("Oturum için kendi OpenAI API anahtarınız ayarlandı.")
        if st.button("Düzenle"):
            st.session_state.user_api_key = ""
            st.rerun()
    else:
        with st.form("api_key_form", clear_on_submit=False):
            user_key_input = st.text_input(
                "Kendi OpenAI API Anahtarınızı girin (isteğe bağlı)",
                type="password",
                value="",
                help="Anahtarınızı https://platform.openai.com/api-keys adresinden alabilirsiniz. Boş bırakırsanız ücretsiz anahtar kullanılacak (sınırlı)."
            )
            submit = st.form_submit_button("Kaydet")
            if submit:
                if user_key_input.strip():
                    st.session_state.user_api_key = user_key_input.strip()
                    st.success("API anahtarınız bu oturum için kaydedildi.")
                    st.rerun()
    return api_key, using_default