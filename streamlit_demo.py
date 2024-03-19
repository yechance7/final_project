import json
import streamlit as st

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.service import Service
import shutil

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#streamlit run .\streamlit_demo.py

def crawl_image_item(url):
    
    options = Options() 
    options.add_argument("--headless=new")
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)

    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        
        img_element = driver.find_element(By.CLASS_NAME, 'item_img')
        img_url = img_element.get_attribute('src')

    return img_url

def crawl_image_store(url):
    
    options = Options() 
    options.add_argument("--headless=new")
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)

    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        
        img_element = driver.find_element(By.CLASS_NAME, 'profile_img')
        img_url = img_element.get_attribute('src')

    return img_url


def search_stores(data, user_input):
    matching_items = set()
    for item in data:
        if user_input in item["title"] or user_input in item["content"]:
            matching_items.add({"id": item["id"], "title": item["title"], "content": item["content"],"view_count": item["view_count"],"alias": item['alias']})
    matching_items=list(matching_items)
    return sorted(matching_items, key=lambda x: x['view_count'], reverse=True)

def search_items(data, user_input):
    matching_items = set()
    for item in data:
        content = item.get("content", "")
        simple_contents = item.get("simple_contents", "")
        if user_input in content or (simple_contents and user_input in simple_contents):
            matching_items.add({"id": item["id"], "content": item["content"], "simple_contents": item["simple_contents"],"view_count": item["view_count"]})
    matching_items=list(matching_items)
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
            # 아이템 검색 및 결과 출력
            matching_items = search_items(item_data, user_input)
            if matching_items:
                st.write(f"아이템에서 찾은 아이템 총 {len(matching_items)}:")
                for item in matching_items:
                    url = f"https://ctee.kr/item/store/{item['id']}"
                    st.write(f"아이템 id: {item['id']}, simple_contents: {item['simple_contents']}, content: {item['content']}")
                    #st.image(crawl_image_item(url), caption=f"아이템 id: {item['id']}, simple_contents: {item['simple_contents']}, content: {item['content']}", width=200,use_column_width=False)
            else:
                st.write("아이템 검색 결과가 없습니다.")

            st.write("----------------------------------------------")
            matching_stores = search_stores(stores_data, user_input)
            if matching_stores:
                st.write(f"스토어에서 찾은 아이템: {len(matching_stores)}")
                for store in matching_stores:
                    url = f"https://ctee.kr/place/{store['alias']}"
                    st.write(f"스토어 id: {store['id']}, title: {store['title']}, content: {store['content']}")
                    #st.image(crawl_image_store(url), caption=f"스토어 id: {store['id']}, title: {store['title']}, content: {store['content']}",width=200, use_column_width=False)
            else:
                st.write("스토어 검색 결과가 없습니다.")

            


if __name__ == "__main__":
    # stores.json 파일 로드
    with open('data/stores.json', 'r', encoding='utf-8') as f:
        stores_data = json.load(f)

    # item.json 파일 로드
    with open('data/items.json', 'r', encoding='utf-8') as f:
        item_data = json.load(f)
    

    main(stores_data, item_data)
