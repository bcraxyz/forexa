import pandas as pd
import streamlit as st
from forex_python.converter import CurrencyRates

# Initialize the CurrencyRates object
c = CurrencyRates()

# Set the page title
st.set_page_config(page_title="Currency Converter")
st.subheader("Currency Converter")

# Get the base currency, quote currency and amount from the user
col1, col2 = st.columns(2)
with col1:
    base_currency = st.selectbox("Base Currency", ("USD", "EUR", "SGD"))
with col2:
    base_amount = st.number_input("Amount", value=1.0)

quote_currency = st.multiselect(
    "Quote Currency", 
    ("USD", "EUR", "SGD", "MYR", "THB", "IDR", "INR"), 
    ("SGD", "MYR", "IDR", "INR")
    )

# Convert the base amount to the selected currencies
if st.button("Convert"):
    try:
        with st.spinner("Please wait..."):
            data = []
            data.append(["Value", "Currency"])
            for currency in quote_currency:
                rate = c.get_rate(base_currency, currency)
                converted_amount = base_amount * rate
                data.append([f"{converted_amount:.2f}", currency])
            
            df = pd.DataFrame(data[1:], columns=data[0])
            st.dataframe(df, width=200, hide_index=True)
    except Exception as e:
        st.exception(f"Exception: {e}")
