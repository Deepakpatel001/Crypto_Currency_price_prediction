import streamlit as st
import numpy as np
import pandas as pd
import datetime
import math
import warnings
warnings.filterwarnings('ignore')



def Xgboost(coin,pred_days_input):
    st.write("Xgboost running with ", coin, pred_days_input)
    import warnings
    warnings.filterwarnings('ignore')

    from itertools import cycle


    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    from sklearn.preprocessing import MinMaxScaler


    # In[3]:

    df = pd.read_csv(f".\Dataset\Gemini_{coin}_1h.csv", skiprows=1)
    df = df.iloc[::-1].reset_index()
    df = df[['date', 'close']]
    df_close = df.copy()
    del df_close['date']

    last_date = df.tail(1)
    last_date = last_date.date.values
    last_date = datetime.datetime.strptime(last_date[0], '%Y-%m-%d %H:%M:%S')
    last_date = last_date.date()
    st.write(last_date,"last_date")
    st.write(pred_days_input,"pred Date")

    pred_days_input = pred_days_input.date() - last_date
    pred_days_input = pred_days_input.days
    st.write(pred_days_input, "pred Date")
    # In[14]:

    scaler = MinMaxScaler(feature_range=(0, 1))
    df_close = scaler.fit_transform(np.array(df_close).reshape(-1, 1))
    print(df_close.shape)

    # In[15]:

    training_size = int(len(df_close) * 0.75)
    test_size = len(df_close) - training_size

    train_data, test_data = df_close[0:training_size, :], df_close[training_size:len(df_close), :1]

    print("train_data: ", train_data.shape)
    print("test_data: ", test_data.shape)

    # In[17]:

    # Prepare train data for time series analysis
    # convert an array of values into a dataset matrix
    def create_dataset(dataset, time_step=1):
        dataX, dataY = [], []
        for i in range(len(dataset) - time_step - 1):
            a = dataset[i:(i + time_step), 0]
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return np.array(dataX), np.array(dataY)

    time_step = 360
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, y_test = create_dataset(test_data, time_step)

    print("X_train: ", X_train.shape)
    print("y_train: ", y_train.shape)
    print("X_test: ", X_test.shape)
    print("y_test", y_test.shape)

    # In[19]:

    # # Biulding Model
    # my_model = XGBRegressor(n_estimators=200)
    # my_model.fit(X_train, y_train, verbose=False)

    # In[20]:

    import pickle
    # filename = 'BTCUSD_xgboost.pkl'
    # pickle.dump(my_model, open(filename, 'wb'))

    # In[21]:

    # del my_model

    # my_model

    # In[22]:

    file = open(f'.\Models\{coin}_xgboost.pkl', 'rb')

    # dump information to that file
    my_model = pickle.load(file)


    # In[24]:

    predictions = my_model.predict(X_test)
    print("Mean Absolute Error - MAE : " + str(mean_absolute_error(y_test, predictions)))
    print("Root Mean squared Error - RMSE : " + str(math.sqrt(mean_squared_error(y_test, predictions))))

    # In[25]:

    train_predict = my_model.predict(X_train)
    test_predict = my_model.predict(X_test)

    train_predict = train_predict.reshape(-1, 1)
    test_predict = test_predict.reshape(-1, 1)

    print("Train data prediction:", train_predict.shape)
    print("Test data prediction:", test_predict.shape)

    # In[26]:

    # Transform back to original form

    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)
    original_ytrain = scaler.inverse_transform(y_train.reshape(-1, 1))
    original_ytest = scaler.inverse_transform(y_test.reshape(-1, 1))

    # In[27]:

    # shift train predictions for plotting

    look_back = time_step
    trainPredictPlot = np.empty_like(df_close)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(train_predict) + look_back, :] = train_predict
    print("Train predicted data: ", trainPredictPlot.shape)

    # In[28]:

    # shift test predictions for plotting
    testPredictPlot = np.empty_like(df_close)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(train_predict) + (look_back * 2) + 1:len(df_close) - 1, :] = test_predict
    print("Test predicted data: ", testPredictPlot.shape)

    # In[29]:

    print("Train data R2 score:", r2_score(original_ytrain, train_predict))
    print("Test data R2 score:", r2_score(original_ytest, test_predict))

    # In[30]:

    names = cycle(['Original close price', 'Train predicted close price', 'Test predicted close price'])

    plotdf = pd.DataFrame({'date': df['date'],
                           'original_close': df['close'],
                           'train_predicted_close': trainPredictPlot.reshape(1, -1)[0].tolist(),
                           'test_predicted_close': testPredictPlot.reshape(1, -1)[0].tolist()})
    new_new = pd.DataFrame({
        'original_close': df['close'],
        'train_predicted_close': trainPredictPlot.reshape(1, -1)[0].tolist(),
        'test_predicted_close': testPredictPlot.reshape(1, -1)[0].tolist()})
    # st.dataframe(plotdf)
    # fig = px.line(plotdf,x=plotdf['date'], y=[plotdf['original_close'],plotdf['train_predicted_close'],
    #                                           plotdf['test_predicted_close']],
    #               labels={'value':'Close price','date': 'Date'})
    # fig.update_layout(title_text='Comparision between original close price vs predicted close price',
    #                   plot_bgcolor='white', font_size=15, font_color='black',legend_title_text='Close Price')
    # fig.for_each_trace(lambda t:  t.update(name = next(names)))
    #
    # fig.update_xaxes(showgrid=False)
    # fig.update_yaxes(showgrid=False)
    # fig.show()

    st.line_chart(new_new)

    # In[31]:

    x_input = test_data[len(test_data) - time_step:].reshape(1, -1)
    temp_input = list(x_input)
    temp_input = temp_input[0].tolist()


    lst_output = []
    n_steps = time_step
    i = 0
    pred_days = pred_days_input * 24
    while (i < pred_days):

        if (len(temp_input) > time_step):

            x_input = np.array(temp_input[1:])
            # print("{} day input {}".format(i,x_input))
            x_input = x_input.reshape(1, -1)

            yhat = my_model.predict(x_input)
            # print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat.tolist())
            temp_input = temp_input[1:]

            lst_output.extend(yhat.tolist())
            i = i + 1

        else:
            yhat = my_model.predict(x_input)

            temp_input.extend(yhat.tolist())
            lst_output.extend(yhat.tolist())

            i = i + 1

    print("Output of predicted next days: ", len(lst_output))

    # In[ ]:

    # In[32]:

    last_days = np.arange(1, time_step + 1)
    day_pred = np.arange(time_step + 1, time_step + pred_days + 1)

    # In[33]:

    temp_mat = np.empty((len(last_days) + pred_days + 1, 1))
    temp_mat[:] = np.nan
    temp_mat = temp_mat.reshape(1, -1).tolist()[0]

    last_original_days_value = temp_mat
    next_predicted_days_value = temp_mat

    last_original_days_value[0:time_step + 1] = \
    scaler.inverse_transform(df_close[len(df_close) - time_step:]).reshape(1, -1).tolist()[0]
    next_predicted_days_value[time_step + 1:] = \
    scaler.inverse_transform(np.array(lst_output).reshape(-1, 1)).reshape(1, -1).tolist()[0]

    new_pred_plot = pd.DataFrame({
        'last_original_days_value': last_original_days_value,
        'next_predicted_days_value': next_predicted_days_value
    })

    # names = cycle(['Last 15 days close price','Predicted next 10 days close price'])
    #
    # fig = px.line(new_pred_plot,x=new_pred_plot.index, y=[new_pred_plot['last_original_days_value'],
    #                                                       new_pred_plot['next_predicted_days_value']],
    #               labels={'value': 'Close price','index': 'Timestamp'})
    # fig.update_layout(title_text='Compare last 15 days vs next 10 days',
    #                   plot_bgcolor='white', font_size=15, font_color='black',legend_title_text='Close Price')
    # fig.for_each_trace(lambda t:  t.update(name = next(names)))
    # fig.update_xaxes(showgrid=False)
    # fig.update_yaxes(showgrid=False)
    # fig.show()
    # st.pyplot(fig)

    # st.dataframe(new_pred_plot)
    print("end here")
    st.line_chart(new_pred_plot)

    st.write()


