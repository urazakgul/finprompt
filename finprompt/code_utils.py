import re
import ast
import streamlit as st
from finprompt.logger import log_prompt_supabase
import traceback

def clean_code_output(code: str) -> str:
    code = re.sub(r"^```(?:python)?", "", code.strip(), flags=re.IGNORECASE)
    code = re.sub(r"```$", "", code.strip())
    code_lines = code.splitlines()
    clean_lines = [line for line in code_lines if not line.strip().startswith("#")]
    return "\n".join(clean_lines)

def is_valid_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def run_generated_code(code: str, user_prompt: str):
    local_namespace = {}
    try:
        exec(code, globals(), local_namespace)
        if 'df' in local_namespace and hasattr(local_namespace['df'], 'head'):
            st.dataframe(local_namespace['df'])
        else:
            st.info("Oluşturulan kodda 'df' isminde bir DataFrame bulunamadı.")
    except Exception as exc:
        tb_str = traceback.format_exc()
        log_prompt_supabase(user_prompt, error_message=tb_str)
        st.error(f"Kod çalıştırılırken bir hata oluştu:\n\n{exc}")
        st.info("Bu hata kayıt altına alındı ve incelenecektir.")