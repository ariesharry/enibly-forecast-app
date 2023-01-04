import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.diagnostics import performance_metrics
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric
import base64
from streamlit.logger import get_logger
import plotly.express as px

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
            page_title="Enibly-Automated Time Series Forecasting",
            page_icon="icon.png",
            layout="wide"
        )
    st.title('Automated Time Series Forecasting')
    st.info(
                f"""
                    This data app uses Facebook's open-source Prophet library to automatically generate future forecast values from an imported dataset.
    You'll be able to import your data from a CSV file, visualize trends and features, analyze forecast performance, and finally download the created forecast! 

    Created by Enibly Technology: http://enibly.com
                    """
            )
   
    # def add_logo():
    #     st.markdown(
    #         """
    #         <style>
                
    #             [data-testid="stSidebarNav"]::before {
    #                 content: "Enibly Technology";
    #                 margin-left: 20px;
    #                 margin-top: 20px;
    #                 font-size: 30px;
    #                 position: relative;
    #                 top: 100px;
    #             }
    #         </style>
    #         """,
    #         unsafe_allow_html=True,
    #     )
    # add_logo()


    df = st.sidebar.file_uploader('Upload dataset here', type='csv')
    with st.sidebar.expander('How to upload dataset?'):
        
        st.info(
                    f"""
                        Import the time series csv file here. Columns must be labeled ds and y. The input to Prophet is always a dataframe with two columns: ds and y. The ds (datestamp) column should be of a format expected by Pandas, ideally YYYY-MM-DD for a date or YYYY-MM-DD HH:MM:SS for a timestamp. The y column must be numeric, and represents the measurement we wish to forecast.
                        Upload a .csv file first. Sample to try: [peyton_manning_wiki_ts.csv](https://raw.githubusercontent.com/zachrenwick/streamlit_forecasting_app/master/example_data/example_wp_log_peyton_manning.csv)
                        """
                )

    st.sidebar.image('image.png')
    st.sidebar.write('Copyright © 2023 Enibly Technology. All rights reserved.')


    if df is not None:
        data = pd.read_csv(df)
        data['ds'] = pd.to_datetime(data['ds'],errors='coerce') 
        
        max_date = data['ds'].max()
        #st.write(max_date)
    """
    ### Select Forecast Horizon
    """

    periods_input = st.number_input('How many periods would you like to forecast into the future?',
    min_value = 1, max_value = 365)

    if df is not None:
        m = Prophet()
        m.fit(data)
    
    
    
    with st.expander('Tips!!'):
        st.info(
                        f"""
                            Keep in mind that forecasts become less accurate with larger forecast horizons.
                            """
                    )

    if st.button('Forecast!'):
        
        """
        ### Visualize Forecast Data

        The below visual shows future predicted values. "yhat" is the predicted value, and the upper and lower limits are (by default) 80% confidence intervals.
        """
        if df is not None:
            future = m.make_future_dataframe(periods=periods_input)
            
            forecast = m.predict(future)
            fcst = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

            fcst_filtered =  fcst[fcst['ds'] > max_date]    
            st.table(fcst_filtered)
            fig = px.line(fcst_filtered, x='ds', y=fcst_filtered.columns)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            
            """
            The next visual shows the actual (black dots) and predicted (blue line) values over time.
            """
            fig1 = m.plot(forecast)
            st.write(fig1)
            


            """
            The next few visuals show a high level trend of predicted values, day of week trends, and yearly trends (if dataset covers multiple years). The blue shaded area represents upper and lower confidence intervals.
            """
            fig2 = m.plot_components(forecast)
            st.write(fig2)


        """
        ### Download the Forecast Data

        The below link allows you to download the newly created forecast to your computer for further analysis and use.
        """
        
        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(fcst_filtered)

        st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='result.csv',
        mime='text/csv',
        )

    else:
        st.write('The results will show here!')

if __name__ == "__main__":
    run()