import graph
import pathlib
import os
import math
from tacka import Point
import random
import numpy as np

#Relativna putanja do foldera
DIR_PATH = str(pathlib.Path(__file__).parent.resolve())

#Naziv txt fajla sa tackama
TXT_NAME = "data_path_nodes.txt"

#Sistemski delimiter
DEL = os.path.sep

#Graf tacaka
point_graph = graph.Graph()

#Dictionary vertexa tj tacaka
vertex_dict = {}

# ------- Parametri -------
RO = 0.5 #Evaporation level
ALPHA = 1
BETA = 1

def calc_euclid_dist(tacka1, tacka2):
    x1,y1 = tacka1.x, tacka1.y
    x2,y2 = tacka2.x, tacka2.y
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

#Puni graf tackama i vezama
def fill_graph():
    global point_graph
    global vertex_dict

    set_of_edges = set()
    tacke = {}
    with open(DIR_PATH + DEL + TXT_NAME, "r", encoding='utf-8') as f:
        for line in f.readlines():
            #Preuzimanje podataka
            line = line.rstrip("\n")
            line = line.split(":")
            susedne_tacke = set()
            if len(line) == 2:
                susedne_tacke = line[1].split(",")
            line = line[0].split("(")
            id = line[0]
            x,y = line[1].rstrip(")").split(",")

            tacka = Point(id,float(x),float(y),susedne_tacke)

            #Punjenje recnika tacaka
            tacke[id] = tacka

    #punjenje grafa
    set_of_lone_vertex = set()
    for tacka in tacke.values():
        if len(tacka.susedne_tacke) == 0:
            set_of_lone_vertex.add(tacka)

        #Racuna euklidsku udaljenost i pravi novu granu izmedju tacaka
        for id_susedne_tacke in tacka.susedne_tacke:
            susedna_tacka = tacke[id_susedne_tacke]
            euklidska_udaljenost = calc_euclid_dist(tacka,susedna_tacka)

            #Tezina grane ce biti tuple gde je prva vrednost euklidska udaljenost
            #a druga vrednost nivo feromona izmedju te 2 tacke
            edge = (tacka.id, susedna_tacka.id, (euklidska_udaljenost,1))
            set_of_edges.add(edge)
        
        
    point_graph, vertex_dict = graph.graph_from_edgelist(set_of_edges)

    #Ubacujem vertexe koji nemaju susedne tacke
    for vertex in set_of_lone_vertex:
        point_graph.insert_vertex(vertex)
        vertex_dict[vertex.id] = graph.Graph.Vertex(vertex)

#Bira narednu tacku
def choose_path(source_point,visited_ids):
    #izbori puta
    choices = []

    #probabilistika
    probabilistic = []

    #racunanje sume
    sum = 0
    for option_edge in point_graph.incident_edges(source_point):
        num = option_edge._element[1] ** ALPHA * 1/option_edge._element[0] ** BETA
        sum += num

    #Smestamo u probabilistiku
    for option_edge in point_graph.incident_edges(source_point):
        #preuzimamo drugu ciljanu tacku
        opposite_point = option_edge.opposite(source_point)
        if opposite_point._element in visited_ids:
            continue

        choices.append(opposite_point)
        num = option_edge._element[1] ** ALPHA * 1/option_edge._element[0] ** BETA
        probabilistic.append(num / sum)

    #Provera da li ima kuda
    if len(probabilistic) == 0:
        return None

    #Kumulativna suma
    sorted_probabilistic = []
    sorted_choices = []
    for x,y in sorted(zip(probabilistic, choices)):
        sorted_probabilistic.append(x)
        sorted_choices.append(y)
    cumsum = np.cumsum(sorted_probabilistic)

    next_id = random.choices(sorted_choices, weights=cumsum)[0]

    return next_id

#Pusti mrave
def ant_colony(source, destination, ant_num, iter_num):
    shortest_path = None
    shortest_lenght = math.inf 
    for i in range(iter_num):   

        #Svaki mrav prolazi
        for ant in range(ant_num):

            len_of_path = 0 #duzina puta koji predje mrav
            found = False 
            visited_ids = {} #da ne bi 2 puta isao istom granom
            path = [] #put kuda je isao mrav

            current_point = vertex_dict[source]
            
            #Ide sve dok ne dodje do trazene tacke
            while True:
                next_point = choose_path(current_point, visited_ids)
                if next_point == None:
                    break
                
                visited_ids[current_point._element] = True #Obelezimo da je posecena tacka
                path.append((current_point._element,next_point._element))

                edge = point_graph.get_edge(current_point,next_point)
                len_of_path += edge._element[0]

                if next_point._element == destination:
                    # print("FOUND")
                    found = True
                    break
                current_point = next_point

            if not found:
                continue

            #Obilazi sve predjene grane i ostavlja feromon
            for src, dest in path:
                src_vertex = vertex_dict[src]
                dest_vertex = vertex_dict[dest]
                edge = point_graph.get_edge(src_vertex,dest_vertex)
                edge_list = list(edge._element) #convertujemo tuple u listu kako bi mogli da izmenimo

                #WITH EVAPORATION
                edge_list[1] = (1-RO) * edge_list[1] + 1/len_of_path

                #WITHOUT EVAPORATION
                # edge_list[1] += 1/len_of_path

                edge_tuple = tuple(edge_list) #convertujemo nazad u tuple za upis u edge

                point_graph.insert_edge(src_vertex,dest_vertex,edge_tuple) #update

            if len_of_path < shortest_lenght:
                shortest_lenght = len_of_path
                shortest_path = path

    if shortest_path:
        print("\n" + "*"*50)
        print("Duzina puta je: {0}\nPutanja:\n{1}".format(shortest_lenght, shortest_path))
        print("*"*50 + "\n")
    else:
        print("Nije pronadjen put izmedju ove 2 tacke")

if __name__ == "__main__":   
    fill_graph()
    while True:
        src = input("Unesite pocetnu tacku: ")
        if src not in vertex_dict:
            print("Tacka se ne nalazi u grafu!")
            continue
        break
    while True:
        dest = input("Unesite krajnju tacku: ")
        if dest not in vertex_dict:
            print("Tacka se ne nalazi u grafu!")
            continue
        break
    while True:
        ant_num = input("Unesite broj mrava: ")
        if not ant_num.isdigit():
            print("Nije unet broj!")
            continue
        break
    while True:
        iter_num = input("Unesite broj iteracija: ")
        if not iter_num.isdigit():
            print("Nije unet broj!")
            continue
        break
    
    #'555371834', '2307129536' 
    ant_colony(src, dest, int(ant_num), int(iter_num))
    # ant_colony("555371834", "2307129536", 100, 10)

    

