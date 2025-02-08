# 🏥 성남시 동물병원·약국 입지 분석 앱  
데이터 기반으로 **성남시 내 동물병원 및 약국의 최적 입지를 분석**하는 AI 웹 애플리케이션  

---

## 📌 앱 개요  
이 애플리케이션은 **성남시 동물병원·약국의 현황과 반려동물 등록 수를 분석하여 입지 선정 인사이트를 제공**합니다.  
**K-Means 클러스터링을 활용한 병원·약국 입지 분석**, **데이터 기반의 수요-공급 비교**를 통해 **수의사 및 약사분들이 최적의 개업 위치를 찾는 데 도움을 줍니다.**  

사용자는 **데이터 기반으로 특정 지역의 동물병원 및 약국 부족 여부를 확인** 할 수 있습니다.

---

## 📀 **사용 기술 및 라이브러리**  

| **분야** | **라이브러리** |
|------|------|
| **웹 프레임워크** | Streamlit |
| **데이터 처리** | Pandas, Geopandas |
| **머신러닝 모델** | Scikit-learn |
| **데이터 시각화** | Matplotlib, Plotly, Folium, streamlit_folium |
| **지도 데이터** | Folium, GeoJSON |
| **모델 저장 및 로드** | Joblib |

---

## 🍿 **주요 기능**  

### 🗺 1. 성남시 동물병원·약국 지도 시각화  
✅ **반려동물 등록 수 및 병원·약국 분포를 한눈에 확인**  
✅ **행정동 기준으로 데이터를 정리하여, 신흥1동·신흥2동 등은 ‘신흥동’으로 통합**  
✅ **Google Maps API를 활용하여 위도·경도 정보를 추가하고, 지도 위에 마커 시각화**  
✅ **GeoJSON 데이터를 활용해 성남시 행정구역 경계를 지도에 표시**  

---

### 📊 2. 반려동물 수 대비 병원·약국 개수 비교  
✅ **각 동별 반려동물 수와 병원·약국 개수를 직관적으로 비교하는 그래프 제공**  
✅ **산점도 및 바 그래프로 지역별 밀집도를 확인 가능**  
✅ **병원·약국이 부족한 지역을 쉽게 식별하여 신규 개업 전략 수립에 도움**  

---

### 📍 3. K-Means 클러스터링을 통한 병원·약국 입지 분석  
✅ **위도·경도, 반려동물 수, 병원·약국 개수를 기준으로 K-Means 클러스터링 수행**  
✅ **엘보우 메소드를 사용하여 최적의 클러스터 개수를 탐색**  
✅ **병원·약국·수요를 토대로 나눠진 클러스터를 지도 위에 색상별로 표시하여 쉽게 인사이트 도출**  

---

### 🏥 4. 신규 개업 입지 추천  
✅ **K-Means 클러스터링을 기반으로 반려동물 대비 병원·약국이 부족한 지역 분석**  
✅ **반려동물 수는 많지만 병원·약국이 부족한 지역 → 개업 추천 지역으로 선정**  
✅ **병원 개설 후 약국과의 협업 가능성도 고려할 수 있도록 병원, 약국위치 시각적 데이터 제공**  

---

## 🚀 Streamlit 배포  
1️⃣ **로컬 환경에서 앱 테스트 후 `requirements.txt`를 생성하여 패키지 관리**  
2️⃣ **GitHub에 애플리케이션 업로드**  
3️⃣ **Streamlit Cloud를 활용하여 외부에서 접근 가능하도록 배포**  


---

## 🏗 **개발 프로세스**  

### **📌 데이터 수집 및 전처리**  
- Kaggle 및 공공데이터포털에서 **성남시 동물병원·약국·반려동물 등록 데이터 수집**  
- **행정동 기준 정리** (신흥1동, 신흥2동 → 신흥동)  
- **병원·약국 주소를 위도·경도로 변환**
- 위례동의 반려동물 등록 수 데이터를 확보하려 했으나, 성남시, 서울 송파구, 경기도 전체 데이터를 모두 확인했음에도 불구하고 관련 정보를 찾을 수 없어 제외됨 (추후 데이터 확보시 추가예정)

### **📌 병원·약국 클러스터링 분석**  
- **K-Means 클러스터링을 활용한 입지 분석**  
- **엘보우 기법으로 최적 클러스터 개수 탐색 (4~6개 사이로 사용자가 직접 설정하고 비교가능)**  
- **병원,약국의 위도와 경도(공간적 분포 고려), 동물 소유자 수, 반려동물 수(수요 분석), 병원·약국 개수(공급 측면 분석), 동별 병원당 반려동물 수, 약국당 반려동물 수 (밀집도 분석)를 기준**으로 클러스터를 나눔

### **📌 신규 개업 입지 추천**  
- **병원당 반려동물 수, 약국당 반려동물 수를 계산하여 밀집도 분석**  
- **신규 개업 추천 지역을 시각화하여 보여줌**  


---

## 🎯 **이 앱을 통해 기대할 수 있는 효과**  
✅ **데이터 기반으로 신규 병원·약국 개업 시 최적 입지를 선정 가능**  
✅ **경쟁이 적고 수요가 높은 지역을 식별하여 보다 전략적인 의사결정 지원**  
✅ **기존 병원·약국과의 협업 가능성 탐색 및 최적의 공급 네트워크 구축 지원**  

🚀 **이제 데이터를 활용해 성남시에서 가장 유망한 입지를 찾아보세요! 😊**

## 🔗 데이터 출처
- [경기도 성남시 반려동물 등록현황](https://www.data.go.kr/data/15047504/fileData.do)
- [경기도 성남시 동물병원 현황](https://www.data.go.kr/data/15000909/fileData.do)
- [경기도 성남시 동물약국 현황](https://www.data.go.kr/data/15061125/fileData.do)
- [대한민국 17개 광역시/도 행정동 GEOJSON 파일](https://github.com/raqoon886/Local_HangJeongDong)

### 📬 개발자 연락처  
📧 marurun66@gmail.com

---


