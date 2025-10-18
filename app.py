from pathlib import Path
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Demo", layout="wide")
st.title("Hello, Streamlit Cloud 👋")

@st.cache_data
def load_data():
    p = Path(__file__).parent / "data" / "demo.csv"
    if p.exists():
        return pd.read_csv(p)
    return pd.DataFrame({"x":[1,2,3], "y":[1,4,9]})

df = load_data()
st.line_chart(df.set_index("x"))

if "db" in st.secrets:
    st.success("Secrets found and loaded.")
else:
    st.info("No secrets configured (that’s fine if you don’t need them).")
