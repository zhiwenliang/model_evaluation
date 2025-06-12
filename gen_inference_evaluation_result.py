# flake8: noqa: E501
import os
import json
import shutil

tmp_output_path = os.getenv("TMP_OUTPUT")
print("tmp_output_path:", tmp_output_path)
inference_result_path = os.getenv("INFERENCE_RESULT", None)
evaluation_result_path = os.getenv("EVALUATION_RESULT", None)
model_configs = os.getenv("MODEL_CONFIGS")
dataset_configs = os.getenv("DATASET_CONFIGS")
operation_type = os.getenv("OPERATION_TYPE")

model_config_ids = []
dataset_config_ids = []
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
    dataset_config_ids = [
        dataset_config['DATASET_CONFIG_ID']
        for dataset_config in dataset_config_list
    ]

subdirs = sorted([d for d in os.listdir(tmp_output_path)])
subdir = ""
if len(subdirs) > 0:
    subdir = subdirs[-1]
else:
    print("Multiple subdirectories found in TMP_OUTPUT, subdirs:", subdirs)
    exit(1)


for model_config_id in model_config_ids:
    for dataset_config_id in dataset_config_ids:
        tmp_prediction_result_path = os.path.join(str(tmp_output_path), subdir, "predictions", str(model_config_id), f"{dataset_config_id}.json")
        tmp_evaluation_result_path = os.path.join(str(tmp_output_path), subdir, "results", str(model_config_id), f"{dataset_config_id}.json")
        # inference result
        if operation_type in ["INFERENCE", "EVALUATION"]:
            if os.path.exists(tmp_prediction_result_path):
                with open(tmp_prediction_result_path, 'r') as f:
                    tmp_result = json.load(f)
                    inference_result = []
                    for index, item in tmp_result.items():
                        inference_result.append({
                            "input": item.get("origin_prompt", ""),
                            "target": item.get("gold", ""),
                            "prediction": item.get("prediction", "")
                        })
                    # save inference result
                    if inference_result_path is not None and not os.path.exists(inference_result_path):
                        os.makedirs(inference_result_path, exist_ok=True)
                    inference_result_file = os.path.join(str(inference_result_path), f"inference_{model_config_id}_{dataset_config_id}.jsonl")
                    with open(inference_result_file, 'w') as out_f:
                        for each_inference in inference_result:
                            out_f.write(json.dumps(each_inference, ensure_ascii=False) + '\n')
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
        # JUDGE result
        # if operation_type == "JUDGE":
            