import os
import torch
import json
from torch.utils.data import Dataset, DataLoader

class QuestionsDataset(Dataset):
    """SCI-test questions dataset."""

    def __init__(self, file_path, args, transform=None):
        """
        Arguments:
            file_path (string): Path to the json file with questions.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        with open(file_path,'r',encoding='utf-8') as f:
            set = json.loads(f.read())
        self.dataset = []
        category = args.category
        ability = args.ability
        type = args.type
        for item in set:
            if (category == "all" or item["category"] == category) and\
                (ability == "all" or item["ability"] == ability) and \
                    (type == "all" or item["type"] == type):
                self.dataset.append(item)
        self.transform = transform

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
 
        sample = {}
        if self.dataset[idx]['type'] == "multiple-choice": 
            sample['prompt'] = "Given a question and four choices, choose the correct answer. Your answer should be A, B, C or D."
        if self.dataset[idx]['type'] == "filling": 
            sample['prompt'] = self.dataset[idx]['cot_prompt']
        if self.dataset[idx]['type'] == "judge": 
            sample['prompt'] = "Given a context and a question, answer the question based on context. Your answer should be yes, no or maybe."
        sample['prompt'] += self.dataset[idx]['question']
    
        sample['id'] = self.dataset[idx]['id']

        if self.transform:
            sample = self.transform(sample)
            
        return sample