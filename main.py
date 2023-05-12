import requests
from bs4 import BeautifulSoup


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
        product_name = product.find("div", class_="name").text.strip()
        # 獲取産品詳情鏈接
        product_link = product.find("a", text="查看更多").get("href")
        productLinks.append(product_link)
    return productLinks


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
    # 獲取產品詳情頁面的產品信息
    return
    ul_block = soup.find("ul", class_="product-list")
    # 找到所有包含産品信息的<li>元素
    product_list = ul_block.find_all("li")

    # 遍曆産品列錶並提取所需信息
    for product in product_list:
        # 取得產品名稱
        name_element = product.find("div", class_="name").text.strip()
        # 獲取産品詳情鏈接
        detail_link = product.find("a", text="查看更多").get("href")
        print("産品名稱:", name_element)
        print("産品鏈接:", detail_link)


main()
