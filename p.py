from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def crawl_website(url):   
    # Chrome 드라이버 서비스 생성
    service = Service('chromedriver.exe')

    # Chrome 드라이버 초기화
    driver = webdriver.Chrome(service=service)

    # 웹페이지 로드
    driver.get(url)

    # 이미지 태그 찾기
    img_element = driver.find_element(By.TAG_NAME, 'img')

    # 이미지 URL 가져오기
    img_src = img_element.get_attribute('src')

    # 브라우저 닫기
    driver.quit()

    return img_src

url = "https://ctee.kr/place/Kimsagua"
print(crawl_website(url))

