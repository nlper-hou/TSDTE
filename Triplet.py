import json

def extract_triplet(language,text, mode = "main"):

    return_triplet = []
    if mode == "test":
        if language=="en":
            path = "Dataset/en/Text2DT_triple_test.json"
        else:
            path = "Res/test_627.json"  # 中文使用的
        with open(path, 'r',encoding="utf-8") as f:
            triplets = json.load(f)
        # 根据text在triplets中找到对应的字典，读取其中的“triples”
        for triplet in triplets:
            if triplet['text'] == text:
                return_triplet = triplet['triples']
    if mode == "dev":
        if language=="en":
            path = "Dataset/en/Text2DT_triple_dev.json"
        else:
            path = "Res/dev_64_new.json"
        with open(path, 'r',encoding="utf-8") as f:
            triplets = json.load(f)
        # 根据text在triplets中找到对应的字典，读取其中的“triples”
        for triplet in triplets:
            if triplet['text'] == text:
                return_triplet = triplet['triples']
    return return_triplet