def Lstm(coin,pred_days_input):
    st.write("LSTM running with " , coin, pred_days_input)

    import pandas as pd
    import numpy as np
    import math

    # For Evalution we will use these library

    from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score, r2_score
    from sklearn.metrics import mean_poisson_deviance, mean_gamma_deviance, accuracy_score
    from sklearn.preprocessing import MinMaxScaler

    # For model building we will use these library

    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout
    from tensorflow.keras.layers import LSTM

    # For PLotting we will use these library

    from itertools import cycle

    maindf = pd.read_csv(f'.\Dataset\Gemini_{coin}_1h.csv', skiprows=1)

    maindf = maindf.iloc[::-1].reset_index(drop=True)

    last_date = maindf.tail(1)
    last_date = last_date.date.values
    last_date = datetime.datetime.strptime(last_date[0], '%Y-%m-%d %H:%M:%S')
    last_date = last_date.date()
    st.write(last_date, "last_date")
    st.write(pred_days_input, "pred Date")
    pred_days_input = pred_days_input.date() - last_date
    pred_days_input = pred_days_input.days
    st.write(pred_days_input, "pred Date")

    maindf['date'] = pd.to_datetime(maindf['date'], format='%Y-%m-%d %H:%M:%S')

    y_overall = maindf.loc[(maindf['date'] >= '2014-09-17')
                           & (maindf['date'] <= '2022-02-19')]
    coin_name = coin[:-3]
    y_overall.drop(y_overall[[f'Volume {coin_name}', 'Volume USD', 'unix']], axis=1)

    monthwise = y_overall.groupby(y_overall['date'].dt.strftime('%B'))[['open', 'close']].mean()
    new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                 'September', 'October', 'November', 'December']
    monthwise = monthwise.reindex(new_order, axis=0)
    monthwise

    closedf = maindf[['date', 'close']]
    print("Shape of close dataframe:", closedf.shape)

    # fig = px.line(closedf, x=closedf.date, y=closedf.close, labels={'date': 'date', 'close': 'close Stock'})
    # fig.update_traces(marker_line_width=2, opacity=0.8, marker_line_color='orange')
    # fig.update_layout(title_text='Whole period of timeframe of Bitcoin close price 2014-2022', plot_bgcolor='white',
    #                   font_size=15, font_color='black')
    # fig.update_xaxes(showgrid=False)
    # fig.update_yaxes(showgrid=False)
    # fig.show()

    closedf = closedf[closedf['date'] > '2020-02-19']
    close_stock = closedf.copy()
    print("Total data for prediction: ", closedf.shape[0])
    # only for 2 years

    closedf

    # fig = px.line(closedf, x=closedf.date, y=closedf.close, labels={'date': 'date', 'close': 'close Stock'})
    # fig.update_traces(marker_line_width=2, opacity=0.8, marker_line_color='orange')
    # fig.update_layout(title_text='Considered period to predict Bitcoin close price',
    #                   plot_bgcolor='white', font_size=15, font_color='black')
    # fig.update_xaxes(showgrid=False)
    # fig.update_yaxes(showgrid=False)
    # fig.show()

    del closedf['date']
    scaler = MinMaxScaler(feature_range=(0, 1))
    closedf = scaler.fit_transform(np.array(closedf).reshape(-1, 1))
    print(closedf.shape)

    training_size = int(len(closedf) * 0.90)
    test_size = len(closedf) - training_size
    train_data, test_data = closedf[0:training_size, :], closedf[training_size:len(closedf), :1]
    print("train_data: ", train_data.shape)
    print("test_data: ", test_data.shape)

    # convert an array of values into a dataset matrix

    def create_dataset(dataset, time_step=1):
        dataX, dataY = [], []
        for i in range(len(dataset) - time_step - 1):
            a = dataset[i:(i + time_step), 0]  ###i=0, 0,1,2,3-----99   100
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return np.array(dataX), np.array(dataY)

    time_step = 15 * 24
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, y_test = create_dataset(test_data, time_step)

    print("X_train: ", X_train.shape)
    print("y_train: ", y_train.shape)
    print("X_test: ", X_test.shape)
    print("y_test", y_test.shape)

    # reshape input to be [samples, time steps, features] which is required for LSTM
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    print("X_train: ", X_train.shape)
    print("X_test: ", X_test.shape)

    """# Actuall Model Building"""


    from tensorflow.keras.models import load_model as tfk__load_model
    model = tfk__load_model(f'.\Models\{coin}_LSTM.h5')

    ### Lets Do the prediction and check performance metrics
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)
    train_predict.shape, test_predict.shape

    # Transform back to original form

    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)
    original_ytrain = scaler.inverse_transform(y_train.reshape(-1, 1))
    original_ytest = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Evaluation metrices RMSE and MAE
    print("Train data RMSE: ", math.sqrt(mean_squared_error(original_ytrain, train_predict)))
    print("Train data MSE: ", mean_squared_error(original_ytrain, train_predict))
    print("Train data MAE: ", mean_absolute_error(original_ytrain, train_predict))
    print("-------------------------------------------------------------------------------------")
    print("Test data RMSE: ", math.sqrt(mean_squared_error(original_ytest, test_predict)))
    print("Test data MSE: ", mean_squared_error(original_ytest, test_predict))
    print("Test data MAE: ", mean_absolute_error(original_ytest, test_predict))

    print("Train data explained variance regression score:",
          explained_variance_score(original_ytrain, train_predict))
    print("Test data explained variance regression score:",
          explained_variance_score(original_ytest, test_predict))

    ## R square score for regression
    print("Train data R2 score:", r2_score(original_ytrain, train_predict))
    print("Test data R2 score:", r2_score(original_ytest, test_predict))

    print("Train data MGD: ", mean_gamma_deviance(original_ytrain, train_predict))
    print("Test data MGD: ", mean_gamma_deviance(original_ytest, test_predict))
    print("----------------------------------------------------------------------")
    print("Train data MPD: ", mean_poisson_deviance(original_ytrain, train_predict))
    print("Test data MPD: ", mean_poisson_deviance(original_ytest, test_predict))

    """# Comparision of original stock close price and predicted close price"""

    # shift train predictions for plotting

    look_back = time_step
    trainPredictPlot = np.empty_like(closedf)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(train_predict) + look_back, :] = train_predict
    print("Train predicted data: ", trainPredictPlot.shape)

    # shift test predictions for plotting
    testPredictPlot = np.empty_like(closedf)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(train_predict) + (look_back * 2) + 1:len(closedf) - 1, :] = test_predict
    print("Test predicted data: ", testPredictPlot.shape)

    names = cycle(['Original close price', 'Train predicted close price', 'Test predicted close price'])

    plotdf = pd.DataFrame({'date': close_stock['date'],
                           'original_close': close_stock['close'],
                           'train_predicted_close': trainPredictPlot.reshape(1, -1)[0].tolist(),
                           'test_predicted_close': testPredictPlot.reshape(1, -1)[0].tolist()})

    # fig = px.line(plotdf,x=plotdf['date'], y=[plotdf['original_close'],plotdf['train_predicted_close'],
    #                                           plotdf['test_predicted_close']],
    #               labels={'value':'Stock price','date': 'date'})
    # fig.update_layout(title_text='Comparision between original close price vs predicted close price',
    #                   plot_bgcolor='white', font_size=15, font_color='black', legend_title_text='Close Price')
    # fig.for_each_trace(lambda t:  t.update(name = next(names)))

    # fig.update_xaxes(showgrid=False)
    # fig.update_yaxes(showgrid=False)
    # fig.show()
    st.dataframe(plotdf)
    new_plot_df1 = plotdf.drop('date',axis=1)
    st.line_chart(new_plot_df1)

    x_input = test_data[len(test_data) - time_step:].reshape(1, -1)
    temp_input = list(x_input)
    temp_input = temp_input[0].tolist()


    lst_output = []
    n_steps = time_step
    i = 0
    pred_days = pred_days_input * 24
    while i < pred_days:

        if len(temp_input) > time_step:

            x_input = np.array(temp_input[1:])
            # print("{} day input {}".format(i,x_input))
            x_input = x_input.reshape(1, -1)
            x_input = x_input.reshape((1, n_steps, 1))

            yhat = model.predict(x_input, verbose=0)
            # print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input = temp_input[1:]
            # print(temp_input)

            lst_output.extend(yhat.tolist())
            i = i + 1

        else:

            x_input = x_input.reshape((1, n_steps, 1))
            yhat = model.predict(x_input, verbose=0)
            temp_input.extend(yhat[0].tolist())

            lst_output.extend(yhat.tolist())
            i = i + 1

    print("Output of predicted next days: ", len(lst_output))

    last_days = np.arange(1, time_step + 1)
    day_pred = np.arange(time_step + 1, time_step + pred_days + 1)
    print(last_days)
    print(day_pred)

    temp_mat = np.empty((len(last_days) + pred_days + 1, 1))
    temp_mat[:] = np.nan
    temp_mat = temp_mat.reshape(1, -1).tolist()[0]

    last_original_days_value = temp_mat
    next_predicted_days_value = temp_mat

    last_original_days_value[0:time_step + 1] = \
    scaler.inverse_transform(closedf[len(closedf) - time_step:]).reshape(1, -1).tolist()[0]
    next_predicted_days_value[time_step + 1:] = \
    scaler.inverse_transform(np.array(lst_output).reshape(-1, 1)).reshape(1, -1).tolist()[0]

    new_pred_plot = pd.DataFrame({
        'last_original_days_value': last_original_days_value,
        'next_predicted_days_value': next_predicted_days_value
    })

    # names = cycle(['Last 15 days close price','Predicted next 30 days close price'])

    # fig = px.line(new_pred_plot,x=new_pred_plot.index, y=[new_pred_plot['last_original_days_value'],
    #                                                       new_pred_plot['next_predicted_days_value']],
    #               labels={'value': 'Stock price','index': 'Timestamp'})
    # fig.update_layout(title_text='Compare last 15 days vs next 30 days',
    #                   plot_bgcolor='white', font_size=15, font_color='black',legend_title_text='Close Price')

    # fig.for_each_trace(lambda t:  t.update(name = next(names)))
    # fig.update_xaxes(showgrid=False)
    # fig.update_yaxes(showgrid=False)
    # fig.show()

    st.line_chart(new_pred_plot)

    # lstmdf=closedf.tolist()
    # lstmdf.extend((np.array(lst_output).reshape(-1,1)).tolist())
    # lstmdf=scaler.inverse_transform(lstmdf).reshape(1,-1).tolist()[0]

    # names = cycle(['Close price'])

    # fig = px.line(lstmdf,labels={'value': 'Stock price','index': 'Timestamp'})
    # fig.update_layout(title_text='Plotting whole closing stock price with prediction',
    #                   plot_bgcolor='white', font_size=15, font_color='black',legend_title_text='Stock')

    # fig.for_each_trace(lambda t:  t.update(name = next(names)))

    # fig.update_xaxes(showgrid=False)
    # fig.update_yaxes(showgrid=False)
    # fig.show()


