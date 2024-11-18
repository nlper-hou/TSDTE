import re
from LLM import LLM_logic_prediction,LLM_extract_pseudocode_without_triplet,LLM_extract_pseudocode,LLM_drug_type,LLM_find_triples,LLM_whether_merge_node,LLM_find_triples_xiaorong,select_triplet_xiaorong,LLM_find_triples_xiaorong2
import copy
import json

def logic_prediction(language,triples,text):
    if language=="en":
        index=[]
        and_words = ['and', 'meanwhile', 'again', 'then', 'joint','+']
        or_words = ['or','such as']
        dict={"clinical manifestation":0,"drug therapy":0,"therapeutic schedule":0,"dosage and administration":0,"basic condition":0,"prohibited drugs":0}
        for triple in triples:
            dict[triple[1]] +=1
        if len(triples) < 2:
            return 'null'
        else:
            try:
                if dict["prohibited drugs"]>0:
                    return 'and'
                elif dict["therapeutic schedule"]+dict["drug therapy"]>1 or dict["basic condition"]>1 or dict["clinical manifestation"] > 1 or dict["basic condition"]+dict["clinical manifestation"] > 1:
                    for triple in triples:
                        index.append(text.index(triple[2]))
                    for word in or_words:
                        if word in text[min(index):max(index)]:
                            return "or"
                    for word in and_words:
                        if word in text[min(index):max(index)]:
                            return "and"
                elif dict["dosage and administration"]>0:
                    return 'and'
            except:
                return LLM_logic_prediction(language,triples, text)
        return LLM_logic_prediction(language,triples, text)
    else:
        index=[]
        and_words = ['且', '同时', '再', '然后', '联合', '继而', '并', '还需', '+', '与', '的']
        or_words = ['或','如']
        dict={"临床表现":0,"治疗药物":0,"治疗方案":0,"用法用量":0,"基本情况":0,"禁用药物":0}
        for triple in triples:
            dict[triple[1]] +=1
        if len(triples) < 2:
            return 'null'
        else:
            try:
                if dict["禁用药物"]>0:
                    return 'and'
                elif dict["治疗方案"]+dict["治疗药物"]>1 or dict["基本情况"]>1 or dict["临床表现"] > 1 or dict["基本情况"]+dict["临床表现"] > 1:
                    for triple in triples:
                        index.append(text.index(triple[2]))
                    for word in or_words:
                        if word in text[min(index):max(index)]:
                            return "or"
                    for word in and_words:
                        if word in text[min(index):max(index)]:
                            return "and"
                elif dict["用法用量"]>0:
                    return 'and'
            except:
                return LLM_logic_prediction(language,triples, text)
        return LLM_logic_prediction(language,triples, text)

def same_statement(text1, text2):
    # 如果 text1 和 text2 中出现或同样不出现，if，elif，else等关键词，可以视为相同的一句返回True
    indent1 = len(re.findall(r'\t', text1))
    indent2 = len(re.findall(r'\t', text2))
    if indent1 == indent2:
        if len(re.findall(r"if|elif|else", text1)) == len(re.findall(r"if|elif|else", text2)):
            return True
    elif len(re.findall(r"if|elif|else", text1)) == 0 and len(re.findall(r"if|elif|else", text2)) == 0:
        return True
    else:
        return False

def extract_pseudocode(language,text, triplets,K) -> list:
    pseudocode = LLM_extract_pseudocode_without_triplet(language,text,K)
    return pseudocode

def drug_type(text, drug) -> bool:

    return LLM_drug_type(text, drug)

def find_triples(language,text : str, triplets, role, patient,k_num,error_triplet=[]) -> list:
    node = []
    if patient not in text:
        text = f"{patient}{text}"
    if role == "C":
        # planselect实验
        index = LLM_find_triples(language,text, triplets['condition triples'],k_num,error_triplet)
        
        index = sorted(index)
        for ID, triple in enumerate(triplets['condition triples']):
            if (ID + 1) in index:
                node.append(triple) 
        for ID in sorted(index, reverse=True):
            if len(triplets['condition triples'])>0:
                try:
                    triplets['condition triples'].pop(ID-1)
                except IndexError:
                    print("IndexError-------")
                    print(triplets)
    else:
        index = LLM_find_triples(language,text, triplets['decision triples'],k_num,error_triplet)
        for ID, triple in enumerate(triplets['decision triples']):
            if (ID + 1) in index:
                node.append(triple)
    return node

