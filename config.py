from opencompass.models import OpenAI
from mmengine.config import read_base
from opencompass.openicl.icl_evaluator import HuggingfaceEvaluator
from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.datasets.custom import CustomDataset
from os import getenv

# datasets config
datasets = []
# models config
models = []

# DATASET_TYPE：BUILT_IN or CUSTOM
dataset_type = getenv("DATASET_TYPE", "")
# EVALUATION_METRICS: ROUGE-1, ROUGE-2, ROUGE-L, BLEU-4
evaluation_metrics = getenv("EVALUATION_METRICS", "")
evaluation_metric_list = evaluation_metrics.split(",")

if dataset_type == "CUSTOM":
    # CUSTOM_DATASET_PATH: directorys or jsonl files
    custom_dataset_path = getenv("CUSTOM_DATASET_PATH", "")
    custom_dataset_path_list = custom_dataset_path.split(",")
    # preprocessing dataset



custom_reader_cfg = dict(input_columns=['input'], output_column='target')

custom_infer_cfg = dict(
    prompt_template=dict(
        type=PromptTemplate,
        template=dict(
            round=[
                dict(role='HUMAN', prompt='{input}\nPlease reason step by step, and put your final answer within \\boxed{}.'),
            ],
        ),
    ),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(type=GenInferencer),
)

custom_eval_cfg = dict(
    evaluator=dict(type=HuggingfaceEvaluator, metric="rouge"),
)

custom_datasets = [
    dict(
        abbr='gsm8k_0',
        type=CustomDataset,
        path='/Users/humuh/source/my/model_evaluation/datasets/gsm8k_0.jsonl',
        reader_cfg=custom_reader_cfg,
        infer_cfg=custom_infer_cfg,
        eval_cfg=custom_eval_cfg,
        local_mode=True,
    ),
    dict(
        abbr='gsm8k_1',
        type=CustomDataset,
        path='/Users/humuh/source/my/model_evaluation/datasets/gsm8k_1.jsonl',
        reader_cfg=custom_reader_cfg,
        infer_cfg=custom_infer_cfg,
        eval_cfg=custom_eval_cfg,
        local_mode=True,
    ),
]


api_meta_template = dict(round=[
    dict(role='HUMAN', api_role='HUMAN'),
    dict(role='BOT', api_role='BOT', generate=True),
], )


datasets += custom_datasets
models += [
    dict(
        type=OpenAI,
        abbr='qwen-plus-2025-01-25',
        path='qwen-plus-2025-01-25',
        key='sk-8c019c61a5524a4fa6222ff0e9de9130',
        openai_api_base=[
            'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',

        ],
        meta_template=api_meta_template,
        query_per_second=1,
        max_out_len=2048,
        max_seq_len=4096,
        batch_size=8,
    ),
    dict(
        type=OpenAI,
        abbr='qwen-plus-2025-04-28',
        path='qwen-plus-2025-04-28',
        key='sk-8c019c61a5524a4fa6222ff0e9de9130',
        openai_api_base=[
            'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',

        ],
        meta_template=api_meta_template,
        query_per_second=1,
        max_out_len=2048,
        max_seq_len=4096,
        batch_size=8,
    ),
]