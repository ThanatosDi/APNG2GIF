# APNG2GIF
將 APNG 圖片轉換成 GIF 圖片

## What is APNG?
APNG（Animated Portable Network Graphics）格式是PNG的點陣圖動畫擴充，但未獲PNG組織官方認可。其擴充方法類似GIF 89a，仍對原版PNG保持向下相容。APNG第1影格為標準PNG圖像，剩餘的動畫和影格速等資料放在PNG擴充資料塊，因此只支援原版PNG的軟體會正確顯示第1影格。APNG與Mozilla社區關係密切，格式標準文件設在Mozilla網站。

## 在哪邊看的到 APNG?
在台灣最常看到的就是 LINE 的貼圖，就是使用 APNG  
或者 LINE Store 的貼圖預覽也是使用 APNG

## 如何使用
```shell
# 安裝必要套件
pip install apng2gif

# 顯示幫助清單
apng2gif -h

# 進行檔案轉換，轉換後的 GIF 會與執行目錄在同一目錄中
apng2gif -i 'example.png'

# 進行檔案轉換，轉換後的 GIF 另存為 /tmp/a.gif
apng2gif -i 'example.png' -o '/tmp/a.gif'
```
