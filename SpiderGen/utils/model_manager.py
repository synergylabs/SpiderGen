from ollama import chat, pull

import json
import ast
import re
'''
ModelManager class to handle multiple LLM and embedding models from different sources.
Supports OpenAI, Anthropic and Sentence Transformers.
'''

def safe_json_load(response_content, top_level_key=None):
    try:
        json_start = response_content.index('{')
        json_end = response_content.rfind('}') + 1
        json_str = response_content[json_start:json_end]
        data = json.loads(json_str)
        if top_level_key:
            return data.get(top_level_key, None)
        return data
    except json.JSONDecodeError as e:
        print("ERROR", e)
        return None

def generate_json_openai(prompt, client, model_name):
    completion = client.chat.completions.create(
        model = model_name,
        #seed = 42,
        messages=[
            {
                "role": "user",
                "content":prompt
            }
        ]
    )
    llm_response = safe_json_load(completion.choices[0].message.content)
    return llm_response

def generate_json_anthropic(prompt, client, model_name):
    completion = client.messages.create(
            model=model_name,
            max_tokens=5000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    
    llm_response = safe_json_load(completion.choices[0].message.content)
    return llm_response

class ModelManager:
    def __init__(self):
        self.models = dict({})
        self.model_names = dict({})
        self.model_source = dict({})
    
    def load_model_from_source(self, name, source):
        if source == 'openai':
            from config import openai_api_key
            import OpenAI
            client = OpenAI(
                api_key=openai_api_key,
            )
            return client
        elif source == 'sentence_transformer':
            from sentence_transformers import SentenceTransformer
            return SentenceTransformer(name)
        elif source == 'anthropic':
            from config import anthropic_api_key
            import anthropic
            client = anthropic.Anthropic(api_key=anthropic_api_key)
            return client
        else:
            raise ValueError(f"Unknown model source '{source}'")

    def register_model(self, name, source, model_name, model):
        self.models[name] = model
        self.model_source[name] = source
        print(self.model_source[name])
        self.model_names[name] = model_name
    
    def create_model_environ(self, sources, model_names, roles):
        if (len(sources) != len(model_names)) or (len(sources) != len(roles)) :
            raise ValueError("Sources and names must be the same length.")
        for i in range(len(sources)):
            model = self.load_model_from_source(model_names[i], sources[i])
            self.register_model(roles[i], sources[i], model_names[i], model)

    def generate_json(self, name, prompt):
        print(self.model_source[name])
        if self.model_source[name] == 'openai':
            return generate_json_openai(prompt,self.models[name], self.model_names[name])
        elif self.model_source[name] == 'anthropic':
            return generate_json_anthropic(prompt, self.models[name], self.model_names[name])
        else:
            raise ValueError(f"Unrecognized model source for model '{name}'.")
    def list_models(self):
        print(f'Model Roles: {self.models.keys()}')
        print(f'Model Sources: {self.model_source.values()}')
        print(f'Model Names: {self.model_names.values()}')
        return list(self.models.keys())
