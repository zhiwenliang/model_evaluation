#!/bin/bash
echo "OPERATION_TYPE: ${OPERATION_TYPE}"
echo "INFERENCE_RESULT: ${INFERENCE_RESULT}"
echo "EVALUATION_RESULT:  ${EVALUATION_RESULT}"

# 处理
case ${OPERATION_TYPE} in
    "BATCH_INFERENCE")
        echo "BATCH_INFERENCE"
        python run.py config.py -m infer -w /tmp/outputs
        ;;
    "EVALUATION")
        echo "EVALUATION"
        python run.py config.py -m all -w /tmp/outputs
        ;;
    "JUDGE")
        echo "JUDGE"
        python run.py config.py -m infer -w /tmp/outputs
        ;;
    *)
        echo "OPERATION_TYPE: ${OPERATION_TYPE} is not supported"
        exit 1
        ;;
esac


# todo 拷贝推理结果到指定目录

# todo copy评估结果到指定目录