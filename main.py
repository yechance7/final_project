import streamlit as st

def main():
    st.title("나의 홈페이지")
    st.write("환영합니다! 이 곳은 나의 홈페이지입니다.")

    # 페이지 내용 추가
    st.header("페이지 내용")
    st.write("이곳에 페이지 내용을 추가하세요.")

    # 사용자 입력 받기
    user_input = st.text_input("여기에 입력하세요", "")

    if st.button("확인"):
        st.write("입력한 내용:", user_input)

if __name__ == "__main__":
    main()
