import tiktoken

def num_tokens_from_string(string: str) -> int:
	"""Returns the number of tokens in a text string."""
	encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
	num_tokens = len(encoding.encode(string))
	return num_tokens

def prompt_ask_pseudocode() -> dict:
	instruction = """As an expert in medical knowledge and natural language processing, I am skilled at performing tasks based on rules and instructions. I will learn form the example and form my response to your question.
	rules：
	- The text in the if or elif statement should only contain information about the patient's clinical manifestations or basic symptoms from the given text.The semantics represented by condition triples should be chosen preferentially
	- Patient should be the subject of the sentence in each statement.
	- Please strictly follow the output format of the given sample.
	"""

	example = """Example1#
	"text":"急性肾小球肾炎患者@对于水肿、少尿、循环出血的患者，轻症可口服氢氯噻嗪，每次1~2mg/kg每日1-2次，重症患者可静脉给予呋塞米强力利尿剂，每次1~2mg/kg每日1-2次。"
	patient:急性肾小球肾炎患者
	condition triples:["[急性肾小球肾炎患者,临床表现,水肿]", "[急性肾小球肾炎患者,临床表现,少尿]","[急性肾小球肾炎患者,临床表现,循环出血]","[急性肾小球肾炎患者,临床表现,轻症]","[急性肾小球肾炎患者,临床表现,重症]"]

	请根据这段text，使用一颗前序二叉树来归纳总结出决策流程

	tree：
	if 急性肾小球肾炎患者有水肿、少尿、循环出血的情况：
	\tif 急性肾小球肾炎患者是轻症：
	\t\t急性肾小球肾炎患者可口服氢氯噻嗪，每次1~2mg/kg每日1-2次
	\telif 急性肾小球肾炎患者是重症：
	\t\t急性肾小球肾炎患者可静脉给予呋塞米强力利尿剂，每次1~2mg/kg每日1-2次。
	#
			
	Example2#
	"text":"肠道念珠菌病患儿@酮康唑开始剂量：体重30kg以下者每日口服100mg；30kg以上者每日口服200~400mg;1~4岁者每日口服50mg;5~12岁者每日口服100mg。"
	patient: 肠道念珠菌病患儿
	condition triples:["[肠道念珠菌病患儿,基本情况,体重30kg以下]","[肠道念珠菌病患儿,基本情况,30kg以上]","[肠道念珠菌病患儿,基本情况,1~4岁]","[肠道念珠菌病患儿,基本情况,5~12岁]"]

	请根据这段text，使用一颗前序二叉树来归纳总结出决策流程

	tree：
	if 肠道念珠菌病患儿的体重在30kg以下：
	\t肠道念珠菌病患儿可以每日口服100mg酮康唑
	elif 肠道念珠菌病患儿的体重在30kg以上：
	\t肠道念珠菌病患儿可以每日口服200~400mg酮康唑
	elif 肠道念珠菌病患儿的年龄在1~4岁：
	\t肠道念珠菌病患儿可以每日口服50mg酮康唑
	elif 肠道念珠菌病患儿的年龄在5~12岁：
	\t肠道念珠菌病患儿可以每日口服100mg酮康唑

	Example3#
	"text":"原发性肝癌患者@对临床肝癌或大肝癌，如患者肝功能代偿良好，无肝硬化者，规则性肝切除仍为主要术式。对亚临床肝癌或小肝癌，非规则性肝切除成为主要术式。"
	patient:原发性肝癌患者
	condition triples:["[原发性肝癌患者,临床表现,临床肝癌]","[原发性肝癌患者,临床表现,大肝癌]", "[原发性肝癌患者,临床表现,肝功能代偿良好]", "[原发性肝癌患者,临床表现,无肝硬化]", "[原发性肝癌患者,临床表现,亚临床肝癌]", "[原发性肝癌患者,临床表现,小肝癌]"]

	请根据这段text，使用一颗前序二叉树来归纳总结出决策流程

	tree：
	if 原发性肝癌患者是临床肝癌或大肝癌：
	\tif 原发性肝癌患者肝功能代偿良好，无肝硬化：
	\t\t规则性肝切除仍为原发性肝癌患者的主要术式
	elif 原发性肝癌患者是亚临床肝癌或小肝癌：
	\t非规则性肝切除仍为原发性肝癌患者的主要术式

	Example4#
	"text":"急性肺血栓栓塞症患者@对于妊娠患者首选低分子肝素，溶栓治疗仅适用于那些严重低血压、休克的妊娠患者。"
	patient:急性肺血栓栓塞症患者
	condition triples:["[急性肺血栓栓塞症患者,基本情况,妊娠]","[急性肺血栓栓塞症患者,临床表现,严重低血压]","[急性肺血栓栓塞症患者,临床表现,休克]"]

	请根据这段text，使用一颗前序二叉树来归纳总结出决策流程

	tree：
	if 急性肺血栓栓塞症患者有妊娠的情况：
	\tif 急性肺血栓栓塞症妊娠患者存在严重低血压、休克的情况：
	\t\t急性肺血栓栓塞症患者可以使用溶栓治疗
	\telse：
	\t\t急性肺血栓栓塞症患者首选低分子肝素治疗
	#
	"""
	en_example1 = """Example1#
	"text":"Patients with acute glomerulonephritis @ For patients with edema, oliguria, and circulatory bleeding, hydrochlorothiazide can be taken orally at 1 to 2 mg/kg 1-2 times a day for mild cases. For severe cases, furosemide, a powerful diuretic, can be given intravenously. 1~2mg/kg each time, 1-2 times a day."
	patient:Patients with acute glomerulonephritis
	condition triples:["[Patients with acute glomerulonephritis,clinical manifestation,edema]", "[Patients with acute glomerulonephritis,clinical manifestation,oliguria]", "[Patients with acute glomerulonephritis,clinical manifestation,circulatory bleeding]", "[Patients with acute glomerulonephritis,clinical manifestation,mild cases]", "[Patients with acute glomerulonephritis,clinical manifestation,severe cases]"]

	Please use a pre-order binary tree to summarize the decision-making process based on this text.

	tree：
	if Patients with acute glomerulonephritis have edema, oliguria, and circulatory bleeding：
	\tif Patients with acute glomerulonephritis have mild case：
	\t\tPatients with acute glomerulonephritis can take hydrochlorothiazide orally, 1 to 2 mg/kg 1 to 2 times a day.
	\telif Patients with acute glomerulonephritis have severe case：
	\t\tPatients with acute glomerulonephritis can be given furosemide, a powerful diuretic, intravenously at 1 to 2 mg/kg 1 to 2 times a day.
	#"""
	en_example2 = """Example2#
	"text":"Children with intestinal candidiasis @ Starting dose of ketoconazole: 100 mg orally daily for those weighing less than 30 kg; 200-400 mg orally daily for those weighing more than 30 kg; 50 mg orally daily for those 1 to 4 years old; 100 mg orally daily for those 5 to 12 years old."
	patient: Children with intestinal candidiasis
	condition triples:["[Children with intestinal candidiasis,basic condition,weighing less than 30 kg]","[Children with intestinal candidiasis,basic condition,weighing more than 30 kg]","[Children with intestinal candidiasis,basic condition,1 to 4 years old]","[Children with intestinal candidiasis,basic condition,5 to 12 years old]"]

	Please use a pre-order binary tree to summarize the decision-making process based on this text.

	tree：
	ifChildren with intestinal candidiasis weigh less than 30kg：
	\tChildren with intestinal candidiasis can take 100 mg of ketoconazole orally daily.
	elif Children with intestinal candidiasis weigh more than 30kg：
	\tChildren with intestinal candidiasis can take 200 to 400 mg of ketoconazole orally daily
	elif Children with intestinal candidiasis are aged 1 to 4 years old：
	\tChildren with intestinal candidiasis can take 50 mg of ketoconazole orally daily
	elif Children with intestinal candidiasis are aged 5 to 12 years old：
	\tChildren with intestinal candidiasis can take 100 mg of ketoconazole orally daily
	"""
	en_example3 = """Example3#
	"text":"Patients with primary liver cancer @ For clinical liver cancer or large liver cancer, if the patient's liver function is well compensated and there is no cirrhosis, regular liver resection is still the main surgical procedure. For subclinical liver cancer or small liver cancer, irregular liver resection has become the main surgical method."
	patient:Patients with primary liver cancer
	condition triples:["[Patients with primary liver cancer,clinical manifestation,clinical liver cancer]","[Patients with primary liver cancer,clinical manifestation,large liver cancer]", "[Patients with primary liver cancer,clinical manifestation,liver function is well compensated]", "[Patients with primary liver cancer,clinical manifestation,no cirrhosis]", "[Patients with primary liver cancer,clinical manifestation,subclinical liver cancer]", "[Patients with primary liver cancer,clinical manifestation,small liver cancer]"]

	Please use a pre-order binary tree to summarize the decision-making process based on this text.

	tree：
	if Patients with primary liver cancer have clinical liver cancer or large liver cancer.：
	\tif Patients with primary liver cancer have well-compensated liver function and no cirrhosis：
	\t\tRegular liver resection is still the main surgical procedure for patients with primary liver cancer.
	elif Patients with primary liver cancer have subclinical liver cancer or small liver cancer.：
	\tIrregular liver resection is still the main surgical procedure for patients with primary liver cancer.
	"""
	en_example4 = """Example4#
	"text":"Patients with acute pulmonary thromboembolism @ Low molecular weight heparin is the first choice for pregnant patients, and thrombolytic therapy is only suitable for pregnant patients with severe hypotension and shock."
	patient:Patients with acute pulmonary thromboembolism
	condition triples:["[Patients with acute pulmonary thromboembolism,basic condition,pregnant]","[Patients with acute pulmonary thromboembolism,clinical manifestation,severe hypotension]","[Patients with acute pulmonary thromboembolism,clinical manifestation,shock]"]
	Please use a pre-order binary tree to summarize the decision-making process based on this text.

	tree：
	if patient with acute pulmonary thromboembolism is pregnant：
	\tif Pregnant patients with acute pulmonary thromboembolism have severe hypotension and shock：
	\t\tPatients with acute pulmonary thromboembolism can use thrombolytic therapy.
	\telse：
	\t\tLow molecular weight heparin is the first choice for patients with acute pulmonary thromboembolism.
	"""
	en_prompt_list = []
	en_prompt_list.append(en_example1)
	en_prompt_list.append(en_example2)
	en_prompt_list.append(en_example3)
	en_prompt_list.append(en_example4)
	prompt = {
		"instruction" : instruction,
		"example" : example,
		"en_example" : en_prompt_list
	}
	return prompt

