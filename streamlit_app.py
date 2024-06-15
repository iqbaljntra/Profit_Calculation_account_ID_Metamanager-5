import pandas as pd
import streamlit as st

def calculate_profit_from_csv(data):
    try:
        # Clean 'Profit' column (remove spaces and commas)
        data['Profit'] = data['Profit'].str.replace(' ', '').str.replace(',', '')
        data['Profit'] = pd.to_numeric(data['Profit'], errors='coerce')  # Convert to numeric, coerce errors to NaN
        
        # Extract deposits and withdrawals based on 'Comment' column
        deposits = data[(data['Type'].str.lower() == 'balance') & (data['Comment'].str.contains('deposit', case=False, na=False))]
        withdrawals = data[(data['Type'].str.lower() == 'balance') & (data['Comment'].str.contains('withdrawal', case=False, na=False))]

        if deposits.empty or withdrawals.empty:
            return {'error': 'No deposits or withdrawals found in the data'}

        # Calculate initial deposit and total withdrawals
        initial_deposit = deposits['Profit'].sum()
        total_withdrawal = withdrawals['Profit'].sum()

        # Calculate profit
        profit = total_withdrawal - initial_deposit

        # Calculate profit percentage
        if initial_deposit != 0:
            profit_percentage = (profit / initial_deposit) * 100
        else:
            profit_percentage = 0.0

        return {
            'initial_deposit': initial_deposit,
            'total_withdrawal': total_withdrawal,
            'profit': profit,
            'profit_percentage': profit_percentage
        }
    except Exception as e:
        return {'error': str(e)}

# Streamlit app
st.title('Profit Calculation from CSV')
st.write("Upload your CSV file to calculate the profit")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        
        # Assuming the first row of the CSV file contains the actual column names
        data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')  # Clean column headers
        
        result = calculate_profit_from_csv(data)
        
        if 'error' in result:
            st.error(result['error'])
        else:
            st.success('Calculation successful')
            st.write(f"Initial Deposit: {result['initial_deposit']}")
            st.write(f"Total Withdrawal: {result['total_withdrawal']}")
            st.write(f"Profit: {result['profit']}")
            st.write(f"Profit Percentage: {result['profit_percentage']}%")
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info('Please upload a CSV file')
