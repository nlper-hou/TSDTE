import os
import json

class ChatLog:

    def __init__(self):
        self.file_path = f"log.json" # Log文件路径

    def log(self, record, logtype = None):
        try:
            with open(self.file_path, 'r',encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []

        record = {"record":str(record),"logtype":logtype}
        history.append(record)

        with open(self.file_path, "w") as f:
            json.dump(history,f,ensure_ascii=False,indent=2)

