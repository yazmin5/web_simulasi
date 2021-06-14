# Import libraries
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import copy
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("TkAgg")
import base64
from io import BytesIO
from scipy.stats import pearsonr

# Create Directed Graph
def make_DiGraph(df, origin_col = 'Origin', destination_col = 'Destination'):
    origins = df[origin_col].tolist()
    destinations = df[destination_col].tolist()

    g = nx.DiGraph() # DiGraph is base class for directed graphs in networkx packages

    for o,d in zip(origins, destinations):
        g.add_edge(o,d) # Adding edge to graph

    # print('Graph Construction Done,'+' No. Nodes : '+str(g.number_of_nodes()) +', No. Edges : '+str(g.number_of_edges()))

    return g

# Create OD Matrix
def create_ODMatrix(g):
    N_Count = g.number_of_nodes()

    OD = nx.to_numpy_matrix(g) # Origin-Destination matrix

    OD_Transpose = OD.transpose()

    OD_Transpose_Sum = OD_Transpose.sum(axis = 0) # Sum every column

    OD_Matrix = np.zeros((N_Count, N_Count)) # Preparing matrix for transition probability matrix

    # Looping to create transition probability matrix
    for i in range(OD_Matrix.shape[0]):
        for j in range(OD_Matrix.shape[1]):
            denominator = float(OD_Transpose_Sum[0, j])
            if denominator > 0:
                numerator = float(OD_Transpose[i, j])
                OD_Matrix[i, j] = numerator / denominator

    print('Preparation Done, Start Iterating...')

    return OD_Matrix

# Calculate PageRank Score
def run_Modified_PageRank(g, OD_Matrix, coeff, d = 0.95, number_of_loops = 10000):
    N_Count = g.number_of_nodes()

    ranks = np.array(np.ones((1, N_Count)) / float(N_Count), dtype = np.float64).transpose() # Initial PageRank Score

    sumofodm = np.array(np.zeros((1, N_Count))).transpose() # Sum of OD Matrix

    # Calculate PageRank score
    for i in range(1, number_of_loops + 1):
        old_ranks = copy.copy(ranks)

        # Calculate the sum of OD Matrix
        for j in range(0, len(OD_Matrix)):
            sumofodm += (coeff[j] * (np.matmul(OD_Matrix[j], ranks)))

        # Calculate the ranks
        ranks = (1. - d) + (d * sumofodm)

        sumofodm = np.array(np.zeros((1, N_Count))).transpose() # Reset sumofodm variable

        # Conditions if it leads to convergence
        if np.ma.allclose(ranks, old_ranks): break

    # Represent PageRank score as dictionary format
    value = [j[0] for j in ranks.tolist()]
    key = list(g.nodes())

    pagerank_score = {}

    for k in range(len(ranks)):
        pagerank_score[key[k]] = value[k]

    pagerank_score_sorted = dict(reversed(sorted(pagerank_score.items(), key = lambda item: item[1])))

    # print('PageRank Calculation Done After Iteration : ' + str(i))

    return pagerank_score_sorted

# Convert data frame to dictionary format
def make_Dict(df, origin_col = 'Node', destination_col = 'Cases'):
    origins = df[origin_col].tolist()
    destinations = df[destination_col].tolist()
    result = dict(zip(origins, destinations))

    cases_dictionary = dict(reversed(sorted(result.items(), key=lambda item: item[1])))

    return result, cases_dictionary

# Calculate Pearson correlation coefficient
def get_pearson_cor(var1, var2):
    val1_list = []

    # Get first variable value
    for key, val1 in sorted(var1.items()):
        val1_list.append(val1)

    val2_list = []

    # Get second variable value
    for key, val2 in sorted(var2.items()):
        val2_list.append(val2)

    corr, _ = pearsonr(val1_list, val2_list)

    return corr

