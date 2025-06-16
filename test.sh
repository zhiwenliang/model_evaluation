# export MODEL_CONFIGS='[{"MODEL_CONFIG_ID":"qwen-turbo-latest","MODEL_TYPE":"API","PROMPT":"","TEMPERATURE":"","TOP_K":"","PRESENCE_PENALTY":"","API_TYPE":"OpenAI","API_URL":"https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions","API_KEY":"sk-8c019c61a5524a4fa6222ff0e9de9130","API_MODEL":"qwen-turbo-latest"}]' 
# export DATASET_CONFIGS='[{"DATASET_CONFIG_ID":"gsm8k_0","DATASET_TYPE":"CUSTOM","EVALUATION_METRICS":"BLEU-4,rouge1,rouge2,rougeL,rougeLsum","BUILT_IN_DATASET":"","CUSTOM_DATASET_PATH":"/Users/humuh/source/my/model_evaluation/datasets/gsm8k_0.jsonl,/Users/humuh/source/my/model_evaluation/datasets/gsm8k_1.jsonl"},{"DATASET_CONFIG_ID":"gsm8k_1","DATASET_TYPE":"CUSTOM","EVALUATION_METRICS":"BLEU-4,rouge1,rouge2,rougeL","BUILT_IN_DATASET":"","CUSTOM_DATASET_PATH":"/Users/humuh/source/my/model_evaluation/datasets/gsm8k_1.jsonl"}]'
# export MODEL_CONFIGS='[{"MODEL_CONFIG_ID":"ChatGLM_4_9B_8K","MODEL_TYPE":"API","PROMPT":"","TEMPERATURE":"","TOP_K":"","PRESENCE_PENALTY":"","API_TYPE":"OpenAI","API_URL":"http://172.30.212.36:80/default/public-cluster-npu/inference/bt-none-296ccf7/inference/v1/chat/completions","API_KEY":"sk-8c019c61a5524a4fa6222ff0e9de9130","API_MODEL":"ChatGLM_4_9B_8K"}]'
# export DATASET_CONFIGS='[{"DATASET_CONFIG_ID":"gsm8k_0","DATASET_TYPE":"CUSTOM","EVALUATION_METRICS":"BLEU-4,rouge1,rouge2,rougeL,rougeLsum","BUILT_IN_DATASET":"","CUSTOM_DATASET_PATH":"/Users/humuh/source/my/model_evaluation/datasets/gsm8k_0.jsonl,/Users/humuh/source/my/model_evaluation/datasets/gsm8k_1.jsonl"}, {"DATASET_CONFIG_ID":"gsm8k_1","DATASET_TYPE":"CUSTOM","EVALUATION_METRICS":"BLEU-4,rouge1,rouge2,rougeL,rougeLsum","BUILT_IN_DATASET":"","CUSTOM_DATASET_PATH":"/Users/humuh/source/my/model_evaluation/datasets/gsm8k_0.jsonl"}]'

# export MODEL_CONFIGS='[{"MODEL_CONFIG_ID":"qwen-turbo-latest","MODEL_TYPE":"API","PROMPT":"","TEMPERATURE":"","TOP_K":"","PRESENCE_PENALTY":"","API_TYPE":"OpenAI","API_URL":"https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions","API_KEY":"sk-8c019c61a5524a4fa6222ff0e9de9130","API_MODEL":"qwen-turbo-latest"}]'

# spark
export MODEL_CONFIGS='[{"MODEL_CONFIG_ID":"","MODEL_TYPE":"API","PROMPT":"","TEMPERATURE":"","TOP_P":"","PRESENCE_PENALTY":"","API_TYPE":"Spark","API_URL":"ws://172.30.212.36:80/default/public-cluster-npu/inference/bt-none-ec9bb83/inference//turing/v3/gpt","API_KEY":"","API_MODEL":""}]'
export DATASET_CONFIGS='[{"DATASET_CONFIG_ID":"gsm8k_1","DATASET_TYPE":"CUSTOM","EVALUATION_METRICS":"BLEU-4,rouge1,rouge2,rougeL,rougeLsum","BUILT_IN_DATASET":"","CUSTOM_DATASET_PATH":"/Users/humuh/source/my/model_evaluation/pre_dataset/gsm8k_0.jsonl"}]'
export OPERATION_TYPE="INFERENCE"
export INFERENCE_RESULT='/tmp/inference'
export EVALUATION_RESULT='/tmp/evaluation'

bash start.sh
