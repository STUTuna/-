import requests
import urllib.parse
from bs4 import BeautifulSoup
import re

baseUrl = "https://www.ouyun.com.tw"


# 移除價格資訊
def removePrice(text):
    pattern = r"\$\d+"  # 匹配$后面的数字
    filtered_text = re.sub(pattern, "", text)
    return filtered_text


# 移除提醒文字
def removeReminder(text):
    pattern = r"本圖片顏色僅供參考.*|產品尺寸、規格若有變更.*"  # 匹配提醒文字的模式
    filtered_text = re.sub(pattern, "", text)
    return filtered_text


# 移除多餘的空行
def removeExtraLines(text):
    filtered_text = re.sub(r"\n\s*\n", "\n", text)
    return filtered_text.strip()


# 過濾說明文字
def filterDescription(text):
    filtered_text = removePrice(text)
    filtered_text = removeReminder(filtered_text)
    filtered_text = removeExtraLines(filtered_text)
    return filtered_text


# 檢查有沒有分頁 根據class pagination是否存在來判斷
def hasPagination(soup):
    pagination = soup.find("ul", class_="pagination")
    if pagination:
        return True
    else:
        return False


# 獲取所有分頁連結 (排除上下頁的控制項:class不包含controls)
def getPaginationLinks(soup) -> list:
    pageLinks = []  # 分頁連結
    pagination = soup.find("ul", class_="pagination")
    page_links = pagination.find_all("li")
    for page_link in page_links:
        if page_link.find("a", class_="controls"):
            continue
        else:
            page_link.find("a").get("href")
            pageLinks.append(page_link.find("a").get("href"))
    return pageLinks


# 取得產品目錄頁面的所有產品連結
def getProductLinks(menuLink) -> list:
    productLinks = []  # 產品連結
    # 發送GET請求獲取頁面內容
    response = requests.get(menuLink)
    html_content = response.text
    # 使用BeautifulSoup解析頁面內容
    soup = BeautifulSoup(html_content, "html.parser")
    ul_block = soup.find("ul", class_="product-list")
    # 找到所有包含産品信息的<li>元素
    product_list = ul_block.find_all("li")
    # 遍曆産品列錶並提取所需信息
    for product in product_list:
        # 獲取産品詳情鏈接
        productLink = product.find("a", string="查看更多").get("href")
        productLinks.append(productLink)
    return productLinks


# 取得產品詳情頁面的產品信息
def getProductDetail(productLink):
    product = {}  # 產品
    # 發送GET請求獲取頁面內容
    response = requests.get(productLink)
    html_content = response.text
    # 使用BeautifulSoup解析頁面內容
    soup = BeautifulSoup(html_content, "html.parser")
    # 獲取產品名稱
    product_name = soup.find("div", class_="product-name").text.strip()
    # 獲取產品說明
    product_description = soup.find("div", class_="product-text").text.strip()
    # 獲取所有產品圖片連結 父元素為 ul list-h
    product_images = soup.find("ul", class_="list-h").find_all("img")
    product_images_links = []
    # 遍歷產品圖片連結
    for product_image in product_images:
        # 取得完整的圖片連結
        full_img_path = urllib.parse.urljoin(baseUrl, product_image.get("src"))
        product_images_links.append(full_img_path)

    product["name"] = product_name
    product["description"] = filterDescription(product_description)
    product["images"] = product_images_links
    return product


# 主函數
def main():
    category_url = "https://www.ouyun.com.tw/products/1_10/1.htm"  # 主管桌
    allProductLinks = []  # 所有產品連結
    pageLinks = [category_url]  # 分頁連結
    # 發送GET請求獲取頁面內容
    response = requests.get(category_url)
    html_content = response.text

    # 使用BeautifulSoup解析頁麵內容
    soup = BeautifulSoup(html_content, "html.parser")

    # 若有分頁 就獲取分頁連結
    if hasPagination(soup):
        # 獲取所有分頁連結
        pageLinks = getPaginationLinks(soup)

    for pageLink in pageLinks:
        # 獲取每個分頁的產品連結
        singlePageProductLinks = getProductLinks(pageLink)
        # 將每個分頁的產品連結加入到所有產品連結中
        allProductLinks.extend(singlePageProductLinks)

    print("所有產品連結:", allProductLinks)

    # 遍歷產品 獲取所有產品詳情頁面的產品信息
    for productLink in allProductLinks:
        product = getProductDetail(productLink)
        print("產品名稱:", product["name"])
        print("產品說明:", product["description"])
        print("產品圖片連結:", product["images"])
        print("=====================================")

    return


main()
