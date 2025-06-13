# flake8: noqa: D100
"""
config for evaluation and inference
"""

from os import getenv
from json import loads as json_loads

from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.openicl.icl_evaluator.custom_evaluator import CustomEvaluator
from opencompass.models import VLLM
from opencompass.models import XunFeiSpark
from opencompass.datasets import CustomDataset
from opencompass.models.custom_openai import CustomOpenAI


print("----------------------------------")
print("Loading config...")
operation_type = getenv("OPERATION_TYPE")
dataset_configs = getenv("DATASET_CONFIGS")
model_configs = getenv("MODEL_CONFIGS")
system_prompt = getenv("SYSTEM_PROMPT")
judge_mode = getenv("JUDGE_MODE")
print("operation_type: ", operation_type)
print("dataset_configs: ", dataset_configs)
print("model_configs: ", model_configs)
print("system_prompt: ", system_prompt)
print("judge_mode: ", judge_mode)

output_column = "target" if operation_type == "EVALUATION" else ""
custom_reader_cfg = dict(
    input_columns=["input", "target", "prediction", "predictions"],
    output_column=output_column
)

custom_infer_cfg = dict(
    prompt_template=dict(
        type=PromptTemplate,
        template="{input}",
    ),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(type=GenInferencer),
)

# datasets config
datasets = []
# models config
models = []

# 数据集配置列表，json数组
if dataset_configs:
    dataset_config_list = json_loads(dataset_configs)
    if operation_type in ["EVALUATION", "INFERENCE"]:
        custom_infer_cfg = dict(
            prompt_template=dict(
                type=PromptTemplate,
                template="{input}",
            ),
            retriever=dict(type=ZeroRetriever),
            inferencer=dict(type=GenInferencer),
        )
        for dataset_config in dataset_config_list:
            # DATASET_CONFIG_ID
            # DATASET_TYPE(BUILT_IN, CUSTOM)
            # EVALUATION_METRICS(ROUGE-1, ROUGE-2, ROUGE-L, BLEU-4)
            # BUILT_IN_DATASET
            # CUSTOM_DATASET_PATH
            # Assemble dataset config for opencompass
            dataset_config_id = dataset_config.get("DATASET_CONFIG_ID")
            dataset_type = dataset_config.get("DATASET_TYPE")
            evaluation_metrics = dataset_config.get("EVALUATION_METRICS")
            evaluation_metric_list = []
            if evaluation_metrics:
                evaluation_metric_list = evaluation_metrics.split(",")
            if dataset_type == "BUILT_IN":
                build_in_dataset = dataset_config.get("BUILT_IN_DATASET")
                # todo
            elif dataset_type == "CUSTOM":
                custom_dataset_path = dataset_config.get("CUSTOM_DATASET_PATH")
                # set metrics for evaluator
                custom_eval_cfg = dict(
                    evaluator=dict(
                        type=CustomEvaluator,
                        metrics=evaluation_metric_list
                    ),
                )
                print("dataset_config_id: ", dataset_config_id)
                datasets += [
                    dict(
                        abbr=dataset_config_id,
                        type=CustomDataset,
                        path=custom_dataset_path,
                        reader_cfg=custom_reader_cfg,
                        infer_cfg=custom_infer_cfg,
                        eval_cfg=custom_eval_cfg,
                        local_mode=True,
                    ),
                ]
    elif operation_type == "JUDGE":
        for dataset_config in dataset_config_list:
            dataset_config_id = dataset_config.get("DATASET_CONFIG_ID")
            custom_dataset_path = dataset_config.get("CUSTOM_DATASET_PATH")
            # 单个数据集配置，评分模式
            # 多个数据集配置，对比模式
            if judge_mode == "SINGLE":
                judge_template = (
                    "用户指令：{input}\n"
                    "模型回答: {prediction}\n"
                    "参考答案：{target}"
                )
            elif judge_mode == "MULTIPLE":
                judge_template = (
                    "用户指令：{input}\n"
                    "模型回答: {predictions}\n"
                    "参考答案：{target}"
                )
            else:
                raise ValueError(
                    "Unsupported judge mode: {}".format(judge_mode)
                )
            judge_infer_cfg = dict(
                prompt_template=dict(
                    type=PromptTemplate,
                    template=dict(
                        begin=[
                            dict(
                                role='SYSTEM',
                                fallback_role='HUMAN',
                                prompt=system_prompt
                            ),
                        ],
                        round=[
                            dict(
                                role='HUMAN',
                                prompt=judge_template,
                            ),
                        ],
                    ),
                ),
                retriever=dict(type=ZeroRetriever),
                inferencer=dict(type=GenInferencer),
            )
            datasets += [
                dict(
                    abbr=dataset_config_id,
                    type=CustomDataset,
                    path=custom_dataset_path,
                    reader_cfg=custom_reader_cfg,
                    infer_cfg=judge_infer_cfg,
                    local_mode=True,
                ),
            ]


