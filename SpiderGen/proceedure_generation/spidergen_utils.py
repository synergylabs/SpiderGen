'''
Supporting functions and utilities for SpiderGen proceedure generation
'''
import numpy as np
import json
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score

def get_k_means_clustering(encoded_processes, processes_dict, all_processes):
    '''
    encoded_processes: encoded processes of sample products
    processes_dict: dictionary of processes for all sample products
    all_processes: list of all processes for for all sample products combined


    '''
    
    # If no processes exist for this category of processes, return an empty dictionary
    if len(all_processes) == 0:
        print('none of the processes')
        return {}
    

    # Step 1: Determining the optimal number of clusters based on the similarity within each cluster

    # Determining the search space for number of clusters - can be at least the minimum number of processes, and at most the maximum number of processes for each sample product 
    nums = []
    for item in processes_dict:
        nums.append(len(processes_dict[item]))
    n_clusters_num = int(np.floor(np.mean(np.array(nums))))
    n_min_clusters_num = min(nums)
    n_max_clusters_num = max(nums)

    # if the average number of processes in each prodcut is 1 or less, we set the number of clusters to 1
    if n_clusters_num <= 1:
        n_clusters_num_arr = [1]
    else:
    
    #otherwise, we set a range of potential numbers of clusters from min to max
        n_clusters_num_arr = []
        for i in range(n_min_clusters_num, n_max_clusters_num+1, 1):
            if i == 0:
                continue
            else:
                n_clusters_num_arr.append(i)
    #we systematically test each number of clusters and compute the davies bouldin score to determine the best number of clusters
    best_k = []
    if n_clusters_num_arr == [1]:
        best_val_k = 1
        clustering_model = KMeans(n_clusters=best_val_k, random_state=0)
        clustering_model.fit(encoded_processes)
        cluster_assignment = clustering_model.labels_
    else:
        for j in set(nums):
            if j == 0:
                continue
            if j == 1:
                continue
            clustering_model = KMeans(n_clusters=j, random_state=0)
            score = davies_bouldin_score(encoded_processes, clustering_model.fit_predict(encoded_processes))
            best_k.append(score)
        
        # we select the number of clusters that gives the lowest davies bouldin score, and create that number of clusters
        best_val_k1 = n_clusters_num_arr[np.argmin(best_k)]
        clustering_model = KMeans(n_clusters=best_val_k1, random_state=0)
        clustering_model.fit(encoded_processes)
        cluster_assignment = clustering_model.labels_
    
    #formatting the clusters into a dictionary
    clusters = {}
    for i, sentence in enumerate(np.array(all_processes)):
        cluster_id = cluster_assignment[i]
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        if sentence not in clusters[cluster_id]:
            clusters[cluster_id].append(sentence)
        
    for cluster_id, cluster_sentences in clusters.items():
        print(f"\nCluster {cluster_id}:")
        for sent in cluster_sentences:
            print(f"  - {sent}")
    return clusters