# Calculate head-tails breaks classification
def htbreak(adic, g = 3):
    alist = [v for k, v in adic.items()]
    temp = copy.copy(alist)
    breaks = []
    for i in range(g - 1):
        avg = sum(temp) / float(len(temp))
        breaks.append(avg)
        temp2 = [v for v in temp if v > avg]
        temp = temp2

    # alist2 = []
    adic2 = {}
    for k, v in adic.items():
        lvl = None
        for i in range(len(breaks)):
            if v <= breaks[i]:
                lvl = i
                break
        if lvl is None:
            lvl = len(breaks)
        # alist2.append(lvl)
        adic2[k] = lvl

    # print(alist2)

    print(adic2)
    print(breaks)

    print('...' * 20)

    return adic2, breaks

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def draw_spatial_graph_east_java(spatial_file, od_file, final_ranks, thres):
    # Read shp file
    gdf = gpd.read_file(spatial_file)

    # Create copy of geo-dataframe
    gdf_points = gdf.copy()

    # Get centroids coordinates of each region
    gdf_points['geometry'] = gdf_points['geometry'].centroid

    # Create new colums for longitude and latitude coordinates
    gdf_points['Long'] = gdf_points.geometry.x
    gdf_points['Lat'] = gdf_points.geometry.y

    final_ranks = pd.DataFrame(final_ranks.items(), columns = ['WADMKK', 'PageRank'])

    print(final_ranks)

    final_ranks['WADMKK'] = final_ranks['WADMKK'].astype(str)
    gdf_points['WADMKK'] = gdf_points['WADMKK'].astype(str)
    
    gdf_points_merge = pd.merge(gdf_points, final_ranks, on='WADMKK') 
    gdf_points_merge['PageRank Label'] = gdf_points_merge['PageRank'].round(3)

    gdf_points_merge['PageRank Label'] = gdf_points_merge['PageRank Label'].astype(str)

    gdf_points_merge['Node Label'] = gdf_points_merge['WADMKK'] + ' ' + '(' +gdf_points_merge['PageRank Label'] + ')'

    label_list = dict(zip(gdf_points_merge['WADMKK'], gdf_points_merge['Node Label']))
    
    print(gdf_points_merge)

    # Manual adjustment to handle too close node which affecting overlapping label between nodes
    
    # Adjust coordinate for Sidoarjo
    gdf_points_merge.at[1, 'Lat'] = -7.408046

    # Adjust coordinate for Kediri
    gdf_points_merge.at[3, 'Lat'] = -7.928923
    gdf_points_merge.at[3, 'Long'] = 112.289499

    # Adjust coordinate for Lamongan
    gdf_points_merge.at[8, 'Lat'] = -7.031358

    # Adjust coordinate for Mojokerto
    gdf_points_merge.at[20, 'Lat'] = -7.599680

    # Adjust coordinate for Kota Blitar
    gdf_points_merge.at[22, 'Lat'] = -8.005235

    # Adjust coordinate for Blitar
    gdf_points_merge.at[23, 'Lat'] = -8.229889

    # Adjust coordinate for Kota Mojokerto
    gdf_points_merge.at[24, 'Long'] = 112.337465

    # Adjust coordinate for Pamekasan
    gdf_points_merge.at[26, 'Lat'] = -7.165152

    # Adjust coordinate for Kota Batu
    gdf_points_merge.at[27, 'Long'] = 112.522421

    # Adjust coordinate for Madiun
    gdf_points_merge.at[29, 'Lat'] = -7.524302

    # Adjust coordinate for Magetan
    gdf_points_merge.at[30, 'Lat'] = -7.763557
    gdf_points_merge.at[30, 'Long'] = 111.257838

    # Adjust coordinate for Bangkalan
    gdf_points_merge.at[31, 'Lat'] = -6.944295

    # Adjust coordinate for Kota Probolinggo
    gdf_points_merge.at[32, 'Long'] = 113.335521

    # Adjust coordinate for Kota Madiun
    gdf_points_merge.at[37, 'Long'] = 111.429918

    # Create graph object
    G = nx.Graph()

    # Iterate to add node in WADMKK column based on coordinates on Long and Lat columns
    for node, posx, posy in zip(gdf_points_merge['WADMKK'], gdf_points_merge['Long'], gdf_points_merge['Lat']):
        G.add_node(node, pos=(posx, posy)) # Adding node to graph

    # Read csv file
    df_graph = pd.read_csv(od_file, error_bad_lines = False)

    # Iterate to add edge between node in Origin column and node in Destination column
    for o, d in zip(df_graph['Origin'].tolist(), df_graph['Destination'].tolist()):
        G.add_edge(o, d) # Adding edge to graph

    # Create a list of color to adjust color for nodes in graph based on threshold produced by Head-Tails Breaks classification
    color_map = []

    for node, score in zip(gdf_points_merge['WADMKK'], gdf_points_merge['PageRank']):
        if score > thres[1]:
            color_map.append('red') # Color for category 2 (High Risk of Covis-19 Spreading)
        if score > thres[0] and score < thres[1]:
            color_map.append('orange') # Color for category 1 (Moderate Risk of Covis-19 Spreading)
        if score < thres[0]:
            color_map.append('yellow') # Color for category 0 (Low Risk of Covis-19 Spreading)

    # Plot the base map and set figure size
    # gdf.plot(figsize=(40,15))
    gdf.plot(figsize=(100,60))

    # Plot the graph
    nx.draw(G, nx.get_node_attributes(G, 'pos'), node_size = gdf_points_merge['PageRank']*100000,
            width = 1.0, node_color=color_map, alpha = 0.8)
    nx.draw_networkx_labels(G, nx.get_node_attributes(G, 'pos'), labels = label_list
                            , font_size = 60, font_color = 'k')

    plt.tight_layout()
    plt.draw()

    graph = get_graph()
    
    return graph

