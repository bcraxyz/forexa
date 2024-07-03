import os, requests
import pandas as pd
import streamlit as st

# Set the page title and get ExchangeRate API key
st.set_page_config(page_title="Currency Converter")
st.subheader("Currency Converter")

exchangerate_api_key = os.environ["EXCHANGERATE_API_KEY"]

# Get the base currency, quote currency and amount from the user
col1, col2 = st.columns(2)
with col1:
    base_currency = st.selectbox("Base Currency", ("SGD", "USD", "EUR"))
with col2:
    base_amount = st.number_input("Amount", value=1.0)

quote_currency = st.multiselect(
    "Quote Currency", 
    ("USD", "EUR", "SGD", "MYR", "THB", "IDR", "INR"), 
    ("MYR", "THB", "IDR", "INR")
    )

# Convert the base amount to the selected currencies
if st.button("Convert"):
    if not exchangerate_api_key.strip():
        st.error("Please provide a valid API key.")
    else:
        try:
            with st.spinner("Please wait..."):
                data = []
                data.append(["Value", "Currency"])
                for currency in quote_currency:
                    url = f"https://v6.exchangerate-api.com/v6/{exchangerate_api_key}/latest/{base_currency}"
                    response = requests.get(url)
                    quote = response.json()

                    # Ensure the API call was successful and the currency is in the response
                    if response.status_code == 200 and "conversion_rates" in quote:
                        rate = quote["conversion_rates"].get(currency)
                        if rate:
                            converted_amount = base_amount * rate
                            data.append([f"{converted_amount:.2f}", currency])
                        else:
                            st.error(f"Currency {currency} not found in conversion rates.")
                    else:
                        st.error(f"Error fetching data: {quote.get('error-type', 'Unknown error')}")
                
                df = pd.DataFrame(data[1:], columns=data[0])
                st.dataframe(df, width=200, hide_index=True)
        except Exception as e:
            st.exception(f"Exception: {e}")
