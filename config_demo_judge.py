from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.datasets.custom import CustomDataset
from opencompass.models import VLLM
from os import getenv

from opencompass.models.custom_openai import CustomOpenAI
from opencompass.openicl.icl_evaluator.custom_evaluator import CustomEvaluator

custom_reader_cfg = dict(input_columns=["input"], output_column="target")

custom_infer_cfg = dict(
    prompt_template=dict(
        type=PromptTemplate,
        template="{input}",
    ),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(type=GenInferencer),
)

custom_eval_cfg = dict(
    evaluator=dict(
        type=CustomEvaluator,
        metrics=["BLEU-4", "rouge1", "rouge2", "rougeL", "rougeLsum"],
    ),
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

custom_datasets = [
    dict(
        abbr="gsm8k_0",
        type=CustomDataset,
        path="/Users/humuh/Downloads/merged_dataset_gsm8k_0.jsonl",
        reader_cfg=custom_reader_cfg,
        infer_cfg=custom_infer_cfg,
        eval_cfg=custom_eval_cfg,
        local_mode=True,
    ),
    # dict(
    #     abbr='gsm8k_1',
    #     type=CustomDataset,
    #     path='/Users/humuh/source/my/model_evaluation/datasets/gsm8k_1.jsonl',
    #     reader_cfg=custom_reader_cfg,
    #     infer_cfg=custom_infer_cfg,
    #     eval_cfg=custom_eval_cfg,
    #     local_mode=True,
    # ),
]

base_model_path = "/iflytek/base_model"
lora_weight_path = ""
temperature = 0
top_k = 0
presence_penalty = 0
num_gpus = 1
datasets += custom_datasets
models += [
    dict(
        type=CustomOpenAI,
        abbr="qwen-turbo-latest",
        path="qwen-turbo-latest",
        key="sk-8c019c61a5524a4fa6222ff0e9de9130",
        openai_api_base=[
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        ],
        meta_template=api_meta_template,
        query_per_second=1,
        max_out_len=2048,
        batch_size=8,
    ),
    # dict(
    #     type=VLLM,
    #     abbr="qwen2.5-7b-instruct-vllm",
    #     path=base_model_path,
    #     lora_path=lora_weight_path,
    #     model_kwargs=dict(tensor_parallel_size=1),
    #     batch_size=16,
    #     generation_kwargs=dict(
    #         temperature=temperature, top_k=top_k, presence_penalty=presence_penalty
    #     ),
    #     run_cfg=dict(num_gpus=1),
    # ),
]
