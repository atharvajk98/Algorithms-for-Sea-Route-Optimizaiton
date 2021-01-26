#_______________Main code_________________

from shortest_path_algorithm import Channel
from shortest_path_algorithm import structure
from shortest_path_algorithm import shortest_path_function
from shortest_path_algorithm.plot_and_print import plotRoute, printGraph, printWavepoints, printPath, plot_all_routes
from time import process_time
import pandas as pd
import numpy as np
from nautical_calculations import get_distance


def main():

    #Our route start and end
    startLat = round( 22.21948, 4);
    startLong = round(-97.8241, 4);
    destLat = round(23.17218 , 4);
    destLong = round(-82.39868, 4);


    ''' 
    #hawai route start and end
    startLat = round(8.8882, 4);
    startLong = round(-79.5214, 4);
    destLat = round(36.8578, 4);
    destLong = round(126.117, 4);
    '''

    boundary_1 = 'Data/Upper_boundary.csv'
    boundary_2 = 'Data/Lower_boundary.csv'

    wavepoint_list = {}
    g = structure.Graph()
    final_coords = []

    #--------------------------- GETTING ALL WAYPOINTS AND CREATING A GRAPH ----------------------------------------

    # 1. Getting all the wavepoints
    print("getting wavepoints")
    wavepoint_list = Channel.getWavepoints(boundary_1, boundary_2)
    print("Wavepoints stored")
    #printWavepoints(wavepoint_list)

    # 2. Creating a mesh-graph of channel
    start = process_time()
    g = Channel.createGraph(startLat, startLong, destLat, destLong, wavepoint_list)
    end = process_time()
    print("\nTime taken to create graph: ", str(end - start))
    start = 0
    end = 0
    print("Mesh created")
    printGraph(g)


    #--------------------------------------- SHORTEST PATH FUNCTION --------------------------------------------------

    # 3. Passing the graph to Shortest Path Algorithm
    print("\nCalculating Shortest path....\n")
    start = process_time()
    final_points, distance = shortest_path_function.shortestDistance(g, '-1,0', '1000,0')
    end = process_time()
    print("\nTime taken to find shortest path: ", str(end - start))
    start = 0
    end = 0
    print("\nShortest path calculated....\n")

    # Converting Points to Lat,Long
    print("\nObtained Points : \n", final_points)
    final_coords = Channel.convert_coordinates(wavepoint_list, final_points, startLat, startLong, destLat, destLong)

    # 4. Displaying best route with total distance
    print("\nFinal Path :")
    printPath(final_coords)
    print("\nTotal Distance covered : ", distance, " nautical km")

    # 5. Plotting the route on Google Maps
    plotRoute(final_coords, 'shortest')
    print("Route Plotting complete")

    #--------------------------------------- FINDING ALL POSSIBLE ROUTES ---------------------------------------------

    total_len = 1
    route_lens = []
    for l in wavepoint_list:
        total_len = total_len * len(l)
        route_lens.append(len(l))

    print("Expected total no of routes: ", total_len)

    print("Each level contains : ")
    for i in route_lens:
        print(i)

    print("\nComputing all the routes....\n")
    start = process_time()
    g_new, routes = shortest_path_function.get_all_routes(g,'-1,0', '1000,0', total_len, route_lens[-1])
    end = process_time()
    print("\nTime taken to compute all paths: ", str(end - start))
    start = 0
    end = 0
    print("\nAll routes computed....\n")

    print("Expected total no of routes: ", total_len)
    print("\nGot total no of routes: ", len(routes))

    print("\nAll routes: \n")
    for r in routes:
        print(r)

    routes_lat_long = []
    for rr in routes:
        ll = Channel.convert_coordinates(wavepoint_list, rr, startLat, startLong, destLat, destLong)
        routes_lat_long.append(ll)


    #--------------------------------- FINDING OPTIMAL ROUTES BASED ON TIME ----------------------------------------

    distances = []
    for x in range(len(routes_lat_long)):
        d = 0
        for y in range(len(routes_lat_long[x]) - 1):
            d = (d + get_distance(routes_lat_long[x][y][0], routes_lat_long[x][y][1], routes_lat_long[x][y + 1][0],
                                 routes_lat_long[x][y + 1][1]))/1.852

        distances.append(d)

    time = []
    for d in distances:
        t = d / 13
        time.append(t)

    df = pd.DataFrame(list(zip(routes_lat_long, distances, time)), columns=['Route', 'Total Distance', 'Time'])
    result = df.sort_values(['Time'])

    #--------------------------------- PLOTTING THE ROUTES ----------------------------------------
    '''
    print("plotting all routes: ")
    plot_all_routes(list(result['Route'][:5]), final_coords)

    print("plotting individual routes")
    cnt = 1
    for path in routes_lat_long:
        plotRoute(path, str(cnt))
        cnt = cnt + 1 
    '''


if __name__ == '__main__':
    main()