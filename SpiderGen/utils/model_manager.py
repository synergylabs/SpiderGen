from ollama import chat, pull
import os
import json
import ast
import re
'''
ModelManager class to handle multiple LLM and embedding models from different sources.
Supports OpenAI, Anthropic and Sentence Transformers.
'''

def safe_json_load(response_content):
    if isinstance(response_content, dict):
        return json.dumps(response_content, ensure_ascii=False)

    if not isinstance(response_content, str):
        response_content = str(response_content)

    response_content = re.sub(r"^```[a-zA-Z]*\n?", "", response_content.strip())
    response_content = re.sub(r"```$", "", response_content.strip())

    if '{' in response_content and '}' in response_content:
        start = response_content.find('{')
        end = response_content.rfind('}') + 1
        response_content = response_content[start:end]

    try:
        python_obj = ast.literal_eval(response_content)
        return python_obj
    except Exception:
        pass

    try:
        python_obj = json.loads(response_content)
        return python_obj
    except Exception:
        pass

    fixed_val = (
        response_content
        .replace(" None", " null")
        .replace(" True", " true")
        .replace(" False", " false")
    )

    fixed_val = re.sub(
        r"(?<=\{|,)\s*'([^']+)'\s*:",
        lambda m: f'"{m.group(1)}":',
        fixed_val
    )
    fixed_val = re.sub(
        r"'([^']*)'",
        lambda m: '"' + m.group(1).replace('"', '\\"') + '"',
        fixed_val
    )

    try:
        python_obj = json.loads(fixed_val)
        return python_obj
    except Exception as e:
        print("Failed to parse JSON-like string:", e)
        print("Offending text:", response_content)
        return "{}"

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
            from openai import OpenAI
            client = OpenAI(
                api_key=openai_api_key,
            )
            return client
        elif source == 'sentence_transformer':
            from sentence_transformers import SentenceTransformer
            return SentenceTransformer(name)
        elif source == 'anthropic':
            from SpiderGen.config import anthropic_api_key
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

    def generate_json(self, name, prompt,trace_folder=None):
        print(self.model_source[name])
        if self.model_source[name] == 'openai':
            response = generate_json_openai(prompt,self.models[name], self.model_names[name])
            if trace_folder:
                os.makedirs(trace_folder, exist_ok=True)
                with open(os.path.join(trace_folder, f"{name}_response.json"), 'w') as f:
                    json.dump(response, f, indent=4)
            return response
        elif self.model_source[name] == 'anthropic':
            response =generate_json_anthropic(prompt, self.models[name], self.model_names[name])
            if trace_folder:
                os.makedirs(trace_folder, exist_ok=True)
                with open(os.path.join(trace_folder, f"{name}_response.json"), 'w') as f:
                    json.dump(response, f, indent=4)
            return response
        else:
            raise ValueError(f"Unrecognized model source for model '{name}'.")
    def list_models(self):
        print(f'Model Roles: {self.models.keys()}')
        print(f'Model Sources: {self.model_source.values()}')
        print(f'Model Names: {self.model_names.values()}')
        return list(self.models.keys())
