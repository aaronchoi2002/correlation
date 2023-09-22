import yfinance as yf
import streamlit as st
import pandas as pd

# 開始 Streamlit 應用
st.title('股票滾動相關性')

# 使用者輸入比較列表和週期
st.sidebar.header('使用者輸入特徵')
default_compare_list = ['AAPL', 'MSFT','CAT']
default_period = 90

user_input_compare_list = st.sidebar.text_input("輸入以逗號 (,) 分隔的股票代號", ','.join(default_compare_list))
user_input_period = st.sidebar.number_input("輸入期間 (以天計)", value=default_period)

compare_list = [symbol.strip().upper() for symbol in user_input_compare_list.split(',')]
period = user_input_period

# 下載數據
df = yf.download(compare_list, start='2020-01-01')['Adj Close']

# 計算滾動相關性
ret_df = df.pct_change()
roll_corr = ret_df.rolling(period).corr()
roll_corr.dropna(inplace=True)

# 選擇要顯示的股票
selected_stock = st.sidebar.selectbox('選擇要顯示的股票', compare_list)

# 建立線圖的DataFrame
chart_data = pd.DataFrame()

# 添加數據到圖表DataFrame
for stock in compare_list:
    if stock != selected_stock:
        chart_data[stock] = roll_corr.unstack()[selected_stock][stock]

# 繪製數據
st.header(f'{selected_stock}的{period}天滾動相關性')
st.line_chart(chart_data)
