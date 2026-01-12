#modify this config file to set API keys and model configurations
# specifically, select a sentence transformer, and a large langugage model 
anthropic_api_key = 'blank'
openai_api_key = ''
model_config = dict({
    'roles': ['embedding_transformer', 'llm'],
    'model_names': ['all-mpnet-base-v2', 'o3'],
    'sources': ['sentence_transformer', 'openai']
})