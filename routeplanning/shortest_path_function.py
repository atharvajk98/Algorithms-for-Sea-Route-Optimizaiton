#_____This code contains all the logic behind returning the shortest path from a given graph____________

from shortest_path_algorithm import Channel
import sys

#----------------Generalised Shortest Path function based on DISTANCE ONLY------------------------------------------------
def shortestDistance(graph, s, e):
    g = Channel.Graph()
    g = graph
    start = g.get_vertex(s)
    end = g.get_vertex(e)
    path = []
    total_distance = 0
    flag = 0
    index = ''
    curr = start

    # print(start,"\n",end,"\n")
    path.append(s)

    while (flag != 1):
        min_dist = sys.maxsize
        print("Current Vertex: ",curr.get_id())

        if (curr.get_id() == end.get_id() or curr.get_id() == '1000,0'):
            flag = 1
            break

        for vertex in curr.get_connections():
            currid = curr.get_id().split(',')
            vertexid = vertex.get_id().split(',')
            print("Accesing : ",vertexid)

            if (currid[0] == vertexid[0]  or int(vertexid[0]) < int(currid[0])):
                continue
            else:
                dist = curr.get_weight(vertex)
                if (dist < min_dist):
                    min_dist = dist
                    index = vertex.get_id()

        print("Next Vertex = ",index)
        path.append(index)
        total_distance += min_dist
        curr = g.get_vertex(index)

    return path, (total_distance)



# -------------------------------------------FUNCTION TO GET ALL POSSIBLE ROUTES-------------------------------------

def get_all_routes(graph, s, e, route_len, num_interval):
    routes = []
    g = Channel.Graph()
    g = graph
    start = g.get_vertex(s)
    end = g.get_vertex(e)
    cnt = 0

    exit_flag = True
    counter = 0

    #--------------- ITERATING THROUGH THIS WHILE LOOP TO COMPUTE TILL ALL THE PATHS ARE COMPUTED -------------------
    # NOTE: total no of possible routes will me the multiplication of the totla no. of waypoints present in each boundary level

    while(exit_flag):
    #for i in range(0, 81):
        path = []
        flag = True
        current = start
        path.append(s)

        #------------------------------------FINDING NEW PATH-----------------------------------------------------
        #print("\n==========================================================================================\nNEW PATH\n")
        while (flag):

            for v in current.get_connections():
                current_id = current.get_id().split(',')
                v_id = v.get_id().split(',')

                if current_id[0] == v_id[0] or int(current_id[0]) > int(v_id[0]):
                    #print("Not included...as the node is behind ...", v_id)
                    continue

                if int(current_id[0]) < int(v_id[0]) and v.get_visited() == True:
                    #print("Not included...as the node is already visited ...", v_id)
                    continue

                else:
                    #print("\nnot visited ...so included in the path..., ", v.get_id())
                    prev = g.get_vertex(current.get_id())
                    current = g.get_vertex(v.get_id())
                    break

            #print("Exited for loop..")
            #print("\n\nPrevious Node: ", prev)
            next_node = current.get_id()
            #print("Current Node: ", current)
            path.append(next_node)
            current.set_previous(prev)

            #------AT LAST NODE--------------
            if current.get_id().split(',')[0] == '1000':
                #print("end encountered...")
                prev.set_visited()
                #print("Visited: ", prev.get_id())
                cnt = cnt + 1
                routes.append(path)
                #print("route " + str(i) + ": ", path)
                #print("route " + str(counter) + ": ", path)
                counter = counter + 1
                flag = False

                if num_interval == cnt:
                    #print("\n....................................TIME TO VISIT NEW NODES....................................\n")
                    cnt = 0

                    flag1 = True
                    middle = 0
                    head = end
                    #print("Head Node: ", head)
                    while(flag1):
                        head_id = head.get_id().split(",")
                        for h in head.get_connections():
                            h_id = h.get_id().split(",")

                            if int(h_id[0]) > int(head_id[0]) or h_id[0] == head_id[0]:
                                #print("Node is not considered: ", h_id)
                                continue

                            if int(h_id[0]) < int(head_id[0]) and h.get_visited() == True:
                                #print("Visited Node found: ", h_id)

                                level_length = len(h.get_same_level())
                                #print("Level length is: ", level_length)

                                if level_length == 1:
                                    break

                                for sl in h.get_same_level():

                                    if level_length == 1:
                                        break

                                    if sl.get_visited() == True:
                                        #print("Visited Node found: ", sl.get_id())
                                        level_length = level_length - 1
                                        #print("Level length is: ", level_length)
                                        continue
                                    else:
                                        #print("Unvisited Node found: ", sl.get_id())
                                        flag1 = False
                                        middle = 1
                                        break

                                break

                            if int(h_id[0]) < int(head_id[0]) and h.get_visited() == False:
                                #print("Unvisited Node found: ", h_id)
                                flag1 = False
                                break

                        if flag1 == False:
                            if middle == 1:
                                to_visit = sl
                                middle = 0
                            else:
                                to_visit = h
                            break

                        head = h
                        #print("Head Node: ", head)

                    #print("\nNode to be set as visited: ", to_visit.get_id())
                    head = None
                    head_id = None
                    h = None
                    h_id = None

                    #print("\n---------------------------------- UNVISITING APPROPRIATE NODES ----------------------------------\n")
                    flag2 = True
                    head = to_visit
                    #print("New Node: ", head)

                    while (flag2):
                        head_id = head.get_id().split(",")
                        for h in head.get_connections():
                            h_id = h.get_id().split(",")

                            if h_id[0] == '1000':
                                #print("End encountered: ", h_id)
                                flag2 = False
                                break

                            if int(h_id[0]) < int(head_id[0]):
                                continue

                            else:
                                h.set_unvisited()
                                #print("Univisited: ", h_id)

                        if flag2 == False:
                            break

                        head = h

                    to_visit.set_visited()
                    #print("Finally Visited: ", to_visit.get_id())
                    #print("\n-------------------------------------------------------------------------------\n\n")


                    if to_visit.get_id().split(",")[0] == '-1':
                        exit_flag = False
                        return g, routes
                        break

    return g, routes