def prompt_ask_pseudocode_without_triplet() -> dict:
	instruction = """As an expert in medical knowledge and natural language processing, I will extract the corresponding if-else pseudocode structure for the sentence. I am skilled at performing tasks based on rules and instructions. I will learn form the example and form my response to your question.
	rules：
	- The text in the if or elif statement should only contain information about the patient's clinical manifestations or basic symptoms from the given text.
	- Patient should be the subject of the sentence in each statement.
	- Please strictly follow the output format of the given sample.
	- Please analyze the semantic structure of the sentence, understand and split it into pseudo-code of the if else structure.
	"""

	example = """Example1#
	"text":"急性肾小球肾炎患者@对于水肿、少尿、循环出血的患者，轻症可口服氢氯噻嗪，每次1~2mg/kg每日1-2次，重症患者可静脉给予呋塞米强力利尿剂，每次1~2mg/kg每日1-2次。"
	patient:急性肾小球肾炎患者
	请根据这段text，使用一颗前序二叉树来归纳总结出决策流程

	tree：
	if 急性肾小球肾炎患者有水肿、少尿、循环出血的情况：
	\tif 急性肾小球肾炎患者是轻症：
	\t\t急性肾小球肾炎患者可口服氢氯噻嗪，每次1~2mg/kg每日1-2次
	\telif 急性肾小球肾炎患者是重症：
	\t\t急性肾小球肾炎患者可静脉给予呋塞米强力利尿剂，每次1~2mg/kg每日1-2次。
	#
			
	Example2#
	"text":"肠道念珠菌病患儿@酮康唑开始剂量：体重30kg以下者每日口服100mg；30kg以上者每日口服200~400mg;1~4岁者每日口服50mg;5~12岁者每日口服100mg。"
	patient: 肠道念珠菌病患
	请根据这段text，使用一颗前序二叉树来归纳总结出决策流程

	tree：
	if 肠道念珠菌病患儿的体重在30kg以下：
	\t肠道念珠菌病患儿可以每日口服100mg酮康唑
	elif 肠道念珠菌病患儿的体重在30kg以上：
	\t肠道念珠菌病患儿可以每日口服200~400mg酮康唑
	elif 肠道念珠菌病患儿的年龄在1~4岁：
	\t肠道念珠菌病患儿可以每日口服50mg酮康唑
	elif 肠道念珠菌病患儿的年龄在5~12岁：
	\t肠道念珠菌病患儿可以每日口服100mg酮康唑

	Example3#
	"text":"原发性肝癌患者@对临床肝癌或大肝癌，如患者肝功能代偿良好，无肝硬化者，规则性肝切除仍为主要术式。对亚临床肝癌或小肝癌，非规则性肝切除成为主要术式。"
	patient:原发性肝癌患者
	请根据这段text，使用一颗前序二叉树来归纳总结出决策流程

	tree：
	if 原发性肝癌患者是临床肝癌或大肝癌：
	\tif 原发性肝癌患者肝功能代偿良好，无肝硬化：
	\t\t规则性肝切除仍为原发性肝癌患者的主要术式
	elif 原发性肝癌患者是亚临床肝癌或小肝癌：
	\t非规则性肝切除仍为原发性肝癌患者的主要术式

	Example4#
	"text":"急性肺血栓栓塞症患者@对于妊娠患者首选低分子肝素，溶栓治疗仅适用于那些严重低血压、休克的妊娠患者。"
	patient:急性肺血栓栓塞症患者
	请根据这段text，使用一颗前序二叉树来归纳总结出决策流程

	tree：
	if 急性肺血栓栓塞症患者有妊娠的情况：
	\tif 急性肺血栓栓塞症妊娠患者存在严重低血压、休克的情况：
	\t\t急性肺血栓栓塞症患者可以使用溶栓治疗
	\telse：
	\t\t急性肺血栓栓塞症患者首选低分子肝素治疗
	#
	"""
	en_example1 = """Example1#
	"text":"Patients with acute glomerulonephritis @ For patients with edema, oliguria, and circulatory bleeding, hydrochlorothiazide can be taken orally at 1 to 2 mg/kg 1-2 times a day for mild cases. For severe cases, furosemide, a powerful diuretic, can be given intravenously. 1~2mg/kg each time, 1-2 times a day."
	patient:Patients with acute glomerulonephritis
	Please use a pre-order binary tree to summarize the decision-making process based on this text.

	tree：
	if Patients with acute glomerulonephritis have edema, oliguria, and circulatory bleeding：
	\tif Patients with acute glomerulonephritis have mild case：
	\t\tPatients with acute glomerulonephritis can take hydrochlorothiazide orally, 1 to 2 mg/kg 1 to 2 times a day.
	\telif Patients with acute glomerulonephritis have severe case：
	\t\tPatients with acute glomerulonephritis can be given furosemide, a powerful diuretic, intravenously at 1 to 2 mg/kg 1 to 2 times a day.
	#"""
	en_example2 = """Example2#
	"text":"Children with intestinal candidiasis @ Starting dose of ketoconazole: 100 mg orally daily for those weighing less than 30 kg; 200-400 mg orally daily for those weighing more than 30 kg; 50 mg orally daily for those 1 to 4 years old; 100 mg orally daily for those 5 to 12 years old."
	patient: Children with intestinal candidiasis
	Please use a pre-order binary tree to summarize the decision-making process based on this text.

	tree：
	ifChildren with intestinal candidiasis weigh less than 30kg：
	\tChildren with intestinal candidiasis can take 100 mg of ketoconazole orally daily.
	elif Children with intestinal candidiasis weigh more than 30kg：
	\tChildren with intestinal candidiasis can take 200 to 400 mg of ketoconazole orally daily
	elif Children with intestinal candidiasis are aged 1 to 4 years old：
	\tChildren with intestinal candidiasis can take 50 mg of ketoconazole orally daily
	elif Children with intestinal candidiasis are aged 5 to 12 years old：
	\tChildren with intestinal candidiasis can take 100 mg of ketoconazole orally daily
	"""
	en_example3 = """Example3#
	"text":"Patients with primary liver cancer @ For clinical liver cancer or large liver cancer, if the patient's liver function is well compensated and there is no cirrhosis, regular liver resection is still the main surgical procedure. For subclinical liver cancer or small liver cancer, irregular liver resection has become the main surgical method."
	patient:Patients with primary liver cancer
	Please use a pre-order binary tree to summarize the decision-making process based on this text.

	tree：
	if Patients with primary liver cancer have clinical liver cancer or large liver cancer.：
	\tif Patients with primary liver cancer have well-compensated liver function and no cirrhosis：
	\t\tRegular liver resection is still the main surgical procedure for patients with primary liver cancer.
	elif Patients with primary liver cancer have subclinical liver cancer or small liver cancer.：
	\tIrregular liver resection is still the main surgical procedure for patients with primary liver cancer.
	"""
	en_example4 = """Example4#
	"text":"Patients with acute pulmonary thromboembolism @ Low molecular weight heparin is the first choice for pregnant patients, and thrombolytic therapy is only suitable for pregnant patients with severe hypotension and shock."
	patient:Patients with acute pulmonary thromboembolism
	Please use a pre-order binary tree to summarize the decision-making process based on this text.

	tree：
	if patient with acute pulmonary thromboembolism is pregnant：
	\tif Pregnant patients with acute pulmonary thromboembolism have severe hypotension and shock：
	\t\tPatients with acute pulmonary thromboembolism can use thrombolytic therapy.
	\telse：
	\t\tLow molecular weight heparin is the first choice for patients with acute pulmonary thromboembolism.
	"""
	en_prompt_list = []
	en_prompt_list.append(en_example1)
	en_prompt_list.append(en_example2)
	en_prompt_list.append(en_example3)
	en_prompt_list.append(en_example4)
	prompt = {
		"instruction" : instruction,
		"example" : example,
		"en_example" : en_prompt_list
	}
	return prompt

