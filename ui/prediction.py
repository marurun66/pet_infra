import json
import joblib
import streamlit as st
import pandas as pd
import folium
from sklearn.cluster import KMeans
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import geopandas as gpd
from folium.plugins import MarkerCluster 


import os
import matplotlib.font_manager as fm

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/font']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)


def run_prediction():
    with open("data/seongnam_geo.json", encoding="utf-8") as f:
        geo_json = json.load(f)

    fontRegistered()
    plt.rc('font', family='NanumGothic')
    
    st.sidebar.title("📍K-Means 클러스터링과 수치로 보는      병원🏥/약국💊 부족지역")
    # 인코딩된 데이터
    X = pd.read_csv("data/X.csv")
    # 클러스터링 결과 데이터
    df = pd.read_csv("data/merged_data.csv")
    #유저친화적으로 클러스터 0,1,2,3 대신 1,2,3,4로 변경
    df['클러스터'] = df['클러스터'] + 1
    # 모델 불러오기
    kmeans_loaded = joblib.load('models/kmeans_model.pkl')

    
    # 성남시 행정동 GeoJSON 불러오기
    geojson_path = "data/seongnam_geo.json"
    gdf = gpd.read_file(geojson_path)
    # folium 지도 생성
    m = folium.Map(location=[37.438, 127.137], zoom_start=12)

    # 사이드바 메뉴 추가
    menu = ["K-Means이란?", "K-Means로 보는 반려동물 인프라 클러스터", "수치로 보는 인프라 부족지역"]
    selected_analysis = st.sidebar.radio("📌 분석할 항목을 선택하세요.", menu)

    if selected_analysis == menu[0]:
        st.subheader(f"📊 {menu[0]}")
        st.markdown("""
        K-Means 클러스터링은 데이터를 **K개의 그룹으로 나누는 비지도 학습 기법**입니다.  
        각 데이터 포인트는 **가장 가까운 중심(centroid)과의 거리**를 기준으로 군집화됩니다.  
        """)
        # 엘보우 기법 설명
        st.subheader("📊 최적의 클러스터 개수 찾기 (Elbow Method)")
        sse = []
        k_range = range(1, 11)
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(df[['위도', '경도']])
            sse.append(kmeans.inertia_)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(k_range, sse, marker='o', linestyle='--')
        ax.set_xlabel('클러스터 개수 (k)')
        ax.set_ylabel('SSE (오차 제곱합)')
        ax.set_title('엘보우 기법을 이용한 최적 클러스터 개수 찾기')
        st.pyplot(fig)

        st.markdown("""
        ### 📌 엘보우 기법이란?
        - 클러스터 개수를 증가시키면 **오차 제곱합(SSE)** 이 감소하지만, 특정 지점 이후로 감소 속도가 둔화됩니다.  
        - 이 변곡점이 바로 **"엘보우 포인트(Elbow Point)"** 입니다.  
        - **해당 그래프를 보면 k=4에서 변화가 둔화**되므로 **4개의 클러스터가 가장 적절한 개수**로 보여집니다.
        - 다음 **K-Means로 보는 부족지역 메뉴**에서 직접 클러스터 개수를 조절해 결과를 확인해보세요.
        """)
        # ✅ 
        st.markdown("""
        ### 📌 성남시 반려동물 인프라 분석 앱에서는
        - 위도와 경도 
        - 동물소유자 수, 반려동물 수,병원 수,약국 수
        - 동 기준 병원 당 반려동물 수,약국 당 반려동물 수
        - 행정동 기준으로 K-Mean 클러스터링을 수행합니다.""")


    elif selected_analysis == menu[1]:
        st.subheader(f"📊 {menu[1]}")
        # 데이터 불러오기
        st.markdown("""
        엘보우 기법으로 확인했을때, **최적 클러스터 개수는 4개**입니다.  
        클러스터는 맵 상에서 **마커 색깔**로 구분할 수 있습니다.
        """)

        cluster_colors = {1: "red", 2: "blue", 3: "green", 4: "purple"}
        
        marker_cluster = MarkerCluster().add_to(m)
        
        for idx, row in df.iterrows():
            folium.Marker(
                location=[row['위도'], row['경도']],
                popup=folium.Popup(f'<div style="white-space: nowrap;">클러스터: {row["클러스터"]}<br>동 이름: {row["지역명"]}<br> 병원 수: {int(row["병원수"])}<br>약국 수: {int(row["약국수"])}<br></div>', max_width=300),
                icon=folium.Icon(color=cluster_colors.get(row['클러스터'], 'medkit'))
            ).add_to(marker_cluster)
        
        # GeoJSON을 추가해서 행정동 구분
        folium.GeoJson(
            gdf,
            name="성남시 행정동",
            style_function=lambda feature: {
                "fillColor": "#add8e6",
                "color": "#2a52be",
                "weight": 1,
                "fillOpacity": 0.5
            },

            show=True
        ).add_to(m)

        # 동 이름 라벨 추가
        for _, row in gdf.iterrows():
            folium.Marker(
                location=[row.geometry.centroid.y, row.geometry.centroid.x],
                icon=folium.DivIcon(html=f'<div style="font-size: 10pt; font-weight: bold; color: black; background-color: rgba(255, 255, 255, 0.0); padding: 2px; border-radius: 3px; display: inline-block; white-space: nowrap;">{row["dong_name"]}</div>')
            ).add_to(m)

        folium_static(m)

        df_sorted = df.sort_values(by="클러스터").reset_index(drop=True)
        st.markdown('<span style="color:red">🔴 <b>1번</b> 클러스터 정보보기</span>', unsafe_allow_html=True)
        st.data_editor(df_sorted[df_sorted["클러스터"]==1].drop(columns=["위도", "경도","클러스터","동별","구별"]),hide_index=True)
        st.markdown('<span style="color:blue"> <b>🔵 2번</b> 클러스터 정보보기</span>', unsafe_allow_html=True)
        st.data_editor(df_sorted[df_sorted["클러스터"]==2].drop(columns=["위도", "경도","클러스터","동별","구별"]),hide_index=True)
        st.markdown('<span style="color:green"> <b>🟢 3번</b> 클러스터 정보보기</span>', unsafe_allow_html=True)
        st.data_editor(df_sorted[df_sorted["클러스터"]==3].drop(columns=["위도", "경도","클러스터","동별","구별"]),hide_index=True)
        st.markdown('<span style="color:purple"> <b>🟣 4번</b> 클러스터 정보보기</span>', unsafe_allow_html=True)
        st.data_editor(df_sorted[df_sorted["클러스터"]==4].drop(columns=["위도", "경도","클러스터","동별","구별"]),hide_index=True)

        # 클러스터별 통계
        st.subheader("📊 클러스터별 평균")
        
        # 클러스터별 평균값 계산
        cluster_avg = df.groupby("클러스터")[["동물소유자수", "반려동물수", "병원수", "약국수", "병원당_반려동물수", "약국당_반려동물수"]].mean().astype(int).reset_index()

        st.data_editor(cluster_avg,hide_index=True)


        st.subheader("📊 클러스터링 분석")
        st.text("반려동물 가구는 반려동물과 동물 소유자수를 합친 값입니다.")
        strategy_data = {
        "클러스터": [1,2,3,4],
        "특징": [
            "소규모 반려동물 가구 지역",
            "대규모 반려동물 가구 지역, 병원 인프라도 많은편이나 수요가 더 있을것으로 보여짐",
            "중규모 반려동물 가구 지역, 병원·약국 인프라 부족",
            "중대형 반려동물 가구 지역, 중간 수준 인프라"
        ],
        "병원 부족 여부": ["❌ (부족하지 않음)", "✅ (부족함)", "✅ (부족함)", "⚠️ (일부 부담)"],
        "추가 병원 개설 필요성": ["❌ (필요 없음)", "✅ (확장 필요)", "✅ (추가 필요)", "⚠️ (확장 고려)"]
    }

            # 데이터프레임 생성
        strategy_df = pd.DataFrame(strategy_data)

        # 전략 표 출력
        st.data_editor(strategy_df,hide_index=True)
        st.markdown(
        """
        <div style="
            background-color: #dff0d8; 
            padding: 15px;  ㄴ
            border-radius: 10px;
            border: 1px solid #c3e6cb;">
        
        #### 🐶클러스터별 활용제안:  
        ✅ **클러스터 2과 3는 추가 병원,약국 개설이 가장 필요한 것 으로 보입니다.**  
        ✅ **클러스터 4도 일부 지역에서는 병원,약국 부족 현상이 발생할 가능성이 있습니다.**  
        ✅ **클러스터 1은 병원,약국 개설 필요성이 낮아보입니다.**  

        Kmeans 분석결과와 다음 수치로 보는 인프라 부족지역 정보를 참고하여 
        추가적인 인프라 확충이 필요한 지역을 파악해보세요.
        
        </div>
        """,
        unsafe_allow_html=True
    )


    elif selected_analysis == menu[2]:
            st.subheader("📍 병원 및 약국 부족 지역 분석")
            st.text("병원과 약국이 부족한 상위 10개 지역과 K-Means 클러스터링 결과를 함께 분석하여 최적의 입지를 고려해보세요.")
            st.info(
            "📌 병원과 약국 당 반려동물 밀도 분석은 다음 공식을 사용하여 계산했습니다:\n"
            '```python\n'
            'df["병원당_반려동물수"] = df["반려동물수"] / (df["병원수"] + 1)\n'
            '```'
        )

            view_option = st.radio("🔎 어떤 부족 지역을 보시겠습니까?", ["병원 부족 지역", "약국 부족 지역"])
            
            if view_option == "병원 부족 지역":

                df["병원당_반려동물수"] = df["반려동물수"] / (df["병원수"] + 1)
                top_needy_hospital = df.sort_values(by="병원당_반려동물수", ascending=False).head(10)
                
                st.subheader("📍 병원 부족 지역 지도")
                st.text("지도 마커를 클릭하면, 반려동물 대비 병원 수 확인이 가능합니다.")
                map_hospital = folium.Map(location=[df["위도"].mean(), df["경도"].mean()], zoom_start=12)
                
            # GeoJSON을 지도에 추가
                folium.GeoJson(
                    gdf,
                    name="성남시 행정동",
                    style_function=lambda feature: {
                        "fillColor": "#add8e6",
                        "color": "#2a52be",
                        "weight": 1,
                        "fillOpacity": 0.5
                    }
                ).add_to(map_hospital)
                
                # 동 이름 라벨 추가
                for _, row in gdf.iterrows():
                    folium.Marker(
                        location=[row.geometry.centroid.y, row.geometry.centroid.x],
                        icon=folium.DivIcon(html=f'<div style="font-size: 10pt; font-weight: bold; color: black; background-color: rgba(255, 255, 255, 0.0); padding: 2px; border-radius: 3px; display: inline-block; white-space: nowrap;">{row["dong_name"]}</div>')
                    ).add_to(map_hospital)
                    

                for idx, row in top_needy_hospital.iterrows():
                    folium.CircleMarker(
                        location=[row["위도"], row["경도"]],
                        radius=20,
                        color="blue",
                        fill=True,
                        fill_color="blue",
                        fill_opacity=0.6,
                        popup=folium.Popup(f'<div style="white-space: nowrap; max-width: 400px;">{row["지역명"]} (반려동물: {int(row["반려동물수"])}, 병원 수: {int(row["병원수"])})</div>', max_width=400)

                    ).add_to(map_hospital)

                folium_static(map_hospital)
                st.subheader("📍 병원이 부족한 상위 10개 지역")
                st.data_editor(top_needy_hospital[["지역명", "반려동물수", "병원수", "병원당_반려동물수"]],hide_index=True)
            
            elif view_option == "약국 부족 지역":

                df["약국당_반려동물수"] = df["반려동물수"] / (df["약국수"] + 1)
                top_needy_pharmacy = df.sort_values(by="약국당_반려동물수", ascending=False).head(10)
                
                st.subheader("📍 약국 부족 지역 지도")
                st.text("지도 마커를 클릭하면, 반려동물 대비 약국 수 확인이 가능합니다.")
                map_pharmacy = folium.Map(location=[df["위도"].mean(), df["경도"].mean()], zoom_start=12)
                
            # GeoJSON을 지도에 추가
                folium.GeoJson(
                    gdf,
                    name="성남시 행정동",
                    style_function=lambda feature: {
                        "fillColor": "#add8e6",
                        "color": "#2a52be",
                        "weight": 1,
                        "fillOpacity": 0.5
                    }
                ).add_to(map_pharmacy)
                
                # 동 이름 라벨 추가
                for _, row in gdf.iterrows():
                    folium.Marker(
                        location=[row.geometry.centroid.y, row.geometry.centroid.x],
                        icon=folium.DivIcon(html=f'<div style="font-size: 10pt; font-weight: bold; color: black; background-color: rgba(255, 255, 255, 0.0); padding: 2px; border-radius: 3px; display: inline-block; white-space: nowrap;">{row["dong_name"]}</div>')
                    ).add_to(map_pharmacy)

                for idx, row in top_needy_pharmacy.iterrows():
                    folium.CircleMarker(
                        location=[row["위도"], row["경도"]],
                        radius=20,
                        color="blue",
                        fill=True,
                        fill_color="blue",
                        fill_opacity=0.6,
                        popup=folium.Popup(f'<div style="white-space: nowrap; max-width: 400px;">{row["지역명"]} (반려동물: {int(row["반려동물수"])}, 약국 수: {int(row["약국수"])})</div>', max_width=400)


                    ).add_to(map_pharmacy)

                folium_static(map_pharmacy)
                st.subheader("📍 약국이 부족한 상위 10개 지역")
                st.data_editor(top_needy_pharmacy[["지역명", "반려동물수", "약국수", "약국당_반려동물수"]],hide_index=True)