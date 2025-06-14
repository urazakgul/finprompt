import re
import ast
import streamlit as st

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

def run_generated_code(code: str):
    local_namespace = {}
    try:
        exec(code, globals(), local_namespace)

        if 'df' in local_namespace and hasattr(local_namespace['df'], 'head'):
            st.dataframe(local_namespace['df'])
        else:
            st.info("Oluşturulan kodda 'df' isminde bir DataFrame bulunamadı.")

    except Exception as exc:
        st.error(f"Kod çalıştırılırken bir hata oluştu:\n\n{exc}")