def prompt_logical_pred() -> dict:
	instruction = """As an expert in medical knowledge and natural lanquage processing, I am skilled at performing tasks based on rules and instructions.
		Here are some rules to follow:
		- The format of each triple is [head entity, relation, tail entity].
		- Each triple can only have one head entity and one tail entity with a single relationship.
		- Answer to my question in the procedure , 1.Observation, 2.Think,3.Plan, 4.Answer.All this procedures should appear in your response.
		- The final output should only be “and” or "or"."""
	example = """Example1#
		"text": "肥厚型心肌病患者@对于伴有左室流出道梗阻的患者，可采用药物治疗、植入ICD、化学消融以及手术治疗等方法以改善症状。对于无左室流出道梗阻的患者，治疗重点在于控制心律失常、改善左室充盈压力、缓解心绞痛和抑制疾病进展。",
		"triples":[[肥厚型心肌病患者,治疗方案,控制心律失常], [肥厚型心肌病患者,治疗方案,改善左室充盈压力],["肥厚型心肌病患者","治疗方案","缓解心绞痛"],["肥厚型心肌病患者", "治疗方案", "抑制疾病进展"]]

		Question:请使用“and","or" 中的一种来回答，依据text的语义，tripes中所有的三元组互相之间的逻辑关系是”and“还是“or".

		Observation:对于无左室流出道梗阻的患者，治疗重点在于控制心律失常、改善左室充盈压力、缓解心绞痛和抑制疾病进展。
		Think:依据observation的结果，triples中的四个三元组互相之间的逻辑关系可以用“and”来总结。
		Plan：我计划使用“and"与“or"中一个来回答，我选择代表且关系的and来回答问题。
		Answer： and
		#

		Example2#
		"text": "主动脉瓣重度狭窄患者@对于有明显症状者，可以进行主动脉瓣置换手术。对于无明显症状的患者，表现为收缩压较基线降低或收缩压较基线不能增加20mmHg以上，或与年龄性别正常标准相比运动耐力明显降低，对此类患者考虑择期手术置换主动脉瓣是合理。",
		"triples":[[主动脉瓣重度狭窄患者,临床表现,收缩压较基线降低], [主动脉瓣重度狭窄患者,临床表现,收缩压较基线不能增加20mmHg以上]]

		Question:请使用“and","or" 中的一种来回答，依据text的语义，tripes中所有的三元组互相之间的逻辑关系是”and“还是“or".

		Observation:对于无明显症状的患者，表现为收缩压较基线降低或收缩压较基线不能增加20mmHg以上，
		Think:依据observation的结果，triples中的两个三元组互相之间的逻辑关系可以用“or”来总结。
		Plan：我只能选择“and"与“or"中一个来回答，我选择代表或关系的or来回答问题。
		Answer： or
		#"""
	en_example = """Example1#
		"text": "Patients with hypertrophic cardiomyopathy @ For patients with left ventricular outflow tract obstruction, drug treatment, ICD implantation, chemical ablation, and surgical treatment can be used to improve symptoms. For patients without left ventricular outflow tract obstruction, treatment focuses on controlling arrhythmias, improving left ventricular filling pressure, relieving angina, and inhibiting disease progression.",
		"triples":[[Patients with hypertrophic cardiomyopathy,therapeutic schedule,controlling arrhythmias], [Patients with hypertrophic cardiomyopathy,therapeutic schedule,improving left ventricular filling pressure],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","relieving angina"],["Patients with hypertrophic cardiomyopathy", "therapeutic schedule", "inhibiting disease progression"]]

		Question:Please use one of "and" and "or" to answer. According to the semantics of text, the logical relationship between all triples in trips is "and" or "or".

		Observation:For patients without left ventricular outflow tract obstruction, treatment focuses on controlling arrhythmias, improving left ventricular filling pressure, relieving angina, and inhibiting disease progression.
		Think:According to the observation results, the logical relationship between the four triples in triples can be summarized by "and".
		Plan:I plan to use one of "and" and "or" to answer the question. I choose and, which represents the relationship, to answer the question.
		Answer:and
		#

		Example2#
		"text": "Patients with severe aortic valve stenosis @ For those with obvious symptoms, aortic valve replacement surgery can be performed. For patients without obvious symptoms whose systolic blood pressure is lower than the baseline or whose systolic blood pressure cannot increase by more than 20mmHg compared with the baseline, or whose exercise tolerance is significantly reduced compared with the normal standards for age and gender, it is reasonable to consider elective surgical replacement of the aortic valve for such patients. ",
		"triples":[[Patients with severe aortic valve stenosis,clinical manifestation,systolic blood pressure is lower than the baseline], [Patients with severe aortic valve stenosis,clinical manifestation,systolic blood pressure cannot increase by more than 20mmHg compared with the baseline]]

		Question:Please use one of "and" and "or" to answer. According to the semantics of text, the logical relationship between all triples in trips is "and" or "or".

		Observation:For patients without obvious symptoms whose systolic blood pressure is lower than the baseline or whose systolic blood pressure cannot increase by more than 20mmHg compared with the baseline.
		Think:According to the observation results, the logical relationship between the two triples in triples can be summarized by "or".
		Plan：I plan to use one of "and" and "or" to answer the question. I choose or which represents or relationship to answer the question.
		Answer： or
		#"""
	prompt={
		"instruction" : instruction,
		"example" : example,
		"en_example" : en_example
	}
	return prompt

