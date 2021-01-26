#--------------Code for performing visualization operations like Plotting route on GMAP, basemap etc

import gmplot
# from mpl_toolkits.basemap import Basemap

# ----------------------------Graph (Mesh) and Wavepoint data visualization functions------------------------------------

def printGraph(g):
    print('Graph data:')
    for v in g:
        print(v)
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print(v.get_weight(w))
        print("\n")
    print('*****************************************************************************')


def printWavepoints(wavepoint_list):
    print(type(wavepoint_list))
    for i in range(len(wavepoint_list)):
        print(i, "\t", wavepoint_list[i], "\n")
        '''
        for j in range(len(wavepoint_list[i])):
            print(wavepoint_list[i][j][0])
        '''
    print('*****************************************************************************')

def printPath(path):
    for i in range(len(path)):
        if not (i == len(path) - 1):
            print(str(i)+'.\t',path[i],'\t->','\n')
        else:
            print(str(i)+'.\t', path[i], '\t', '\n')

    print('*****************************************************************************')
#--------------------------------------------------------------------------

def plotRoute(path_list):
    gmap3 = gmplot.GoogleMapPlotter(path_list[0][0], path_list[0][1], 13)
    latitude_list = []
    longitude_list = []

    for i in range(len(path_list)):
        latitude_list.append(path_list[i][0])
        longitude_list.append(path_list[i][1])

    gmap3.scatter(latitude_list, longitude_list, '# FF0000', size=40, marker=False)

    # Plot method Draw a line in
    # between given coordinates
    gmap3.plot(latitude_list, longitude_list, 'cornflowerblue', edge_width=2.5)

    gmap3.draw("Results/plotted_path.html")

#-----------------------------------------------------------------------------
# def plot_basemap(wavepoint_list):
#     lat = []
#     lon = []
#
#     # Code for extracting and plotting all the wavepoints:
#
#     for i in range(len(wavepoint_list)):
#         for j in range(len(wavepoint_list[i])):
#             # print(wavepoint_list[i][j][0],wavepoint_list[i][j][1])
#             lat.append(wavepoint_list[i][j][0])
#             lon.append(wavepoint_list[i][j][1])
#
#     # 2. scatter city data, with color reflecting population
#     # and size reflecting area
#     m = Basemap(projection='hammer', lon_0=180)
#     x, y = m(lon, lat)
#     m.drawmapboundary(fill_color='#99ffff')
#     m.fillcontinents(color='#cc9966', lake_color='#99ffff')
#     m.scatter(x, y, 3, marker='o', color='k')
#     plt.title('OUR VERY OWN WAVEPOINTS')
#     plt.show()
