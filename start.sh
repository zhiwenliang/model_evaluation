#!/bin/bash
echo "OPERATION_TYPE: ${OPERATION_TYPE}"
echo "INFERENCE_RESULT: ${INFERENCE_RESULT}"
echo "EVALUATION_RESULT:  ${EVALUATION_RESULT}"

# 处理
case ${OPERATION_TYPE} in
    "INFERENCE")
        echo "BATCH_INFERENCE"
        python run.py config.py -m infer -w /tmp/outputs --debug
        ;;
    "EVALUATION")
        echo "EVALUATION"
        python run.py config.py -m all -w /tmp/outputs --debug
        ;;
    "JUDGE")
        echo "JUDGE"
        python run.py config.py -m infer -w /tmp/outputs --debug
        ;;
    *)
        echo "OPERATION_TYPE: ${OPERATION_TYPE} is not supported"
        exit 1
        ;;
esac


# 处理并copy推理结果到指定目录


# 处理并copy评估结果到指定目录zh