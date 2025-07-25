# API

## 环境变量

暴露的参数，通过容器配置环境变量传入

| 参数              | 必传 | 说明                                                                                                                                                                                                                                                                                                     |
| ----------------- | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OPERATION_TYPE    | 是   | 操作类型<br>- 推理模式（INFERENCE）<br>- 评估模式（EVALUATION）<br>- 裁判模式（JUDGE）                                                                                                                                                                                                                   |
| INFERENCE_RESULT  | 是   | 推理结果路径，文件夹，多模型采用 inference_{MODEL_CONFIG_ID}_{DATASET_CONFIG_ID}.jsonl 文件名输出                                                                                                                                                                                                        |
| EVALUATION_RESULT | 是   | 评估结果路径，文件夹，多模型采用 evaluation_{MODEL_CONFIG_ID}_{DATASET_CONFIG_ID}.json 文件名输出                                                                                                                                                                                                        |
| DATASET_CONFIGS   | 是   | 支持传入多个数据集，使用 json 数组字符串形式，数组中 json 对象参考下方单个数据集配置设置                                                                                                                                                                                                                 |
| MODEL_CONFIGS     | 是   | 支持传入多模型配置，使用 json 数组字符串形式，数组中 json 对象参考下方单个模型配置设置                                                                                                                                                                                                                   |
| JUDGE_MODE        | 否   | 裁判模式<br>- 打分模式（SINGLE）<br>- 对比模式（MULTIPLE）                                                                                                                                                                                                                                               |
| INFERENCE_MODE    | 否   | 推理模式<br>- 覆盖原答案（OVERWRITE）<br>- 不覆盖原答案（NOT_OVERWRITE）                                                                                                                                                                                                                                 |
| PROMPT            | 否   | 提示词                                                                                                                                                                                                                                                                                                   |
| PROMPT_MODE       | 否   | 配合 PROMPT 参数使用，不同模式组装出的提示词不同，参数值如下<br>- System 角色注入模式(SYSTEM_PROMPT)：使用 system 角色传入 prompt<br>- 双 Human 轮次模式(DUAL_HUMAN)：通过两次 human 角色提问来传入 prompt<br>- Prompt 合并输入模式(PROMPT_MERGE)：通过替换 prompt 中 `{{}}` 关键字为 `\n[{用户问题}]\n` |

**PROMPT_MODE 参数说明：**
```json
// SYSTEM_PROMPT
[{"role": "system", "content": "{prompt}"},{"role": "human", "content": "{question}"},{"role": "bot", "content": "{anwser}"}]
// DUAL_HUMAN
[{"role": "human", "content": "{prompt}"},{"role": "human", "content": "{question}"},{"role": "bot", "content": "{anwser}"}]
// PROMPT_MERGE，会合并prompt和问题作为新的
[{"role": "human", "content": "{prompt}{question}"},{"role": "bot", "content": "{anwser}"}]
```

### 数据集配置（DATASET_CONFIGS）

| 参数               | 必传 | 说明                                                                                                                                   |
| ------------------ | ---- | -------------------------------------------------------------------------------------------------------------------------------------- |
| DATASET_CONFIG_ID  | 是   | 数据集配置id，唯一即可                                                                                                                 |
| DATASET_TYPE       | 是   | 数据集配置类型，支持用户自定义数据集和内置数据集<br>- BUILT_IN：内置数据集<br>- CUSTOM：用户自定义数据集                               |
| EVALUATION_METRICS | 否   | 评估指标，多个指标使用 "," 分隔开，不传时使用通用的默认指标进行评估<br>- 通用指标：BLEU-4,rouge1,rouge2,rougeL,rougeLsum<br>- 其他指标 |

#### 数据集配置类型 - 内置数据集配置（BUILT_IN）
**注意**： 由于每种内置数据集都可能包含多个子数据集，输出推理结果难以和配置一一对应，所以不支持推理模式，不保存推理结果，在评估模式中也仅输出评估结果

| 参数             | 必传 | 说明                                                                                                        |
| ---------------- | ---- | ----------------------------------------------------------------------------------------------------------- |
| BUILT_IN_DATASET | 是   | 内置数据集名称，部分指标和数据集存在特定的 n-n 关系，请注意区分，内置数据集评估指标目前固定，暂不支持自定义 |

#### 数据集配置类型 - 自定义数据集配置（CUSTOM）

| 参数                | 必传 | 说明                                                                                                                                                                                                          |
| ------------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CUSTOM_DATASET_PATH | 是   | 自定义数据集路径<br>- 支持文件夹和jsonl文件，多个路径使用 "," 分隔<br>- 文件夹内需包含数据集对应的jsonl文件<br>- jsonl文件内容请使用平台数据集标准格式<br>- **注意**：多路径进行评估时会先合并成一个jsonl文件 |


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

