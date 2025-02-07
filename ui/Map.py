from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import json



def run_map():


    # 데이터 불러오기
    pet_data = pd.read_csv("data/pet_data.csv")
    hospital_data = pd.read_csv("data/hospitals.csv")
    pharmacy_data = pd.read_csv("data/pharmacies.csv")
    # 성남시 행정구역 GeoJSON 데이터
    with open("data/seongnam_geo.json", encoding="utf-8") as f:
        geo_json = json.load(f)

    # Streamlit 사이드바 구성
    st.sidebar.title("📍 성남시 반려동물 & 동물병원/약국 분석")

    # 구 선택
    selected_gu = st.sidebar.selectbox("구 선택", ["전체"] + list(pet_data["구별"].unique()))

    # 선택된 구에 따라 동 선택 목록 업데이트
    if selected_gu == "전체":
        available_dongs = list(pet_data["동별"].unique())  # 모든 동 포함
    else:
        available_dongs = list(pet_data[pet_data["구별"] == selected_gu]["동별"].unique())  # 선택된 구에 속한 동만 포함

    # 동 선택 
    selected_dong = st.sidebar.selectbox("동 선택", ["전체"] + available_dongs)

    # 병원/약국 필터링 체크박스 추가
    show_hospitals = st.sidebar.checkbox("병원 보기", value=True)
    show_pharmacies = st.sidebar.checkbox("약국 보기", value=True)

    # 구/동 선택 시 지도 중심 이동 기능
    # 구별 또는 동별 중심 좌표 찾기
    def get_center_coordinates(selected_gu, selected_dong):
        if selected_dong != "전체":
            subset = hospital_data[hospital_data["동별"] == selected_dong]
            if subset.empty:
                subset = pharmacy_data[pharmacy_data["동별"] == selected_dong]
        elif selected_gu != "전체":
            subset = hospital_data[hospital_data["구별"] == selected_gu]
            if subset.empty:
                subset = pharmacy_data[pharmacy_data["구별"] == selected_gu]
        else:
            return 37.4200, 127.1265  # 기본 성남시 중심 좌표
        
        if not subset.empty:
            return subset["위도"].mean(), subset["경도"].mean()
        
        return 37.4200, 127.1265  # 기본 성남시 중심 좌표
    
    # 선택된 구/동에 따라 지도 확대
    def get_zoom_level(selected_gu, selected_dong):
        if selected_dong != "전체":
            return 14  # ✅ 동을 선택하면 더 확대
        elif selected_gu != "전체":
            return 13  # ✅ 구를 선택하면 적절한 확대 수준 적용
        else:
            return 12  # 기본 성남시 전체 확대

    # 데이터 필터링 (사용자가 선택한 구·동별 데이터만 표시)
    filtered_hospital_data = hospital_data.copy()
    filtered_pharmacy_data = pharmacy_data.copy()

    if selected_gu != "전체":
        pet_data = pet_data[pet_data["구별"] == selected_gu]
        filtered_hospital_data = filtered_hospital_data[filtered_hospital_data["구별"] == selected_gu]
        filtered_pharmacy_data = filtered_pharmacy_data[filtered_pharmacy_data["구별"] == selected_gu]

    if selected_dong != "전체":
        pet_data = pet_data[pet_data["동별"] == selected_dong]
        filtered_hospital_data = filtered_hospital_data[filtered_hospital_data["동별"] == selected_dong]
        filtered_pharmacy_data = filtered_pharmacy_data[filtered_pharmacy_data["동별"] == selected_dong]

    # 지도 중심 좌표 설정 (선택한 구/동에 따라 이동)
    center_lat, center_lon = get_center_coordinates(selected_gu, selected_dong)
    zoom_level = get_zoom_level(selected_gu, selected_dong)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_level, tiles="cartodb positron")

    # 반려동물 수 히트맵 (GeoJSON의 'dong_name' 속성 활용)
    choropleth = folium.Choropleth(
        geo_data=geo_json,
        name="반려동물 등록 수",
        data=pet_data,
        columns=["동별", "반려동물수"],
        key_on="feature.properties.dong_name",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="반려동물 등록 수"
    ).add_to(m)

    # 동 이름 및 반려동물 수 팝업으로 표시
    for feature in geo_json["features"]:
        coords = feature["geometry"]["coordinates"][0][0]
        avg_lat = sum([c[1] for c in coords]) / len(coords)
        avg_lon = sum([c[0] for c in coords]) / len(coords)
        dong_name = feature["properties"]["dong_name"]
        pet_count = pet_data[pet_data["동별"] == dong_name]["반려동물수"].sum()
        
        folium.Marker(
            location=[avg_lat, avg_lon],
            popup=folium.Popup(f"{dong_name} - 반려동물 등록 수: {pet_count}", max_width=300),
            icon=folium.DivIcon(html=f'<div style="font-size: 10pt; color: black; font-weight: bold; white-space: nowrap;">{dong_name}</div>')
        ).add_to(m)

    # 병원/약국 마커 추가 (체크박스 선택 여부에 따라 표시)
    if show_hospitals:
        for _, row in filtered_hospital_data.iterrows():
            folium.Marker(
                location=[row["위도"], row["경도"]],
                popup=folium.Popup(f"🏥 {row['사업장명']}<br>{row['소재지도로명주소']}", max_width=300),
                tooltip=row["사업장명"],
                icon=folium.Icon(color="blue", icon="medkit")
            ).add_to(m)

    if show_pharmacies:
        for _, row in filtered_pharmacy_data.iterrows():
            folium.Marker(
                location=[row["위도"], row["경도"]],
                popup=folium.Popup(f"💊 {row['사업장명']}<br>{row['소재지도로명주소']}", max_width=300),
                tooltip=row["사업장명"],
                icon=folium.Icon(color="green", icon="medkit")
            ).add_to(m)

    # Streamlit에서 지도 표시
    st.subheader("🗺️ 지도에서 확인하기")
    st.markdown(
    """
    🔍 **사이드바에서 구/동을 선택하면 지도가 업데이트됩니다.**<br>
    🏥 **마커를 클릭하면 병원, 약국 정보를 확인할 수 있습니다..**<br>
    📌 **동을 클릭하면 반려동물 등록 수를 확인할 수 있습니다.**<br>
    🐶현재 위례동에 대한 반려동물 등록수는 제공되지 않아 지도에 표시되지 않습니다.<br>
    <br>지도의 색이 진할수록 반려동물 수가 많음을 나타냅니다.<br>**반려동물 대비 병원, 약국이 적은 지역을 직접 확인**하고 **새로운 병원,약국 입지를 결정**해보세요.
    
    """, unsafe_allow_html=True
    )
    

    folium_static(m)





