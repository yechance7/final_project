import json
import streamlit as st

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#streamlit run .\streamlit_demo.py

@st.cache
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

@st.cache
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
    matching_items = []
    matching_id=set()
    for item in data:
        if (item["id"] not in matching_id) and (user_input in item["title"] or user_input in item["content"]):
            matching_id.add(item["id"])
            matching_items.append({"id": item["id"], "title": item["title"], "content": item["content"],"view_count": item["view_count"],"alias": item['alias'],"updated_at":item["updated_at"]})
    return matching_items

def search_items(data, user_input):
    matching_items = []
    matching_id=set()
    for item in data:
        content = item.get("content", "")
        simple_contents = item.get("simple_contents", "")
        if (item["id"] not in matching_id) and (user_input in content or (simple_contents and user_input in simple_contents)) :
            matching_id.add(item["id"])
            matching_items.append({"id": item["id"], "content": item["content"], "simple_contents": item["simple_contents"],"view_count": item["view_count"],"updated_at":item['updated_at']})
    return matching_items

def sorting_result(options,matching_items):
    if options== '조회순':
        matching_items= sorted(matching_items, key=lambda x: x['view_count'], reverse=True)
    elif options ==  '최신순':
        matching_items= sorted(matching_items, key=lambda x: x['updated_at'], reverse=True)

    return matching_items

def main(stores_data, item_data):
    st.title("CTEE")
    st.write("환영합니다! 디지털 콘텐츠 판매를 쉽고 빠르게 크티 플레이스")

    st.header("검색")
    options = ['조회순', '최신순','오래된순']
    selected_option = st.selectbox('Select Option', options)
    user_input = st.text_input("찾고 계신 크리에이터 또는 콘텐츠가 있나요?", "")

    if st.button("검색"):
        st.write("최근 검색어:", user_input)

        if not user_input:
            st.write("검색어를 입력하세요.")
        else: 
            matching_items = search_items(item_data, user_input)
            matching_items=sorting_result(selected_option,matching_items)

            if matching_items:
                st.write(f"아이템에서 찾은 아이템 총 {len(matching_items)}:")
                data = []
                num_items = len(matching_items)
                num_items_per_row = min(num_items, 3)
                num_rows = (num_items + num_items_per_row - 1) // num_items_per_row

                for i in range(num_rows):
                    row = st.columns(num_items_per_row)
                    for j in range(num_items_per_row):
                        index = i * num_items_per_row + j
                        if index < num_items:
                            item = matching_items[index]
                            url = f"https://ctee.kr/item/store/{item['id']}"
                            with row[j]:
                                caption=f"id: {item['id']}, simple_contents: {item['simple_contents']}, content: {item['content']}"
                                #st.image(crawl_image_item(url),caption=caption , width=200, use_column_width=False)
                                #st.markdown(f"[![{Link}]({crawl_image_item(url)})]({url})")
                                st.markdown(f"<a href='{url}'><img src='{crawl_image_item(url)}' width='200'></a>", unsafe_allow_html=True)
                                st.write(f"<span style='font-size:14px; color:gray;'>{caption}</span>", unsafe_allow_html=True)

            else:
                st.write("아이템 검색 결과가 없습니다.")

            st.write("----------------------------------------------")
            matching_stores = search_stores(stores_data, user_input)
            matching_items=sorting_result(selected_option,matching_items)

            if matching_stores:
                st.write(f"스토어에서 찾은 아이템: {len(matching_stores)}")
                
                # 이미지를 한 줄에 출력하기 위해 열 생성
                num_images = len(matching_stores)
                num_images_per_row = min(num_images, 4)
                num_rows = (num_images + num_images_per_row - 1) // num_images_per_row

                for i in range(num_rows):
                    row = st.columns(num_images_per_row)
                    for j in range(num_images_per_row):
                        index = i * num_images_per_row + j
                        if index < num_images:
                            store = matching_stores[index]
                            url = f"https://ctee.kr/place/{store['alias']}"
                            with row[j]:
                                caption=f"id: {store['id']}, title: {store['title']}, content: {store['content']}"
                                #st.image(crawl_image_store(url), caption= caption, width=150, use_column_width=False)
                                st.markdown(f"<a href='{url}'><img src='{crawl_image_store(url)}' width='150'></a>", unsafe_allow_html=True)
                                st.markdown(f"<span style='font-size:14px; color:gray;'>{caption}</span>", unsafe_allow_html=True)

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
