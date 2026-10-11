import os
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

def get_api_url():
    try:
        return st.secrets["API_URL"]
    except Exception:
        return os.getenv("API_URL", "http://127.0.0.1:8000")


API = get_api_url().rstrip("/")

st.set_page_config(page_title="ShopSense Admin", layout="wide")
st.title("ShopSense Admin - Marketplace Foundation")

page = st.sidebar.radio("Menu", ["Dashboard", "Vendors", "Products", "Transactions"])


def get(path):
    try:
        return requests.get(f"{API}{path}", timeout=10).json()
    except Exception:
        st.error("Cannot reach the API. Start it with: uvicorn app.main:app --reload")
        st.stop()


if page == "Dashboard":
    st.header("Dashboard")
    s = get("/analytics/summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"₹{s['total_revenue']:,.2f}")
    c2.metric("Transactions", s["total_transactions"])
    c3.metric("Units Sold", s["total_units_sold"])
    c4.metric("Vendors", s["total_vendors"])

    left, right = st.columns(2)
    rv = pd.DataFrame(get("/analytics/revenue-by-vendor"))
    if not rv.empty:
        left.plotly_chart(px.bar(rv, x="vendor", y="revenue",
                                 title="Revenue by Vendor"),
                          use_container_width=True)
    tp = pd.DataFrame(get("/analytics/top-products"))
    if not tp.empty:
        right.plotly_chart(px.bar(tp, x="product", y="revenue",
                                  title="Top Products by Revenue"),
                           use_container_width=True)
    dr = pd.DataFrame(get("/analytics/daily-revenue"))
    if not dr.empty:
        st.plotly_chart(px.line(dr, x="date", y="revenue",
                                title="Daily Revenue Trend"),
                        use_container_width=True)

    with st.expander("Transaction consistency check"):
        st.json(get("/analytics/consistency"))

elif page == "Vendors":
    st.header("Vendor Onboarding")
    with st.form("vendor_form"):
        name = st.text_input("Business Name")
        email = st.text_input("Contact Email")
        submitted = st.form_submit_button("Submit")
    if submitted:
        r = requests.post(f"{API}/vendors/",
                          json={"business_name": name, "email": email})
        if r.status_code == 201:
            st.success("Vendor registered (Pending approval)")
        else:
            st.error(r.json().get("detail", "Validation failed"))

    vendors = pd.DataFrame(get("/vendors/"))
    if not vendors.empty:
        st.dataframe(
            vendors[["vendor_id", "business_name", "email", "status"]]
            .rename(columns={"vendor_id": "Vendor ID",
                             "status": "Status (Pending)"}),
            use_container_width=True, hide_index=True)

elif page == "Products":
    st.header("Products")
    products = pd.DataFrame(get("/products/"))
    st.dataframe(products, use_container_width=True, hide_index=True)

else:
    st.header("Transactions")
    tx = pd.DataFrame(get("/transactions/"))
    st.dataframe(tx, use_container_width=True, hide_index=True)