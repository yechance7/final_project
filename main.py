import streamlit as st
import json

def search_stores(data, user_input):
    matching_items = []
    for item in data:
        if user_input in item["title"] or user_input in item["content"]:
            matching_items.append(item["id"])
    return matching_items

def search_items(data, user_input):
    matching_items = []
    for item in data:
        if user_input in item["content"]:
            matching_items.append(item["id"])
    return matching_items

def main(stores_data, item_data):
    st.title("CTEE")
    st.write("환영합니다! 디지털 콘텐츠 판매를 쉽고 빠르게 크티 플레이스")

    # 페이지 내용 추가
    st.header("검색")

    # 사용자 입력 받기
    user_input = st.text_input("찾고 계신 크리에이터 또는 콘텐츠가 있나요?", "")

    if st.button("검색"):
        st.write("최근 검색어:", user_input)

        # 사용자 입력이 없는 경우 처리
        if not user_input:
            st.write("검색어를 입력하세요.")
        else:
            # 스토어 검색 및 결과 출력
            matching_stores = search_stores(stores_data, user_input)
            if matching_stores:
                st.write("스토어에서 찾은 아이템 번호:")
                for store_id in matching_stores:
                    st.write(f"스토어 번호: {store_id}")
            else:
                st.write("스토어 검색 결과가 없습니다.")

            # 아이템 검색 및 결과 출력
            matching_items = search_items(item_data, user_input)
            if matching_items:
                st.write("아이템에서 찾은 아이템 번호:")
                for item_id in matching_items:
                    st.write(f"아이템 번호: {item_id}")
            else:
                st.write("아이템 검색 결과가 없습니다.")


if __name__ == "__main__":
    # stores.json 파일 로드
    with open('data/stores.json', 'r', encoding='utf-8') as f:
        stores_data = json.load(f)

    # item.json 파일 로드
    with open('data/items.json', 'r', encoding='utf-8') as f:
        item_data = json.load(f)
    main(stores_data, item_data)
