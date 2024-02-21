from Prompt import num_tokens_from_string,prompt_logical_pred,prompt_ask_pseudocode_without_triplet,prompt_ask_pseudocode,prompt_drug_type,prompt_find_triples,prompt_find_triples_xiaorong,prompt_select_triplet_xiaorong,prompt_find_triples_xiaorong2
import os
import openai
import tiktoken
from Log import ChatLog
import re
from collections import Counter
import json

openai.api_base = "XXX"
openai.api_key = "XXX"
proxies = {'XXX'}
openai.proxy = proxies

def LLM(instruction, example, input, note = None):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        top_p = 0.1,
        messages=[
            {'role': 'system', 'content': instruction},
            {'role': 'user', 'content': example +"\n"+ input}
        ]
    )
    answers = []
    result = completion["choices"][0]["message"]["content"]
    answers.append(result.strip())
    return answers

def brackets_symbol(string:str,reverse = True) -> str:
    if reverse:
        matches = re.findall(r'\[[^,]*?\]', string)
        for match in matches:
            string = string.replace(f"[{match[1:-1]}]", f"!#{match[1:-1]}#!")
    else:
        string = string.replace("!#",'[')
        string = string.replace("#!",']')

    return string

def LLM_whether_merge_node(language,text, condition, decision) -> bool:

    instruction = ""
    example = ""
    if language=="en":
        input = f"""text:{text},
        Statement:当{condition}时，{decision}。
        请根据text中的内容回答，Statement中称述的内容是否合理准确。注意，如果没有明确的指出statement中的称述是不正确或者没有提到statement中称述的内容，则应当认为该称述是正确的，仅回答”True“ or ”False“
        """
    else:
        input = f"""text:{text},
        Statement:当{condition}时，{decision}。
        Please answer based on the content in the text and whether the content stated in the Statement is reasonable and accurate. Note that if there is no clear indication that the statement in the statement is incorrect or the content of the statement is not mentioned, the statement should be considered correct and only "True" or "False" will be answered.“
        """
    answer = LLM(instruction, example, input, note="节点合并")[0]

    if "True" in answer:
        return True
    elif "False" in answer:
        return False

def LLM_logic_prediction(language,triples, text) -> str:
    prompt = prompt_logical_pred()
    instruction = prompt['instruction']
    if language=="en":
        example = prompt['en_example']
    else:
        example = prompt['example']

    str_triples = ""
    for triple in triples:
        str_triple = ",".join(triple).replace("\"","")
        str_triple = f"[{str_triple}], "
        str_triples += str_triple
    str_triples = f"[{str_triples[:-2]}]"
    if language=="en":
        input = f"""Actual Input#
        "text": "{text}",
        "triples" : {str_triples}

        Question:
        Please use one of "and" and "or" to answer. According to the semantics of text, the logical relationship between all triples in trips is "and" or "or"."""
    else:
        input = f"""Actual Input#
        "text": "{text}",
        "triples" : {str_triples}

        Question:
        请使用“and","or" 中的一种来回答，依据text的语义，tripes中所有的三元组互相之间的逻辑关系是”and“还是“or"."""

    answer = LLM(instruction, example, input, note="逻辑分组")[0]
    route = answer
    if "or" in route:
        return "or"
    else:
        return "and"

