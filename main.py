import threading
import utils.util as util

# 要
categoryUrls = [
    "https://www.ouyun.com.tw/products/1_28/1.htm",  # 活動櫃
    "https://www.ouyun.com.tw/products/1_37/1.htm",  # 折合椅、鐵合椅
    "https://www.ouyun.com.tw/products/1_32/1.htm",  # 金庫
    # "https://www.ouyun.com.tw/products/1_31/1.htm",  # 鐵櫃
    # "https://www.ouyun.com.tw/products/1_86/1.htm",  # 辦公桌、書桌
    # "https://www.ouyun.com.tw/products/1_89/1.htm",  # 辦公椅、網椅
    "https://www.ouyun.com.tw/products/1_26/1.htm"  # 會議桌
    # "https://www.ouyun.com.tw/products/1_10/1.htm"  # 主管桌
]


def process_url(url):
    util.main(url)


threads = []
# 创建线程并启动
for url in categoryUrls:
    thread = threading.Thread(target=process_url, args=(url,))
    thread.start()
    threads.append(thread)

# 等待所有线程完成
for thread in threads:
    thread.join()
