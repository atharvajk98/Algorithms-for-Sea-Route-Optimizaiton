# This code contains funcions for calculating wavepoints, creating a graph out of the given wavepoints and class definitions of Graph and Vertex. (Each Vertex denoting a seperate Lat-Long coordinate).
from shortest_path_algorithm import ReadingExcelFile         # Reading data from given CSV (Lat - Long data)
from shortest_path_algorithm.structure import Graph
from nautical_calculations import *

# -----------------Storing Wavepoint data-----------------------------------------------------

# 1) This function is used for storing all the wavepoints from the given CSV file.
# 2) The wavepoints (lat-long) values are further sorted and stored in two lists (b1, b2).
# 3) Each list contains the wavepoints from each of the two boundaries of the channel.


def getWavepoints(path1, path2):
    # ------This method generates all the wavepoints (lat,long) which are going to be a part of the channel-----------#
    # 1. Generating boundary coordinates
    b1_lat = []
    b1_long = []
    b2_lat = []
    b2_long = []

    # Extracting boundary coordinates and storing them in seperate lists b1 and b2 ;
    b1_lat, b1_long = ReadingExcelFile.readLatLong(path1)
    b2_lat, b2_long = ReadingExcelFile.readLatLong(path2)

    # 2. Generating intermidiate points to complete the mesh

    wavepoint_list = []  # list contaning all points stored in chronological order
    choice = "1" #input("Input Form :1.Interval (in nautical miles) 2.Number")
    if (choice == "2"):
        num = input("Enter the number of intermidiate points")
        num = int(num)

        # Storing all the vertices in the form of a list, with similar boundary points grouped together for better understanding
        for i in range(len(b1_lat)):
            lat1 = b1_lat[i]
            lat2 = b2_lat[i]
            lng1 = b1_long[i]
            lng2 = b2_long[i]
            azimuth =   get_bearing(lat1, lng1, lat2, lng2)
            wavepoint_list.append( divide_by_number( lat1, lng1, lat2, lng2, num))
    elif (choice == "1"):
        # interval = input("Enter the interval in nautical miles")
        # interval = int(interval)
        interval = 100
        # Storing all the vertices in the form of a list, with similar boundary points grouped together for better understanding
        for i in range(len(b1_lat)):
            lat1 = b1_lat[i]
            lat2 = b2_lat[i]
            lng1 = b1_long[i]
            lng2 = b2_long[i]
            azimuth =   get_bearing(lat1, lng1, lat2, lng2)
            wavepoint_list.append( divide_by_interval(lat1, lng1, lat2, lng2, interval))
    return wavepoint_list

# --------------------------------------------Creating a graph out of {{ wavepoint_list }}------------------------------------
def createGraph(slat, slong, dlat, dlong, wavepoint_list):
    g = Graph()
    start = '-1,0'
    end = '1000,0'
    g.add_vertex(start)
    for i in range(len(wavepoint_list)):
        for j in range(len(wavepoint_list[i])):
            g.add_vertex(str(i) + "," + str(j))
    g.add_vertex(end)

    last = len(wavepoint_list) - 1

    # Adding edges for start
    for k in range(len(wavepoint_list[0])):
        g.add_edge(start, str(0) + "," + str(k),
                    get_distance(slat, slong, wavepoint_list[0][k][0], wavepoint_list[0][k][1]))

    for i in range(len(wavepoint_list)):
        for j in range(len(wavepoint_list[i])):
            # General Condition satisfied by all type of points
            if (i != len(wavepoint_list) - 1):
                for k in range(len(wavepoint_list[i])):
                    g.add_edge(str(i) + "," + str(j), str(i + 1) + "," + str(k), get_distance(wavepoint_list[i][j][0], wavepoint_list[i][j][1],wavepoint_list[i + 1][k][0],wavepoint_list[i + 1][k][1]))
            else:
                break

    # Adding edges for end
    for k in range(len(wavepoint_list[last])):
        g.add_edge(str(last) + "," + str(k), end,
                    get_distance(wavepoint_list[last][k][0], wavepoint_list[last][k][1], dlat,
                                                      dlong))

    return g

# ------------------------------------Getting Final coordinates from Mesh------------------------------------

def convert_coordinates(wavepoint_list,path,startLat,startLong,destLat,destLong):
    list = []
    for i in path:
        if (i == '-1,0'):
            list.append([startLat, startLong])
        elif (i == '1000,0'):
            list.append([destLat, destLong])
        else:
            i = i.split(',')
            lat = int(i[0])
            long = int(i[1])
            point = wavepoint_list[lat][long]
            list.append(point)

    return list
