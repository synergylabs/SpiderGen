import os
from spidergen_utils import get_clusters_summary
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
    with open('SpiderGen/proceedure_generation/prompts/prompt_for_similar_products.txt', 'r') as f:
        prompt_similar_products_template = f.read().format(product_category_name, product_category_description, number_sample_products)
    
    with open('SpiderGen/proceedure_generation/prompts/prompt_for_sample_product_template.txt', 'r') as f:
        prompt_sample_product_template = f.read().format()
    
    with open('SpiderGen/proceedure_generation/prompts/prompt_for_generating_pfg.txt', 'r') as f:
        prompt_generating_clusters_template = f.read()

    # If trace is enabled, each step of the generation process will be recorded in a folder
    if trace:
        trace_folder = f"traces/spidergen/{product_category_name.replace(' ', '_')}"
        os.makedirs(trace_folder, exist_ok=True)
        os.makedirs(os.path.join(trace_folder, "similar_products"), exist_ok=True)
        os.makedirs(os.path.join(trace_folder, "sample_products_templates"), exist_ok=True)
        os.makedirs(os.path.join(trace_folder, "clusters"), exist_ok=True)
        os.makedirs(os.path.join(trace_folder, "final_pfg"), exist_ok=True)
    else:
        trace_folder = None
        
    
    # Generate similar products
    similar_products_response = model_manager.generate_json(prompt_similar_products_template, trace_folder=os.path.join(trace_folder, "similar_products") if trace else None)

    #generate template for similar products
    sample_product_response_list = []
    for product in similar_products_response['product']:
        prompt_sample_product = prompt_sample_product_template.format(product, similar_products_response['product'][product]['description'])
        sample_product_response = model_manager['llm'].generate_json(prompt_sample_product, trace_folder=os.path.join(trace_folder, "sample_products_templates") if trace else None)
        sample_product_response_list.append(sample_product_response)
    
    # generate semantically similar clusters
    #prompt_generating_clusters = prompt_generating_clusters_template.format(sample_product_response_list, model.embedding_model_name)
    clusters_response = get_clusters_summary(sample_product_response_list, model_manager['embedding_transformer'])
    #prompt_generating_clusters = prompt_generating_clusters_template.format(clusters_response, product_category_description)

    # Combine clusters into final Process Flow Graph
    prompt_generating_clusters = prompt_generating_clusters_template.format( clusters_response, product_category_description)
    final_pfg_response = model_manager['llm'].generate_json(prompt_generating_clusters, trace_folder=os.path.join(trace_folder, "final_pfg/{product_category_name}.json") if trace else None)

    return final_pfg_response

#example of spidergen usage
if __name__ == "__main__":
    from SpiderGen.utils.model_manager import ModelManager
    from config import model_config

    model_manager = ModelManager()
    model_manager.create_model_environ(
        sources=model_config['sources'],
        model_names=model_config['model_names'],
        roles=model_config['roles']
    )

    product_category_name = "Smartphones"
    product_category_description = "Devices that combine a mobile phone with a handheld computer, typically offering internet access, data storage, and multimedia capabilities."
    number_sample_products = 5

    pfg = spidergen(
        product_category_name,
        product_category_description,
        number_sample_products,
        model_manager,
        trace=True
    )

    print("Generated Process Flow Graph:")
    print(pfg)

