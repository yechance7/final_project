import json
import streamlit as st

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import shutil

from PIL import Image
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_website(url):   
    # Chrome 드라이버 서비스 생성
    #service = Service('chromedriver.exe')
    service=Service(ChromeDriverManager(driver_version="122.0.6261.129").install())
    options= webdriver.ChromeOptions()

    # Chrome 드라이버 초기화
    #driver = webdriver.Chrome(service=service)
    with webdriver.Chrome(service=service, options=options) as driver:
        # 웹페이지 로드
        driver.get(url)

        # 이미지 태그 찾기
        img_element = driver.find_element(By.TAG_NAME, 'img')

        # 이미지 URL 가져오기
        img_src = img_element.get_attribute('src')

    return img_src

def get_chromedriver_path() -> str:
    return shutil.which('chromedriver')

def get_webdriver_service() -> Service:
    service = Service(
        executable_path=get_chromedriver_path()
    )
    return service

def crawl_image_store(url):
    # 웹페이지 요청
    response = requests.get(url)
    
    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 이미지 태그 찾기
    img_element = soup.find('img', class_='profile_img')  # 예시 클래스 이름, 실제로 사용하는 클래스명으로 수정해야 합니다.
    
    # 이미지 URL 가져오기
    img_url = img_element['src']
    
    # 이미지 다운로드
    img_response = requests.get(img_url)
    
    # 이미지를 PIL Image로 변환
    image = Image.open(BytesIO(img_response.content))

    return image


def crawl_image_item(url):
    
    # Chrome 드라이버 서비스 생성
    service = Service('chromedriver.exe')

    # Chrome 드라이버 초기화
    driver = webdriver.Chrome(service=service)

    # 웹페이지 로드
    driver.get(url)

    # 이미지 태그 찾기
    img_element = driver.find_element(By.CLASS_NAME, 'item_img')

    # 이미지 데이터 가져오기
    img_data = img_element.screenshot_as_png

    # 이미지 데이터를 PIL Image로 변환
    image = Image.open(BytesIO(img_data))

    # 브라우저 닫기
    driver.quit()

    return image




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



def main(stores_data, item_data):
    st.title("CTEE")
    st.write("환영합니다! 디지털 콘텐츠 판매를 쉽고 빠르게 크티 플레이스")

    st.header("검색")
    user_input = st.text_input("찾고 계신 크리에이터 또는 콘텐츠가 있나요?", "")

    if st.button("검색"):
        st.write("최근 검색어:", user_input)

        if not user_input:
            st.write("검색어를 입력하세요.")
        else: 
            matching_stores = search_stores(stores_data, user_input)
            if matching_stores:
                st.write(f"스토어에서 찾은 아이템: {len(matching_stores)}")
                for store in matching_stores:
                    url = f"https://ctee.kr/place/{store['alias']}"
                    #st.write(f"스토어 id: {store['id']}, title: {store['title']}, content: {store['content']}")
                    st.image(crawl_image_store(url), caption=f"스토어 id: {store['id']}, title: {store['title']}, content: {store['content']}", use_column_width=True)
            else:
                st.write("스토어 검색 결과가 없습니다.")

            st.write("----------------------------------------------")

            # 아이템 검색 및 결과 출력
            matching_items = search_items(item_data, user_input)
            if matching_items:
                st.write(f"아이템에서 찾은 아이템 총 {len(matching_items)}:")
                for item in matching_items:
                    url = f"https://ctee.kr/item/store/{item['id']}"
                    #st.write(f"아이템 id: {item['id']}, simple_contents: {item['simple_contents']}, content: {item['content']}")
                    st.image(crawl_image_item(url), caption=f"아이템 id: {item['id']}, simple_contents: {item['simple_contents']}, content: {item['content']}", use_column_width=True)
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