def deduplicate_list_of_lists(list) -> list:
    seen = set()
    result = []
    for sublst in list:
        sublst_tuple = tuple(sublst)  # 将子列表转换为元组，因为元组是可哈希的
        if sublst_tuple not in seen:
            seen.add(sublst_tuple)
            result.append(sublst)
    return result

def insert_node(node, DT, last_condition_node, node_path=""):
    root = eval("DT" + node_path)
    if not root:
        return False
    elif root['role'] == "D":
        if node['role'] == "D":
            return False
        else:
            extra = root.copy()
            Node = node.copy()
            Node["LD"] = {}
            Node["RD"] = {}
            Node['extra_decision'] = extra
            exec(f"DT{node_path} = Node")
            last_condition_node[0] = node_path
            return True
    elif node['role'] == "C":
        if node['indent'] == root['indent']:
            node_path += "[\"RD\"]"
            if not root.get("RD"):
                Node = node.copy()
                Node["LD"] = {}
                Node["RD"] = {}
                exec(f"DT{node_path} = Node")
                last_condition_node[0] = node_path
                return True
            else:
                if not insert_node(node, DT, last_condition_node, node_path):
                    insert_node(node , DT, last_condition_node,node_path[:-12])
        elif node['indent'] >= root['indent'] + 1:
            node_path += "[\"LD\"]"
            if not root.get("LD"):
                Node = node.copy()
                Node["LD"] = {}
                Node["RD"] = {}
                exec(f"DT{node_path} = Node")
                last_condition_node[0] = node_path
                return True
            else:
                if not insert_node(node, DT, last_condition_node, node_path):
                    insert_node(node , DT, last_condition_node,node_path[:-12])
        else:
            insert_node(node , DT, last_condition_node, node_path[:-12])
    elif node['role'] == "D":
        if node['indent'] == root['indent'] + 1:
            if not root.get('LD'):
                node_path += "[\"LD\"]"
                Node = node.copy()
                exec(f"DT{node_path} = Node")
                return True
            elif not root.get('RD'):
                node_path += "[\"RD\"]"
                Node = node.copy()
                exec(f"DT{node_path} = Node")
                return True
            elif root["RD"]['role'] == "C":
                node_path += "[\"RD\"]"
                insert_node(node, DT, last_condition_node, node_path)
        else:
            node_path_LD = node_path + "[\"LD\"]"
            node_path_RD = node_path + "[\"RD\"]"
            if not insert_node(node, DT, last_condition_node, node_path_LD):
                insert_node(node, DT, last_condition_node, node_path_RD)

def whether_merge_node(language,root, text):
    condition = root['text']
    decision = root['extra_decision']['text']
    condition = re.sub(r'[elif|if\t:：]', "", condition).strip()
    decision = re.sub(r'[elif|if\t:：]', "", decision).strip()

    return LLM_whether_merge_node(language,text, condition, decision)

def preorder_visit(language,root, DT, text):
    if not root:
        DT.append({
            "role" : "D",
            "triples" : [],
            "logical_rel" : "null"
        })
        return
    else:
        if root.get('extra_decision'):
            if whether_merge_node(language,root, text):
                if root.get('LD'):
                    root['LD']['triples'].extend(root['extra_decision']['triples'])
                    root['LD']['logical_rel'] = logic_prediction(language,root['LD']['triples'], text)
                else:
                    root['LD']['role'] = "D"
                    root['LD']['triples'] = root['extra_decision']['triples']
                    root['LD']['logical_rel'] = root['extra_decision']['logical_rel']
            
            if root.get('RD'):
                root['RD']['triples'].extend(root['extra_decision']['triples'])
                root['RD']['logical_rel'] = logic_prediction(language,root['RD']['triples'], text)
            else:
                root['RD']['role'] = "D"
                root['RD']['triples'] = root['extra_decision']['triples']
                root['RD']['logical_rel'] = root['extra_decision']['logical_rel']

        DT.append({
            "role" : root['role'],
            "triples" : root['triples'],
            "logical_rel" : root['logical_rel']
        })

        if root['role'] != "D":
            preorder_visit(language,root["LD"], DT, text)
            preorder_visit(language,root["RD"], DT, text)

