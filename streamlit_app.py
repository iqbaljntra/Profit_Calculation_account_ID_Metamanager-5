import pandas as pd
import streamlit as st

def calculate_profit_from_csv(data):
    try:
        # Clean 'Profit' column (remove spaces and commas, convert to float)
        data['Profit'] = data['Profit'].str.replace(' ', '').str.replace(',', '').astype(float)
        
        # Extract deposits and withdrawals based on 'Comment' column
        deposits = data[(data['Type'] == 'balance') & (data['Comment'].str.contains('Deposit', na=False))]
        withdrawals = data[(data['Type'] == 'balance') & (data['Comment'].str.contains('Withdrawal', na=False))]

        if deposits.empty or withdrawals.empty:
            return {'error': 'No deposits or withdrawals found in the data'}

        # Summing up the 'Profit' column for deposits and withdrawals
        initial_balance = deposits['Profit'].iloc[0] if not deposits.empty else 0.0
        total_withdrawal = withdrawals['Profit'].sum()

        # Calculate the profit
        profit = total_withdrawal - initial_balance

        # Calculate the profit percentage
        if initial_balance != 0:
            profit_percentage = (profit / initial_balance) * 100
        else:
            profit_percentage = 0.0

        return {
            'initial_balance': initial_balance,
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
        data = pd.read_csv(uploaded_file, delimiter=',')
        
        # Assuming the first row of the CSV file contains the actual column names
        data.columns = data.columns.str.strip()  # Strip any leading/trailing spaces from column names
        data.columns = data.columns.str.replace(' ', '_')  # Replace spaces in column names with underscores
        data.columns = data.columns.str.lower()  # Convert column names to lowercase
        
        result = calculate_profit_from_csv(data)
        
        if 'error' in result:
            st.error(result['error'])
        else:
            st.success('Calculation successful')
            st.write(f"Initial Balance: {result['initial_balance']}")
            st.write(f"Total Withdrawal: {result['total_withdrawal']}")
            st.write(f"Profit: {result['profit']}")
            st.write(f"Profit Percentage: {result['profit_percentage']}%")
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info('Please upload a CSV file')