def get_clusters_summary(product_templates, transformer_model):
    '''
    generating clusters for all processes in all parts of the life cycle, based on EPD International guidelines for processes
    product_templates: product templates for all sample products
    transformer_model: embedding model to use for generating embeddings

    returns: clusters for all processes in all parts of the life cycle
    '''

    A1_dict = dict({})
    A2_dict = dict({})
    A3_dict = dict({})
    A4_dict = dict({})
    A5_dict = dict({})

    B1_dict = dict({})
    B2_dict = dict({})
    B3_dict = dict({})
    B4_dict = dict({})
    B5_dict = dict({})
    B6_dict = dict({})
    B7_dict = dict({})

    C1_dict = dict({})
    C2_dict = dict({})
    C3_dict = dict({})
    C4_dict = dict({})

    all_A1 = []
    all_A2 = []
    all_A3 = []
    all_A4 = []
    all_A5 = []
    all_B1 = []
    all_B2 = []
    all_B3 = []
    all_B4 = []
    all_B5 = []
    all_B6 = []
    all_B7 = []
    all_C1 = []
    all_C2 = []
    all_C3 = []
    all_C4 = []
    for item in product_templates['product']:
        curr_product = product_templates['product'][item]
        print(item)
        if curr_product == "null":
            print('skipping nulled product')
            continue
        for process in curr_product['processes']:
            #print(process)
            A1_dict[item] = []
            for a1 in curr_product['processes']['A1 Processes']:
                if a1 != 'N/A':
                    A1_dict[item].append(a1)
                    all_A1.append(a1)
            A2_dict[item] = []
            for a2 in curr_product['processes']['A2 Processes']:
                if a2 != 'N/A':
                    A2_dict[item].append(a2)
                    all_A2.append(a2)
            A3_dict[item] = []
            for a3 in curr_product['processes']['A3 Processes']:
                if a3 != 'N/A':
                    A3_dict[item].append(a3)
                    all_A3.append(a3)
            A4_dict[item] = []
            for a4 in curr_product['processes']['A4 Processes']:
                if a4 != 'N/A':
                    A4_dict[item].append(a4)
                    all_A4.append(a4)
            A5_dict[item] = []
            for a5 in curr_product['processes']['A5 Processes']:
                if a5 != 'N/A':
                    A5_dict[item].append(a5)
                    all_A5.append(a5)
            B1_dict[item] = []
            for b1 in curr_product['processes']['B1 Processes']:
                if b1 != 'N/A':
                    B1_dict[item].append(b1)
                    all_B1.append(b1)
            B2_dict[item] = []
            for b2 in curr_product['processes']['B2 Processes']:
                if b2 != 'N/A':
                    B2_dict[item].append(b2)
                    all_B2.append(b2)
            B3_dict[item] = []
            for b3 in curr_product['processes']['B3 Processes']:
                if b3 != 'N/A':
                    B3_dict[item].append(b3)
                    all_B3.append(b3)
            B4_dict[item] = []
            for b4 in curr_product['processes']['B4 Processes']:
                if b4 != 'N/A':
                    B4_dict[item].append(b4)
                    all_B4.append(b4)
            B5_dict[item] = []
            for b5 in curr_product['processes']['B5 Processes']:
                if b5 != 'N/A':
                    B5_dict[item].append(b5)
                    all_B5.append(b5)
            B6_dict[item] = []
            for b6 in curr_product['processes']['B6 Processes']:
                if b6 != 'N/A':
                    B6_dict[item].append(b6)
                    all_B6.append(b6)
            B7_dict[item] = []
            for b7 in curr_product['processes']['B7 Processes']:
                if b7 != 'N/A':
                    B7_dict[item].append(b7)
                    all_B7.append(b7)
            C1_dict[item] = []
            for c1 in curr_product['processes']['C1 Processes']:
                if c1 != 'N/A':
                    C1_dict[item].append(c1)
                    all_C1.append(c1)
            C2_dict[item] = []
            for c2 in curr_product['processes']['C2 Processes']:
                if c2 != 'N/A':
                    C2_dict[item].append(c2)
                    all_C2.append(c2)
            C3_dict[item] = []
            for c3 in curr_product['processes']['C3 Processes']:
                if c3 != 'N/A':
                    C3_dict[item].append(c3)
                    all_C3.append(c3)
            C4_dict[item] = []
            for c4 in curr_product['processes']['C4 Processes']:
                if c4 != 'N/A':
                    C4_dict[item].append(c4)
                    all_C4.append(c4)
            
    print('start clustering within dictionaries')
    processes_list = []
    if len(all_A1) > 0:
        encoded_processes_a1 = transformer_model.encode(np.array(all_A1), normalize_embeddings=True)
        print('a1 clusters')
        a1_clusters = get_k_means_clustering(encoded_processes_a1, A1_dict, all_A1)
        processes_list.append(a1_clusters)
    
    if len(all_A2) > 0:
        encoded_processes_a2 = transformer_model.encode(np.array(all_A2), normalize_embeddings=True)
        print('a2 clusters')
        a2_clusters = get_k_means_clustering(encoded_processes_a2, A2_dict, all_A2)
        processes_list.append(a2_clusters)
    
    if len(all_A3) > 0:
        encoded_processes_a3 = transformer_model.encode(np.array(all_A3), normalize_embeddings=True)
        print('a3 clusters')
        a3_clusters = get_k_means_clustering(encoded_processes_a3, A3_dict, all_A3)
        processes_list.append(a3_clusters)

    if len(all_A4) > 0:
        encoded_processes_a4 = transformer_model.encode(np.array(all_A4), normalize_embeddings=True)
        print('a4 clusters')
        a4_clusters = get_k_means_clustering(encoded_processes_a4, A4_dict, all_A4)
        processes_list.append(a4_clusters)
    if len(all_A5) > 0:
        encoded_processes_a5 = transformer_model.encode(np.array(all_A5), normalize_embeddings=True)
        print('a5 clusters')
        a5_clusters = get_k_means_clustering(encoded_processes_a5, A5_dict, all_A5)
        processes_list.append(a5_clusters)
    
    if len(all_B1) > 0:
        encoded_processes_b1 = transformer_model.encode(np.array(all_B1), normalize_embeddings=True)
        print('b1 clusters')
        b1_clusters = get_k_means_clustering(encoded_processes_b1, B1_dict, all_B1)
        processes_list.append(b1_clusters)
    
    if len(all_B2) > 0:
        encoded_processes_b2 = transformer_model.encode(np.array(all_B2), normalize_embeddings=True)
        print('b2 clusters')
        b2_clusters = get_k_means_clustering(encoded_processes_b2, B2_dict, all_B2)
        processes_list.append(b2_clusters)
    
    if len(all_B3) > 0:
        encoded_processes_b3 = transformer_model.encode(np.array(all_B3), normalize_embeddings=True)
        print('b3 clusters')
        b3_clusters = get_k_means_clustering(encoded_processes_b3, B3_dict, all_B3)
        processes_list.append(b3_clusters)
    
    if len(all_B4) > 0:
        encoded_processes_b4 = transformer_model.encode(np.array(all_B4), normalize_embeddings=True)
        print('b1 clusters')
        b4_clusters = get_k_means_clustering(encoded_processes_b4, B4_dict, all_B4)
        processes_list.append(b4_clusters)
    
    if len(all_B5) > 0:
        encoded_processes_b5 = transformer_model.encode(np.array(all_B5), normalize_embeddings=True)
        print('b5 clusters')
        b5_clusters = get_k_means_clustering(encoded_processes_b5, B5_dict, all_B5)
        processes_list.append(b5_clusters)
    
    if len(all_B6) > 0:
        encoded_processes_b6 = transformer_model.encode(np.array(all_B6), normalize_embeddings=True)
        print('b6 clusters')
        b6_clusters = get_k_means_clustering(encoded_processes_b6, B6_dict, all_B6)
        processes_list.append(b6_clusters)
    
    if len(all_B7) > 0:
        encoded_processes_b7 = transformer_model.encode(np.array(all_B7), normalize_embeddings=True)
        print('b7 clusters')
        b7_clusters = get_k_means_clustering(encoded_processes_b7, B7_dict, all_B7)
        processes_list.append(b7_clusters)
    
    if len(all_C1) > 0:
        encoded_processes_c1 = transformer_model.encode(np.array(all_C1), normalize_embeddings=True)
        print('c1 clusters')
        c1_clusters = get_k_means_clustering(encoded_processes_c1, C1_dict, all_C1)
        processes_list.append(c1_clusters)
    
    if len(all_C2) > 0:
        encoded_processes_c2 = transformer_model.encode(np.array(all_C2), normalize_embeddings=True)
        print('c2 clusters')
        c2_clusters = get_k_means_clustering(encoded_processes_c2, C2_dict, all_C2)
        processes_list.append(c2_clusters)
    
    if len(all_C3) > 0:
        encoded_processes_c3 = transformer_model.encode(np.array(all_C3), normalize_embeddings=True)
        print('c3 clusters')
        c3_clusters = get_k_means_clustering(encoded_processes_c3, C3_dict, all_C3)
        processes_list.append(c3_clusters)
    
    if len(all_C4) > 0:
        encoded_processes_c4 = transformer_model.encode(np.array(all_C4), normalize_embeddings=True)
        print('c4 clusters')
        c4_clusters = get_k_means_clustering(encoded_processes_c4, C4_dict, all_C4)
        processes_list.append(c4_clusters)
    
    return np.array(processes_list).flatten()