from joblib import load
import pandas as pd
import numpy as np

model_info = load('artifacts/model_info.joblib')

model = model_info['model']
features = model_info['features']
scaler = model_info['scaler']
col_to_scale = ['age', 'income', 'number_of_dependants', 'years_at_current_address',
       'processing_fee', 'gst', 'net_disbursement', 'loan_tenure_months',
       'principal_outstanding', 'bank_balance_at_application',
       'number_of_open_accounts', 'number_of_closed_accounts', 'enquiry_count',
       'credit_utilization_ratio', 'loan_to_income', 'delinquent_ratio',
       'avg_dpd_per_delinquent']


def scaling(df):
    df[['number_of_dependants', 'years_at_current_address',
             'processing_fee', 'gst', 'net_disbursement', 'income',
             'principal_outstanding', 'bank_balance_at_application',
             'number_of_closed_accounts', 'enquiry_count']] = 1
    df[col_to_scale] = scaler.transform(df[col_to_scale])
    return df[features]

def get_credit_score(df, base_score=300, scale_len=600):
    X = np.dot(df.values, model.coef_.T) + model.intercept_   # y = mx + c
    default_prob = 1 / (1+np.exp(-X))
    no_default_prob = 1 - default_prob

    score = base_score + no_default_prob.flatten() * scale_len

    rating = ''
    if 300 <= score < 500:
        rating += 'Poor'
    elif 500 <= score < 650:
        rating += 'Average'
    elif 650 <= score < 750:
        rating += 'Good'
    elif 750 <= score <900:
        rating += 'Excellent'
    else:
        rating += 'Undefined'

    return default_prob.flatten()[0], int(score), rating


def preprocess(data):
    df = pd.DataFrame(0,columns=features,index=[0])
    for key, value in data.items():
        if key == 'Age':
            df['age'] = value
        elif key == 'Loan Tenure':
            df['loan_tenure_months'] = value
        elif key == 'LTI Ratio':
            df['loan_to_income'] = value
        elif key == 'Avg DPD':
            df['avg_dpd_per_delinquent'] = value
        elif key == 'Delinquency Ratio':
            df['delinquent_ratio'] = value
        elif key == 'Credit Utilization':
            df['credit_utilization_ratio'] = value
        elif key == 'Open Loan Accounts':
            df['number_of_open_accounts'] = value
        elif key == 'Residence Type':
            if value == 'Owned':
                df['residence_type_Owned'] = 1
            elif value == 'Rented':
                df['residence_type_Rented'] = 1
        elif key == 'Loan Purpose':
            if value == 'Personal':
                df['loan_purpose_Personal'] = 1
            elif value == 'Education':
                df['loan_purpose_Education'] = 1
            elif value == 'Home':
                df['loan_purpose_Home'] = 1
        elif key == 'Loan Type':
            if value == 'Unsecured':
                df['loan_type_Unsecured'] = 1

    scaled_df = scaling(df)
    return scaled_df


def predict(input_data):
    df = preprocess(input_data)
    probability, credit_score, rating = get_credit_score(df)
    return probability, credit_score, rating
