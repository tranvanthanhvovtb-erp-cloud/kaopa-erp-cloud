
import os
from pathlib import Path
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(page_title="KaoPa ERP Cloud v2.0", layout="wide")
st.title("KaoPa ERP Cloud v2.0 Starter")
st.caption("Bản khởi tạo cloud: kiểm tra kết nối Supabase/PostgreSQL và tạo bảng dữ liệu.")

def get_database_url():
    try:
        return st.secrets["DATABASE_URL"]
    except Exception:
        return os.getenv("DATABASE_URL", "")

DATABASE_URL = get_database_url()

def get_engine():
    if not DATABASE_URL:
        return None
    return create_engine(DATABASE_URL, pool_pre_ping=True)

def query_df(sql):
    engine = get_engine()
    with engine.begin() as conn:
        return pd.read_sql(text(sql), conn)

tab1, tab2, tab3 = st.tabs(["🔌 Kết nối", "🧱 Tạo bảng", "📊 Kiểm tra dữ liệu"])

with tab1:
    st.subheader("Kiểm tra kết nối")
    if not DATABASE_URL:
        st.error("Chưa cấu hình DATABASE_URL trong Streamlit Secrets.")
        st.code('DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@YOUR_HOST:5432/postgres"', language="toml")
    else:
        st.success("Đã có DATABASE_URL trong cấu hình.")
        if st.button("Kiểm tra kết nối database"):
            try:
                engine = get_engine()
                with engine.begin() as conn:
                    now = conn.execute(text("select now()")).scalar()
                st.success(f"Kết nối thành công: {now}")
            except Exception as e:
                st.error("Kết nối thất bại.")
                st.exception(e)

with tab2:
    st.subheader("Tạo/cập nhật cấu trúc database")
    st.warning("Chỉ bấm sau khi đã cấu hình DATABASE_URL. Lệnh dùng IF NOT EXISTS nên không xóa dữ liệu cũ.")
    if st.button("TẠO BẢNG DATABASE"):
        try:
            sql = Path("schema.sql").read_text(encoding="utf-8")
            engine = get_engine()
            with engine.begin() as conn:
                conn.execute(text(sql))
            st.success("Đã tạo/cập nhật database.")
        except Exception as e:
            st.error("Không tạo được database.")
            st.exception(e)

with tab3:
    st.subheader("Kiểm tra số dòng trong các bảng")
    if st.button("Tải lại"):
        pass
    try:
        df = query_df("""
            select 'employees' as bang, count(*) as so_dong from employees
            union all select 'products', count(*) from products
            union all select 'pn_prices', count(*) from pn_prices
            union all select 'opening_balances', count(*) from opening_balances
            union all select 'sales_reports', count(*) from sales_reports
            order by bang
        """)
        st.dataframe(df, use_container_width=True)
    except Exception:
        st.info("Chưa có bảng hoặc chưa kết nối database.")
