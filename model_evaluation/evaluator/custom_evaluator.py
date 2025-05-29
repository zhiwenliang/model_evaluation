import os
import random
from typing import List

import evaluate
import numpy as np
from datasets import Dataset

from opencompass.registry import ICL_EVALUATORS

from opencompass.openicl.icl_evaluator.icl_base_evaluator import BaseEvaluator


@ICL_EVALUATORS.register_module()
class CustomEvaluator(BaseEvaluator):
    """Use huggingface evaluate module to calculate the target metrics.

    Args:
        metric (str): Metric name in evaluate module.
        seed (int): There exists some randomness during the calculation of some
            metrics, thus we set a fixed random seed for reproducing. Defaults
            to 0.
    """

    def __init__(self, metrics: List, seed: int = 0) -> None:
        self.metrics = metrics
        self.seed = seed
        super().__init__()

    def _preprocess(self, predictions: List, references: List) -> dict:
        """Preprocess the final predictions and references to needed format.

        Args:
            predictions (List): List of predictions of each sample.
            references (List): List of targets for each sample.

        Returns:
            dict: preprocessed results.
        """
        return {
            'predictions': predictions,
            'references': references,
        }

    def _postprocess(self, scores: dict) -> dict:
        """Postprocess for final scores.

        Args:
            scores (dict): Dict of calculated scores of metrics.

        Returns:
            dict: postprocessed scores.
        """
        return scores

    def score(self, predictions: List, references: List) -> dict:
        """Calculate scores.

        Args:
            predictions (List): List of predictions of each sample.
            references (List): List of targets for each sample.

        Returns:
            dict: calculated scores.
        """
        random_state = random.getstate()
        np_random_state = np.random.get_state()

        random.seed(self.seed)
        np.random.seed(self.seed)
        if len(predictions) != len(references):
            return {
                'error':
                'predictions and references have different '
                f'length. len(predictions): {len(predictions)}, '
                f'len(references): {len(references)}'
            }
        # use codes pre-downloaded to opencompass repo, avoid downloading
        result = dict()
        for metric_name in self.metrics:
            if metric_name == "rouge1":
                metric_code = "rouge"
                rouge_types = ["rouge1"]
            elif metric_name == "rouge2":
                metric_code = "rouge"
                rouge_types = ["rouge2"]
            elif metric_name == "rougeL":
                metric_code = "rouge"
                rouge_types = ["rougeL"]
            elif metric_name == "BLEU-4":
                metric_code = "sacrebleu"
            
            local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'hf_metrics', metric_code + '.py')
            if os.path.exists(local_path):
                metric = evaluate.load(local_path)
            else:
                print("metric is not supported, please check your metric name")
            
            if metric_code == "rouge":
                scores = metric.compute(**self._preprocess(predictions, references), rouge_types=rouge_types)
                result.update(self._postprocess(scores))
            else:
                scores = metric.compute(**self._preprocess(predictions, references))
                result[metric_name] = self._postprocess(scores)
            random.setstate(random_state)
            np.random.set_state(np_random_state)
        return result