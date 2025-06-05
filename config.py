from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.datasets.custom import CustomDataset
from opencompass.models import VLLM
from opencompass.models import DeepseekAPI
from os import getenv
from json import loads as json_loads

from model_evaluation.model.custom_openai import CustomOpenAI
from model_evaluation.evaluator.custom_evaluator import CustomEvaluator


print("----------------------------------")
print("Loading config...")
# custom reader config, if operation type is EVALUATION, set output column to "target"
operation_type = getenv("OPERATION_TYPE")
dataset_configs = getenv("DATASET_CONFIGS")
model_configs = getenv("MODEL_CONFIGS")
merged_dataset_paths = getenv("MERGED_DATASET_PATH_DICT")
print("operation_type: ", operation_type)
print("dataset_configs: ", dataset_configs)
print("model_configs: ", model_configs)

output_column = "target" if operation_type == "EVALUATION" else ""
custom_reader_cfg = dict(input_columns=["input"], output_column=output_column)

custom_infer_cfg = dict(
    prompt_template=dict(
        type=PromptTemplate,
        template="{input}",
    ),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(type=GenInferencer),
)

api_meta_template = dict(
    round=[
        dict(role="HUMAN", api_role="HUMAN"),
        dict(role="BOT", api_role="BOT", generate=True),
    ],
)

# datasets config
datasets = []
# models config
models = []

# 数据集配置列表，json数组
if dataset_configs:
    dataset_config_list = json_loads(dataset_configs)
    if dataset_config_list is not None:
        for dataset_config in dataset_config_list:
            # DATASET_CONFIG_ID, DATASET_TYPE(BUILT_IN, CUSTOM), EVALUATION_METRICS(ROUGE-1, ROUGE-2, ROUGE-L, BLEU-4),
            # BUILT_IN_DATASET
            # CUSTOM_DATASET_PATH
            # Assemble dataset config for opencompass
            dataset_config_id = dataset_config.get("DATASET_CONFIG_ID")
            dataset_type = dataset_config.get("DATASET_TYPE")
            evaluation_metrics = dataset_config.get("EVALUATION_METRICS")
            evaluation_metric_list = evaluation_metrics.split(",")
            if dataset_type == "BUILT_IN":
                build_in_dataset = dataset_config.get("BUILT_IN_DATASET")
                # todo
            elif dataset_type == "CUSTOM":
                merged_dataset_path_dict = {}
                if merged_dataset_paths:
                    merged_dataset_path_dict = json_loads(merged_dataset_paths)
                merged_dataset_path = merged_dataset_path_dict.get(dataset_config_id)
                # set metrics for evaluator
                custom_eval_cfg = dict(
                    evaluator=dict(type=CustomEvaluator, metrics=evaluation_metric_list),
                )
                print("dataset_config_id: ", dataset_config_id)
                print("merged_dataset_path: ", merged_dataset_path)
                datasets += [
                    dict(
                        abbr=dataset_config_id,
                        type=CustomDataset,
                        path=merged_dataset_path,
                        reader_cfg=custom_reader_cfg,
                        infer_cfg=custom_infer_cfg,
                        eval_cfg=custom_eval_cfg,
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
            prompt = model_config.get("PROMPT")
            temperature = (
                model_config.get("TEMPERATURE")
                if model_config.get("TEMPERATURE")
                else 0
            )
            top_k = model_config.get("TOP_K", 0)
            presence_penalty = (
                model_config.get("PRESENCE_PENALTY", -1)
            )
            if model_type == "API":
                # OpenAI,Spark, DeepSeek
                api_type = model_config.get("API_TYPE")
                api_url = model_config.get("API_URL")
                api_key = model_config.get("API_KEY")
                api_model = model_config.get("API_MODEL", model_config_id)
                api_extra_config = model_config.get("API_EXTRA_CONFIG")
                print("api_type:", api_type)
                print("api_url:", api_url)
                print("api_key:", api_key)
                print("api_model:", api_model)
                print("api_extra_config:", api_extra_config)
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
                            batch_size=8,
                        )
                    ]
                elif api_type == "Spark":
                    # todo
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
                            batch_size=8,
                        )
                    ]
                elif api_type == "DeepSeek":
                    # todo
                    models += [
                        dict(
                            type=DeepseekAPI,
                            abbr=model_config_id,
                            path=api_model,
                            key=api_key,
                            url=api_url,
                            meta_template=api_meta_template,
                            query_per_second=1,
                            max_out_len=2048,
                            batch_size=8,
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
                            top_k=top_k,
                            presence_penalty=presence_penalty,
                        ),
                        run_cfg=dict(num_gpus=nums_gpus),
                    )
                ]
            elif model_type == "BUILT_IN":
                # todo
                models += []

print("datasets: ", datasets)
print("models: ", models)
print("----------------------------------")