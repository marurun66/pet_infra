import streamlit as st


def run_home():
    st.subheader("Home")
    st.info("""
             이 앱은 성남시의 반려동물 데이터, 동물병원·약국 분포를 분석하고,\n
             부족한 지역을 예측하는 인공지능 모델을 제공합니다.
             """)
    
    st.write("데이터 출처: ")

    # 데이터 링크 목록
    links = {
        "📌 경기도 성남시 반려동물 등록현황": "https://www.data.go.kr/data/15047504/fileData.do",
        "🏥 경기도 성남시 동물병원 현황": "https://www.data.go.kr/data/15000909/fileData.do",
        "💊 경기도 성남시 동물약국 현황": "https://www.data.go.kr/data/15061125/fileData.do",
        "🗺️ 경기도 성남시 행정구역 GeoJSON": "https://github.com/vuski/admdongkor?utm_source=chatgpt.com",
    }
    # 버튼 형식으로 링크 생성
    for title, url in links.items():
        st.markdown(f"[🔗 {title}]({url})", unsafe_allow_html=True)

    


    # 페이지 설명


