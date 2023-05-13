import requests
import urllib.parse
from bs4 import BeautifulSoup
import re
import csv

baseUrl = "https://www.ouyun.com.tw"

# 匯出CSV檔案


def exportToCsv(products, filename):
    print("匯出CSV檔案...")
    print("檔案名稱: " + filename)
    print("產品數量: " + str(len(products)))

    # fieldnames = ["description", "images", "name"]
    fieldnames = ["名稱", "描述", "分類", "圖片"]

    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            writer.writerow(product)


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

    product["名稱"] = product_name
    product["描述"] = filterDescription(product_description)
    product["圖片"] = ",".join(product_images_links)  # 圖片連結陣列轉字串
    return product


# 主函數
def main():
    csvFilenamePath = "./ouyun.csv"  # CSV檔案名稱
    # categoryUrl = "https://www.ouyun.com.tw/products/1_10/1.htm"  # 主管桌
    categoryUrl = "https://www.ouyun.com.tw/products/1_26/1.htm"  # 會議桌

    allProductLinks = []  # 所有產品連結
    products = []  # 產品
    pageLinks = [categoryUrl]  # 分頁連結
    # 發送GET請求獲取頁面內容
    response = requests.get(categoryUrl)
    html_content = response.text

    # 使用BeautifulSoup解析頁麵內容
    soup = BeautifulSoup(html_content, "html.parser")

    # 取得分類名稱 連結要和categoryUrl一樣
    category_name = soup.find_all("li", class_="active")[3].text.strip()
    csvFilenamePath = "./" + category_name + ".csv"
    # 若有分頁 就獲取分頁連結
    if hasPagination(soup):
        # 獲取所有分頁連結
        pageLinks = getPaginationLinks(soup)

    for pageLink in pageLinks:
        # 獲取每個分頁的產品連結
        singlePageProductLinks = getProductLinks(pageLink)
        # 將每個分頁的產品連結加入到所有產品連結中
        allProductLinks.extend(singlePageProductLinks)

    print("所有產品連結已取得")
    print("需要處理的產品數量:", len(allProductLinks))
    # 遍歷產品 獲取所有產品詳情頁面的產品信息
    for productLink in allProductLinks:
        # 印出需要處理的產品數量
        # 印出目前處理的第幾個產品
        print("正在處理第", allProductLinks.index(productLink) + 1, "個產品")
        # 獲取產品詳情頁面的產品信息
        product = getProductDetail(productLink)
        product["分類"] = category_name
        products.append(product)

    print("所有產品:", products)
    # 將產品資訊寫入CSV文件
    exportToCsv(products, csvFilenamePath)
    return


main()
