import os 
import json

def parse_json(json_str):
    try:
        json_obj = json.loads(json_str)
        return json_obj
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    
# Merge all jsonl files into one jsonl file, return new jsonl file path
def handle_custom_dataset(custom_dataset_path, dataset_config_id):
    print("handle custom_dataset_path")
    # check custom_dataset_path is not empty
    if not custom_dataset_path:
        raise ValueError("custom_dataset_path is empty")
    
    # split dataset_path by comma for next step
    dataset_path_list = custom_dataset_path.split(",")
    merged_dataset_path = f"/tmp/merged_dataset_{dataset_config_id}.jsonl"
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
    print("handle custom_dataset_path done, result: ", merged_dataset_path)
    return merged_dataset_path
