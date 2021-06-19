import networkx as nx             # graph
import matplotlib.pyplot as plt   # plot
import numpy as np                # calculation
import pandas as pd
import copy as copy
import geopandas as gpd
import matplotlib
matplotlib.use("TkAgg")
import base64
from io import BytesIO
from scipy.stats import pearsonr


# create Directed Graph
def cre_DiGraph(df, origin_col='origin', destination_col='destination', 
                distance_col='distance', exclude_selfloop=True):
    origins = df[origin_col].tolist()
    destinations = df[destination_col].tolist()
    distances = df[distance_col].tolist()
    # Making a Adjacency matrix
    g = nx.DiGraph()
    for o,d,f in zip(origins, destinations, distances):
        g.add_edge(o, d, weight=float(f))

    pos = nx.spring_layout(g)
    # Save graph as picture
    nx.draw(g, with_labels = True, pos = pos)
    plt.savefig("Graph.png")

    print('Graph Construction Succeed,'+' No. Nodes : '+str( g.number_of_nodes()) +', No. Edges : '+str(g.number_of_edges()))
    print(g.nodes())

    print('===' * 20)
    print('...' * 20)
    print('===' * 20)
    return g


# DDPR algorithm
def run_ddpr(g, b=0.9, number_of_loops=1000, exfac=None) :
    N_Count = g.number_of_nodes()

    # Initial PageRank Score
    ranks = np.array(np.ones((1, N_Count)) / float(N_Count)).transpose() 
    print('Preparation Done, Start Iterating...')
    #print(ranks)

    # Origin-Destination matrix
    MatrixOD = nx.to_numpy_matrix(g, weight = 'weight')  
    #MatrixODSum = MatrixOD.sum(axis=0)  # Sum every column (outdegree)

    # Preparing matrix for distance-decay effect
    MatrixDD = np.zeros((N_Count,N_Count)) 
    # Preparing matrix for partition score
    MatrixPart = np.zeros((N_Count,N_Count))

    # Looping to defining distance-decay effect
    for i in range(MatrixDD.shape[0]):
        for j in range(MatrixDD.shape[1]):

            #defining distance-decay effect
            if MatrixOD[i,j] > 0 :

              denominator = float(MatrixOD[i, j])
              MatrixDD[i, j] = 1 / (denominator) ** b
    #print(MatrixDD)
    # Defining sum of distance-decay effect of each node
    MatrixDDSum = MatrixDD.sum(axis=0)
    #print(MatrixDDSum)

    # Looping to defining matrix for partition score
    for i in range(MatrixPart.shape[0]):
        for j in range(MatrixPart.shape[1]):
          if MatrixOD[i,j] > 0 :
            x = float(MatrixDD[i,j])
            y = float(MatrixDDSum[j])
            MatrixPart[i,j] = x / y

    # Calculate DDPR score
    for i in range(1, number_of_loops + 1):
        old_ranks = copy.copy(ranks)
        ranks = np.matmul(MatrixPart, ranks)

        # Equillibrium until convergence
        if np.ma.allclose(ranks, old_ranks): break

    print('Calculation Done After Iteration : ' + str(i))
    print('With b = ' + str(b))

    # Represent DDPR score as dictionary format
    value = [i[0] for i in ranks.tolist()]
    key = list(g.nodes())

    ddprScore = {}
    for i in range(len(ranks)):
        ddprScore[key[i]] = value[i]

    #hasil
    nama = key
    skor = value

    print('===' * 20)
    print('===' * 20)

    dictionary = dict(reversed(sorted(ddprScore.items(), key = lambda item: item[1])))

    for key, value in dictionary.items(): print("{} : ({})".format(key, value))

    #plt.rcdefaults()
    #fig, ax = plt.subplots()

    #ax.barh(nama, skor, align='center')
    #ax.set_yticks(np.arange(len(nama)))
    #ax.set_yticklabels(nama)
    #ax.invert_yaxis()  # labels read top-to-bottom
    #ax.set_xlabel('Score')
    #ax.set_title('DDPR Score')

    #plt.show()

    list1 = [ddprScore, b, nama, skor]

    print('letsgow')

    return list1


# Function for making a dictionary
def makeDict(dfCases, origin_col='node', destination_col='cases'):
   nodes = dfCases[origin_col].tolist()
   cases = dfCases[destination_col].tolist()
   result = dict(zip(nodes, cases))
   
   return result 


# Pearson Correlation
def pearsonCorr(var1, var2):
   val1_list = []

   for key, val1 in sorted(var1.items()):
       val1_list.append(val1)

   val2_list = []

   for key, val2 in sorted(var2.items()):
       val2_list.append(val2)

   corr, p_value = pearsonr(val1_list, val2_list)
   print("Nilai Korelasi : ", corr)

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

#visualisasi
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


#visualisasi graf wilayah jatim
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