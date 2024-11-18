# MSDTE

Code of our paper: [An Novel Framework for Medical Decision Tree Extraction using If-Else Pseudocode and Node Filling Strategy]

### Environment Setup
There are two ways to install the environment:
```yaml
conda create -n tsdte python=3.10 -y
conda activate tsdte
pip install tqdm
pip install langchain==0.0.327
pip install openai==0.28.0
pip install tiktoken==0.5.1
```
or
```yaml
conda env create -f freeze.yml
conda activate tsdte
```

### Set the OpenAI API key
First you need to set ’‘openai.api_key’‘ and ‘’openai.api_base‘’ in LLM.py.
```yaml
openai.api_key="XXX"
openai.api_base="XXX"
```

### Run
Where K represents the number of samples provided, and language represents the language of the data set.
index represents the number of executions, which is used to record the number of results of the run, so as to facilitate statistics and calculation of the standard deviation of multiple results. Here, English data is used as an example. For Chinese data, main.py can be run, and the Chinese data set can be obtained from : https://tianchi.aliyun.com/specials/promotion/2021chinesemedicalnlpleaderboardchallenge 
```yaml
mkdir -p Result_en/chatgpt
python main_en.py --K=0 --language="en" --index=1
```
For the triple extraction part, we mainly refer to the method in “苏剑林. (Jan. 30, 2022). 《GPLinker：基于GlobalPointer的实体关系联合抽取 》[Blog post]. Retrieved from https://kexue.fm/archives/8888 ”。

### Evaluate
‘’reference.json‘’ refers to the standard answer, and ‘’predict.json‘’ refers to the answer predicted by the model. It should be noted that since the English data is the dataset constructed for this study, the following method can be used for evaluation. As for the evaluation of Chinese, since we do not have the standard answer of the test set, it needs to be submitted to the CBLUE evaluation system for evaluation : https://tianchi.aliyun.com/specials/promotion/2021chinesemedicalnlpleaderboardchallenge
```yaml
cd evaluate/
python Text2DT_eval.py reference.json  predict.json
```

### Check the format of the results
If format problems occur when evaluating directly, this may be because the result does not conform to the standard format. You can use "Post-processing.ipynb" to verify and modify the format. Normally, format verification is not required.

