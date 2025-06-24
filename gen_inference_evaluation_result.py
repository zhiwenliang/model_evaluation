# flake8: noqa: E501
import os
import json
import shutil
import re
import logging

agieval_datasets = ['agieval-gaokao-english', 'agieval-lsat-lr', 'agieval-gaokao-biology', 'agieval-gaokao-mathcloze', 'agieval-gaokao-physics', 'agieval-aqua-rat', 'agieval-sat-math', 'agieval-lsat-rc', 'agieval-sat-en', 'agieval-jec-qa-kd', 'agieval-gaokao-mathqa', 'agieval-gaokao-history', 'agieval-math', 'agieval-jec-qa-ca', 'agieval-gaokao-geography', 'agieval-gaokao-chemistry', 'agieval-lsat-ar', 'agieval-sat-en-without-passage', 'agieval-logiqa-en', 'agieval-gaokao-chinese', 'agieval-logiqa-zh']
gaokao_bench_datasets = ['2010-2022_Math_I_MCQs', '2010-2022_Chinese_Language_Literary_Text_Reading', '2010-2022_Chinese_Modern_Lit', '2014-2022_English_Language_Cloze_Passage', '2010-2022_Chinese_Language_Ancient_Poetry_Reading', '2010-2022_Chemistry_MCQs', '2010-2022_Math_II_MCQs', '2010-2022_Chemistry_Open-ended_Questions', '2010-2013_English_MCQs', '2010-2022_History_MCQs', '2010-2022_Chinese_Language_Classical_Chinese_Reading', '2010-2022_Political_Science_MCQs', '2010-2022_Math_I_Fill-in-the-Blank', '2010-2022_Math_II_Open-ended_Questions', '2010-2022_Political_Science_Open-ended_Questions', '2010-2022_Math_II_Fill-in-the-Blank', '2010-2022_Geography_Open-ended_Questions', '2010-2022_Math_I_Open-ended_Questions', '2010-2022_Biology_Open-ended_Questions', '2010-2022_Physics_MCQs', '2010-2022_Chinese_Language_Language_and_Writing_Skills_Open-ended_Questions', '2010-2022_Geography_MCQs', '2010-2022_Biology_MCQs', '2010-2022_English_Reading_Comp', '2010-2022_Physics_Open-ended_Questions', '2010-2022_History_Open-ended_Questions', '2010-2022_Chinese_Lang_and_Usage_MCQs', '2010-2022_Chinese_Language_Practical_Text_Reading', '2010-2022_Chinese_Language_Famous_Passages_and_Sentences_Dictation', '2010-2022_English_Fill_in_Blanks', '2012-2022_English_Cloze_Test', '2012-2022_English_Language_Error_Correction']
boolq_datasets = ['BoolQ']
winogrande_datasets = ['winogrande']
drop_datasets = ['drop']
gpqa_datasets = ['GPQA_diamond']
teval_datasets = ['teval-plan_json_v1', 'teval-instruct_v1', 'teval-reason_retrieve_understand_json_v1', 'teval-review_str_v1', 'teval-retrieve_str_v1', 'teval-plan_str_v1', 'teval-reason_str_v1', 'teval-understand_str_v1']
race_datasets = ['race-middle', 'race-high']
humaneval_datasets = ['openai_humaneval']
ifeval_datasets = ['IFEval']


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

tmp_output_path = os.getenv("TMP_OUTPUT")
logger.info("tmp_output_path: %s", tmp_output_path)
inference_result_path = os.getenv("INFERENCE_RESULT", None)
evaluation_result_path = os.getenv("EVALUATION_RESULT", None)
model_configs = os.getenv("MODEL_CONFIGS")
dataset_configs = os.getenv("DATASET_CONFIGS")
operation_type = os.getenv("OPERATION_TYPE")
inference_mode = os.getenv("INFERENCE_MODE")

model_config_ids = []
dataset_config_ids = []
built_in_datasets = []
# get model_config_id list from model_configs
if model_configs:
    model_config_list = json.loads(model_configs)
    model_config_ids = [
        model_config['MODEL_CONFIG_ID']
        for model_config in model_config_list
    ]
# get dataset_config_id list from dataset_configs
if dataset_configs:
    dataset_config_list = json.loads(dataset_configs)
    for dataset_config in dataset_config_list:
        if dataset_config.get("DATASET_TYPE") == "BUILT_IN":
            built_in_datasets.append(dataset_config)
        else:
            dataset_config_ids.append(dataset_config.get("DATASET_CONFIG_ID"))

subdirs = sorted([d for d in os.listdir(tmp_output_path)])
subdir = ""
if len(subdirs) > 0:
    subdir = subdirs[-1]
else:
    logger.error("Multiple subdirectories found in TMP_OUTPUT, subdirs: %s", subdirs)
    exit(1)