def draw_spatial_graph_central_java(spatial_file, od_file, final_ranks, thres):
    # Read shp file
    gdf = gpd.read_file(spatial_file)

    # Create copy of geo-dataframe
    gdf_points = gdf.copy()

    # Get centroids coordinates of each region
    gdf_points['geometry'] = gdf_points['geometry'].centroid

    # Create new colums for longitude and latitude coordinates
    gdf_points['Long'] = gdf_points.geometry.x
    gdf_points['Lat'] = gdf_points.geometry.y

    final_ranks = pd.DataFrame(final_ranks.items(), columns = ['WADMKK', 'PageRank'])

    print(final_ranks)

    final_ranks['WADMKK'] = final_ranks['WADMKK'].astype(str)
    gdf_points['WADMKK'] = gdf_points['WADMKK'].astype(str)
    
    gdf_points_merge = pd.merge(gdf_points, final_ranks, on='WADMKK') 
    gdf_points_merge['PageRank Label'] = gdf_points_merge['PageRank'].round(3)

    gdf_points_merge['PageRank Label'] = gdf_points_merge['PageRank Label'].astype(str)

    gdf_points_merge['Node Label'] = gdf_points_merge['WADMKK'] + ' ' + '(' +gdf_points_merge['PageRank Label'] + ')'

    label_list = dict(zip(gdf_points_merge['WADMKK'], gdf_points_merge['Node Label']))
    
    print(gdf_points_merge)

    # Manual adjustment to handle too close node which affecting overlapping label between nodes

    # Adjust coordinate for Pekalongan
    gdf_points_merge.at[2, 'Lat'] = -7.156843

    # Adjust coordinate for Magelang
    gdf_points_merge.at[7, 'Lat'] = -7.551585

    # Adjust coordinate for Kota Semarang
    gdf_points_merge.at[11, 'Lat'] = -7.000126

    # Adjust coordinate for Klaten
    gdf_points_merge.at[19, 'Lat'] = -7.726320

    # Adjust coordinate for Purbalingga
    gdf_points_merge.at[20, 'Lat'] = -7.222902

    # Adjust coordinate for Kota Magelang
    gdf_points_merge.at[22, 'Lat'] = -7.428071

    # Create graph object
    G = nx.Graph()

    # Iterate to add node in WADMKK column based on coordinates on Long and Lat columns
    for node, posx, posy in zip(gdf_points_merge['WADMKK'], gdf_points_merge['Long'], gdf_points_merge['Lat']):
        G.add_node(node, pos=(posx, posy)) # Adding node to graph

    # Read csv file
    df_graph = pd.read_csv(od_file)

    # Iterate to add edge between node in Origin column and node in Destination column
    for o, d in zip(df_graph['Origin'].tolist(), df_graph['Destination'].tolist()):
        G.add_edge(o, d) # Adding edge to graph

    # Create a list of color to adjust color for nodes in graph based on threshold produced by Head-Tails Breaks classification
    color_map = []

    for node, score in zip(gdf_points_merge['WADMKK'], gdf_points_merge['PageRank']):
        if score > thres[1]:
            color_map.append('red') # Color for category 2 (High Risk of Covis-19 Spreading)
        if score > thres[0] and score < thres[1]:
            color_map.append('orange') # Color for category 1 (Moderate Risk of Covis-19 Spreading)
        if score < thres[0]:
            color_map.append('yellow') # Color for category 0 (Low Risk of Covis-19 Spreading)

    gdf.plot(figsize=(100,60))

    # Plot the graph
    nx.draw(G, nx.get_node_attributes(G, 'pos'), node_size = gdf_points_merge['PageRank']*100000,
            width = 1.0, node_color=color_map, alpha = 0.8)
    nx.draw_networkx_labels(G, nx.get_node_attributes(G, 'pos'), labels = label_list
                            , font_size = 60, font_color = 'k')

    plt.tight_layout()
    plt.draw()

    graph = get_graph()
    
    return graph

