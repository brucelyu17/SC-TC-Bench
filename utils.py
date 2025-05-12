import numpy as np
import pandas as pd
import random
import torch
from openai import OpenAI
from time import sleep
from transformers import AutoTokenizer, AutoModel
from transformers import pipeline
import warnings
warnings.filterwarnings('ignore')

def set_random_seed(seed):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

class LLMEngine(object):
    def __init__(self, llm):
        self.llm = llm
        self.get_hyperpara()

        if llm == 'gpt4o':
            self.engine = 'gpt-4o-2024-05-13'
        elif llm == 'gpt4':
            self.engine = 'gpt-4'
        elif llm == 'gpt3.5':
            self.engine = 'gpt-3.5-turbo'
        elif llm == 'ds':
            self.engine = 'deepseek-r1'
        elif llm in ['qwen', 'baichuan2', 'chatglm2', 'breeze', 'taiwan-llm', 'llama3-70b', 'llama3-8b']:
            if llm == 'qwen':
                self.model_label = "Qwen/Qwen2.5-7B-Instruct"
            elif llm == 'baichuan2':
                self.model_label = "baichuan-inc/Baichuan2-7B-Chat"
            elif llm == 'chatglm2':
                self.model_label = "THUDM/chatglm2-6b"
            elif llm == 'breeze':
                self.model_label = "MediaTek-Research/Breeze-7B-Instruct-v1_0"
            elif llm == 'taiwan-llm':
                self.model_label = "yentinglin/Taiwan-LLM-7B-v2.1-chat"
            elif llm == 'llama3-70b':
                self.model_label = "meta-llama/Meta-Llama-3-70B-Instruct"
            elif llm == 'llama3-8b':
                self.model_label = "meta-llama/Meta-Llama-3-8B-Instruct"
            if self.llm in ['chatglm2']:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_label, trust_remote_code=True)
                self.engine = AutoModel.from_pretrained(self.model_label, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True, do_sample=False).eval()
            else:
                self.engine = pipeline("text-generation", model=self.model_label, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto", trust_remote_code=True)

    def generate_response(self, prompt):
        if self.llm in ['ds']:
            full_prompt=[{"role": "system", "content": "You are a helpful assistant."},{"role":"user","content":prompt}]
        elif self.llm in ['baichuan2', 'chatglm2']:
            full_prompt = prompt
        else:
            full_prompt=[{"role":"user","content":prompt}]

        if self.llm in ['gpt4o', 'gpt4', 'gpt3.5', 'ds']:
            return prompt_with_openai(full_prompt=full_prompt, chat_model=self.engine)
        elif self.llm in ['qwen', 'baichuan2', 'chatglm2', 'breeze', 'taiwan-llm', 'llama3-70b', 'llama3-8b']:
            if self.llm in ['chatglm2']:
                response_str, _ = self.engine.chat(self.tokenizer, full_prompt, history=[])
                return response_str
            else:
                response_str = self.engine(full_prompt, do_sample=False, pad_token_id=self.engine.tokenizer.eos_token_id, max_new_tokens=self.max_new_tokens)
                if self.llm in ['baichuan2']:
                    return response_str[0]['generated_text'].replace(f'{prompt}\n\n','')
                else:
                    return response_str[0]['generated_text'][1]['content']

    def get_hyperpara(self):
        self.max_new_tokens = 512


def prompt_with_openai(full_prompt, chat_model):
    api_key = "<your-api-key>"
    client = OpenAI(api_key=api_key)
    response=None
    timeout_counter=0

    while response is None and timeout_counter<=30:
        try:
            response = client.chat.completions.create(
                            messages=full_prompt,
                            model=chat_model,
                            temperature=0
                            )    
        except Exception as msg:
            if "timeout=600" in str(msg):
                timeout_counter+=1
            print(msg)
            sleep(5)
            continue

    if response==None:
        response_str=""
    else:
        response_str = response.choices[0].message.content
    return response_str


def construct_path(file_type, task, lang, prompt_id=None, llm=None, sub_file_type=None):
    if task not in ['term', 'name']:
        raise NotImplementedError
    if file_type in ['response']:
        if sub_file_type:
            return f'{file_type}/regional_{task}/{sub_file_type}/{llm}_{lang}_{prompt_id}.csv'
        else:
            return f'{file_type}/regional_{task}/{llm}_{lang}_{prompt_id}.csv'
    
    elif file_type in ['prompt']:
        return f'{file_type}/regional_{task}/{lang}_{prompt_id}.csv'

def process_df(file_type, task, lang, prompt_id=None, llm=None, action=None, df_to_save=None, sub_file_type=None):
    path = construct_path(file_type=file_type, task=task, lang=lang, prompt_id=prompt_id, llm=llm, sub_file_type=sub_file_type)
    
    if file_type in ['response']:
        if action == 'save':
            df_to_save.to_csv(path, index=False)
        elif action == 'load':
            return pd.read_csv(path)
        else:
            raise NotImplementedError
    elif file_type in ['prompt']:
        return pd.read_csv(path)
    else:
        raise NotImplementedError