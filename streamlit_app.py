import pandas as pd
import streamlit as st

def calculate_profit_from_csv(data):
    # Clean 'Profit' column (remove spaces and commas)
    data['Profit'] = data['Profit'].str.replace(' ', '').str.replace(',', '').astype(float)
    
    # Extract deposits and withdrawals based on 'Comment' column
    deposits = data[(data['Type'] == 'balance') & (data['Comment'].str.contains('Deposit', na=False))]
    withdrawals = data[(data['Type'] == 'balance') & (data['Comment'].str.contains('Withdrawal', na=False))]

    if deposits.empty or withdrawals.empty:
        return {'error': 'No deposits or withdrawals found in the data'}

    # Summing up the 'Profit' column for deposits and withdrawals
    jumlah_awal_deposit = deposits['Profit'].sum()
    total_withdraw = withdrawals['Profit'].sum()

    # Calculate the profit
    profit = total_withdraw - jumlah_awal_deposit

    # Calculate the profit percentage
    profit_percentage = (profit / jumlah_awal_deposit) * 100

    return {
        'jumlah_awal_deposit': jumlah_awal_deposit,
        'total_withdraw': total_withdraw,
        'profit': profit,
        'profit_percentage': profit_percentage
    }

# Streamlit app
st.title('Profit Calculation from CSV')
st.write("Upload your CSV file to calculate the profit")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file, delimiter='\t')
        data.columns = [
            'Time', 'Deal', 'Symbol', 'Type', 'Direction', 'Volume', 'Price', 'Order',
            'Commission', 'Fee', 'Swap', 'Profit', 'Balance', 'Comment'
        ]

        result = calculate_profit_from_csv(data)
        
        if 'error' in result:
            st.error(result['error'])
        else:
            st.success('Calculation successful')
            st.write(f"Initial Deposit: {result['jumlah_awal_deposit']}")
            st.write(f"Total Withdrawals: {result['total_withdraw']}")
            st.write(f"Profit: {result['profit']}")
            st.write(f"Profit Percentage: {result['profit_percentage']}%")
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info('Please upload a CSV file')
