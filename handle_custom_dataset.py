import os
import json


def handle_custom_dataset(dataset_config_id, custom_dataset_path):
    # split dataset_path by comma for next step
    dataset_path_list = custom_dataset_path.split(",")
    os.makedirs("/tmp/merged_dataset", exist_ok=True)
    merged_dataset_path = f"/tmp/merged_dataset/merged_dataset_{dataset_config_id}.jsonl"
    with open(merged_dataset_path, "a") as merged_file:
        for dataset_path in dataset_path_list:
            # check if dataset_path is a directory, if yes, loop through all jsonl files in the directory
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


dataset_configs = os.getenv("DATASET_CONFIGS")
result = dict()
if dataset_configs:
    dataset_configs_list = json.loads(dataset_configs)
    for dataset_config in dataset_configs_list:
        if dataset_config.get("DATASET_TYPE") == "CUSTOM":
            dataset_config_id = dataset_config.get("DATASET_CONFIG_ID")
            custom_dataset_path = dataset_config.get("CUSTOM_DATASET_PATH")
            result[dataset_config_id] = handle_custom_dataset(dataset_config_id, custom_dataset_path)
                

print(json.dumps(result))