def draw_spatial_graph_bali(spatial_file, od_file, final_ranks, thres):
    # Read shp file
    gdf = gpd.read_file(spatial_file)

    # Create copy of geo-dataframe
    gdf_points = gdf.copy()

    # Get centroids coordinates of each region
    gdf_points['geometry'] = gdf_points['geometry'].centroid

    # Create new colums for longitude and latitude coordinates
    gdf_points['Long'] = gdf_points.geometry.x
    gdf_points['Lat'] = gdf_points.geometry.y

    final_ranks = pd.DataFrame(final_ranks.items(), columns = ['WADMKK', 'PageRank'])

    print(final_ranks)

    final_ranks['WADMKK'] = final_ranks['WADMKK'].astype(str)
    gdf_points['WADMKK'] = gdf_points['WADMKK'].astype(str)
    
    gdf_points_merge = pd.merge(gdf_points, final_ranks, on='WADMKK') 
    gdf_points_merge['PageRank Label'] = gdf_points_merge['PageRank'].round(3)

    gdf_points_merge['PageRank Label'] = gdf_points_merge['PageRank Label'].astype(str)

    gdf_points_merge['Node Label'] = gdf_points_merge['WADMKK'] + ' ' + '(' +gdf_points_merge['PageRank Label'] + ')'

    label_list = dict(zip(gdf_points_merge['WADMKK'], gdf_points_merge['Node Label']))

    # Create graph object
    G = nx.Graph()

    # Iterate to add node in WADMKK column based on coordinates on Long and Lat columns
    for node, posx, posy in zip(gdf_points_merge['WADMKK'], gdf_points_merge['Long'], gdf_points_merge['Lat']):
        G.add_node(node, pos=(posx, posy)) # Adding node to graph

    # Read csv file
    df_graph = pd.read_csv(od_file)

    # Iterate to add edge between node in Origin column and node in Destination column
    for o, d in zip(df_graph['Origin'].tolist(), df_graph['Destination'].tolist()):
        G.add_edge(o, d) # Adding edge to graph

    # Create a list of color to adjust color for nodes in graph based on threshold produced by Head-Tails Breaks classification
    color_map = []

    for node, score in zip(gdf_points_merge['WADMKK'], gdf_points_merge['PageRank']):
        if score > thres[1]:
            color_map.append('red') # Color for category 2 (High Risk of Covis-19 Spreading)
        if score > thres[0] and score < thres[1] :
            color_map.append('orange') # Color for category 1 (Moderate Risk of Covis-19 Spreading)
        if score < thres[0]:
            color_map.append('yellow') # Color for category 0 (Low Risk of Covis-19 Spreading)

    gdf.plot(figsize=(100,60))

    # Plot the graph
    nx.draw(G, nx.get_node_attributes(G, 'pos'), node_size = gdf_points_merge['PageRank']*1000000,
            width = 1.0, node_color=color_map, alpha = 0.8)
    nx.draw_networkx_labels(G, nx.get_node_attributes(G, 'pos'), labels = label_list
                            , font_size = 60, font_color = 'k')

    plt.tight_layout()
    plt.draw()

    graph = get_graph()
    
    return graph