from matplotlib import pyplot as plt
import streamlit as st

from ui.home import run_home
from ui.Map import run_map
from ui.eda import run_eda
from ui.prediction import run_prediction

import os
import matplotlib.font_manager as fm

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/custom_fonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)


def main():
        # 📌 Streamlit 사이드바 너비 조절 (기본보다 넓게 설정)

    fontRegistered()
    plt.rc('font', family='NanumGothic')
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

    menu = ["Home", "Map", "EDA", "Prediction"]
    choice = st.sidebar.selectbox("Menu", menu)
 # 📌 사이드바 맨 위에 이미지 추가 (가운데 정렬)
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

if __name__ == '__main__':
    main()
