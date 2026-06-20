import streamlit as st
import requests

API_URL = "http://localhost:8000/predict/"

st.set_page_config(page_title="Advertising Sales Forecast", layout="centered")
st.title("Advertising Spend Sales Forecast")

st.markdown(
    "Use the sliders below to adjust TV, Radio, and Digital marketing budgets, then predict expected sales revenue."
)

tv_budget = st.slider("TV Budget", min_value=0.0, max_value=400.0, value=150.0, step=1.0)
radio_budget = st.slider("Radio Budget", min_value=0.0, max_value=100.0, value=30.0, step=1.0)
digital_budget = st.slider("Digital Budget", min_value=0.0, max_value=100.0, value=25.0, step=1.0)

if st.button("Predict Sales"):
    payload = {
        "tv_budget": tv_budget,
        "radio_budget": radio_budget,
        "digital_budget": digital_budget,
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        st.success(f"Predicted Sales: {data['predicted_sales']:.2f}")
    except requests.RequestException as exc:
        st.error(f"Prediction request failed: {exc}")

st.markdown("---")

st.subheader("Budget Breakdown")
st.write(f"- TV: {tv_budget}")
st.write(f"- Radio: {radio_budget}")
st.write(f"- Digital: {digital_budget}")

st.subheader("What-if Scenario Comparison")
scenario_a = {
    'name': st.text_input('Scenario A name', value='Current Budget'),
    'tv': st.number_input('Scenario A TV', value=tv_budget, key='a_tv'),
    'radio': st.number_input('Scenario A Radio', value=radio_budget, key='a_radio'),
    'digital': st.number_input('Scenario A Digital', value=digital_budget, key='a_digital'),
}
scenario_b = {
    'name': st.text_input('Scenario B name', value='Alternative Budget'),
    'tv': st.number_input('Scenario B TV', value=tv_budget, key='b_tv'),
    'radio': st.number_input('Scenario B Radio', value=radio_budget, key='b_radio'),
    'digital': st.number_input('Scenario B Digital', value=digital_budget, key='b_digital'),
}

if st.button('Compare Scenarios'):
    def get_prediction(tv, radio, digital):
        payload = {'tv_budget': tv, 'radio_budget': radio, 'digital_budget': digital}
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()['predicted_sales']

    try:
        sales_a = get_prediction(scenario_a['tv'], scenario_a['radio'], scenario_a['digital'])
        sales_b = get_prediction(scenario_b['tv'], scenario_b['radio'], scenario_b['digital'])
        st.write(f"**{scenario_a['name']} predicted sales:** {sales_a:.2f}")
        st.write(f"**{scenario_b['name']} predicted sales:** {sales_b:.2f}")

        if sales_a > sales_b:
            st.success(f"{scenario_a['name']} performs better by {sales_a - sales_b:.2f} sales units.")
        elif sales_b > sales_a:
            st.success(f"{scenario_b['name']} performs better by {sales_b - sales_a:.2f} sales units.")
        else:
            st.info('Both scenarios forecast the same sales.')
    except requests.RequestException as exc:
        st.error(f"Scenario comparison failed: {exc}")