def classify_triplet(language,triplets) -> dict:
    """
        将抽取出的三元组分为条件三元组与决策三元组。    
        return:
        {
            "condition triples":[triple1,triple2],
            "decision triples":[
                [triple1],
                [triple1, triple2]
            ]
        }
    """
    classified_triplet = {
        "condition triples" : [],
        "decision triples" : []
    }
    if language=="en":
        for triplet in triplets:
            if triplet[1] in ["clinical manifestation", "basic condition"]:
                classified_triplet['condition triples'].append(triplet)
            else:
                classified_triplet['decision triples'].append(triplet)
    else:
        for triplet in triplets:
            if triplet[1] in ["临床表现", "基本情况"]:
                classified_triplet['condition triples'].append(triplet)
            else:
                classified_triplet['decision triples'].append(triplet)
    
    classified_triplet = {
        "condition triples" : deduplicate_list_of_lists(classified_triplet['condition triples']),
        "decision triples" : deduplicate_list_of_lists(classified_triplet['decision triples'])
    }
    return classified_triplet

def convert_pseudocode2DT(language,pseudocode, triplets, text,k_num) -> list:
    triplets = classify_triplet(language,triplets)
    patient = triplets['condition triples'][0][0]

    temp_triplets = copy.deepcopy(triplets)
    pop_id = []
    del_indent = -1
    for ID, line in enumerate(pseudocode):
        indent = len(re.findall(r'\t', line))
        if del_indent != -1:
            if indent <= del_indent:
                del_indent = -1
            elif indent > del_indent:
                indent -= 1
                pseudocode[ID] = pseudocode[ID].replace((indent+1)*"\t",indent*"\t")
        # 选择条件三元组
        if "if" in line or "elif" in line:
            node = find_triples(language,line, temp_triplets, "C", patient,k_num) 
            if len(node) == 0:
                pop_id.append(ID)
                del_indent = indent

    for id in pop_id[::-1]:
        pseudocode.pop(id)
    pop_id = []
    ID_checkpoint = 0
    for ID in range(1,len(pseudocode)):
        if same_statement(pseudocode[ID_checkpoint], pseudocode[ID]):
            pseudocode[ID_checkpoint] += (" ," + pseudocode[ID].replace("\t", ""))
            pop_id.append(ID)
        else:
            ID_checkpoint = ID
    for id in pop_id[::-1]:
        pseudocode.pop(id)

    # 遍历每一行，判断三元组是否在这行中，药物做特殊处理，然后再拼接逻辑关系
    del_indent = -1
    tree_list = []
    for line in pseudocode:
        indent = len(re.findall(r'\t', line))

        if "if" in line or "elif" in line:
            role = "C"
            node = find_triples(language,line, triplets, role, patient,k_num)   
        # 注意，这里不确定是不是有一条cdcdd没有抽取出来的原因，后续待验证
        elif "else" in line:
            continue
        else:
            role = "D"
            node = find_triples(language,line, triplets, role, patient,k_num)

        if len(node) == 0 and "pass" not in line:
            if role == "C":
                del_indent = indent
            continue

        if del_indent != -1:
            if indent == del_indent:
                del_indent = -1
            elif indent > del_indent:
                indent -= 1
        if len(node) != 0:
            logical_rel = logic_prediction(language,node, line)
        else:
            logical_rel = "null"
        tree_list.append({
            "indent" : indent,
            "role" : role,
            "triples" : node,
            "logical_rel" : logical_rel,
            "text" : line
        })
    node_c = {"role": "C","triples": [],"logical_rel": "null"}
    node_d = {"role": "D","triples": [],"logical_rel": "null"}
    if len(tree_list) == 0:
        tree_list.append(node_c)
        tree_list.append(node_d)
        tree_list.append(node_d)
        return tree_list
    DT_temp = {
        "indent" : tree_list[0]['indent'],
        "role" : tree_list[0]['role'],
        "triples" : tree_list[0]['triples'],
        "logical_rel" : tree_list[0]['logical_rel'],
        "LD" : {},
        "RD" : {},
        "text" : tree_list[0]['text'],
    }

    # 调整插入节点
    last_condition_node = [""]
    for node in tree_list[1:]:
        insert_node(node, DT_temp, last_condition_node, node_path=last_condition_node[0])

    DT = []
    preorder_visit(language,DT_temp, DT, text)
    return DT

