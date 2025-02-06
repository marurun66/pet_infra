import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import json
import plotly.graph_objects as go
import plotly.express as px

def run_eda():

    pet_df = pd.read_csv("data/pet_data.csv")
    hospital_df = pd.read_csv("data/hospitals.csv")
    pharmacy_df = pd.read_csv("data/pharmacies.csv")

    # 📌 Streamlit 사이드바 구성
    st.sidebar.title("📊 데이터 탐색 (EDA)")

    # 🔹 데이터 선택 옵션
    menu=["동 별 반려동물/병원/약국 개수 비교",
        "병원/약국이 없는 지역 찾기",
        "병원/약국 접근성 분석",
        "반려동물 수와 병원 개수의 상관관계"]
    
    selected_analysis = st.sidebar.radio("분석 항목 선택", menu)

    pet_hospital_counts = pet_df.groupby(["구별", "동별"])["반려동물수"].sum().reset_index()
    hospital_counts = hospital_df.groupby(["구별", "동별"])["사업장명"].count().reset_index()
    hospital_counts.rename(columns={"사업장명": "병원 개수"}, inplace=True)
    pharmacy_counts = pharmacy_df.groupby(["구별", "동별"])["사업장명"].count().reset_index()
    pharmacy_counts.rename(columns={"사업장명": "약국 개수"}, inplace=True)

    merged_df = pet_hospital_counts.merge(hospital_counts, on=["구별", "동별"], how="left")\
                                .merge(pharmacy_counts, on=["구별", "동별"], how="left")

    merged_df.fillna(0, inplace=True)
    # 📌 병원/약국 개수를 정수형으로 변환
    merged_df["병원 개수"] = merged_df["병원 개수"].astype(int)
    merged_df["약국 개수"] = merged_df["약국 개수"].astype(int)

    merged_df = merged_df.sort_values(by=['구별', '동별']).reset_index(drop=True)


    # 📌 EDA 분석 수행
    if selected_analysis == menu[0]:
        st.subheader(menu[0])
        # 📌 Streamlit UI - 구 선택 추가
        selected_gu = st.selectbox("구 선택", ["전체"] + list(merged_df["구별"].unique()))

        # ✅ 선택한 구에 해당하는 동만 필터링
        if selected_gu != "전체":
            filtered_df = merged_df[merged_df["구별"] == selected_gu]
        else:
            filtered_df = merged_df  # 전체 구 표시

        fig = go.Figure()
        fig.add_trace(go.Bar(x=filtered_df["동별"], y=filtered_df["반려동물수"], name="반려동물 수", marker_color="blue"))
        fig.add_trace(go.Scatter(x=filtered_df["동별"], y=filtered_df["병원 개수"], name="병원 개수", mode='lines+markers', line=dict(color='red'), yaxis='y2'))
        fig.add_trace(go.Scatter(x=filtered_df["동별"], y=filtered_df["약국 개수"], name="약국 개수", mode='lines+markers', line=dict(color='green'), yaxis='y2'))
        
        fig.update_layout(
            title=f"📍{selected_gu} 동별 반려동물 수 및 병원/약국 개수 비교" if selected_gu != "전체" else "동별 반려동물 수 및 병원/약국 개수 비교",
            xaxis_title="동별",
            yaxis=dict(title="반려동물 수", side="left"),
            yaxis2=dict(title="병원/약국 개수", overlaying="y", side="right", showgrid=False),
            legend_title="항목",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig)
        # 📌 구 선택 시 데이터프레임 출력 로직 (인덱스 제거)
        if selected_gu != "전체":
            st.write(f"📍 {selected_gu} 데이터 프레임 확인:")
            st.dataframe(merged_df[merged_df["구별"] == selected_gu].style.hide(axis="index"))
        else:
            st.write("📍 전체 데이터 프레임 확인:")
            st.dataframe(merged_df.style.hide(axis="index"))


    elif selected_analysis == menu[1]:
        st.subheader(menu[1])
        # 📌 Streamlit UI - 구 선택 추가
        selected_gu = st.selectbox("구 선택", ["전체"] + list(merged_df["구별"].unique()))

        # ✅ 선택한 구에 해당하는 동만 필터링
        if selected_gu != "전체":
            filtered_df = merged_df[merged_df["구별"] == selected_gu]
        else:
            filtered_df = merged_df  # 전체 구 표시

        if selected_gu != "전체":
            filtered_df = merged_df[merged_df["구별"] == selected_gu]
        else:
            filtered_df = merged_df

        # 반려동물이 많은 순으로 정렬
        missing_hospital = filtered_df[filtered_df["병원 개수"] == 0].sort_values("반려동물수", ascending=False)
        missing_pharmacy = filtered_df[filtered_df["약국 개수"] == 0].sort_values("반려동물수", ascending=False)
        
        st.write("**❌🏥 병원이 없는 지역:**")
        st.dataframe(missing_hospital)
        st.write("**❌💊 약국이 없는 지역:**")
        st.dataframe(missing_pharmacy)

    # 📌 병원/약국 접근성 분석
    elif selected_analysis == menu[2]:
        st.subheader(menu[2])

        # 📌 Streamlit UI - 구 선택 추가
        selected_gu = st.selectbox("구 선택", ["전체"] + list(merged_df["구별"].unique()))

        # ✅ 선택한 구에 해당하는 동만 필터링
        if selected_gu != "전체":
            filtered_df = merged_df[merged_df["구별"] == selected_gu]
        else:
            filtered_df = merged_df  # 전체 구 표시

        # ✅ 병원 및 약국 개수 계산
        hospital_counts = hospital_df.groupby("동별").size().reset_index(name="병원 개수")
        pharmacy_counts = pharmacy_df.groupby("동별").size().reset_index(name="약국 개수")
        pet_hospital_data = pet_df.merge(hospital_counts, on="동별", how="left").merge(pharmacy_counts, on="동별", how="left")
        pet_hospital_data.fillna(0, inplace=True)

        # ✅ 선택한 구 필터 적용
        if selected_gu != "전체":
            pet_hospital_data = pet_hospital_data[pet_hospital_data["구별"] == selected_gu]
        
        menu1=["산점도 (반려동물 수 대비 병원/약국 개수)", "막대그래프 (동별 병원/약국 개수)"]
        chart_option = st.radio("📊 그래프 선택", menu1)

        if chart_option == menu1[0]:
            # ✅ Scatter Plot: 반려동물 수 대비 병원/약국 개수 (Hover에 동 이름 추가)
            fig = px.scatter(pet_hospital_data, 
                            x="반려동물수", 
                            y=["병원 개수", "약국 개수"], 
                            labels={"value": "개수", "variable": "항목"},
                            title=f"{selected_gu} 반려동물수와 병원/약국 개수 관계" if selected_gu != "전체" else "반려동물수와 병원/약국 개수 관계",
                            hover_name="동별")  # ✅ 동별 정보 추가
            st.plotly_chart(fig)

        elif chart_option == menu1[1]:
            # ✅ Bar Chart: 동별 병원/약국 개수 비교
            fig = px.bar(pet_hospital_data, 
                        x="동별", 
                        y=["병원 개수", "약국 개수"], 
                        title=f"{selected_gu} 동별 병원/약국 개수 비교" if selected_gu != "전체" else "동별 병원/약국 개수 비교",
                        barmode="group")  # ✅ 병원과 약국을 그룹화하여 비교
            st.plotly_chart(fig)


    elif selected_analysis == menu[3]:
        st.subheader(menu[3])

        menu2=["병원 대비 반려동물수", "약국 대비 반려동물수"]
        analysis_option = st.radio("분석 선택", menu2)

        if analysis_option == menu2[0]:
            correlation1 = merged_df[["반려동물수", "병원 개수"]].corr(numeric_only=True).loc["반려동물수", "병원 개수"]
            st.write(f"**반려동물수와 병원 개수 간의 상관계수:** {correlation1:.2f}")

            fig1 = px.scatter(merged_df, x="반려동물수", y="병원 개수", trendline="ols",
                            labels={"반려동물수": "반려동물수", "병원 개수": "병원 개수"},
                            title="반려동물수 대비 병원 개수 회귀 분석")
            st.plotly_chart(fig1)

        elif analysis_option == menu2[1]:
            correlation2 = merged_df[["반려동물수", "약국 개수"]].corr(numeric_only=True).loc["반려동물수", "약국 개수"]
            st.write(f"**반려동물수와 약국 개수 간의 상관계수:** {correlation2:.2f}")

            fig2 = px.scatter(merged_df, x="반려동물수", y="약국 개수", trendline="ols",
                            labels={"반려동물수": "반려동물수", "약국 개수": "약국 개수"},
                            title="반려동물수 대비 약국 개수 회귀 분석")
            st.plotly_chart(fig2)

        if st.button("📖 상관계수란?"):
            st.markdown(
                """
                <div style="padding:10px; border-radius:5px; background-color:#eef7ff;">
                <h4>📊 반려동물 수와 병원/약국 개수의 상관계수 해석</h4>
                <ul>
                    <li><b> r > 0.7</b> → 반려동물이 많을수록 병원(약국)도 많음</li>
                    <li><b> 0.4 ≤ r ≤ 0.7</b> → 반려동물이 많을수록 병원(약국) 개수가 증가하는 경향이 있음</li>
                    <li><b> r ≈ 0</b> → 반려동물 수와 병원(약국) 개수는 별다른 관계가 없음</li>
                    <li><b> r < 0</b> → 반려동물이 많을수록 병원(약국)이 적어지는 경향이 있음</li>
                </ul>
                <p>📍 <b>쉽게 말해, 값이 1에 가까울수록 관련성이 크고, 0이면 관계가 없으며, -1이면 반대 방향으로 강한 관계가 있다는 의미입니다!</b> 😊</p>
                </div>
                """,
                unsafe_allow_html=True
            )


            


    st.sidebar.write("📌 분석할 항목을 선택하세요.")
