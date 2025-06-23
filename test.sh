bash purge.sh
# export MODEL_CONFIGS='[{"MODEL_CONFIG_ID":"qwen-turbo-latest","MODEL_TYPE":"API","PROMPT":"","TEMPERATURE":"","TOP_K":"","PRESENCE_PENALTY":"","API_TYPE":"OpenAI","API_URL":"https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions","API_KEY":"sk-8c019c61a5524a4fa6222ff0e9de9130","API_MODEL":"qwen-turbo-latest"}]' 
# export DATASET_CONFIGS='[{"DATASET_CONFIG_ID":"gsm8k_0","DATASET_TYPE":"CUSTOM","EVALUATION_METRICS":"BLEU-4,rouge1,rouge2,rougeL,rougeLsum","BUILT_IN_DATASET":"","CUSTOM_DATASET_PATH":"/Users/humuh/source/my/model_evaluation/datasets/gsm8k_0.jsonl,/Users/humuh/source/my/model_evaluation/datasets/gsm8k_1.jsonl"},{"DATASET_CONFIG_ID":"gsm8k_1","DATASET_TYPE":"CUSTOM","EVALUATION_METRICS":"BLEU-4,rouge1,rouge2,rougeL","BUILT_IN_DATASET":"","CUSTOM_DATASET_PATH":"/Users/humuh/source/my/model_evaluation/datasets/gsm8k_1.jsonl"}]'
# export MODEL_CONFIGS='[{"MODEL_CONFIG_ID":"ChatGLM_4_9B_8K","MODEL_TYPE":"API","PROMPT":"","TEMPERATURE":"","TOP_K":"","PRESENCE_PENALTY":"","API_TYPE":"OpenAI","API_URL":"http://172.30.212.36:80/default/public-cluster-npu/inference/bt-none-296ccf7/inference/v1/chat/completions","API_KEY":"sk-8c019c61a5524a4fa6222ff0e9de9130","API_MODEL":"ChatGLM_4_9B_8K"}]'
# export DATASET_CONFIGS='[{"DATASET_CONFIG_ID":"gsm8k_0","DATASET_TYPE":"CUSTOM","EVALUATION_METRICS":"BLEU-4,rouge1,rouge2,rougeL,rougeLsum","BUILT_IN_DATASET":"","CUSTOM_DATASET_PATH":"/Users/humuh/source/my/model_evaluation/datasets/gsm8k_0.jsonl,/Users/humuh/source/my/model_evaluation/datasets/gsm8k_1.jsonl"}, {"DATASET_CONFIG_ID":"gsm8k_1","DATASET_TYPE":"CUSTOM","EVALUATION_METRICS":"BLEU-4,rouge1,rouge2,rougeL,rougeLsum","BUILT_IN_DATASET":"","CUSTOM_DATASET_PATH":"/Users/humuh/source/my/model_evaluation/datasets/gsm8k_0.jsonl"}]'

export MODEL_CONFIGS='[{"MODEL_CONFIG_ID":"gemma3:1b","MODEL_TYPE":"API","PROMPT":"","TEMPERATURE":"","TOP_K":"","PRESENCE_PENALTY":"","API_TYPE":"OpenAI","API_URL":"http://127.0.0.1:11434/v1/chat/completions","API_KEY":"","API_MODEL":"gemma3:1b"}]'

