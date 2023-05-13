import threading
import util

categoryUrls = ["https://www.ouyun.com.tw/products/1_28/1.htm",  # 活動櫃
                "https://www.ouyun.com.tw/products/1_37/1.htm",  # 折合椅、鐵合椅
                "https://www.ouyun.com.tw/products/1_32/1.htm"  # 金庫
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