def example_formation(language,example_text, k)-> str:
    if language=="en":
        #相似的英文样例，此处路径还未修改
        with open("/root/nas/llm-prompt/text2DT/Pseudocode_language/Res/en_train_decision_path.json", 'r') as f:
            examples = json.load(f)
        # 读取相似度的文本
        with open("/root/nas/llm-prompt/text2DT/Pseudocode_language/Dataset/en/en_sim_result.json", 'r') as f:
            sim_examples = json.load(f)
    else:
        with open("/root/nas/llm-prompt/text2DT/Pseudocode_language/Res/text_pseudocode.json", 'r') as f:
            examples = json.load(f)
        # 读取相似度的文本
        with open("/root/nas/llm-prompt/text2DT/Pseudocode_language/Res/sim_result.json", 'r') as f:
            sim_examples = json.load(f)
    sample_texts = ""
    for sim in sim_examples:
        if example_text == sim['text']:
            sim_list = sim['result']
            for index in range(0,k):
                # 选择相似文本
                example_text = examples[sim_list[index]]['text']
                pseudocode = examples[sim_list[index]]['pseudocode']
                patient = re.match(r'(.*?)@', example_text)[0][:-1]
                if language=="en":
                    sample_text = f"""Example{index+1}#
                    "text":{example_text}
                    patient:{patient}
                    Please use a pre ordered binary tree to summarize the decision-making process based on this text.
                    tree：
                    {pseudocode}
                    #"""
                else:
                    sample_text = f"""Example{index+1}#
                    "text":{example_text}
                    patient:{patient}
                    请根据这段text，使用一颗前序二叉树来归纳总结出决策流程。
                    tree：
                    {pseudocode}
                    #"""
                sample_texts += sample_text + "\n"
    return sample_texts

def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("text-davinci-003")
    num_tokens = len(encoding.encode(string))
    return num_tokens

def LLM_extract_pseudocode(language,text, triplets,K) -> list:
    # 原始方案
    prompt = prompt_ask_pseudocode()

    instruction = prompt['instruction']
    if language=="en":
        example_list = prompt['en_example'] # K=3,固定例子
        example = ""
        for index in range(len(example_list)):
            if index < K:
                example = example + "\n" + example_list[index]
    else:
        example = example_formation(language,text, k = K) # KNN临近选择例子
    
    str_triples = ""
    for triple in triplets:
        if language=="en":
            if triple[1] in ['clinical manifestation','basic condition']:
                str_triple = ",".join(triple).replace("\"","")
                str_triple = f"\"[{str_triple}]\", "
                str_triples += str_triple
        else:
            if triple[1] in ['临床表现','基本情况']:
                str_triple = ",".join(triple).replace("\"","")
                str_triple = f"\"[{str_triple}]\", "
                str_triples += str_triple
    str_triples = f"[{str_triples[:-2]}]"

    patient = re.match(r'(.*?)@', text)[0][:-1]
    if language=="en":
        input = f"""Actual Input#
        "text": "{text}",
        patient:{patient}
        condition triples : {str_triples}
        Please use a pre ordered binary tree to summarize the decision-making process based on this text.
        tree：
        """
    else:
        input = f"""Actual Input#
        "text": "{text}",
        patient:{patient}
        condition triples : {str_triples}
        请根据这段text，使用一颗前序二叉树来归纳总结出决策流程
        tree：
        """
    # if num_tokens_from_string(instruction+example+input)>=3400:
    #     K = K-1
    #     example = example_formation(language,text, k = K)
    answer = LLM(instruction, example, input, note="问取伪代码")
    answer = answer[0].split("\n")

    for ID, line in enumerate(answer):
        answer[ID] = line.replace("    ", "\t")
    return answer

def LLM_extract_pseudocode_without_triplet(language,text,K) -> list:
    prompt = prompt_ask_pseudocode_without_triplet()
    
    instruction = prompt['instruction']
    if language=="en":
        example_list = prompt['en_example'] # K=3,固定例子
        example = ""
        for index in range(0,len(example_list)):
            if index < K:
                example = example + "\n" + example_list[index]
        if K == 0:
            example = ""
        if K == 0:
            example = ""
    else:
        example = example_formation(language,text, k = K) # KNN临近选择例子
        if K == 0:
            example = ""

    patient = re.match(r'(.*?)@', text)[0][:-1]
    if language=="en":
        input = f"""Actual Input#
        "text": "{text}",
        patient:{patient}
        Please use a pre ordered binary tree to summarize the decision-making process based on this text.
        tree：
        """
    else:
        input = f"""Actual Input#
        "text": "{text}",
        patient:{patient}
        请根据这段text，使用一颗前序二叉树来归纳总结出决策流程
        tree：
        """
    # if num_tokens_from_string(instruction+example+input)>=3400:
    #     K = K-1
    #     example = example_formation(language,text, k = K)
    answer = LLM(instruction, example, input, note="问取伪代码")
    
    answer = answer[0].split("\n")

    for ID, line in enumerate(answer):
        answer[ID] = line.replace("    ", "\t")
    return answer