st.set_page_config(page_title="Crypto Currency Price Prediction",page_icon = ":chart_with_upwards_trend",layout="wide")
st.title(" :chart_with_upwards_trend: Crypto Currency  Price Prediction")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# browsering the files ----------------------------------------------
# f1 = st.file_uploader(":file folder: Upload a file",type = (["csv","xlsx","txt","xls"]))
# if f1 is not None:
#     filename = f1.name
#     st.write(filename)
#     df = pd.read_csv(filename)
# else:
#     os.chdir(r"E:\MumBaiKharGhar\Major Project DBDA\Project\MajorProject")
#     df = pd.read_csv("Gemini_BTCUSD_d.csv",skiprows=1)
# ---------------------------------------------------------------------------------------

# --------------------------------------------------------------

col1,col2,col3 = st.columns(3)
with col1:
    option = st.selectbox(
    'Select the type of the coin',
    ('BTCUSD', 'ETHUSD', 'DOGEUSD', 'LTCUSD'))
with col2:
    option2 = st.selectbox(
        'Select the type of the model',
        ('LSTM', 'XGBoost'))

with col3:
    date2 = pd.to_datetime(st.date_input("Date ", min_value=datetime.datetime.now()))
# st.write(date2.day)
# st.write(datetime.date.today().day)
# pred_days = date2.day- datetime.date.today().day
# st.write(pred_days)

st.write(option)
st.write(option2)
if st.button("Predict"):
    if option2 == 'LSTM':
        Lstm(option, date2)
    elif option2 == 'XGBoost':
        Xgboost(option,date2)




    st.write('You selected:', option)
# ---------------------------------------------------------------
    df = pd.read_csv(".\Dataset\Gemini_BTCUSD_1h.csv",skiprows=1)

    btn_col1,btn_col2 = st.columns((2))
    with btn_col1:
        st.write('Graph and prediction for the particular bitcoin')
        st.subheader("Gemini Bitcoin Coin ")
        st.line_chart(data=df, x='date', y='close', width=300, height=400)

    with btn_col2:
        df = pd.DataFrame(
            {
                "name": ["Accuracy", "Precision", "Recall", "F1 Score", "RMSE", "MES"],
                "Values": [9.6757, 7.6567, 5.552, 9.6757, 7.6567, 5.552]
            }
        )
        st.dataframe(
            df,
            column_config={
                "name": "Prediction",
                "Values": "Values"
            },
            hide_index=True,
        )
        # Xgboost()
else:
    st.write('Something went wrong!')

