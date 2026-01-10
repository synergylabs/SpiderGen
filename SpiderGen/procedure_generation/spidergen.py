import os
from procedure_generation.spidergen_utils import get_clusters_summary
import json
def spidergen(product_category_name, product_category_description, number_sample_products, model_manager, trace=True):
    """
    Generates a Process Flow Graph for the given product category.

    Args:
        product_category_name (str): The name of the product category.
        product_category_description (str): A description of the product category.
        number_sample_products (int): The number of sample products to generate.
        model (ModelManager): The model manager instance to use for generation.
        trace (bool): Whether to enable tracing for LCA transparency. """
    
    # Load prompts
    with open('procedure_generation/prompts/prompt_for_similar_products.txt', 'r') as f:
        prompt_similar_products_template = f.read().format(product_category_name, product_category_description, number_sample_products)
    
    with open('procedure_generation/prompts/prompt_for_sample_product_template.txt', 'r') as f:
        prompt_sample_product_template = f.read()
    
    with open('procedure_generation/prompts/prompt_for_generating_pfg.txt', 'r') as f:
        prompt_generating_clusters_template = f.read()

    # If trace is enabled, each step of the generation process will be recorded in a folder
    if trace:
        trace_folder = f"./traces/spidergen/{product_category_name.replace(' ', '_')}"
        os.makedirs(trace_folder, exist_ok=True)
        os.makedirs(os.path.join(trace_folder, "similar_products"), exist_ok=True)
        os.makedirs(os.path.join(trace_folder, "sample_products_templates"), exist_ok=True)
        os.makedirs(os.path.join(trace_folder, "clusters"), exist_ok=True)
        os.makedirs(os.path.join(trace_folder, "final_pfg"), exist_ok=True)
    else:
        trace_folder = None
        
    
    # Generate similar products
    if trace:
        trace_path_similar_products = os.path.join(trace_folder, "similar_products")
        print(trace_path_similar_products)
        trace_file = os.path.join(trace_path_similar_products, "llm_response.json")
        if os.path.isfile(trace_file) and trace:
            with open(trace_file, "r") as f:
                similar_products_response = json.load(f)
    else:
        similar_products_response = model_manager.generate_json('llm',prompt_similar_products_template, trace_folder=trace_path_similar_products if trace else None)
    print("Similar Products Response:", similar_products_response)
    #generate template for similar products
    sample_product_response_list = dict({})
    for product in similar_products_response['product']:
        prompt_sample_product = prompt_sample_product_template.format(product, similar_products_response['product'][product]['description'])
        if trace:
            save_path_sample_product_template = os.path.join(trace_folder, f"sample_products_templates/{product}/llm_response.json")
            if os.path.exists(save_path_sample_product_template) and trace:
                with open(save_path_sample_product_template, 'r') as f:
                    sample_product_response = json.load(f)
        else:
            sample_product_response = model_manager.generate_json('llm', prompt_sample_product, trace_folder=os.path.join(trace_folder,f"sample_products_templates/{product}") if trace else None)
        sample_product_response_list[product] = sample_product_response
    
    # generate semantically similar clusters
    #prompt_generating_clusters = prompt_generating_clusters_template.format(sample_product_response_list, model.embedding_model_name)
    clusters_response = get_clusters_summary(sample_product_response_list, model_manager.models['embedding_transformer'])
    
    #prompt_generating_clusters = prompt_generating_clusters_template.format(clusters_response, product_category_description)

    # Combine clusters into final Process Flow Graph
    prompt_generating_clusters = prompt_generating_clusters_template.format(product_category_description,  clusters_response, product_category_description)
    final_pfg_response = model_manager.generate_json('llm', prompt_generating_clusters, trace_folder=os.path.join(trace_folder, "final_pfg.json") if trace else None)

    return final_pfg_response