def find_list_difference(list1, list2):
    """找到两个list的相差的元素，并返回该元素"""
    set1 = set(map(tuple, list1))
    set2 = set(map(tuple, list2))
    difference = set1 - set2
    return list(map(list, difference))

def convert_pseudocode2DT2(language,pseudocode, triplets, text,k_num) -> list:
    """此方法目前为测试代码"""
    triplets = classify_triplet(language,triplets)
    patient = triplets['condition triples'][0][0]

    
    temp_triplets = copy.deepcopy(triplets)
    pop_id = []
    del_indent = -1
    for ID, line in enumerate(pseudocode):
        indent = len(re.findall(r'\t', line))
        if del_indent != -1:
            if indent <= del_indent:
                del_indent = -1
            elif indent > del_indent:
                indent -= 1
                pseudocode[ID] = pseudocode[ID].replace((indent+1)*"\t",indent*"\t")
        # 选择条件三元组
        if "if" in line or "elif" in line:
            node = find_triples(language,line, temp_triplets, "C", patient,k_num) 
            if len(node) == 0:
                pop_id.append(ID)
                del_indent = indent

    for id in pop_id[::-1]:
        pseudocode.pop(id)
    pop_id = []
    ID_checkpoint = 0
    for ID in range(1,len(pseudocode)):
        if same_statement(pseudocode[ID_checkpoint], pseudocode[ID]):
            pseudocode[ID_checkpoint] += (" ," + pseudocode[ID].replace("\t", ""))
            pop_id.append(ID)
        else:
            ID_checkpoint = ID
    for id in pop_id[::-1]:
        pseudocode.pop(id)


    condition_triplets = []
    decision_triplets = []
    # 遍历每一行，判断三元组是否在这行中，药物做特殊处理，然后再拼接逻辑关系
    stop_iter = 5
    error_condition_triplet = []
    error_dicision_triplet = []
    for i in range(0,stop_iter):
        tree_list = []
        del_indent = -1
        for line in pseudocode:
            # 遍历每一行伪代码
            indent = len(re.findall(r'\t', line))
            # 选择三元组
            if "if" in line or "elif" in line:
                role = "C"
                # 返回的是选择的三元组
                node = find_triples(language,line, triplets, role, patient,k_num,error_condition_triplet)   
                condition_triplets.extend(node)
            else:
                role = "D"
                node = find_triples(language,line, triplets, role, patient,k_num,error_dicision_triplet)
                decision_triplets.extend(node)

            if len(node) == 0 and "pass" not in line:
                if role == "C":
                    del_indent = indent
                continue

            if del_indent != -1:
                if indent == del_indent:
                    del_indent = -1
                elif indent > del_indent:
                    indent -= 1
            if len(node) != 0:
                logical_rel = logic_prediction(language,node, line)
            else:
                logical_rel = "null"
            tree_list.append({
                "indent" : indent,
                "role" : role,
                "triples" : node,
                "logical_rel" : logical_rel,
                "text" : line
            })
        error_condition_triplet = []
        error_dicision_triplet = []
        # 迭代找到未选择的三元组
        if len(condition_triplets)!=len(triplets['condition triples']):
            print(triplets['condition triples'])
            print(condition_triplets)
            error_condition_triplet = find_list_difference(triplets['condition triples'],condition_triplets)
            print(error_condition_triplet)
        if len(decision_triplets)!=len(triplets['decision triples']):
            print("***********")
            print(triplets['decision triples'])
            print(decision_triplets)
            error_dicision_triplet = find_list_difference(triplets['decision triples'],decision_triplets)
            print(error_dicision_triplet)
        # 如果全部选择，则跳出循环，否则至少迭代5次
        if len(error_condition_triplet) == 0 and len(error_dicision_triplet) == 0 :
            break

    node_c = {"role": "C","triples": [],"logical_rel": "null"}
    node_d = {"role": "D","triples": [],"logical_rel": "null"}
    if len(tree_list) == 0:
        tree_list.append(node_c)
        tree_list.append(node_d)
        tree_list.append(node_d)
        return tree_list
    DT_temp = {
        "indent" : tree_list[0]['indent'],
        "role" : tree_list[0]['role'],
        "triples" : tree_list[0]['triples'],
        "logical_rel" : tree_list[0]['logical_rel'],
        "LD" : {},
        "RD" : {},
        "text" : tree_list[0]['text'],
    }
    # 调整插入节点
    last_condition_node = [""]
    for node in tree_list[1:]:
        insert_node(node, DT_temp, last_condition_node, node_path=last_condition_node[0])

    DT = []
    preorder_visit(language,DT_temp, DT, text)
    return DT