def prompt_find_triples() -> dict:
	instruction = """作为医学知识和自然语言处理方面的专家，我需要为提供的句子选择语义相似的三元组，并且我擅长根据规则和指令执行任务。 我将从示例中学习并形成对您问题的回答。
	规则：
	- 你应该按照以下步骤回答：1.Observation；2.Thought；3.Plan；4.Answer
	- 你应该在观察中首先理解并列出每个三元组的含义
	- 将给定文本中在语义上所匹配的所有三元组添加到Answer中
	- 如果答案中添加了药物，您应该考虑该药物的用法用量信息
	- 你应该只在一个列表中回答，该列表指示特定的三元组是否出现在给定的文本中。如果列表为空，只需回答“[]”。仅此而已。
	- 例如：对于某个三元组列表[triple1:(triple1), Triple2(triple2),triple3:(triple3)]，如果文本中出现了triple1和triple3，则最终答案为[1,3]。"""
	
	example = """
	Example1#
	"text":"肠道念珠菌病患儿可以每日口服200~400mg酮康唑"
	"triples":[triple1:"[肠道念珠菌病患儿,治疗药物,酮康唑]", triple2:"[酮康唑,用法用量,口服]",triple3:"[酮康唑,用法用量，100mg]",triple4:"[酮康唑,用法用量，200~400mg]",triple5:"[酮康唑,用法用量，50mg]"，triple6:"[酮康唑,用法用量，100mg]]

	Question:
	请使用一个list来表示哪些triple所代表的语义出现在了给定text中，list中仅回答triple的序号即可，如果没有找到任何一个对应的triple，则回答一个空list"[]"。

	Observation：各个三元组的语义分别是，从第一个三元组triple1开始分析，triple1表示肠道念珠菌病患儿的治疗药物是酮康唑, triple2表示酮康唑的用法用量是口服,triple3:表示酮康唑的用法用量是100mg,triple4表示酮康唑的用法用量是200~400mg,triple5表示酮康唑的用法用量是50mg，triple6表示酮康唑的用法用量是100mg。
	Thought:根据observation中各个三元组的语义以及text中的内容"肠道念珠菌病患儿可以每日口服200~400mg酮康唑"，发现triple1，triple2，triple4的语义信息出现在了text中。
	Plan：将triple1，triple2，triple4的序号加入到answer的list中。
	Answer：
	[1,2,4]
	#

	Example2#
	"text":"肠道念珠菌病患儿可以每日口服50mg酮康唑"
	"triples":[triple1:"[肠道念珠菌病患儿,治疗药物,酮康唑]", triple2:"[酮康唑,用法用量,口服]",triple3:"[酮康唑,用法用量，100mg]",triple4:"[酮康唑,用法用量，200~400mg]",triple5:"[酮康唑,用法用量，50mg]"，triple6:"[酮康唑,用法用量，100mg]]

	Question:
	请使用一个list来表示哪些triple所代表的语义出现在了给定text中，list中仅回答triple的序号即可，如果没有找到任何一个对应的triple，则回答一个空list"[]"。

	Observation：各个三元组的语义分别是，从第一个三元组triple1开始分析，triple1表示肠道念珠菌病患儿的治疗药物是酮康唑, triple2表示酮康唑的用法用量是口服,triple3:表示酮康唑的用法用量是100mg,triple4表示酮康唑的用法用量是200~400mg,triple5表示酮康唑的用法用量是50mg，triple6表示酮康唑的用法用量是100mg。
	Thought:根据observation中各个三元组的语义以及text中的内容"肠道念珠菌病患儿可以每日口服50mg酮康唑"，发现triple1，triple2，triple5的语义信息出现在了text中。
	Plan：将triple1，triple2，triple5的序号加入到answer的list中。
	Answer：
	[1,2,5]
	#"""

	en_example = """
	Example1#
	"text":"Children with intestinal candidiasis can take orally 200-400mg of ketoconazole daily."
	"triples":[triple1:"[Children with intestinal candidiasis,drug therapy,ketoconazole]", triple2:"[ketoconazole,dosage and administration,orally]",triple3:"[ketoconazole,dosage and administration,100mg]",triple4:"[ketoconazole,dosage and administration,200~400mg]",triple5:"[ketoconazole,dosage and administration,50mg]",triple6:"[ketoconazole,dosage and administration,100mg]]

	Question:
	Please use a list to indicate which semantics represented by triples appear in the given text. Only the sequence number of the triples can be answered in the list. If no corresponding triple is found, answer an empty list "[]".

	Observation:The semantics of each triple are as follows: start with the analysis of the first triple 1, triple 1 indicates that the treatment drug for children with intestinal candidiasis is ketoconazole, triple 2 indicates that the usage and dosage of ketoconazole is oral, triple 3: Indicates the usage and dosage of ketoconazole is 100mg, triple4 indicates the usage and dosage of ketoconazole is 200~400mg, triple5 indicates the usage and dosage of ketoconazole is 50mg, triple6 indicates the usage and dosage of ketoconazole is 100mg.
	Thought:According to the semantics of each triple in the observation and the content in the text "Children with intestinal candidiasis can take 200~400 mg of ketoconazole orally every day", it was found that the semantic information of triple1, triple2, and triple4 appeared in the text.
	Plan:Add the serial numbers of triple1, triple2, and triple4 to the answer list.
	Answer:
	[1,2,4]
	#
	
	Example2#
	"text":"Children with intestinal candidiasis can take 50 mg of ketoconazole orally daily."
	"triples":[triple1:"[Children with intestinal candidiasis,drug therapy,ketoconazole]", triple2:"[ketoconazole,dosage and administration,orally]",triple3:"[ketoconazole,dosage and administration,100mg]",triple4:"[ketoconazole,dosage and administration,200~400mg]",triple5:"[ketoconazole,dosage and administration,50mg]",triple6:"[ketoconazole,dosage and administration,100mg]]

	Question:
	Please use a list to indicate which semantics represented by triples appear in the given text. Only the sequence number of the triples can be answered in the list. If no corresponding triple is found, answer an empty list "[]".

	Observation:The semantics of each triple are as follows: start with the analysis of the first triple 1, triple 1 indicates that the treatment drug for children with intestinal candidiasis is ketoconazole, triple 2 indicates that the usage and dosage of ketoconazole is oral, triple 3: Indicates the usage and dosage of ketoconazole is 100mg, triple4 indicates the usage and dosage of ketoconazole is 200~400mg, triple5 indicates the usage and dosage of ketoconazole is 50mg, triple6 indicates the usage and dosage of ketoconazole is 100mg.
	Thought:According to the semantics of each triple in the observation and the content in the text "Children with intestinal candidiasis can take 50 mg of ketoconazole daily", it was found that the semantic information of triple1, triple2, and triple5 appeared in the text.
	Plan:Add the serial numbers of triple1, triple2, and triple5 to the answer list.
	Answer:
	[1,2,5]
	#"""
	prompt = {
                  "instruction" : instruction,
                  "example" : example,
				  "en_example" : en_example
            }
	return prompt


