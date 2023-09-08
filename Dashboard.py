import streamlit as st
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import streamlit.components.v1 as components



st.set_page_config(page_title="Crypto Currency Prediction",page_icon = ":chart_with_upwards_trend",layout="wide")
st.title(" :chart_with_upwards_trend: Crypto Currency Prediction")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
components.html(
    """
    <script src="https://public.bnbstatic.com/unpkg/growth-widget/cryptoCurrencyWidget@0.0.9.min.js" ></script><div class="binance-widget-marquee" data-cmc-ids="1,1027,1839,52,3408,74,5426,3890,5805,7083" data-theme="dark" data-transparent="true" data-locale="en" data-powered-by="Powered by" data-disclaimer="Disclaimer" ></div>
    
    """
)

def eda(coin):
    df = pd.read_csv(f'.//Dataset//Gemini_{coin}_1h.csv', skiprows=1)
    # df = df1
    df = df.iloc[::-1].reset_index()
    df1 = pd.read_csv(f".//Dataset//day_wise//Gemini_{coin}_d.csv", skiprows=1)
    df1 = df1.iloc[::-1].reset_index()
    st.header("All time: ")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("All time High Close Price: ")
        col4,col5 = st.columns(2)

        # st.write(df[df.close == df.close.max()],"max")
        all_high = df[df.close == df.close.max()]['close'].values[0]
        all_high_date = df[df.close == df.close.max()]['date'].values[0]
        with col4:
            st.write("$ "+ str(all_high))
        with col5:
            st.write("Date: "+ str(all_high_date))
    with col2:
        st.subheader("All time Low Close Price: ")
        col4, col5 = st.columns(2)
        # st.write(df[df.close == df.close.min()],"min")
        all_low = df[df.close == df.close.min()]['close'].values[0]
        all_low_date = df[df.close == df.close.min()]['date'].values[0]
        with col4:
            st.write("$ " + str(all_low))
        with col5:
            st.write("Date: " + str(all_low_date))
    # df = pd.to_datetime(df['date'])
    df1['date'] = pd.to_datetime(df1['date'])
    st.line_chart(data=df1, x="date", y="close")


    st.markdown("""---""")
    # ----------------------------------------------------------------------

    st.header("7 Days : ")
    last7 = df.tail(7*24)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("High Close Price: ")
        col4,col5 = st.columns(2)

        # st.write(df[df.close == df.close.max()],"max")
        days60_high = last7[last7.close == last7.close.max()]['close'].values[0]
        days60_high_date = last7[last7.close == last7.close.max()]['date'].values[0]
        with col4:
            st.write("$ "+ str(days60_high))
        with col5:
            st.write("Date: "+ str(days60_high_date))
    with col2:
        st.subheader("Low Close Price: ")
        col4, col5 = st.columns(2)
        # st.write(df[df.close == df.close.min()],"min")
        all_low = last7[last7.close == last7.close.min()]['close'].values[0]
        all_low_date = last7[last7.close == last7.close.min()]['date'].values[0]
        with col4:
            st.write("$ "+ str(all_low))
        with col5:
            st.write("Date: "+ str(all_low_date))

    # display plot
    last7["Date1"] = pd.to_datetime(last7['date']).dt.date
    st.line_chart(data=last7, x="Date1", y="close")
    # ----------------------------------------------------------------------



    st.markdown("""---""")
    # ----------------------------------------------------------------------

    st.header("30 Days : ")
    last30 = df.tail(30*24)
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("High Close Price: ")
        col4,col5 = st.columns(2)

        # st.write(df[df.close == df.close.max()],"max")
        days30_high = last30[last30.close == last30.close.max()]['close'].values[0]
        days30_high_date = last30[last30.close == last30.close.max()]['date'].values[0]
        with col4:
            st.write("$ "+ str(days30_high))
        with col5:
            st.write("Date: "+ str(days30_high_date))
    with col2:
        st.subheader("Low Close Price: ")
        col4, col5 = st.columns(2)
        # st.write(df[df.close == df.close.min()],"min")
        all_low = last30[last30.close == last30.close.min()]['close'].values[0]
        all_low_date = last30[last30.close == last30.close.min()]['date'].values[0]
        with col4:
            st.write("$ "+ str(all_low))
        with col5:
            st.write("Date: "+ str(all_low_date))


    # display plot
    last30['date'] = pd.to_datetime(last30['date'])
    st.line_chart(data=last30, x="date", y="close")
    # ----------------------------------------------------------------------


    st.markdown("""---""")
    # ----------------------------------------------------------------------

    st.header("60 Days : ")
    last60 = df.tail(60*24)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("High Close Price: ")
        col4,col5 = st.columns(2)

        # st.write(df[df.close == df.close.max()],"max")
        days60_high = last60[last60.close == last60.close.max()]['close'].values[0]
        days60_high_date = last60[last60.close == last60.close.max()]['date'].values[0]
        with col4:
            st.write("$ "+ str(days60_high))
        with col5:
            st.write("Date: "+ str(days60_high_date))
    with col2:
        st.subheader("Low Close Price: ")
        col4, col5 = st.columns(2)
        # st.write(df[df.close == df.close.min()],"min")
        days60_low = last60[last60.close == last60.close.min()]['close'].values[0]
        days60_low_date = last60[last60.close == last60.close.min()]['date'].values[0]
        with col4:
            st.write("$ "+ str(days60_low))
        with col5:
            st.write("Date: "+ str(days60_low_date))


    # display plot
    last60['date'] = pd.to_datetime(last60['date'])
    st.line_chart(data=last60, x="date", y="close")
    # ----------------------------------------------------------------------





col1, col2, col3 = st.columns(3)
with col1:
    option = st.selectbox(
        'Select the type of the coin',
        ('BTCUSD', 'ETHUSD', 'DOGEUSD', 'LTCUSD'))

if st.button("Analyse "):
    if option == "BTCUSD":
        eda(option)
    elif option == "ETHUSD":
        eda(option)
    elif option == "DOGEUSD":
        eda(option)
    elif option == "LTCUSD":
        eda(option)





df1 = pd.read_csv(".//Dataset//day_wise//Gemini_BTCUSD_d.csv", skiprows=1)
df2 = pd.read_csv(".//Dataset//day_wise//Gemini_ETHUSD_d.csv", skiprows=1)
df3 = pd.read_csv(".//Dataset//day_wise//Gemini_DOGEUSD_d.csv", skiprows=1)
df4 = pd.read_csv(".//Dataset//day_wise//Gemini_LTCUSD_d.csv", skiprows=1)

# get latest data
# ---------------------------------------------------------------
BTC_close = df1.head(1)['close']
ETH_close = df2.head(1)['close']
DOGE_close = df3.head(1)['close']
LTC_close = df4.head(1)['close']
# ---------------------------------------------------------------


df=pd.read_csv('.//Dataset//Gemini_BTCUSD_1h.csv',skiprows=1)
# df = df1
df=df.iloc[::-1].reset_index()

# df=df[['date', 'close']]
st.markdown("""---""")



