# Import libraries
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from matplotlib import pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def draw_graph(spatial_file, od_file):
    # Read shp file
    gdf = gpd.read_file(spatial_file)

    # Delete unused columns
    del gdf['NAMOBJ']
    del gdf['SHAPE_AREA']
    del gdf['SHAPE_LEN']

    # Rename columns
    gdf = gdf.rename({'COVID_CASE' : 'Jumlah Kasus Terkonfirmasi',
                'PAGERANK' : 'Nilai PageRank'}, axis = 1)

    # Create copy of geo-dataframe
    gdf_points = gdf.copy()

    # Get centroids coordinates of each region
    gdf_points['geometry'] = gdf_points['geometry'].centroid

    # Create new colums for longitude and latitude coordinates
    gdf_points['Long'] = gdf_points.geometry.x
    gdf_points['Lat'] = gdf_points.geometry.y

    # Manual adjustment to handle too close node which affecting overlapping label between nodes

    # Adjust coordinate for Sidoarjo
    gdf_points.at[1, 'Lat'] = -7.408046

    # Adjust coordinate for Kediri
    gdf_points.at[3, 'Lat'] = -7.928923
    gdf_points.at[3, 'Long'] = 112.289499

    # Adjust coordinate for Lamongan
    gdf_points.at[8, 'Lat'] = -7.031358

    # Adjust coordinate for Mojokerto
    gdf_points.at[20, 'Lat'] = -7.599680

    # Adjust coordinate for Kota Blitar
    gdf_points.at[22, 'Lat'] = -8.005235

    # Adjust coordinate for Blitar
    gdf_points.at[23, 'Lat'] = -8.229889

    # Adjust coordinate for Kota Mojokerto
    gdf_points.at[24, 'Long'] = 112.337465

    # Adjust coordinate for Pamekasan
    gdf_points.at[26, 'Lat'] = -7.165152

    # Adjust coordinate for Kota Batu
    gdf_points.at[27, 'Long'] = 112.522421

    # Adjust coordinate for Madiun
    gdf_points.at[29, 'Lat'] = -7.524302

    # Adjust coordinate for Magetan
    gdf_points.at[30, 'Lat'] = -7.763557
    gdf_points.at[30, 'Long'] = 111.257838

    # Adjust coordinate for Bangkalan
    gdf_points.at[31, 'Lat'] = -6.944295

    # Adjust coordinate for Kota Probolinggo
    gdf_points.at[32, 'Long'] = 113.335521

    # Adjust coordinate for Kota Madiun
    gdf_points.at[37, 'Long'] = 111.429918

    # Create graph object
    G = nx.Graph()

    # Iterate to add node in WADMKK column based on coordinates on Long and Lat columns
    for node, posx, posy in zip(gdf_points['WADMKK'], gdf_points['Long'], gdf_points['Lat']):
        G.add_node(node, pos=(posx, posy)) # Adding node to graph

    # Read csv file
    df_graph = pd.read_csv(od_file)
    df_graph.head(15)

    # Iterate to add edge between node in Origin column and node in Destination column
    for o, d in zip(df_graph['Origin'].tolist(), df_graph['Destination'].tolist()):
        G.add_edge(o, d)  # Adding edge to graph

    # Create a list of color to adjust color for nodes in graph based on threshold produced by Head-Tails Breaks classification
    color_map = []

    for node, score in zip(gdf['WADMKK'], gdf['Nilai PageRank']):
        if score > 2.28979956970993:
            color_map.append('red') # Color for category 2 (High Risk of Covis-19 Spreading)
        if score > 0.6681497153118374 and score < 2.28979956970993:
            color_map.append('orange') # Color for category 1 (Moderate Risk of Covis-19 Spreading)
        if score < 0.6681497153118374:
            color_map.append('yellow') # Color for category 0 (Low Risk of Covis-19 Spreading)

    # Rename the label to add PageRank score information
    label_list = {}
    label_list["Jember"] = "Jember (0.904)"
    label_list["Sidoarjo"] = "Sidoarjo (1.043)"
    label_list["Bojonegoro"] = "Bojonegoro (2.042)"
    label_list["Kediri"] = "Kediri (0.749)"
    label_list["Kota Pasuruan"] = "Kota Pasuruan (1.179)"
    label_list["Ponorogo"] = "Kota Pasuruan (0.301)"
    label_list["Bondowoso"] = "Bondowoso (0.176)"
    label_list["Situbondo"] = "Situbondo (0.125)"
    label_list["Lamongan"] = "Lamongan (0.090)"
    label_list["Malang"] = "Malang (1.202)"

    label_list["Banyuwangi"] = "Banyuwangi (1.814)"
    label_list["Nganjuk"] = "Nganjuk (0.215)"
    label_list["Sumenep"] = "Sumenep (0.768)"
    label_list["Tuban"] = "Tuban (0.146)"
    label_list["Trenggalek"] = "Trenggalek (0.105)"
    label_list["Kota Kediri"] = "Kota Kediri (1.632)"
    label_list["Lumajang"] = "Lumajang (0.012)"
    label_list["Pasuruan"] = "Pasuruan (1.149)"
    label_list["Kota Surabaya"] = "Kota Surabaya (11.440)"
    label_list["Tulungagung"] = "Tulungagung (0.371)"

    label_list["Mojokerto"] = "Mojokerto (0.253)"
    label_list["Gresik"] = "Gresik (-0.294)"
    label_list["Kota Blitar"] = "Kota Blitar (0.116)"
    label_list["Blitar"] = "Blitar (0.168)"
    label_list["Kota Mojokerto"] = "Kota Mojokerto (0.123)"
    label_list["Kota Malang"] = "Kota Malang (0.141)"
    label_list["Pamekasan"] = "Pamekasan (0.168)"
    label_list["Kota Batu"] = "Kota Batu (0.097)"
    label_list["Pacitan"] = "Pacitan (0.072)"
    label_list["Madiun"] = "Madiun (0.084)"

    label_list["Magetan"] = "Magetan (0.157)"
    label_list["Bangkalan"] = "Bangkalan (0.226)"
    label_list["Kota Probolinggo"] = "Kota Probolinggo (0.111)"
    label_list["Ngawi"] = "Ngawi (0.348)"
    label_list["Sampang"] = "Sampang (0.150)"
    label_list["Probolinggo"] = "Probolinggo (0.201)"
    label_list["Jombang"] = "Jombang (0.309227)"
    label_list["Kota Madiun"] = "Kota Madiun (0.095)"

    # Plot the base map and set figure size
    gdf.plot(figsize=(21,8))

    # Plot the graph
    nx.draw(G, nx.get_node_attributes(G, 'pos'), node_size = (gdf_points['Nilai PageRank'])*350,
            width = 0.5, node_color=color_map, alpha = 0.8)
    nx.draw_networkx_labels(G, nx.get_node_attributes(G, 'pos'), labels = label_list
                            , font_size = 8, font_color = 'k')

    plt.tight_layout()
    plt.show()

    graph = get_graph()
    return graph