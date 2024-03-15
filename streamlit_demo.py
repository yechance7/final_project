import streamlit as st
import json
import requests
from bs4 import BeautifulSoup
import os


def search_stores(data, user_input):
    matching_items = []
    for item in data:
        if user_input in item["title"] or user_input in item["content"]:
            matching_items.append({"id": item["id"], "title": item["title"], "content": item["content"],"view_count": item["view_count"],"alias": item["alias"]})
    return sorted(matching_items, key=lambda x: x['view_count'], reverse=True)

def search_items(data, user_input):
    matching_items = []
    for item in data:
        content = item.get("content", "")
        simple_contents = item.get("simple_contents", "")
        if user_input in content or (simple_contents and user_input in simple_contents):
            matching_items.append({"id": item["id"], "content": item["content"], "simple_contents": item["simple_contents"],"view_count": item["view_count"]})
    return sorted(matching_items, key=lambda x: x['view_count'], reverse=True)

def crawl_website(url):
    # URL에서 HTML을 가져옵니다.
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 첫 번째 이미지 태그를 찾습니다.
    img_tag = soup.find('img')
    
    # 이미지가 없는 경우 예외 처리합니다.
    if img_tag is None:
        st.error("이미지를 찾을 수 없습니다.")
        return
    
    # 이미지를 표시합니다.
    return img_tag['src']




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
                st.write(f"스토어에서 찾은 아이템: {len(matching_stores)}")
                for store in matching_stores:
                    url = f"https://ctee.kr/place/{store['alias']}"
                    #st.write(f"스토어 id: {store['id']}, title: {store['title']}, content: {store['content']}")
                    st.image(crawl_website(url), caption=f"스토어 id: {store['id']}, title: {store['title']}, content: {store['content']}", use_column_width=True)
            else:
                st.write("스토어 검색 결과가 없습니다.")

            st.write("----------------------------------------------")

            # 아이템 검색 및 결과 출력
            matching_items = search_items(item_data, user_input)
            if matching_items:
                st.write(f"아이템에서 찾은 아이템 총 {len(matching_items)}:")
                for item in matching_items:
                    st.write(f"아이템 id: {item['id']}, simple_contents: {item['simple_contents']}, content: {item['content']}")
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