def LLM_drug_type(text, drug) -> bool:

    prompt = prompt_drug_type()
    instruction = prompt['instruction']
    example = prompt['example']

    input = f"""Actual Input#
    "text": "{text}",
    Question:
    根据这段text描述的情况，判断{drug}是：禁用药物还是治疗药物
    Answer:
    """
    answer = LLM(instruction, example, input, note="判断药物类型")    

    if "禁" in answer[0]:
        return False
    else:
        return True

def LLM_find_triples(language,text, triples,k_num,error_triplet = []) -> list:

    prompt = prompt_find_triples()
    instruction = prompt['instruction']
    if len(error_triplet) != 0:
        error = "If there is a forgotten triple, remember to select it."
        instruction = instruction + error
    if language=="en":
        example = prompt['en_example']
    else:
        example = prompt['example']
    if k_num == 0:
        example = ""
    str_triples = ""
    for ID, triple in enumerate(triples):
        str_triple = ",".join(triple).replace("\"","")
        str_triple = f"triple{ID+1}:\"[{str_triple}]\", "
        str_triples += str_triple
    str_triples = f"[{str_triples[:-2]}]"

    text = re.sub(r'if|elif|\t|then|pass', "", text).strip()
    if language=="en":
        if len(error_triplet) == 0:
            input = f"""Actual Input#
            "text": "{text}",
            "triples":{str_triples}

            Question:
            Please use a list to indicate which semantics represented by triples appear in the given text. Only the sequence number of the triples can be answered in the list. If no corresponding triple is found, answer an empty list "[]".
            """
        else:
            input = f"""Actual Input#
            "text": "{text}",
            "triples":{str_triples}
            "Forgotten triplet": {error_triplet}
            Question:
            Please use a list to indicate which semantics represented by triples appear in the given text. Only the sequence number of the triples can be answered in the list. If no corresponding triple is found, answer an empty list "[]".
            """
    else:
        if len(error_triplet) == 0:
            input = f"""Actual Input#
            "text": "{text}",
            "triples":{str_triples}

            Question:
            请使用一个list来表示哪些triple所代表的语义出现在了给定text中，list中仅回答triple的序号即可，如果没有找到任何一个对应的triple，则回答一个空list"[]"。
            """
        else:
            input = f"""Actual Input#
            "text": "{text}",
            "triples":{str_triples}
            "Forgotten triplet": {error_triplet}
            Question:
            请使用一个list来表示哪些triple所代表的语义出现在了给定text中，list中仅回答triple的序号即可，如果没有找到任何一个对应的triple，则回答一个空list"[]"。
            """
    # Observation:各个三元组的语义分别是，从第一个三元组triple1开始分析，
    answers = LLM(instruction, example, input, note="判断三元组是否出现")
    merged_array = []
    for answer in answers:
        if '[]' in answer:
            index = []
        else:
            try:
                index = re.findall(r'(\[[\d,\s]*\])', answer, re.M|re.S)[0]
                index = eval(index)
            except IndexError:
                index = []
        merged_array += index
    # 使用Counter计数
    counter = Counter(merged_array)
    # 找出出现一次以上的元素
    result = [num for num, count in counter.items() if count >= 1]
    return result