def prompt_drug_type() -> dict:
	instruction = """As an expert in medical knowledge and natural language processing, I am skilled at performing tasks based on rules and instructions. I will learn form the example and form my response to your question.

	rules：
	- You can only answer "治疗药物“  or "禁用药物".No matter what!
	- You should answer the question only base on the given text
	- If you can't decide whether the drug is a banned drug or a therapeutic drug, please judge from the text whether it supports the use of this drug. If it is supported, it is a "治疗药物“, but if it is not supported, it is a "禁用药物".  """

	example = """Example#
	"text": "拉莫三嗪可能会加重肌阵挛发作。",

	Question:
	根据这段text描述的情况，判断拉莫三嗪是：禁用药物还是治疗药物

	Answer：禁用药物
	#"""
	prompt = {
                  "instruction" : instruction,
                  "example" : example
            }
	return prompt

def prompt_select_triplet_xiaorong() -> dict:
	instruction = """As an expert in medical knowledge and natural language processing, I am skilled at performing tasks based on rules and instructions. I will learn form the example and form my response to your question.
	rules：
	- You need to understand the text and extract a complete decision tree based on the given pseudocode and triples.
	- The provided pseudocode represents the structure of a decision tree. The natural language after if represents the conditional branch of the decision tree.
	- The provided triplet is the content of the decision tree node."""

	example = """Example1#
	"text": "肥厚型心肌病患者@对于伴有左室流出道梗阻的患者，可采用药物治疗、植入ICD、化学消融以及手术治疗等方法以改善症状。对于无左室流出道梗阻的患者，治疗重点在于控制心律失常、改善左室充盈压力、缓解心绞痛和抑制疾病进展。",
	"pseudocode":"if 肥厚型心肌病患者伴有左室流出道梗阻：\n    肥厚型心肌病患者可以采用药物治疗、植入ICD、化学消融以及手术治疗等方法以改善症状\nelse:\n    肥厚型心肌病患者的治疗重点在于控制心律失常、改善左室充盈压力、缓解心绞痛和抑制疾病进展",
	"triples":"["肥厚型心肌病患者","临床表现","左室流出道梗阻"],["肥厚型心肌病患者","治疗方案","药物治疗"],["肥厚型心肌病患者","治疗方案","植入ICD"],["肥厚型心肌病患者","治疗方案","化学消融"],["肥厚型心肌病患者","治疗方案","手术治疗"],["肥厚型心肌病患者","治疗方案","控制心律失常"],["肥厚型心肌病患者","治疗方案","改善左室充盈压力"],["肥厚型心肌病患者","治疗方案","缓解心绞痛"],["肥厚型心肌病患者","治疗方案","抑制疾病进展"]"
	Question:
	请根据提供的text、pseudocode和triples，抽取出text对应的诊疗决策树。
	Tree:
	[{"role": "C","triples": [["肥厚型心肌病患者","临床表现","左室流出道梗阻"]],"logical_rel": "null"},{"role": "D","triples": [["肥厚型心肌病患者","治疗方案","药物治疗"],["肥厚型心肌病患者","治疗方案","植入ICD"],["肥厚型心肌病患者","治疗方案","化学消融"],["肥厚型心肌病患者","治疗方案","手术治疗"]],"logical_rel": "or"},{"role": "D","triples": [["肥厚型心肌病患者","治疗方案","控制心律失常"],["肥厚型心肌病患者","治疗方案","改善左室充盈压力"],["肥厚型心肌病患者","治疗方案","缓解心绞痛"],["肥厚型心肌病患者","治疗方案","抑制疾病进展"]],"logical_rel": "and"}]
	#

	Example2#
	"text": "CAP患者@对于轻度患者，进行常规检查即可；对于中度或重度患者，进行血痰培养以及考虑进行肺炎球菌抗原检测和军团菌尿抗原检测。",
	"pseudocode":"if CAP患者是轻度患者：\n    CAP患者只需要进行常规检查即可\nelif CAP患者是中度或重度患者：\n    CAP患者需要进行血痰培养，同时考虑进行肺炎球菌抗原检测和军团菌尿抗原检测。",
	"triples":"["CAP患者","临床表现","轻度"],["CAP患者","治疗方案","常规检查"],["CAP患者","临床表现","中度"],["CAP患者","临床表现","重度"],["CAP患者","治疗方案","血痰培养"],["CAP患者","治疗方案","肺炎球菌抗原检测"],["CAP患者","治疗方案","军团菌尿抗原检测"]"
	Question:
	请根据提供的text、pseudocode和triples，抽取出text对应的诊疗决策树。
	Tree:
	[{"role": "C","triples": [["CAP患者","临床表现","轻度"]],"logical_rel": "null"},{"role": "D","triples": [["CAP患者","治疗方案","常规检查"]],"logical_rel": "null"},{"role": "C","triples": [["CAP患者","临床表现","中度"],["CAP患者","临床表现","重度"]],"logical_rel": "or"},{"role": "D","triples": [["CAP患者","治疗方案","血痰培养"],["CAP患者","治疗方案","肺炎球菌抗原检测"],["CAP患者","治疗方案","军团菌尿抗原检测"]],"logical_rel": "and"},{"role": "D","triples": [],"logical_rel": "null"}]
	"""

	en_example = """Example1#
	"text": "Patients with hypertrophic cardiomyopathy @ For patients with left ventricular outflow tract obstruction, drug therapy, ICD implantation, chemical ablation, and surgical treatment can be used to improve symptoms. For patients without left ventricular outflow tract obstruction, treatment focuses on controlling arrhythmias, improving left ventricular filling pressure, relieving angina, and inhibiting disease progression.",
	"pseudocode":"if patients with hypertrophic cardiomyopathy and left ventricular outflow tract obstruction：\n    Patients with hypertrophic cardiomyopathy can use drug treatment, ICD implantation, chemical ablation, and surgical treatment to improve symptoms.\nelse:\n    The treatment of patients with hypertrophic cardiomyopathy focuses on controlling arrhythmias, improving left ventricular filling pressure, relieving angina, and inhibiting disease progression.",
	"triples":"["Patients with hypertrophic cardiomyopathy","clinical manifestation","left ventricular outflow tract obstruction"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","drug treatment"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","ICD implantation"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","chemical ablation"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","surgical treatment"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","controlling arrhythmias"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","improving left ventricular filling pressure"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","relieving angina"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","inhibiting disease progression"]"
	Question:
	Please extract the diagnosis and treatment decision tree corresponding to the text based on the provided text, pseudocode and triples.
	Tree:
	[{"role": "C","triples": [["Patients with hypertrophic cardiomyopathy","clinical manifestation","left ventricular outflow tract obstruction"]],"logical_rel": "null"},{"role": "D","triples": [["Patients with hypertrophic cardiomyopathy","therapeutic schedule","drug treatment"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","ICD implantation"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","chemical ablation"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","surgical treatment"]],"logical_rel": "or"},{"role": "D","triples": [["Patients with hypertrophic cardiomyopathy","therapeutic schedule","controlling arrhythmias"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","improving left ventricular filling pressure"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","relieving angina"],["Patients with hypertrophic cardiomyopathy","therapeutic schedule","inhibiting disease progression"]],"logical_rel": "and"}]
	#

	Example2#
	"text": "Patients with CAP @ For mild patients, routine examinations are enough; for moderate or severe patients, blood sputum culture and pneumococcal antigen testing and Legionella urine antigen testing should be considered.",
	"pseudocode":"if Patients with CAP are mild patients:\n    Patients with CAP only need routine examinations\nelif Patients with CAP are moderate or severe patients:\n    Patients with CAP need to undergo blood sputum culture, and consider pneumococcal antigen testing and Legionella urinary antigen testing.",
	"triples":"["Patients with CAP","clinical manifestation","mild"],["Patients with CAP","therapeutic schedule","routine examinations"],["Patients with CAP","clinical manifestation","moderate"],["Patients with CAP","clinical manifestation","severe"],["Patients with CAP","therapeutic schedule","Blood sputum culture"],["Patients with CAP","therapeutic schedule","pneumococcal antigen testing"],["Patients with CAP","therapeutic schedule","Legionella urinary antigen testing"]"
	Question:
	Please extract the diagnosis and treatment decision tree corresponding to the text based on the provided text, pseudocode and triples.
	Tree:
	[{"role": "C","triples": [["Patients with CAP","clinical manifestation","mild"]],"logical_rel": "null"},{"role": "D","triples": [["Patients with CAP","therapeutic schedule","routine examinations"]],"logical_rel": "null"},{"role": "C","triples": [["Patients with CAP","clinical manifestation","moderate"],["Patients with CAP","clinical manifestation","severe"]],"logical_rel": "or"},{"role": "D","triples": [["Patients with CAP","therapeutic schedule","Blood sputum culture"],["Patients with CAP","therapeutic schedule","pneumococcal antigen testing"],["Patients with CAP","therapeutic schedule","Legionella urinary antigen testing"]],"logical_rel": "and"},{"role": "D","triples": [],"logical_rel": "null"}]
	#"""
	prompt = {
                  "instruction" : instruction,
                  "example" : example,
				  "en_example" : en_example
            }
	return prompt