| 参数             | 必传 | 说明                                                                                                                                                        |
| ---------------- | ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MODEL_CONFIG_ID  | 是   | 模型配置ID，唯一即可                                                                                                                                        |
| MODEL_TYPE       | 是   | 模型配置类型<br>- API: 推理服务API，仅提供API，兼容 OPENAI 规范推理接口<br>- BUILT_IN: 内置模型，根据内置配置决定模型加载和使用方式<br>- CUSTOM: 自定义模型 |
| TEMPERATURE      | 否   | 控制采样温度（0 表示贪婪解码），默认0                                                                                                                       |
| TOP_P            | 否   | 控制要考虑的排名靠前的 token 的累积概率的浮点数。必须在(0, 1]之间。设置为 1 表示考虑所有 token。，默认1                                                     |
| PRESENCE_PENALTY | 否   | 对已经出现过的 token 增加/减少其再次出现的概率，默认0                                                                                                       |
| CONCURRENCY      | 否   | 并发请求数量，默认1                                                                                                                                         |


#### 模型配置类型 - API

| 参数             | 必传 | 说明                                                                                  |
| ---------------- | ---- | ------------------------------------------------------------------------------------- |
| API_TYPE         | 是   | API类型，用来区分请求和返回数据格式<br>- OpenAI: OpenAI 格式<br>- Spark: 星火API 格式 |
| API_URL          | 是   | API地址                                                                               |
| API_KEY          | 是   | API的key                                                                              |
| API_MODEL        | 否   | API的model，有些api需要设置，不设置默认使用MODEL_CONFIG_ID                            |
| API_EXTRA_CONFIG | 否   | 其他配置，json字符串形式                                                              |
```json
// 讯飞公有云协议相关参数参考
{
  "DOMAIN": "",
  "APP_ID": "",
  "API_KEY": "",
  "API_SECRET": ""
}
```

#### 模型配置类型 - CUSTOM

| 参数              | 必传 | 说明                                     |
| ----------------- | ---- | ---------------------------------------- |
| CUSTOM_MODEL_NAME | 否   | 自定义模型名称                           |
| BASE_MODEL_PATH   | 是   | 基础模型路径                             |
| LORA_WEIGHT_PATH  | 否   | LoRA权重路径，有的话就会加载，否则不加载 |
| NUMS_GPUS         | 是   | 占卡数量                                 |

#### 模型配置类型 - BUILT_IN

| 参数                | 必传 | 说明         |
| ------------------- | ---- | ------------ |
| BUILD_IN_MODEL_NAME | 是   | 内置模型名称 |

#### 示例

```json
[
  {
    "MODEL_CONFIG_ID": "qwen-plus-2025-01-25",
    "MODEL_TYPE": "API",
    "TEMPERATURE": "",
    "TOP_P": "",
    "PRESENCE_PENALTY": "",
    "API_TYPE": "OpenAI",
    "API_URL": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "API_KEY": "dasfasdfasdfasdf",
    "API_MODEL": "qwen-plus-2025-01-25",
  },
  {
    "MODEL_CONFIG_ID": "qwen-plus-2025-01-25",
    "MODEL_TYPE": "CUSTOM",
    "TEMPERATURE": "",
    "TOP_P": "",
    "PRESENCE_PENALTY": "",
    "CUSTOM_MODEL_NAME": "",
    "BASE_MODEL_PATH": "/iflytek/base_model",
    "LORA_WEIGHT_PATH": "",
    "NUMS_GPUS": 1,
  }
]
```

## 数据集格式

### 输入数据集
输入数据集目前支持平台一问一答类型数据，裁判模式（JUDGE）需要额外 prediction 字段用来标识推理结果

**注意**：
裁判模式为对比模式时
  - 相同数据集来源，不同模型的推理结果存储于单个jsonl文件时，jsonl文件内容需满足特定格式
```json
// 多个模型推理结果，对比模式
{
    "input": "1 + 1 = ?",
    "target": "2",
    "predictions": {
      "model_A": "3",
      "model_B": "2"
    }
}
```
- 相同数据集来源，不同模型的推理结果存储于多个jsonl文件时，文件路径需同时放在数据集配置 `DATASET_CONFIGS` 下的  `CUSTOM_DATASET_PATH` 参数下，用逗号分隔，每个jsonl文件格式如下，后续也会合并为单个jsonl，合并结果格式同上，模型名称会取文件名称
```json
// 单个模型推理结果，打分模式
{
    "input": "1 + 1 = ?",
    "target": "2",
    "prediction": "2"
}
```


### 推理结果
推理结果保存在 INFERENCE_RESULT 路径下，文件名为 inference_{MODEL_CONFIG_ID}_{DATASET_CONFIG_ID}.jsonl，推理结果为 jsonl 格式，每行一个 json 对象。

### 示例
```json
{
    "input": "1 + 1 = ?",
    "target": "2",
    "prediction": "2"
}
```

### 字段说明
- input: 输入数据集问题
- target: 输入数据集答案
- prediction: 推理结果

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