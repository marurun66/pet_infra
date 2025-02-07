from matplotlib import pyplot as plt
import streamlit as st

from ui.about import run_about
from ui.home import run_home
from ui.Map import run_map
from ui.eda import run_eda
from ui.prediction import run_prediction



def main():

    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                min-width: 500px;
                max-width: 550px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("성남시 반려동물 인프라 분석")

    menu = ["Home", "Map", "EDA", "Prediction","About"]
    choice = st.sidebar.selectbox("Menu", menu)

    st.sidebar.markdown(
        """
        <div style="text-align: center;">
            <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiKzGxl8LBCvZICAbTzXWlxOzFLf6IHIN0nCGF_gceGGMzc_0Txbq8oymI-MQpLx3s-ZFTxn_FKyyGTrtCclAGdzBVZqJc7xjfSZjumMT8d1O32wxmQeyMhryr2funFqMjTN_-iHFmvHu0/s400/pet_doctor_juui_woman.png" width="200px">
        </div>
        """,
        unsafe_allow_html=True
    )



    if choice == "Home":
        run_home()

    elif choice == "Map":
        run_map()

    elif choice == "EDA":
        run_eda()

    elif choice == "Prediction":
        run_prediction()

    elif choice == "About":
        run_about()

if __name__ == '__main__':
    main()
