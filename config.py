from opencompass.openicl.icl_evaluator import HuggingfaceEvaluator
from model_evaluation.evaluator.custom_evaluator import CustomEvaluator
from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.datasets.custom import CustomDataset
from opencompass.models import VLLM
from os import getenv

from model_evaluation.util.common_util import parse_json, handle_custom_dataset
from model_evaluation.model.custom_openai import CustomOpenAI


custom_reader_cfg = dict(input_columns=["input"], output_column="target")

custom_infer_cfg = dict(
    prompt_template=dict(
        type=PromptTemplate,
        template=dict(
            round=[
                dict(
                    role="HUMAN",
                    prompt="{input}\nPlease reason step by step, and put your final answer within \\boxed{}.",
                ),
            ],
        ),
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
dataset_configs = getenv("DATASET_CONFIGS", "")
if dataset_configs != "":
    dataset_config_list = parse_json(dataset_configs)
    if dataset_config_list is not None:
        for dataset_config in dataset_config_list:
            # DATASET_CONFIG_ID, DATASET_TYPE(BUILT_IN, CUSTOM), EVALUATION_METRICS(ROUGE-1, ROUGE-2, ROUGE-L, BLEU-4),
            # BUILT_IN_DATASET
            # CUSTOM_DATASET_PATH
            # Assemble dataset config for opencompass
            dataset_config_id = dataset_config["DATASET_CONFIG_ID"]
            dataset_type = dataset_config["DATASET_TYPE"]
            evaluation_metrics = dataset_config["EVALUATION_METRICS"]
            evaluation_metric_list = evaluation_metrics.split(",")
            if dataset_type == "BUILT_IN":
                build_in_dataset = dataset_config["BUILT_IN_DATASET"]
                # todo
            elif dataset_type == "CUSTOM":
                custom_dataset_path = dataset_config["CUSTOM_DATASET_PATH"]
                merged_dataset_path = handle_custom_dataset(
                    custom_dataset_path, dataset_config_id
                )
                # set metrics for evaluator
                custom_eval_cfg = dict(
                    evaluator=dict(type=CustomDataset, metrics=evaluation_metric_list),
                )
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
model_configs = getenv("MODEL_CONFIGS", "")
if model_configs != "":
    model_config_list = parse_json(model_configs)
    if model_config_list is not None:
        for model_config in model_config_list:
            # MODEL_CONFIG_ID,MODEL_TYPE,PROMPT
            # CUSTOM_MODEL_NAME,BASE_MODEL_PATH,LORA_WEIGHT_PATH
            # BUILD_IN_MODEL_NAME
            # API_TYPE,API_URL,API_KEY,API_EXTRA_CONFIG
            model_config_id = model_config["MODEL_CONFIG_ID"]
            model_type = model_config["MODEL_TYPE"]
            prompt = model_config["PROMPT"]
            temperature = (
                model_config["TEMPERATURE"]
                if model_config["TEMPERATURE"]
                else 0
            )
            top_k = model_config["TOP_K"] if model_config["TOP_K"] else 0
            presence_penalty = (
                model_config["PRESENCE_PENALTY"]
                if model_config["PRESENCE_PENALTY"]
                else -1
            )
            if model_type == "API":
                # OpenAI,Spark, DeepSeek
                api_type = model_config["API_TYPE"]
                api_url = model_config["API_URL"]
                api_key = model_config["API_KEY"]
                api_model = (
                    model_config["API_MODEL"] if model_config else model_config_id
                )
                api_extra_config = model_config["API_EXTRA_CONFIG"]
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
                            max_seq_len=4096,
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
                            max_seq_len=4096,
                        )
                    ]
                elif api_type == "DeepSeek":
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
                        )
                    ]
                else:
                    print("Unsupported api_type")
            elif model_type == "CUSTOM":
                custom_model_name = model_config["CUSTOM_MODEL_NAME"]
                base_model_path = model_config["BASE_MODEL_PATH"]
                lora_weight_path = model_config["LORA_WEIGHT_PATH"]
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
