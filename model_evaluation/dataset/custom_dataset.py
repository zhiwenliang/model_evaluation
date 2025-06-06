import csv
import json
import os

from datasets import Dataset

from opencompass.registry import LOAD_DATASET
from opencompass.utils import get_data_path
from opencompass.datasets.base import BaseDataset

@LOAD_DATASET.register_module()
class CustomDataset(BaseDataset):

    @staticmethod
    def load(path, file_name=None, local_mode=False):
        path = get_data_path(path, local_mode=local_mode)
        if file_name is not None:
            path = os.path.join(path, file_name)
        if path.endswith('.jsonl'):
            with open(path, 'r', encoding='utf-8-sig') as f:
                data = [json.loads(line) for line in f]
        elif path.endswith('.csv'):
            with open(path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                header = next(reader)
                data = [dict(zip(header, row)) for row in reader]
        else:
            raise ValueError(f'Unsupported file format: {path}')

        return Dataset.from_list(data)