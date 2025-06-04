#!/bin/bash

set -x
echo "OPERATION_TYPE: ${OPERATION_TYPE}"
echo "INFERENCE_RESULT: ${INFERENCE_RESULT}"
echo "EVALUATION_RESULT:  ${EVALUATION_RESULT}"
echo "MODEL_CONFIGS:  ${MODEL_CONFIGS}"
echo "DATASET_CONFIGS:  ${DATASET_CONFIGS}"

export TMP_OUTPUT="/tmp/output1"
echo "tmp_output: ${TMP_OUTPUT}"


# handle custom dataset
handle_custom_dataset_result=$(python handle_custom_dataset.py)
export MERGED_DATASET_PATH_DICT=$handle_custom_dataset_result
echo "MERGED_DATASET_PATH_DICT: ${MERGED_DATASET_PATH_DICT}"

# run operation
case ${OPERATION_TYPE} in
    "INFERENCE")
        echo "OPERATION_TYPE is: BATCH_INFERENCE"
        python run.py config.py -m infer -w $TMP_OUTPUT --debug
        ;;
    "EVALUATION")
        echo "OPERATION_TYPE is: EVALUATION"
        python run.py config.py -w $TMP_OUTPUT --debug
        ;;
    "JUDGE")
        echo "OPERATION_TYPE is: JUDGE"
        python run.py config.py -m infer -w $TMP_OUTPUT --debug
        ;;
    *)
        echo "OPERATION_TYPE: ${OPERATION_TYPE} is not supported"
        exit 1
        ;;
esac

# get inference result and evaluation result from tmp_output, save to INFERENCE_RESULT and EVALUATION_RESULT
python gen_inference_evaluation_result.py

# run further operation for judge mode