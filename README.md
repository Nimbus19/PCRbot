# 公主連結 公會戰排隊機器人
Discord bot for プリコネ クランバトル
## 如何執行 Bot
1. 安裝 Python
2. 安裝 Discord.py
3. 執行 `python3 main.py`

## 使用方法
用 -w 加入等待列隊，當有人打死王並 -d 時，機器人會用 @ 通知你
## 指令列表:
-w <boss編號> : 表示你在等這隻王，機器人會把你加入等待名單

-d <boss編號> : 表示這隻王已死，機器人會刪除等待名單，並通知等下隻王的人

-s : 顯示所有王的等待名單
-s <boss編號> : 顯示該王等待名單

-r : 將自己從所有王的等待名單中刪除
-r <boss編號> : 將自己從該王的等待名單中刪除

-c : 將自己加到殘刀列表，再呼叫一次可移除

-n : 呼叫殘刀支援

-help : 顯示沒屁用的幫助訊息