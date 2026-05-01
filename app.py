import streamlit as st
import pickle
import pandas as pd


model = pickle.load(open("churn_model.pkl", "rb"))


st.title("Customer Churn Prediction App")
st.markdown("### Enter customer details")


st.sidebar.title("About")
st.sidebar.info("Predict customer churn using Machine Learning")


tenure = st.number_input("Tenure (months)", 0, 72, 12)
monthly_charges = st.number_input("Monthly Charges", 0.0, 200.0, 50.0)

gender = st.selectbox("Gender", ["Male", "Female"])
contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
payment = st.selectbox(
    "Payment Method",
    ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
)


if st.button("Predict"):

   
    columns = model.feature_names_in_

  
    input_df = pd.DataFrame(columns=columns)
    input_df.loc[0] = 0

    
    if 'tenure' in input_df.columns:
        input_df['tenure'] = tenure

    if 'MonthlyCharges' in input_df.columns:
        input_df['MonthlyCharges'] = monthly_charges

    
    def safe_set(col):
        if col in input_df.columns:
            input_df[col] = 1


    safe_set(f'gender_{gender}')
    safe_set(f'Contract_{contract}')
    safe_set(f'InternetService_{internet}')
    safe_set(f'PaymentMethod_{payment}')

   
    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df)

   
    if prediction[0] == 1 or prediction[0] == "Yes":
        st.error("⚠️ Customer is likely to churn")
    else:
        st.success("✅ Customer will stay")

   
    st.write("### 📊 Prediction Probability")
    st.write("Churn Probability:", round(probability[0][1] * 100, 2), "%")