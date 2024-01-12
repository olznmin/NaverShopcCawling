# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time 
from selenium.webdriver.common.by import By
import json
# 크롬 드라이버 자동 업데이트을 위한 모듈
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json 
import codecs

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# 불필요한 에러 메시지 삭제
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 드라이버 최신 버전 설정
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# 터미널에서 URL 입력 받기
url = input("웹 페이지 URL을 입력하세요: ")
# https://smartstore.naver.com/nande/products/477282453

# 웹페이지 해당 주소 이동
browser.get(url)

#페이지 로딩을 위한 대기 시간 설정
time.sleep(5)

# 페이지 소스코드 가져오기
html = browser.page_source

# JSON 데이터 추출을 위한 JavaScript 실행
json_data = browser.execute_script("return JSON.stringify(window.__PRELOADED_STATE__)")

# JSON 데이터가 있는지 확인
if json_data:
    # JSON 데이터 파싱
    parsed_json = json.loads(json_data)

    with codecs.open('output.json', 'w', encoding='utf-8') as file:
        json.dump(parsed_json, file, indent=4, ensure_ascii=False)

    print("JSON 파일이 성공적으로 저장되었습니다.")

with open('output.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 상품정보 데이터
name_extracted_data=""

# 첫 번째 경로
name_data_A = data.get('product', {}).get('A', None)

# 다른 경로 설정
name_data_B = data.get('productDetail', {}).get('A', {}).get('contents', None)

# 첫 번째 경로에서 데이터를 찾음
if name_data_A and 'name' in name_data_A:
    name_extracted_data = name_data_A['name']
# 첫 번째 경로에 데이터가 없다면 다른 경로에서 데이터를 찾음
elif name_data_B and 'name' in name_data_B:
    name_extracted_data = name_data_B['name']

print(name_extracted_data)

# 가격 데이터 
# 첫 번째 경로   [product][A][benefitsView]["discountedPrice"]   -> 두번째 경로 [productDetail][A][benefitsView]["discountedSalePrice"]
# 첫 번째 경로에서 데이터를 찾음
price_data = data.get('product', {}).get('A', {}).get('benefitsView', {}).get('discountedSalePrice', None)

# 첫 번째 경로에서 데이터가 없다면 다른 경로에서 데이터를 찾음
if price_data is None:
    # 다른 경로에서 데이터를 찾음
    productDetail_data = data.get('productDetail', {})
    A_data = productDetail_data.get('A', {}) if productDetail_data else {}
    contents_data = A_data.get('contents', {}) if A_data else {}
    benefitsView_data = contents_data.get('benefitsView', {}) if contents_data else {}
    price_data = benefitsView_data.get('discountedSalePrice', None)

print(price_data)  # 출력은 None 혹은 'discountedSalePrice'에 해당하는 값을 출력합니다.


#이미지 데이터
# 첫 번째 경로에서 데이터를 찾음
productImages_data = data.get('product', {}).get('A', {}).get('productImages', [])
url_data = productImages_data[0].get('url', None) if productImages_data else None

# 첫 번째 경로에서 데이터가 없다면 다른 경로에서 데이터를 찾음
if url_data is None:
    # 다른 경로에서 데이터를 찾음
    contents_data = data.get('productDetail', {}).get('A', {}).get('contents', {})
    productImages_data = contents_data.get('productImages', []) if contents_data else []
    url_data = productImages_data[0].get('url', None) if productImages_data else None

print(url_data)  # 출력은 None 혹은 'url'에 해당하는 값을 출력합니다.

#상품 옵션 데이터  
# 첫 번째 경로에서 데이터를 찾음
optionCombinations_data = data.get('product', {}).get('A', {}).get('optionCombinations', None)

# 첫 번째 경로에서 데이터가 없다면 다른 경로에서 데이터를 찾음
if optionCombinations_data is None:
    # 다른 경로에서 데이터를 찾음
    productDetail_data = data.get('productDetail',{})
    A_data = productDetail_data.get('A', {}) if productDetail_data else {}
    contents_data = A_data.get('contents', {}) if A_data else {}
    optionCombinations_data = contents_data.get('optionCombinations', None)
    print(optionCombinations_data)
else:
    print(optionCombinations_data)

#추가상품 데이터 
# 첫 번째 경로에서 데이터를 찾음
supplementProducts_data = data.get('product', {}).get('A', {}).get('supplementProducts', None)

# 첫 번째 경로에서 데이터가 없다면 다른 경로에서 데이터를 찾음
if supplementProducts_data is None:
    # 다른 경로에서 데이터를 찾음
    contents_data = data.get('productDetail', {}).get('A', {}).get('contents', {})
    supplementProducts_data = contents_data.get('supplementProducts', None)

print(supplementProducts_data)  # 출력은 None 혹은 'supplementProducts'에 해당하는 데이터를 출력합니다.


# 추출된 데이터 저장
extracted_data = [
    {
        "product_title": name_extracted_data,
        "price": price_data,
        "image": url_data,
        "option": optionCombinations_data,
        "optionCombinations": supplementProducts_data
    }
]

# JSON 파일로 저장
with codecs.open('extracted_data.json', 'w', encoding='utf-8') as file:
    json.dump(extracted_data, file, indent=4, ensure_ascii=False)

print("추출된 데이터가 성공적으로 저장되었습니다.")

browser.close()

# 햇반
# 침대 희망배송일 detail product https://shopping.naver.com/window-products/homeliving/7056179579?NaPm=ct%3Dlr9vnnol%7Cci%3Dshoppingwindow%7Ctr%3Dswl%7Chk%3D32ecc5c8e958a9a7ffe22be53a828301697cf523%7Ctrx%3D 