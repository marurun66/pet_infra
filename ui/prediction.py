import streamlit as st
import pandas as pd
import folium
from sklearn.cluster import KMeans
from streamlit_folium import folium_static
import matplotlib.pyplot as plt

import os
import matplotlib.font_manager as fm

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/custom_fonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)


def run_prediction():

    fontRegistered()
    plt.rc('font', family='NanumGothic')
    
    st.sidebar.title("📍K-Means 클러스터링과 수치로 보는      병원🏥/약국💊 부족지역")
    # 🔹 스케일링된 데이터 X
    X = pd.read_csv("data/scalerX_data.csv")
    # 🔹 기존 데이터
    df = pd.read_csv("data/merged_data.csv")
    
    


    # 🔹 사이드바 메뉴 추가
    menu = ["K-Means이란?", "K-Means로 보는 부족지역", "수치로 보는 부족지역"]
    selected_analysis = st.sidebar.radio("📌 분석할 항목을 선택하세요.", menu)

    if selected_analysis == menu[0]:
        st.subheader(f"📊 {menu[0]}")
        st.markdown("""
        K-Means 클러스터링은 데이터를 **K개의 그룹으로 나누는 비지도 학습 기법**입니다.  
        각 데이터 포인트는 **가장 가까운 중심(centroid)과의 거리**를 기준으로 군집화됩니다.  
        """)
        # ✅ 엘보우 기법 적용
        st.subheader("📊 최적의 클러스터 개수 찾기 (Elbow Method)")
        sse = []
        k_range = range(1, 11)
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X)
            sse.append(kmeans.inertia_)

        # ✅ 엘보우 기법 차트 시각화
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(k_range, sse, marker='o', linestyle='--')
        ax.set_xlabel('클러스터 개수 (k)')
        ax.set_ylabel('SSE (오차 제곱합)')
        ax.set_title('엘보우 기법을 이용한 최적 클러스터 개수 찾기')
        st.pyplot(fig)

        # ✅ 엘보우 기법 설명 멘트
        st.markdown("""
        ### 📌 엘보우 기법이란?
        - 클러스터 개수를 증가시키면 **오차 제곱합(SSE)** 이 감소하지만, 특정 지점 이후로 감소 속도가 둔화됩니다.  
        - 이 변곡점이 바로 **"엘보우 포인트(Elbow Point)"** 입니다.  
        - **해당 그래프를 보면 k=5에서 변화가 둔화**되므로 **4~5개의 클러스터가 가장 적절한 개수**로 보여집니다.
        - 다음 **K-Means로 보는 부족지역 메뉴**에서 직접 클러스터 개수를 조절해 결과를 확인해보세요.
        """)


    elif selected_analysis == menu[1]:
        
        # 🔹 유저가 클러스터 개수 선택
        n_clusters = st.slider("🔢 클러스터 개수를 선택하세요", min_value=2, max_value=10, value=5, step=1)

        # 데이터 불러오기
        st.write("사용자가 선택한 클러스터 개수를 적용하여 클러스터를 나눕니다.")
        cluster_colors = {0: "red", 1: "blue", 2: "green", 3: "purple", 4: "orange", 5: "pink", 6: "cyan", 7: "brown", 8: "gray", 9: "yellow"}
        
        # 🔹 K-Means 클러스터링 수행 (사용자 입력 반영)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df["클러스터"] = kmeans.fit_predict(X)

        cluster_colors = {i: color for i, color in enumerate(["red", "blue", "green", "purple", "orange", "pink", "cyan", "brown", "gray", "yellow"])}
        
        legend_html = """
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 180px; height: 250px;
                    background-color: white; z-index:9999; font-size:14px;
                    border-radius: 10px; padding: 10px;">
        <b>📌 클러스터 범례</b><br>
        """ + "".join([f"<i style='background:{color}; width:10px; height:10px; display:inline-block;'></i> 클러스터 {i}<br>" for i, color in cluster_colors.items()]) + """
        </div>
        """
        
        # ✅ 병원 / 약국 선택 버튼 추가
        menu2 = ["병원 클러스터링", "약국 클러스터링"]
        view_option = st.radio("🔎 어떤 클러스터링을 보시겠습니까?", menu2)

        if view_option == menu2[0]:
            st.subheader(f"📍 병원 클러스터링된 지역 보기 (클러스터 {n_clusters}개)")
            st.write(df[["지역명", "반려동물수", "병원수","병원당_반려동물수", "클러스터"]])
        elif view_option == menu2[1]:
            st.subheader(f"📍 약국 클러스터링된 지역 보기 (클러스터 {n_clusters}개)")
            st.write(df[["지역명", "반려동물수", "약국수","약국당_반려동물수", "클러스터"]])
        
        map_clustered = folium.Map(location=[df["위도"].mean(), df["경도"].mean()], zoom_start=12)

        for idx, row in df.iterrows():
            folium.CircleMarker(
                location=[row["위도"], row["경도"]],
                radius=6,
                color=cluster_colors.get(row["클러스터"], "gray"),
                fill=True,
                fill_color=cluster_colors.get(row["클러스터"], "gray"),
                fill_opacity=0.6,
                popup=f"{row['지역명']} (클러스터: {row['클러스터']})"
            ).add_to(map_clustered)
        
        map_clustered.get_root().html.add_child(folium.Element(legend_html))
        folium_static(map_clustered)


    elif selected_analysis == menu[2]:
            st.subheader("📍 병원 및 약국 부족 지역 분석")
            view_option = st.radio("🔎 어떤 부족 지역을 보시겠습니까?", ["병원 부족 지역", "약국 부족 지역"])
            
            if view_option == "병원 부족 지역":
                st.subheader("📍 병원이 부족한 상위 10개 지역")
                df["병원당_반려동물수"] = df["반려동물수"] / (df["병원수"] + 1)
                top_needy_hospital = df.sort_values(by="병원당_반려동물수", ascending=False).head(10)
                st.write(top_needy_hospital[["지역명", "반려동물수", "병원수", "병원당_반려동물수"]])
                
                st.subheader("📍 병원 부족 지역 지도")
                map_hospital = folium.Map(location=[df["위도"].mean(), df["경도"].mean()], zoom_start=12)
                
                for idx, row in top_needy_hospital.iterrows():
                    folium.CircleMarker(
                        location=[row["위도"], row["경도"]],
                        radius=8,
                        color="blue",
                        fill=True,
                        fill_color="blue",
                        fill_opacity=0.6,
                        popup=f"{row['지역명']} (반려동물: {row['반려동물수']}, 병원 수: {row['병원수']})"
                    ).add_to(map_hospital)
                
                folium_static(map_hospital)
            
            elif view_option == "약국 부족 지역":
                st.subheader("📍 약국이 부족한 상위 10개 지역")
                df["약국당_반려동물수"] = df["반려동물수"] / (df["약국수"] + 1)
                top_needy_pharmacy = df.sort_values(by="약국당_반려동물수", ascending=False).head(10)
                st.write(top_needy_pharmacy[["지역명", "반려동물수", "약국수", "약국당_반려동물수"]])
                
                st.subheader("📍 약국 부족 지역 지도")
                map_pharmacy = folium.Map(location=[df["위도"].mean(), df["경도"].mean()], zoom_start=12)
                
                for idx, row in top_needy_pharmacy.iterrows():
                    folium.CircleMarker(
                        location=[row["위도"], row["경도"]],
                        radius=8,
                        color="red",
                        fill=True,
                        fill_color="red",
                        fill_opacity=0.6,
                        popup=f"{row['지역명']} (반려동물: {row['반려동물수']}, 약국 수: {row['약국수']})"
                    ).add_to(map_pharmacy)
                
                folium_static(map_pharmacy)