# MSDTE

Code of our paper: [An Novel Framework for Medical Decision Tree Extraction using If-Else Pseudocode and Node Filling Strategy]

### Environment Setup
可以采用下面两种方式安装环境
```yaml
conda create -n tsdte python=3.10 -y
conda activate tsdte
pip install tqdm
pip install langchain==0.0.327
pip install openai==0.28.0
pip install tiktoken==0.5.1
```
或者
```yaml
conda env create -f freeze.yml
conda activate tsdte
```

### Set the OpenAI API key
首先在LLM.py中设置openai.api_key和openai.api_base。
```yaml
openai.api_key="XXX"
openai.api_base="XXX"
```

### Run
K代表提供的样例个数，language代表数据集的语种。index代表执行的次数，用于记录运行的结果次数，便于统计并计算多次结果的标准差。下面这里在英文数据为例子，中文数据可以运行main.py，中文数据集可以从:https://tianchi.aliyun.com/specials/promotion/2021chinesemedicalnlpleaderboardchallenge 中获取。
```yaml
mkdir -p Result_en/chatgpt
python main_en.py --K=0 --language="en" --index=1
```
对于三元组抽取部分，我们主要参考了“苏剑林. (Jan. 30, 2022). 《GPLinker：基于GlobalPointer的实体关系联合抽取 》[Blog post]. Retrieved from https://kexue.fm/archives/8888”中的方法。

### Evaluate
reference.json指的是标准答案，predict.json指的是模型预测的答案。需要注意的是，由于英文数据是本研究构建的数据集，因此可以使用下面的方法进行评测。至于中文的评测，由于我们没有测试集的标准答案，因此需要提交到CBLUE评测系统上进行评测:https://tianchi.aliyun.com/specials/promotion/2021chinesemedicalnlpleaderboardchallenge
```yaml
cd evaluate/
python Text2DT_eval.py reference.json  predict.json
```

### Check the format of the results
如果直接进行evaluate出现格式的问题，这可能是由于结果与标准格式不符，可以使用"Post-processing.ipynb"进行验证修改格式。通常情况下是不需要验证格式。

