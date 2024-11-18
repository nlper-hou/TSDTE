from eval_func import eval
import json
import sys


def compute_score(gold_data, predict_data):

    gold_tree_num, correct_tree_num = 0.000001, 0.000001
    gold_triplet_num, predict_triplet_num, correct_triplet_num = 0.000001, 0.000001, 0.000001
    gold_path_num, predict_path_num, correct_path_num= 0.000001, 0.000001, 0.000001
    gold_node_num, predict_node_num, correct_node_num = 0.000001, 0.000001, 0.000001

    edit_dis = 0
    max_edit_dis = 0

    for i in range(len(gold_data)):
        print(i)
        tmp= eval(predict_data[i]['tree'], gold_data[i]['tree'])
        gold_tree_num += tmp[0]
        correct_tree_num += tmp[1]
        correct_triplet_num += tmp[2]
        predict_triplet_num += tmp[3]
        gold_triplet_num += tmp[4]
        correct_path_num += tmp[5]
        predict_path_num += tmp[6]
        gold_path_num += tmp[7]
        edit_dis += tmp[8]

        # 计算最大编辑数
        max_edit_dis += (tmp[3]+ tmp[10]*2) + (tmp[4]+ tmp[11]*2)

        correct_node_num += tmp[9]
        predict_node_num += tmp[10]
        gold_node_num += tmp[11]

    tree_acc= correct_tree_num/gold_tree_num
    triplet_f1 = 2 * (correct_triplet_num/predict_triplet_num) * (correct_triplet_num/gold_triplet_num)/(correct_triplet_num/predict_triplet_num + correct_triplet_num/gold_triplet_num)
    path_f1 = 2 * (correct_path_num/predict_path_num) * (correct_path_num/gold_path_num)/(correct_path_num/predict_path_num + correct_path_num/gold_path_num)
    tree_edit_radio = edit_dis/max_edit_dis
    node_f1 = 2 * (correct_node_num/predict_node_num) * (correct_node_num/gold_node_num) / (correct_node_num/predict_node_num + correct_node_num/gold_node_num)
    node_p = correct_node_num/predict_node_num
    node_R = correct_node_num/gold_node_num
    path_P = correct_path_num/predict_path_num
    path_R = correct_path_num/gold_path_num

    print("  Triplet_F1(三元组抽取F1): ", triplet_f1 , '\n',
          "  Node_F1(节点抽取F1): ",node_f1, '\n',
          "  Tree_Acc(树抽取准确率): ",tree_acc, '\n',
          "  DP_F1(决策路径抽取F1): ",path_f1, '\n',
          "  TER(树编辑比率): ", tree_edit_radio, '\n',
          "  TER(树编辑距离): ", edit_dis, '\n',
          "  Final score (tree level score): ", ((1 - tree_edit_radio) + path_f1) / 2,
          "  node_p(节点抽取P): ",node_p, '\n',
          "  node_R(节点抽取R): ",node_R, '\n',
          "  path_P(决策路径抽取P): ",path_P, '\n',
          "  path_R(决策路径抽取R): ",path_R, '\n')


if __name__ == '__main__':
    golden_file = sys.argv[1]
    pred_file = sys.argv[2]
    # golden_file = "Text2DT_test_raw.json"
    # pred_file = "Text2DT_test.json"
    
    with open(golden_file, "r") as f:
        gold_data = json.load(f)
    with open(pred_file, "r") as f:
        predict_data = json.load(f)
    compute_score(gold_data, predict_data)