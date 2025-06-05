import os
import json

tmp_output_path = os.getenv("TMP_OUTPUT")
inference_result_path = os.getenv("INFERENCE_RESULT", None)
evaluation_result_path = os.getenv("EVALUATION_RESULT", None)

# 打分模式
'''
{
    "score": 0.8,
    "reason": "The model's response is accurate and relevant to the question asked."
}
'''


# 对比模式
'''
{
    "score_a": 0.8,
    "score_b": 0.9,
    "winner": "A",
    "reason": "The model's response is accurate and relevant to the question asked."
}
'''
