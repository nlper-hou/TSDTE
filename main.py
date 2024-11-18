import os
os.chdir("/root/nas/Text2DT")
import json
import argparse
from tqdm import tqdm
from Triplet import extract_triplet
from Pseudocode import extract_pseudocode,convert_pseudocode2DT,find_triplet_xiaorong,convert_pseudocode2DT2

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--K', type=int)
    parser.add_argument('--language', type=str,default="zh")
    parser.add_argument('--index', type=int)
    args = parser.parse_args()
    k_num = args.K
    language = args.language
    index = args.index
    
    # k_num = 4
    # language = "zh"
    # index = 2

    # 加载数据集
    if language=="en":
        input_dataset_path = "Dataset/en/Text2DT_test.json"
    else:
        input_dataset_path = "Dataset/Text2DT_test.json"
    with open(input_dataset_path, 'r') as f:
        input_dataset = json.load(f)
    print(f"{len(input_dataset)} texts loaded!")
    try:
        with open(f"Result/并行chatgpt/test/{input_dataset_path.split('.')[0].split('/')[1]}_DT并行实验第"+str(index+1)+"次_knn="+str(k_num)+".json", 'r') as f:
            data_list = json.load(f)
    except FileNotFoundError:
        data_list = []
    # Text2DT
    begin = len(data_list)
    end = len(input_dataset)
    for ID, text in tqdm(enumerate(input_dataset[begin:end]),total=end-begin):
        text = text['text']
        # badcase
        if ID in []: continue
        
        # 抽取三元组
        triplets = extract_triplet(language,text,'test')
        # 抽取决策伪代码结构
        pseudocode_path = f"Result/并行chatgpt/test/{input_dataset_path.split('.')[0].split('/')[1]}_pseudocode并行实验第"+str(index+1)+"次_knn="+str(k_num)+".json"
        try:
            with open(pseudocode_path, 'r') as f:
                pseudocode_history = json.load(f)
        except:
            pseudocode_history = []

        pseudocode = []
        for _ in pseudocode_history:
            if _['text'] == text:
                pseudocode = _['pseudocode']
                break
        
        if len(pseudocode) == 0:
            pseudocode = extract_pseudocode(language,text,triplets,k_num)
            pseudocode_history.append({
                "text" : text,
                "pseudocode" : pseudocode
            })
            with open(pseudocode_path, 'w') as f:
                json.dump(pseudocode_history, f, ensure_ascii=False, indent=2)
        # 消融实验专用
        # DT = find_triplet_xiaorong(language,pseudocode, triplets, text)
        
        # 将决策路径转化为决策树
        DT = convert_pseudocode2DT(language,pseudocode, triplets, text,k_num)

        DT_path = f"Result/并行chatgpt/test/{input_dataset_path.split('.')[0].split('/')[1]}_DT并行实验第"+str(index+1)+"次_knn="+str(k_num)+".json"
        try:
            with open(DT_path, 'r') as f:
                DT_history = json.load(f)
        except:
            DT_history = []
        DT_history.append({
            "text" : text,
            "tree" : DT
        })
        with open(DT_path, 'w') as f:
            json.dump(DT_history, f, ensure_ascii=False, indent=2)

            