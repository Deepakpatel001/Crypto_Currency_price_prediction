import streamlit as st
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Crypto Currency Prediction",page_icon = ":chart_with_upwards_trend",layout="wide")
st.title(" :chart_with_upwards_trend: Crypto Currency Prediction")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# browsering the files ----------------------------------------------
# f1 = st.file_uploader(":file folder: Upload a file",type = (["csv","xlsx","txt","xls"]))
# if f1 is not None:
#     filename = f1.name
#     st.write(filename)
#     df = pd.read_csv(filename)
# else:
#     df = pd.read_csv("Gemini_BTCUSD_1h.csv",skiprows=1)
# ---------------------------------------------------------------------------------------

df1 = pd.read_csv(".\Dataset\Gemini_BTCUSD_1h.csv",skiprows=1)
df2 = pd.read_csv(".\Dataset\Gemini_ETHUSD_1h.csv",skiprows=1)
df3 = pd.read_csv(".\Dataset\Gemini_DOGEUSD_1h.csv",skiprows=1)
df4 = pd.read_csv(".\Dataset\Gemini_LTCUSD_1h.csv",skiprows=1)


# col1,col2 = st.columns((2))
# df["date"] = pd.to_datetime(df["date"])
# # #Getting min and max date
# startDate = pd.to_datetime(df["date"]).min()
# endDate = pd.to_datetime(df["date"]).max()

# with col1:
#     date1 = pd.to_datetime(st.date_input("Start Date",startDate))
# with col2:
#     date2 = pd.to_datetime(st.date_input("End Date",endDate))
# -------------------------------------------------------------------------

col1, col2= st.columns([2, 2])
data = np.random.randn(5, 5)

col1.subheader("Gemini Bitcoin Coin ")
col1.line_chart(data=df1,x='date',y='close',width=200, height=500)
col2.subheader("Gemini Bitcoin Coin ")
col2.line_chart(data=df2,x='date',y='close',width=200, height=500)

col3, col4= st.columns([2, 2])
data = np.random.randn(5, 5)

col3.subheader("Gemini Bitcoin Coin ")
col3.line_chart(data=df3,x='date',y='close',width=200, height=500)
col4.subheader("Gemini Bitcoin Coin ")
col4.line_chart(data=df4,x='date',y='close',width=200, height=500)


# col3.subheader("Gemini Bitcoin Coin ")
# col3.line_chart(data=df3,x='date',y='close',width=200, height=500)
# col4.subheader("Gemini Bitcoin Coin ")
# col4.line_chart(data=df4,x='date',y='close',width=200, height=500)
# single line chart -------------------------------------------------------------------
# df_new = df[['close','date']]
# chart_data = df_new
# st.line_chart(data=df_new,x='date',y='close')
# -------------------------------------------------------------------------------

# col1,col2 = st.columns((2))
# df["time"] = pd.to_datetime(df["time"])
#
# #Getting min and max date
# startDate = pd.to_datetime(df["time"]).min()
# endDate = pd.to_datetime(df["time"]).max()
#
# with col1:
#     date1 = pd.to_datetime(st.date_input("Start Date",startDate))
# with col2:
#     date2 = pd.to_datetime(st.date_input("End Date",endDate))
#
# df_new = df[['close','date']]
#
# chart_data = df_new
# st.line_chart(data = df_new,x='date',y'close')

#Extra Code ------------------------------------

# chart_data = pd.DataFrame(
#     np.random.randn(20, 2),
#     columns=['time', 'date'])

# st.line_chart(chart_data,use_container_width=True)
# ------------------------------------------------------
# list_of_df = [df1,df2,df3,df4]
# for i in list_of_df:
#     df_new = i[['close', 'date']]
#     chart_data = df_new
#     st.line_chart(data=df_new,x='date',y='close',width=100, height=600)
#--------------------------------------------------------