def pseudocode_find_triples(language,text) -> list:
    # 初步清洗
    sentence = text.strip()
    sentence = sentence.lstrip("ifelifelse：:")
    sentence = sentence.strip()
    node = []
    if language=="en":
        with open('/root/nas/llm-prompt/text2DT/Pseudocode_language/Res/先抽伪代码再抽三元组.json', 'r') as f1:
            tree_list = json.load(f1,encoding="utf-8")
    else:
        with open('/root/nas/llm-prompt/text2DT/Pseudocode_language/Res/先抽伪代码再抽三元组.json', 'r') as f1:
            tree_list = json.load(f1,encoding="utf-8")
    for tree in tree_list:
        if tree['text'] == sentence:
            node = tree['triples']
    return node

def pseudocode_extract_triplet2DT(language,pseudocode, triplets, text) -> list:
    # 先伪代码再三元组的消融实验
    # 遍历每一行，判断三元组是否在这行中，药物做特殊处理，然后再拼接逻辑关系
    del_indent = -1
    tree_list = []
    for line in pseudocode:
        indent = len(re.findall(r'\t', line))
        if "if" in line or "elif" in line:
            role = "C"
            node = pseudocode_find_triples(language,line)   
        elif "else" in line:
            continue
        else:
            role = "D"
            node = pseudocode_find_triples(language,line)
        if len(node) == 0 and "pass" not in line:
            if role == "C":
                del_indent = indent
            continue

        if del_indent != -1:
            if indent == del_indent:
                del_indent = -1
            elif indent > del_indent:
                indent -= 1
        if len(node) != 0:
            logical_rel = logic_prediction(language,node, line)
        else:
            logical_rel = "null"
        tree_list.append({
            "indent" : indent,
            "role" : role,
            "triples" : node,
            "logical_rel" : logical_rel,
            "text" : line
        })
    node_c = {"role": "C","triples": [],"logical_rel": "null"}
    node_d = {"role": "D","triples": [],"logical_rel": "null"}
    if len(tree_list) == 0:
        tree_list.append(node_c)
        tree_list.append(node_d)
        tree_list.append(node_d)
        return tree_list
    DT_temp = {
        "indent" : tree_list[0]['indent'],
        "role" : tree_list[0]['role'],
        "triples" : tree_list[0]['triples'],
        "logical_rel" : tree_list[0]['logical_rel'],
        "LD" : {},
        "RD" : {},
        "text" : tree_list[0]['text'],
    }
    # 调整插入节点
    last_condition_node = [""]
    for node in tree_list[1:]:
        insert_node(node, DT_temp, last_condition_node, node_path=last_condition_node[0])
    DT = []
    preorder_visit(language,DT_temp, DT, text)
    return DT

def find_triplet_xiaorong(language,pseudocode, triplets, text) -> list:
    """删除选三元组模块，思路：直接把伪代码、三元组和文本扔给大模型，不去选三元组"""
    temp_triplets = copy.deepcopy(triplets)
    DT = select_triplet_xiaorong(language,pseudocode, temp_triplets, text)
    return DT
