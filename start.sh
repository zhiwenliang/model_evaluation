#!/bin/bash

# set -e
# source ~/.bashrc
# source /usr/local/Ascend/ascend-toolkit/set_env.sh
# source /usr/local/Ascend/nnal/atb/set_env.sh
# export PATH=/usr/local/python3.10/bin:${PATH}
# export LD_LIBRARY_PATH=/usr/local/Ascend/driver/lib64/common:/usr/local/Ascend/driver/lib64/driver:${LD_LIBRARY_PATH}
# export LD_LIBRARY_PATH=${ASCEND_TOOLKIT_HOME}/runtime/lib64/stub/linux/aarch64/:${LD_LIBRARY_PATH}
# source ~/.bashrc
# source /usr/local/Ascend/ascend-toolkit/set_env.sh
# source /usr/local/Ascend/nnal/atb/set_env.sh


echo "OPERATION_TYPE: ${OPERATION_TYPE}"
echo "INFERENCE_RESULT: ${INFERENCE_RESULT}"
echo "EVALUATION_RESULT:  ${EVALUATION_RESULT}"
echo "MODEL_CONFIGS:  ${MODEL_CONFIGS}"
echo "DATASET_CONFIGS:  ${DATASET_CONFIGS}"

export TMP_OUTPUT="/tmp/output"
echo "tmp_output: ${TMP_OUTPUT}"


# handle custom dataset for evaluation or inference
handle_custom_dataset_result=$(python handle_custom_dataset.py)
export MERGED_DATASET_PATH_DICT=$handle_custom_dataset_result
echo "MERGED_DATASET_PATH_DICT: ${MERGED_DATASET_PATH_DICT}"

# 生成裁判模式新的数据集文件
export JUDGE_DATASET_PATH=/tmp/judge_dataset.jsonl
python gen_judge_dataset.py

# run operation
case ${OPERATION_TYPE} in
    "INFERENCE")
        echo "OPERATION_TYPE is: INFERENCE"
        python run.py config.py -m infer -w $TMP_OUTPUT --dump-eval-details False --debug
        ;;
    "EVALUATION")
        echo "OPERATION_TYPE is: EVALUATION"
        python run.py config.py -w $TMP_OUTPUT  --dump-eval-details False --debug
        ;;
    "JUDGE")
        echo "OPERATION_TYPE is: JUDGE"
        python run.py config.py -m infer -w $TMP_OUTPUT --dump-eval-details False --debug
        ;;
    *)
        echo "OPERATION_TYPE: ${OPERATION_TYPE} is not supported"
        exit 1
        ;;
esac

# get inference result and evaluation result from tmp_output, save to INFERENCE_RESULT and EVALUATION_RESULT
python gen_inference_evaluation_result.py

# run further operation for judge mode
if [ "${OPERATION_TYPE}" = "JUDGE" ]; then
    echo "OPERATION_TYPE is: JUDGE, run further operation"
    python handle_judge_result.py
fi