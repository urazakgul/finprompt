from supabase import create_client
import streamlit as st

def get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def log_prompt_supabase(user_prompt, error_message=None):
    supabase = get_supabase_client()
    data = {
        "user_prompt": user_prompt,
        "error_message": error_message or ""
    }
    try:
        supabase.table("prompt_logs").insert(data).execute()
    except Exception as e:
        st.warning(f"Prompt loglanamadı: {e}")