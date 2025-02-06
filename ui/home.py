import streamlit as st

#

def run_home():
    st.subheader("🐾 우리 동네에 반려동물 병원과 약국이 충분할까?")

    st.text(
        "반려동물과 함께하는 가족이 늘어나면서, 병원과 약국의 위치가 더욱 중요해졌어요. \n"
        "이 앱은 성남시의 반려동물 병원·약국 현황과 데이터를 분석해 부족한 지역을 쉽게 확인할 수 있도록 도와줍니다!"
    )

    st.header("🗺 주요 기능")

    st.subheader("📍 실시간 지도")
    st.write("- 동물병원·약국의 위치를 한눈에!")
    st.write("- **Google Maps API 적용**으로 지도에서 쉽게 확인")
    st.write("- **행정구역별 데이터 시각화**로 부족한 지역 확인 가능")

    st.subheader("📊 데이터 분석")
    st.write("- 성남시 **반려동물 등록 수, 병원·약국 분포 데이터** 기반")
    st.write("- **K-Means 클러스터링 분석**을 통해 병원·약국이 부족한 지역을 추천")

    st.subheader("🏥 신규 개업 추천")
    st.write("- **반려동물 대비 병원·약국이 부족한 지역을 분석**하여 예비 창업자에게 도움!")

    st.header("🔗 데이터 출처")
    st.write("- [경기도 성남시 반려동물 등록현황](https://www.data.go.kr/data/15047504/fileData.do)")
    st.write("- [경기도 성남시 동물병원 현황](https://www.data.go.kr/data/15000909/fileData.do)")
    st.write("- [경기도 성남시 동물약국 현황](https://www.data.go.kr/data/15061125/fileData.do)")

    st.write("📍 **우리 동네의 반려동물 의료 환경을 한눈에 확인해보세요!**")


    


    # 페이지 설명


