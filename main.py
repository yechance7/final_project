import streamlit as st

def main():
    st.title("CTEE")
    st.write("환영합니다! 찾으시는 굿즈 또는 스트리머를 입력하세요.")

    # 페이지 내용 추가
    st.header("검색")

    # 사용자 입력 받기
    user_input = st.text_input("찾고 계신 크리에이터 또는 콘텐츠가 있나요?", "")

    if st.button("확인"):
        st.write("최근 검색어:", user_input)

if __name__ == "__main__":
    main()
