
import streamlit as st
from prophet import Prophet
import plotly.express as px
import inspect
import textwrap
import time
import numpy as np
import pandas as pd
from datetime import datetime


import streamlit as st

def about(): 
    st.set_page_config(
            page_title="Enibly-About",
            page_icon="icon.png",
        )
    st.sidebar.image('image.png')
    st.sidebar.write('Copyright © 2023 Enibly Technology. All rights reserved.')
    st.image('image.png')
    st.header("About Enibly")

    st.markdown("**:blue[Enibly is a technology enabler for businesses]**, focused on implementing advance technologies like Artificial Intelligence, IoT, and Blockchain to boost performance. Our goal is to help companies leverage the power of these technologies to streamline their operations, make better decisions, and stay ahead of the competition.")
    st.markdown("In addition to our technology solutions, we also offer :orange[custom software development services]. We can customize a software or embed technology in your existing systems based on your specific business requirements. Contact us to learn more about how we can help your business succeed.")
    st.markdown("For more information, visit our website [Enibly](http://enibly.com).")


about()