import streamlit as st
from prediction_helper import predict

st.title('Credit Risk Management')


row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

with row1[0]:
    age = st.number_input('Age', min_value=18, max_value=100, step=1)
with row1[1]:
    income = st.number_input('Income', min_value=0, value=1200000)
with row1[2]:
    loan_amt = st.number_input('Loan amount', min_value=0, value=2560000)


with row2[0]:
    loan_to_income_ratio = loan_amt / income if income > 0 else 0
    st.text('Loan to Income Ratio:')
    st.text(f'{loan_to_income_ratio:.2f}')
with row2[1]:
    loan_tenure = st.number_input('Loan Tenure(months)', min_value=0, value=10)
with row2[2]:
    avg_dpd = st.number_input('Avg DPD', min_value=0, value=20)


with row3[0]:
    delinquency_ratio = st.number_input('Delinquency Ratio', min_value=0, value=20)
with row3[1]:
    credit_util_ratio = st.number_input('Credit Utilization Ratio', min_value=0, value=12)
with row3[2]:
    open_account = st.number_input('Open Loan accounts', min_value=0, value=2)


with row3[0]:
    residence_type = st.selectbox('Residence Type',['Owned', 'Rented', 'Mortgage'])
with row3[1]:
    loan_purpose = st.selectbox('Loan Purpose',['Personal', 'Education', 'Auto', 'Home'])
with row3[2]:
    loan_type = st.selectbox('Loan Type',['Unsecured', 'Secured'])


input_data = {
    'Age':age,
    'Income':income,
    'Loan Amount':loan_amt,
    'LTI Ratio':loan_to_income_ratio,
    'Loan Tenure':loan_tenure,
    'Avg DPD':avg_dpd,
    'Delinquency Ratio':delinquency_ratio,
    'Credit Utilization':credit_util_ratio,
    'Open Loan Accounts':open_account,
    'Residence Type':residence_type,
    'Loan Purpose':loan_purpose,
    'Loan Type':loan_type
}

if st.button('Calculate Risk'):
    probability, credit_score, rating = predict(input_data)
    st.write(f'Default Probability: {probability:.2%}')
    st.write(f'Credit Score: {credit_score}')
    st.write(f'Rating: {rating}')