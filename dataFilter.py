import utils.util as util
import os


# 讀取目錄下的所有csv檔案
def readAllCSVFilePath(folderPath):
    csvFiles = []
    for root, dirs, files in os.walk(folderPath):
        for file in files:
            if file.endswith(".csv"):
                csvFiles.append(os.path.join(root, file))
    return csvFiles


def main():
    print("開始過濾產品資訊...")
    paths = readAllCSVFilePath("./raw_data/")
    for path in paths:
        util.filter_description(path, "./filtered_data/")


if __name__ == "__main__":
    main()