for model_config_id in model_config_ids:
    # 处理内置数据集，不保存推理结果
    for built_in_dataset in built_in_datasets:
        built_in_dataset_id = built_in_dataset.get("DATASET_CONFIG_ID")
        built_in_dataset_name = built_in_dataset.get("BUILT_IN_DATASET")
        evaluation_result = dict()
        tmp_evaluation_result_path = os.path.join(str(tmp_output_path), subdir, "results", str(model_config_id))
        if os.path.exists(tmp_evaluation_result_path):
            # loop all json file in tmp_evaluation_result_path
            for file in os.listdir(tmp_evaluation_result_path):
                if file.endswith(".json"):
                    file_name = file.split(".")[0]
                    # Create a mapping of dataset names to their corresponding dataset lists
                    dataset_mapping = {
                        "AGIEval": agieval_datasets,
                        "GaokaoBench": gaokao_bench_datasets,
                        "BoolQ": boolq_datasets,
                        "WinoGrande": winogrande_datasets,
                        "DROP": drop_datasets,
                        "GPQA": gpqa_datasets,
                        "T-Eval": teval_datasets,
                        "RACE": race_datasets,
                        "HumanEval": humaneval_datasets,
                        "IFEval": ifeval_datasets
                    }
                    
                    # Check if the built-in dataset name exists in mapping and file_name is in corresponding dataset list
                    if built_in_dataset_name in dataset_mapping and file_name in dataset_mapping[built_in_dataset_name]:
                        with open(os.path.join(tmp_evaluation_result_path, file), 'r') as f:
                            tmp_result = json.load(f)
                            evaluation_result[file_name] = tmp_result
        else:
            logger.error("Evaluation result is not exist for %s", built_in_dataset_name)        
        # save evaluation result
        if evaluation_result_path is not None and not os.path.exists(evaluation_result_path):
            os.makedirs(evaluation_result_path, exist_ok=True)
        evaluation_result_file = os.path.join(str(evaluation_result_path), f"evaluation_{model_config_id}_{built_in_dataset_id}.json")
        with open(evaluation_result_file, 'w') as out_f:
            json.dump(evaluation_result, out_f, ensure_ascii=False)
    # 处理自定义数据集
    for dataset_config_id in dataset_config_ids:
        tmp_prediction_result_path = os.path.join(str(tmp_output_path), subdir, "predictions", str(model_config_id), f"{dataset_config_id}.json")
        tmp_evaluation_result_path = os.path.join(str(tmp_output_path), subdir, "results", str(model_config_id), f"{dataset_config_id}.json")
        # inference result
        if operation_type in ["INFERENCE", "EVALUATION"]:
            if os.path.exists(tmp_prediction_result_path):
                with open(tmp_prediction_result_path, 'r') as f:
                    tmp_result = json.load(f)
                    inference_result = []
                    if inference_mode == "OVERWRITE":
                        for index, item in tmp_result.items():
                            inference_result.append({
                                "input": item.get("origin_prompt", ""),
                                "target": item.get("prediction", "")
                            })
                    else:
                        for index, item in tmp_result.items():
                            inference_result.append({
                                "input": item.get("origin_prompt", ""),
                                "target": item.get("gold", "") ,
                                "prediction": item.get("prediction", "")
                            })
                    # save inference result
                    if inference_result_path is not None and not os.path.exists(inference_result_path):
                        os.makedirs(inference_result_path, exist_ok=True)
                    inference_result_file = os.path.join(str(inference_result_path), f"inference_{model_config_id}_{dataset_config_id}.jsonl")
                    print(inference_result)
                    with open(inference_result_file, 'w') as out_f:
                        for each_inference in inference_result:
                            out_f.write(json.dumps(each_inference, ensure_ascii=False) + '\n')
            else:
                logger.error("Inference result is not exist")
        # evaluation result
        if operation_type == "EVALUATION":
            if os.path.exists(tmp_evaluation_result_path):
                if evaluation_result_path is not None and not os.path.exists(evaluation_result_path):
                    os.makedirs(evaluation_result_path, exist_ok=True)
                evaluation_result = os.path.join(
                    str(evaluation_result_path),
                    f"evaluation_{model_config_id}_{dataset_config_id}.json"
                )
                shutil.copy(tmp_evaluation_result_path, evaluation_result)
            else:
                logger.error("Evaluation result is not exist")
        # JUDGE result
        if operation_type == "JUDGE":
            if os.path.exists(tmp_prediction_result_path):
                with open(tmp_prediction_result_path, 'r') as f:
                    tmp_result = json.load(f)
                    evaluation_result = []
                    for index, item in tmp_result.items():
                            logger.info(item)
                            origin_prompt = item.get("origin_prompt", "")
                            # 利用正则解析原问题
                            last_human_prompt=origin_prompt[-1].get("prompt", "")
                            pattern = r"用户指令：(.*?)\n"
                            match = re.search(pattern, last_human_prompt)
                            if match:
                                input = match.group(1)
                            else:
                                input = last_human_prompt
                            evaluation_result.append({
                                "input": input,
                                "score": item.get("prediction", "")
                            })
                    logger.debug("evaluate result is: %s", evaluation_result)
                    # save inference result
                    if evaluation_result_path is not None and not os.path.exists(evaluation_result_path):
                        os.makedirs(evaluation_result_path, exist_ok=True)
                    evaluation_result_file = os.path.join(str(evaluation_result_path), f"evaluation_{model_config_id}_{dataset_config_id}.json")
                    with open(evaluation_result_file, 'w') as out_f:
                        out_f.write(json.dumps(evaluation_result, ensure_ascii=False))
            else:
                logger.error("Judge result is not exist")