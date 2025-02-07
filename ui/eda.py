import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def run_eda():

    pet_df = pd.read_csv("data/pet_data.csv")
    hospital_df = pd.read_csv("data/hospitals.csv")
    pharmacy_df = pd.read_csv("data/pharmacies.csv")

    # 사이드바
    st.sidebar.title("📊 데이터 탐색 (EDA)")

    # 데이터 선택 옵션
    menu=["동 별 반려동물/병원/약국 개수 비교",
        "병원/약국이 없는 지역 찾기",
        "병원/약국 산점도 분석",
        "반려동물 수와 병원 개수의 상관관계"]
    
    selected_analysis = st.sidebar.radio("📌 분석할 항목을 선택하세요.", menu)
    pet_hospital_counts = pet_df.groupby(["구별", "동별"])["반려동물수"].sum().reset_index()
    hospital_counts = hospital_df.groupby(["구별", "동별"])["사업장명"].count().reset_index()
    hospital_counts.rename(columns={"사업장명": "병원 개수"}, inplace=True)
    pharmacy_counts = pharmacy_df.groupby(["구별", "동별"])["사업장명"].count().reset_index()
    pharmacy_counts.rename(columns={"사업장명": "약국 개수"}, inplace=True)

    merged_df = pet_hospital_counts.merge(hospital_counts, on=["구별", "동별"], how="left")\
                                .merge(pharmacy_counts, on=["구별", "동별"], how="left")

    merged_df.fillna(0, inplace=True)
    # 병원/약국 개수를 정수형으로 변환
    merged_df["병원 개수"] = merged_df["병원 개수"].astype(int)
    merged_df["약국 개수"] = merged_df["약국 개수"].astype(int)

    merged_df = merged_df.sort_values(by=['구별', '동별']).reset_index(drop=True)


    # EDA 분석 수행
    if selected_analysis == menu[0]:
        st.subheader(menu[0])
        # 구 선택 추가
        st.markdown("""
        📍차트를 이렇게 활용해보세요. 
                    
        구 선택을 통해 각 동별 **반려동물 수와 동물병원 및 동물약국 개수를 한눈에 비교**할 수 있습니다.
        - **X축**: 지역별 동 이름  
        - **Y축**: 반려동물 수(파란색), 병원 개수(빨간색), 약국 개수(초록색)       
                    """)
        selected_gu = st.selectbox("구 선택", ["전체"] + list(merged_df["구별"].unique()))

        
        # 선택한 구에 해당하는 동만 필터링
        if selected_gu != "전체":
            filtered_df = merged_df[merged_df["구별"] == selected_gu]
        else:
            filtered_df = merged_df  # 전체 구 표시

        fig = go.Figure()
        fig.add_trace(go.Bar(x=filtered_df["동별"], y=filtered_df["반려동물수"], name="반려동물 수", marker_color="blue"))
        fig.add_trace(go.Scatter(x=filtered_df["동별"], y=filtered_df["병원 개수"], name="병원 개수", mode='lines+markers', line=dict(color='red'), yaxis='y2'))
        fig.add_trace(go.Scatter(x=filtered_df["동별"], y=filtered_df["약국 개수"], name="약국 개수", mode='lines+markers', line=dict(color='green'), yaxis='y2'))
        
        fig.update_layout(
            title=f"📍{selected_gu} 동별 반려동물 수와 병원/약국 개수 비교" if selected_gu != "전체" else "동별 반려동물 수 및 병원/약국 개수 비교",
            xaxis_title="동별",
            yaxis=dict(title="반려동물 수", side="left"),
            yaxis2=dict(title="병원/약국 개수", overlaying="y", side="right", showgrid=False),
            legend_title="항목",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig)
        # 구 선택 시 데이터프레임 출력 인덱스 숨기기
        if selected_gu != "전체":
            st.write(f"📍 {selected_gu} 데이터 수치 확인:")
            st.dataframe(merged_df[merged_df["구별"] == selected_gu].style.hide(axis="index"))
        else:
            st.write("📍 전체 데이터 수치 확인:")
            st.dataframe(merged_df.style.hide(axis="index"))


    elif selected_analysis == menu[1]:
        st.subheader(menu[1])
        st.markdown("""
        📍구 선택을 통해 병원, 약국이 없는 지역을 확인하세요.  
                    """)
        # 구 선택 추가
        selected_gu = st.selectbox("구 선택", ["전체"] + list(merged_df["구별"].unique()))

        # 선택한 구에 해당하는 동만 필터링
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

    # 병원/약국 접근성 분석
    elif selected_analysis == menu[2]:
        st.subheader(menu[2])

        # Streamlit UI - 구 선택 추가
        selected_gu = st.selectbox("구 선택", ["전체"] + list(merged_df["구별"].unique()))

        # 선택한 구에 해당하는 동만 필터링
        if selected_gu != "전체":
            filtered_df = merged_df[merged_df["구별"] == selected_gu]
        else:
            filtered_df = merged_df  # 전체 구 표시

        # 동별 병원 및 약국 개수 계산
        hospital_counts = hospital_df.groupby("동별").size().reset_index(name="병원 개수")
        pharmacy_counts = pharmacy_df.groupby("동별").size().reset_index(name="약국 개수")
        pet_hospital_data = pet_df.merge(hospital_counts, on="동별", how="left").merge(pharmacy_counts, on="동별", how="left")
        pet_hospital_data.fillna(0, inplace=True)

        # 선택한 구 필터 적용
        if selected_gu != "전체":
            pet_hospital_data = pet_hospital_data[pet_hospital_data["구별"] == selected_gu]
        
        menu1=["산점도 (반려동물 수 대비 병원/약국 개수)", "막대그래프 (동별 병원/약국 개수)"]
        chart_option = st.radio("📊 그래프 선택", menu1)

        if chart_option == menu1[0]:
            
            # 반려동물 수 대비 병원/약국 개수 산점도 그래프
            fig = px.scatter(pet_hospital_data, 
                            x="반려동물수", 
                            y=["병원 개수", "약국 개수"], 
                            labels={"value": "개수", "variable": "항목"},
                            title=f"{selected_gu} 반려동물수와 병원/약국 개수 관계" if selected_gu != "전체" else "반려동물수와 병원/약국 개수 관계",
                            hover_name="동별")  # 동별 정보 추가
            st.plotly_chart(fig)

            with st.container():
                st.markdown(
                    """
                    <div style="
                        background-color: #dff0d8; 
                        padding: 15px; 
                        border-radius: 10px;
                        border: 1px solid #c3e6cb;">
                    
                    #### 📊 반려동물 수 대비 병원/약국 개수 산점도 해석

                    ##### - X축(반려동물 수) → 반려동물이 많은 지역
                    - X축 값이 클수록 반려동물 양육 가구가 많은 지역
                    - 오른쪽으로 갈수록 반려동물 수요가 높은 지역

                    ##### - Y축(병원/약국 개수) → 의료 인프라 수준
                    - Y축 값이 클수록 해당 지역의 병원·약국 개수 증가
                    - 위쪽으로 갈수록 동물 의료 인프라가 풍부한 지역

                    ### 🏥 결론  
                    <p>✔ <b>반려동물은 많지만 병원·약국이 부족한 지역(X축에 가까운 지역)</b>은 <br> 신규 병원·약국 개설이 필요한 후보지입니다.</p>  
                    <p>✔ <b>병원·약국이 많지만 반려동물이 적은 지역(Y축에 가까운 지역)</b>은 <br> 의료 인프라가 과포화 상태일 가능성이 높습니다.</p>  
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        elif chart_option == menu1[1]:
            st.text("📍 동별 병원/약국 개수를 차트로 비교합니다.")
            # 동별 병원/약국 개수 막대 그래프
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

        with st.container():
                st.markdown(
                    """
                    <div style="
                        background-color: #dff0d8; 
                        padding: 15px; 
                        border-radius: 10px;
                        border: 1px solid #c3e6cb;">
                    
                    #### 📊 반려동물 수와 병원/약국 개수의 상관계수 해석

                     1️⃣ r > 0.7</b> → 반려동물이 많을수록 병원(약국)도 많음  
                     2️⃣ 0.4 ≤ r ≤ 0.7</b> → 반려동물이 많을수록 병원(약국) 개수가 증가하는 경향이 있음  
                     3️⃣ r ≈ 0</b> → 반려동물 수와 병원(약국) 개수는 별다른 관계가 없음  
                     4️⃣ r < 0</b> → 반려동물이 많을수록 병원(약국)이 적어지는 경향이 있음

                    **즉, 반려동물수가 많을수록 병원, 약국도 많습니다!** 😊

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            


    