# spark
# export MODEL_CONFIGS='[{"MODEL_CONFIG_ID":"","MODEL_TYPE":"API","PROMPT":"","TEMPERATURE":"","TOP_P":"","PRESENCE_PENALTY":"","API_TYPE":"Spark","API_URL":"ws://172.30.212.36:80/default/public-cluster-npu/inference/bt-none-96c2dd8/inference//turing/v3/gpt","API_KEY":"","API_MODEL":""}]'
# export DATASET_CONFIGS='[{"DATASET_CONFIG_ID":"gsm8k_1","DATASET_TYPE":"CUSTOM","CUSTOM_DATASET_PATH":"/Users/humuh/source/my/model_evaluation/pre_dataset/gsm8k_0.jsonl", "EVALUATION_METRICS":"BLEU-4,rouge1,rouge2,rougeL,rougeLsum"}]'
export DATASET_CONFIGS='[{"DATASET_CONFIG_ID":"GaokaoBench","DATASET_TYPE":"BUILT_IN","BUILT_IN_DATASET":"GaokaoBench"}]'
export OPERATION_TYPE="EVALUATION"
export INFERENCE_RESULT='/tmp/inference'
export EVALUATION_RESULT='/tmp/evaluation'
# export INFERENCE_MODE="OVERWRITE"
# export PROMPT="【系统提示】\n你是一名公正、客观且专业的 AI 模型评估专家，核心任务是对多个 AI 助手（模型数量≥2）针对相同问题所生成的回答进行全面质量比较，并分别精准打分，最终判定出最优模型，或明确为并列情况。\n本次评估场景为{{scene}}，具体定义如下：\n{{scene_desc}}\n在评估过程中，需严格依据下列多维度评估标准，对每一个模型的输出回答进行仔细考量与打分，满分为{{max_score}}分。\n【评估标准】\n{{metric}}\n【评分流程】\n仔细研读用户输入内容、参考答案（若有），以及所有待评估模型的输出回答。\n按照各项评估标准，逐一、严谨地对每个模型的回答进行逐项打分，确保评分公正合理，如实反映各模型回答质量，分数为0 ~ {{max_score}}间的整数。\n综合各模型在各评估标准下的得分及其整体表现，精准判定出表现最优的模型，或确定各模型间是否为并列关系。若存在多个模型并列最优的情况，亦需明确指出；若所有模型表现均不佳，可判定没有胜出者。\n凝练、准确地阐述评分依据，突出各模型之间的主要优劣对比点，便于理解本次评分的合理性与准确性。\n【用户指令】\n{{input}}\n【模型回答列表】\n各模型对应的回答(json格式）：\n{\n	A:{{output_a}}（模型A的回答内容）\n	B:{{output_b}}（模型B的回答内容）\n	C:{{output_c}}（模型C的回答内容）\n	……（依次罗列所有模型的回答）\n}\n\n【参考答案】（如无可留空）\n{{ref_answer}}\n请严格遵循如下结构化格式输出结果，不得添加 JSON 结构之外的任何额外内容：\n【输出格式】\n{\n\"scores\": {\n	\"score_a\": 4,  // 模型A的得分\n	\"score_b\": 3,  // 模型B的得分\n	\"score_c\": 5   // 模型C的得分\n	……  // 其他模型对应分数组\n},\n\"best_model\": \"C\",  // 可选值为模型标识（如\"A\"、\"B\"、\"C\"等），若存在多个最优模型，则以列表形式呈现，如[\"A\", \"C\"]；若无胜出者，则填\"NO_WINNER\"\n\"reason\": \"模型C在准确性、逻辑性及完整性等多方面表现突出，优于其他模型；模型A虽表述较清晰但在关键信息覆盖上不足；模型B准确性欠佳且条理性差。\"\n}\n\n注意事项：\n- 各模型分数务必为0 ~ {{max_score}} 间的整数，如实体现回答整体质量。\n- \"best_model\" 字段需精准填写最优模型标识，多个并列最优用列表形式，无胜出者填 \"NO_WINNER\"。\n- \"reason\" 字段应简洁明了、重点突出，清晰呈现各模型间的优劣对比关键点，字数一般控制在100字以内。\n- 严格遵守上述输出格式要求，确保输出内容完整准确且可直接解析利用，不得出现任何不符合格式规范的内容。"
# export PROMPT_MODE="PROMPT_MERGE"
# export JUDGE_MODE="MULTIPLE"

# export DATASET_SOURCE="ModelScope"

bash start.sh
