import os
import json


def handle_custom_dataset(dataset_config_id, custom_dataset_path):
    # split dataset_path by comma for next step
    dataset_path_list = custom_dataset_path.split(",")
    os.makedirs("/tmp/merged_dataset", exist_ok=True)
    merged_dataset_path = (
        f"/tmp/merged_dataset/merged_dataset_{dataset_config_id}.jsonl"
    )
    with open(merged_dataset_path, "a") as merged_file:
        for dataset_path in dataset_path_list:
            """check if dataset_path is a directory,
            if yes, loop through all jsonl files in the directory
            """
            if os.path.isdir(dataset_path):
                for file in os.listdir(dataset_path):
                    if file.endswith(".jsonl"):
                        with open(os.path.join(dataset_path, file), "r") as f:
                            # write all content to merged_file
                            merged_file.write(f.read())
            else:
                if dataset_path.endswith(".jsonl"):
                    with open(dataset_path, "r") as f:
                        # write all content to merged_file
                        merged_file.write(f.read())
    return merged_dataset_path


"""
对比模式合并数据集
{
    "input": "1 + 1 = ?",
    "target": "2",
    "prediction": "2"
}
合并后：
{
    "input": "1 + 1 = ?",
    "target": "2",
    "predictions": {
      "model_A": "3",
      "model_B": "2"
    }
}
"""
def handle_judge_dataset(custom_dataset_path):
    # 
    custom_dataset_path_list = custom_dataset_path.split(",")
    result = []
    # 读取文件内容，将 prediction 参数合并到相同input的json对象中
    if custom_dataset_path_list:
        for dataset_path in custom_dataset_path_list:
            if dataset_path.endswith(".jsonl"):
                    with open(dataset_path, "r") as f:
                        for line in f:
                            data = json.loads(line.strip())
                            data["predictions"] = 
                            result.append(data)
    


dataset_configs = os.getenv("DATASET_CONFIGS")
operation_type = os.getenv("OPERATION_TYPE")
judge_mode = os.getenv("JUDGE_MODE")

if dataset_configs:
    dataset_configs_list = json.loads(dataset_configs)
    if judge_mode == "MULTIPLE":
        # 处理对比模式
        for dataset_config in dataset_configs_list:
            custom_dataset_path = dataset_config.get("CUSTOM_DATASET_PATH")
            handled_judge_dataset_path = handle_judge_dataset(custom_dataset_path)
            dataset_config["CUSTOM_DATASET_PATH"] = handled_judge_dataset_path
    else:
        for dataset_config in dataset_configs_list:
            if dataset_config.get("DATASET_TYPE") == "CUSTOM":
                dataset_config_id = dataset_config.get("DATASET_CONFIG_ID")
                custom_dataset_path = dataset_config.get("CUSTOM_DATASET_PATH")
                merged_path = handle_custom_dataset(
                    dataset_config_id, custom_dataset_path
                )
                dataset_config["CUSTOM_DATASET_PATH"] = merged_path
    print(json.dumps(dataset_configs_list, ensure_ascii=False))
    