# set model configs
if model_configs:
    model_config_list = json_loads(model_configs)
    if model_config_list is not None:
        for model_config in model_config_list:
            print("model_config: ", model_config)
            # MODEL_CONFIG_ID,MODEL_TYPE,PROMPT
            # CUSTOM_MODEL_NAME,BASE_MODEL_PATH,LORA_WEIGHT_PATH
            # BUILD_IN_MODEL_NAME
            # API_TYPE,API_URL,API_KEY,API_EXTRA_CONFIG
            model_config_id = model_config.get("MODEL_CONFIG_ID")
            model_type = model_config.get("MODEL_TYPE")
            if model_config.get("TEMPERATURE"):
                temperature = float(model_config.get("TEMPERATURE"))
            else:
                temperature = 0.0
            if model_config.get("TOP_P"):
                top_p = float(model_config.get("TOP_P"))
            else:
                top_p = 1.0
            if model_config.get("PRESENCE_PENALTY"):
                presence_penalty = float(model_config.get("PRESENCE_PENALTY"))
            else:
                presence_penalty = 0.0
            print("---model config---")
            print("model_config_id: ", model_config_id)
            print("model_type: ", model_type)
            print("temperature: ", temperature)
            print("top_p: ", top_p)
            print("presence_penalty: ", presence_penalty)
            print("------------------")
            if model_type == "API":
                api_meta_template = dict(
                    round=[
                        dict(role="HUMAN", api_role="HUMAN"),
                        dict(role="BOT", api_role="BOT", generate=True),
                    ],
                    reserved_roles=[
                        dict(role='SYSTEM', api_role='SYSTEM'),
                    ],
                )
                # OpenAI,Spark, DeepSeek
                api_type = model_config.get("API_TYPE")
                api_url = model_config.get("API_URL")
                if model_config.get("API_KEY"):
                    api_key = model_config.get("API_KEY")
                else:
                    api_key = ""
                api_model = model_config.get("API_MODEL", model_config_id)
                if model_config.get("API_EXTRA_CONFIG"):
                    api_extra_config = model_config.get("API_EXTRA_CONFIG")
                else:
                    api_extra_config = "{}"
                print("---api config---")
                print("api_type:", api_type)
                print("api_url:", api_url)
                print("api_key:", api_key)
                print("api_model:", api_model)
                print("api_extra_config:", api_extra_config)
                print("----------------")
                if api_type == "OpenAI":
                    models += [
                        dict(
                            type=CustomOpenAI,
                            abbr=model_config_id,
                            path=api_model,
                            key=api_key,
                            openai_api_base=[api_url],
                            meta_template=api_meta_template,
                            query_per_second=1,
                            max_out_len=2048,
                            batch_size=2,
                        )
                    ]
                elif api_type == "Spark":
                    api_extra_config_json = json_loads(api_extra_config)
                    domain = api_extra_config_json.get("DOMAIN", "")
                    app_id = api_extra_config_json.get("APP_ID", "")
                    api_key_spark = api_extra_config_json.get("API_KEY", "")
                    api_secret = api_extra_config_json.get("API_SECRET", "")
                    print("---api extra config---")
                    print("domain:", domain)
                    print("appid:", app_id)
                    print("api_key_spark:", api_key_spark)
                    print("api_secret:", api_secret)
                    print("----------------------")
                    models += [
                        dict(
                            type=XunFeiSpark,
                            abbr=model_config_id,
                            url=api_url,
                            path=domain,
                            app_id=app_id,
                            api_secret=api_secret,
                            api_key=api_key_spark,
                            meta_template=api_meta_template,
                            query_per_second=1,
                            max_out_len=2048,
                            batch_size=2,
                        )
                    ]
                else:
                    print("Unsupported api_type")
            elif model_type == "CUSTOM":
                # run model in local
                custom_model_name = model_config.get("CUSTOM_MODEL_NAME")
                base_model_path = model_config.get("BASE_MODEL_PATH")
                lora_weight_path = model_config.get("LORA_WEIGHT_PATH")
                nums_gpus = 1
                models += [
                    dict(
                        type=VLLM,
                        abbr=model_config_id,
                        path=base_model_path,
                        lora_path=lora_weight_path,
                        model_kwargs=dict(tensor_parallel_size=1),
                        batch_size=16,
                        generation_kwargs=dict(
                            temperature=temperature,
                            top_p=top_p,
                            presence_penalty=presence_penalty,
                        ),
                        run_cfg=dict(num_gpus=nums_gpus),
                    )
                ]
            elif model_type == "BUILT_IN":
                # todo，for future use
                models += []

print("load config done.")
print("datasets: ", datasets)
print("models: ", models)
print("----------------------------------")
