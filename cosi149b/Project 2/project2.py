from IPython.display import HTML, display

def set_css():
  display(HTML('''
  <style>
    pre {
        white-space: pre-wrap;
    }
  </style>
  '''))

get_ipython().events.register('pre_run_cell', set_css)

def clear_cache():
  if torch.cuda.is_available():
    model = None
    torch.cuda.empty_cache()
  

import getpass
import locale; locale.getpreferredencoding = lambda: "UTF-8"
import logging
import os
import torch
import yaml

from ludwig.api import LudwigModel

os.environ["HUGGING_FACE_HUB_TOKEN"] = "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"

import numpy as np
import pandas as pd
import pickle as pkl
df = pd.read_pickle("training.pkl")
df = df.fillna("")
#90/10 partition of data
total_rows = len(df)
split_0_count = int(total_rows * 0.9)
split_1_count = total_rows - split_0_count

split_values = np.concatenate([
    np.zeros(split_0_count),
    np.ones(split_1_count),
])

np.random.shuffle(split_values)

df['split'] = split_values
df['split'] = df['split'].astype(int)

PROMPT = "Based on the following medical notes, please predict whether the patient described is likely to have Acute Respiratory Distress Syndrome (ARDS). Your prediction should be either 'true' if ARDS is likely, or 'false' if it is not likely."
df['instruction'] = PROMPT
df = df.rename(columns={'text':'notes', 'label':'output'})
df = df.astype({'output':'str'})

TOKEN_LIMIT = 400
df['input'] = df['notes'].apply(lambda x: x[0:min(len(x), 320)])
df['num_characters_input'] = df['input'].apply(lambda x: len(x))

model = None
clear_cache()
df_train = df
qlora_fine_tuning_config = yaml.safe_load(
"""
model_type: llm
base_model: meta-llama/Llama-2-7b-hf

input_features:
  - name: instruction
    type: text

output_features:
  - name: output
    type: text

prompt:
  template: >-
    Below is an instruction that describes a task, paired with an input
    that may provide further context. Write a response that appropriately
    completes the request.

    ### Instruction: {instruction}

    ### Input: {input}

    ### Response:

generation:
  temperature: 0
  max_new_tokens: 10

adapter:
  type: lora
  r: 4

quantization:
  bits: 4

trainer:
  type: finetune
  epochs: 1
  batch_size: 1
  eval_batch_size: 1
  gradient_accumulation_steps: 16
  learning_rate: 0.00001
  optimizer:
    type: adam
    params:
      eps: 1.e-8
      betas:
        - 0.9
        - 0.999
      weight_decay: 0
  learning_rate_scheduler:
    warmup_fraction: 0.03
    reduce_on_plateau: 0
"""
)

model = LudwigModel(config=qlora_fine_tuning_config, logging_level=logging.INFO)
results = model.train(dataset=df_train)

