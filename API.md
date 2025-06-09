# API

## ENVIRONMENT

暴露的参数，通过容器配置的环境变量传入

1. OPERATION_TYPE： 操作类型，固定枚举，推理模式（INFERENCE），评估模式（EVALUATION），裁判模式（JUDGE）
2. INFERENCE_RESULT: 推理结果路径，文件夹，多模型采用 inference_{MODEL_CONFIG_ID}_{DATASET_CONFIG_ID}.jsonl 文件名输出
3. EVALUATION_RESULT: 评估结果路径，文件夹，多模型采用 evaluation_{MODEL_CONFIG_ID}_{DATASET_CONFIG_ID}.json 文件名输出
4. DATASET_CONFIGS: 支持传入多个数据集，使用 json 数组字符串形式，数组中 json 对象参考下方单个数据集配置设置
5. MODEL_CONFIGS: 支持传入多模型配置，使用 json 数组字符串形式，数组中 json 对象参考下方单个模型配置设置
6. JUDGE_PROMPT：裁判模型提示词

### DATASET_CONFIGS

1. DATASET_CONFIG_ID: 数据集配置id，唯一即可
2. DATASET_TYPE: 数据集类型，支持用户自定义数据集和内置数据集
	- BUILT_IN：内置数据集
	- CUSTOM：用户自定义数据集
3. EVALUATION_METRICS: 评估指标，多个指标使用 "," 分隔开，不传时使用通用的默认指标进行评估
	- 通用指标：BLEU-4,rouge1,rouge2,rougeL,rougeLsum
	- 其他指标

#### BUILT_IN
1. BUILT_IN_DATASET: 内置数据集名称，部分指标和数据集存在特定的 n-n 关系，请注意区分，内置数据集评估指标目前固定，暂不支持自定义

#### CUSTOM
1. CUSTOM_DATASET_PATH: 自定义数据集路径
	- 支持文件夹和jsonl文件，多个路径使用 "," 分隔
	- 文件夹内需包含数据集对应的jsonl文件
	- jsonl文件内容请使用平台数据集标准格式
	- 注意：多路径进行评估时会先合并成一个jsonl文件


#### 示例

```json
[
  {
    "DATASET_CONFIG_ID": "gsm8k_0",
    "DATASET_TYPE": "CUSTOM",
    "EVALUATION_METRICS": "BLEU-4,rouge1,rouge2,rougeL",
    "BUILT_IN_DATASET": "",
    "CUSTOM_DATASET_PATH": "/your_dataset_dir/gsm8k_0.jsonl"
  }
]
```

### MODEL_CONFIGS
1. MODEL_CONFIG_ID: 模型配置ID，唯一即可
2. MODEL_TYPE: 模型类型
	- API: 推理服务API，仅提供API，兼容 OPENAI 规范推理接口
	- BUILT_IN: 内置模型，根据内置配置决定模型加载和使用方式
	- CUSTOM: 自定义模型
3. TEMPERATURE: 控制采样温度（0 表示贪婪解码），默认0
4. TOP_K: 每一步只从 top_k 个 token 中采样，默认-1(disable)
5. PRESENCE_PENALTY: 对已经出现过的 token 增加/减少其再次出现的概率，默认0

#### API
1. API_TYPE: API类型，用来区分请求和返回数据格式
	- OpenAI: OpenAI 格式
	- Spark: 星火API 格式
2. API_URL: API地址
3. API_KEY: API的key
4. API_MODEL: API的model，有些api需要设置，不设置默认使用MODEL_CONFIG_ID
5. API_EXTRA_CONFIG: 其他配置，json字符串形式

#### BUILT_IN
1. BUILD_IN_MODEL_NAME: 内置模型名称

#### CUSTOM
1. CUSTOM_MODEL_NAME: 自定义模型名称
2. BASE_MODEL_PATH: 基础模型路径
3. LORA_WEIGHT_PATH: LoRA权重路径，有的话就会加载，否则不加载

#### 示例

```json
[
  {
    "MODEL_CONFIG_ID": "qwen-plus-2025-01-25",
    "MODEL_TYPE": "API",
    "PROMPT": "",
    "TEMPERATURE": "",
    "TOP_K": "",
    "PRESENCE_PENALTY": "",
    "API_TYPE": "OpenAI",
    "API_URL": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "API_KEY": "sk-8c019c61a5524a4fa6222ff0e9de9130",
    "API_MODEL": "qwen-plus-2025-01-25"
  },
  {
    "MODEL_CONFIG_ID": "qwen-plus-2025-01-25",
    "MODEL_TYPE": "CUSTOM",
    "PROMPT": "",
    "TEMPERATURE": "",
    "TOP_K": "",
    "PRESENCE_PENALTY": "",
    "CUSTOM_MODEL_NAME": "",
    "BASE_MODEL_PATH": "/iflytek/base_model",
    "LORA_WEIGHT_PATH": ""
  }
]
```

## 评估结果
评估结果保存在 EVALUATION_RESULT 路径下，文件名为 evaluation_{MODEL_CONFIG_ID}_{DATASET_CONFIG_ID}.json

示例如下：
```json
{
    "BLEU-4": {
        "score": 4.044942824477648,
        "counts": [
            637,
            233,
            90,
            36
        ],
        "totals": [
            3676,
            3666,
            3656,
            3646
        ],
        "precisions": [
            17.328618063112078,
            6.355701036552101,
            2.461706783369803,
            0.9873834339001646
        ],
        "bp": 1.0,
        "sys_len": 3676,
        "ref_len": 997
    },
    "rouge1": {
        "precision": 0.21715204862065327,
        "recall": 0.7614587955888169,
        "fmeasure": 0.3308124911310067
    },
    "rouge2": {
        "precision": 0.08071117172277745,
        "recall": 0.2744374163707398,
        "fmeasure": 0.1227120876612372
    },
    "rougeL": {
        "precision": 0.15354296085506028,
        "recall": 0.5562949883181789,
        "fmeasure": 0.23563005831748232
    }
}
```

## 推理结果
推理结果保存在 INFERENCE_RESULT 路径下，文件名为 inference_{MODEL_CONFIG_ID}_{DATASET_CONFIG_ID}.jsonl，推理结果为 jsonl 格式，每行一个 json 对象。

示例如下：
```json
{
    "input": "1 + 1 = ?",
    "target": "2",
}
```