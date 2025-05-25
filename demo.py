import json


def is_evaluation(line_json):
    for key in line_json.keys():
        if key.startswith("eval_"):
            return True
    return False

logging_json_path = 'logging.json'
with open("./train_indi.json", "w") as train_indi_file:
    with open("./eval_indi.json", "w") as eval_indi_file:
        with open(logging_json_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line_json = json.loads(line.strip())
                if is_evaluation(line_json):
                    eval_indi_file.write(json.dumps(line_json) + "\n")
                else:
                    train_indi_file.write(json.dumps(line_json) + "\n")


