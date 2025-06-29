import openai
import streamlit as st
from importlib import import_module
from finprompt.logger import log_prompt_supabase
import traceback

def load_prompt_for_datasource(datasource, data_mode, financial_group_display=None):
    module = import_module(f"finprompt.datasources.{datasource}")
    if datasource == "isyatirim":
        if data_mode == "historical":
            return module.get_prompt_historical()
        elif data_mode == "financial":
            return module.get_prompt_financial(financial_group_display)
    return ""

@st.cache_data(ttl=3600, show_spinner=False)
def generate_code_from_prompt(
    user_prompt: str,
    api_key: str,
    datasource: str,
    data_mode: str = "historical",
    model: str = "gpt-4o",
    financial_group_display: str = None
) -> str:
    try:
        client = openai.OpenAI(api_key=api_key)
        system_message = load_prompt_for_datasource(datasource, data_mode, financial_group_display)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        tb_str = traceback.format_exc()
        log_prompt_supabase(user_prompt, error_message=tb_str)
        st.error(f"OpenAI API'dan yanıt alınırken hata oluştu: {exc}")
        st.info("Bu hata kayıt altına alındı ve incelenecektir.")
        return ""