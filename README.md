# SpiderGen: Towards Procedure Generation for Carbon Life Cycle Assessments With Generative AI

Read our full paper here: https://arxiv.org/abs/2511.10684
Authors: Anupama Sitaraman, Bharathan Balaji, Yuvraj Agarwal

** Abstract **
Investigating the effects of climate change and global warm-
ing caused by GHG emissions have been a key concern
worldwide. These emissions are largely contributed to by the
production, use and disposal of consumer products. Thus, it
is important to build tools to estimate the environmental im-
pact of consumer goods, an essential part of which is con-
ducting Life Cycle Assessments (LCAs). LCAs specify and
account for the appropriate processes involved with the pro-
duction, use, and disposal of the products. We present Spider-
Gen, an LLM-based workflow which integrates the taxonomy
and methodology of traditional LCA with the reasoning ca-
pabilities and world knowledge of LLMs to generate graphi-
cal representations of the key procedural information used for
LCA, known as Product Category Rules Process Flow Graphs
(PCR PFGs). We additionally evaluate the output of Spider-
Gen by comparing it with 65 real-world LCA documents. We
find that SpiderGen provides accurate LCA process informa-
tion that is either fully correct or has minor errors, achieving
an F1-Score of 65% across 10 sample data points, as com-
pared to 53% using a one-shot prompting method. We ob-
serve that the remaining errors occur primarily due to differ-
ences in detail between LCA documents, as well as differ-
ences in the “scope” of which auxiliary processes must also
be included. We also demonstrate that SpiderGen performs
better than several baselines techniques, such as chain-of-
thought prompting and one-shot prompting. Finally, we high-
light SpiderGen’s potential to reduce the human effort and
costs for estimating carbon impact, as it is able to produce
LCA process information for less than $1 USD in under 10
minutes as compared to the status quo LCA, which can cost
over $25000 USD and take up to 21-person days.

## Source Code Details
This source code contains the following:

The **spiderGen** folder contains the core modules to run SpiderGen, including:
- **utils**, which contains code to configure an LLM backend for SpiderGen
- **procedure_generation**, which contains the prompts for each stage of the workflow, as well as code for the clustering steps. The proceedure generation steps are based on ISO standard ISO 14025:2006.
- **spidergen_example.ipynb**, which is Jupyter notebook containing an example PFG using the SpiderGen workflow. Run each cell to get the an example usage of SpiderGen.

## Getting Started

### Pre-requisites:
You must have 
* Python 3.8+ installed
* Api keys for LLM services
* pip installed

### Creating the python environment:
First, create a python environment using 
```
python3 -m venv spidergen
```
then activate it with 
```
source spidergen/bin/activate
```
To ensure that requirements are installed run "pip install -r requirements.txt"

### Modifying the model configuration
To select models to use in the SpiderGen workflow, edit config.py with your api key and model configuration. 
You must configure a Sentence Transformer model, as well as an LLM. 
We currently support openai and anthropic models for the LLM.

When designating the model, the "role" indicates what the model is used for, and the "model_name" indicates the specific model that is being used. The "sources" are the source of the model (i.e, openai). 

For example:
```
model_config = dict({
    'roles': ['embedding_transformer', 'llm'],
    'model_names': ['all-mpnet-base-v2', 'gpt-4o-2024-08-06'],
    'sources': ['sentence_transformer', 'openai']
})
```

These models are then handled by ModelManager (in the utils folder) to handle both sentence embedding and response generation requests. 


### Getting Ground-Truth Data for Evaluation 
Our ground-truth evaluation relies on data from EPD International's PCR Library (https://www.environdec.com/pcr-library). To access these PCRs, you must make an account. We then downloaded every document and determined which would be suitable as evaluation data points based on how complete the information was in each document (i.e, not including any documents that were simply supplementary and did not contain a PCR PFG on its own). For the list of PCRs that we utilized, refer to the technical appendix in our paper. 

***Evaluation Code: Coming soon!!***
The **evaluation** folder contains the modules used to evaluate SpiderGen, including:
- **pmi.py**, which contains code for calculating the PMI between ground-truth PCR PFG processes and SpiderGen PFG processes
- **metrics.py** which contains code for calculating existing semantic similarity metrics, such as ROUGE and BLEU between ground-truth PCR PFG processes and SpiderGen PFG processes
- **baselines.py** which contains LLM prompts and code to generate the baselines used in our paper