def LLM_find_triples_xiaorong(language,text, triples) -> list:
    """此处是选三元组时使用standard prompt的方法"""
    prompt = prompt_find_triples_xiaorong()
    instruction = prompt['instruction']
    if language=="en":
        example = prompt['en_example']
    else:
        example = prompt['example']

    str_triples = ""
    for ID, triple in enumerate(triples):
        str_triple = ",".join(triple).replace("\"","")
        str_triple = f"triple{ID+1}:\"[{str_triple}]\", "
        str_triples += str_triple
    str_triples = f"[{str_triples[:-2]}]"

    text = re.sub(r'if|elif|\t|then|pass', "", text).strip()
    if language=="en":
        input = f"""Actual Input#
        "text": "{text}",
        "triples":{str_triples}
        Question: Please use a list to indicate which semantics represented by triples appear in the given text. Only the sequence number of the triples can be answered in the list.
        """
    else:
        input = f"""Actual Input#
        "text": "{text}",
        "triples":{str_triples}
        Question: 请使用一个list来表示哪些triple所代表的语义出现在了给定text中，list中仅回答triple的序号即可。
        """
    answers = LLM(instruction, example, input, note="判断三元组是否出现")
    merged_array = []
    for answer in answers:
        if '[]' in answer:
            index = []
        else:
            try:
                index = re.findall(r'(\[[\d,\s]*\])', answer, re.M|re.S)[0]
                index = eval(index)
            except IndexError:
                index = []
        merged_array += index
    # 使用Counter计数
    counter = Counter(merged_array)
    # 找出出现一次以上的元素
    result = [num for num, count in counter.items() if count >= 1]
    return result

def select_triplet_xiaorong(language,pseudocode, triplets, text):
    """此处为删除选择三元组模块"""
    prompt = prompt_select_triplet_xiaorong()
    instruction = prompt['instruction']
    if language=="en":
        example = prompt['en_example']
    else:
        example = prompt['example']
    if language=="en":
        input = f"""Actual Input#
        "text": "{text}",
        "pseudocode": "{pseudocode}",
        "triples":{str(triplets)}

        Question:
        Please extract the diagnosis and treatment decision tree corresponding to the text based on the provided text, pseudocode and triples.
        """
    else:
        input = f"""Actual Input#
        "text": "{text}",
        "pseudocode": "{pseudocode}",
        "triples":{str(triplets)}

        Question:
        请根据提供的text、pseudocode和triples，抽取出text对应的诊疗决策树。
        """
    answer = LLM(instruction, example, input)
    return answer

def LLM_find_triples_xiaorong2(language,text, triples) -> list:
    """此处是选三元组时使用COT的方法"""
    prompt = prompt_find_triples_xiaorong2()
    instruction = prompt['instruction']
    if language=="en":
        example = prompt['en_example']
    else:
        example = prompt['example']

    str_triples = ""
    for ID, triple in enumerate(triples):
        str_triple = ",".join(triple).replace("\"","")
        str_triple = f"triple{ID+1}:\"[{str_triple}]\", "
        str_triples += str_triple
    str_triples = f"[{str_triples[:-2]}]"

    text = re.sub(r'if|elif|\t|then|pass', "", text).strip()
    if language=="en":
        input = f"""Actual Input#
        "text": "{text}",
        "triples":{str_triples}

        Question:
        Please use a list to indicate which semantics represented by triples appear in the given text. Only the sequence number of the triples can be answered in the list. If no corresponding triple is found, answer an empty list "[]", let's think step by step.
        """
    else:
        input = f"""Actual Input#
        "text": "{text}",
        "triples":{str_triples}

        Question:
        请使用一个list来表示哪些triple所代表的语义出现在了给定text中，list中仅回答triple的序号即可，如果没有找到任何一个对应的triple，则回答一个空list"[]"，让我一步一步来分析吧。
        """
    answers = LLM(instruction, example, input, note="判断三元组是否出现")
    merged_array = []
    for answer in answers:
        if '[]' in answer:
            index = []
        else:
            try:
                index = re.findall(r'(\[[\d,\s]*\])', answer, re.M|re.S)[0]
                index = eval(index)
            except IndexError:
                index = []
        merged_array += index
    # 使用Counter计数
    counter = Counter(merged_array)
    # 找出出现一次以上的元素
    result = [num for num, count in counter.items() if count >= 1]
    return result