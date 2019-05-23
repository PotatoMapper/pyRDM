#!/usr/bin/python
import numpy, sys
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from Utilities.TSP_Solver import solve_tsp


class TSP(object):

        def __init__(self, data):
                self.points = data
                self.tour = [i for i in range(len(self.points))]
                self.array = numpy.zeros((len(self.points),len(self.points)))

                for i in range(len(self.points)):
                        for j in range(len(self.points)):
                                self.array[i][j] = numpy.linalg.norm(numpy.subtract(self.points[i],self.points[j]))

        def Solve(self):

                self.tour = solve_tsp(self.array)

                self.sorted = []
                
                for i in self.tour:
                        lat = self.points[i][0]
                        lon = self.points[i][1]
                        ### Format The output to return it easy to the Instance() model to be easily written back in proper format to push back to DB
                        out = {'lat': lat, 'lon': lon }
                        self.sorted.append(out)

                return(self.sorted)

        def Plot(self):
                plt.plot([self.points[self.tour[i]][0] for i in range(len(self.points))], [self.points[self.tour[i]][1] for i in range(len(self.points))], 'xb-')
                plt.show()

### Leaving until I remember the damn format of this stupid shit
"""                        
{'max_level': 10, 'timezone_offset': 0, 'min_level': 1, 'area': [{'lat': 42.5969728664992, 'lon': -82.8127105516635}, {'lat': 42.5804426349319, 'lon': -82.810670085777}, {'lat': 42.5759537567604, 'lon': -82.8267410337183}, {'lat': 42.5673097522189, 'lon': -82.8393044763456}, {'lat': 42.5700155689156, 'lon': -82.8535877375514}, {'lat': 42.5541840061774, 'lon': -82.8544922820319}, {'lat': 42.5499427999898, 'lon': -82.8707618092491}, {'lat': 42.5447043172567, 'lon': -82.8925934950029}, {'lat': 42.5382220790348, 'lon': -82.910349193095}, {'lat': 42.5498461678989, 'lon': -82.9154378879462}, {'lat': 42.5369153392913, 'lon': -82.9572249758108}, {'lat': 42.5476644076677, 'lon': -82.9287423563501}, {'lat': 42.551343028435, 'lon': -82.9464164615765}, {'lat': 42.5534924933519, 'lon': -82.9627167558462}, {'lat': 42.5380638103512, 'lon': -82.9883805140627}, {'lat': 42.5513181383085, 'lon': -82.9873086270571}, {'lat': 42.5650987227546, 'lon': -82.981474837529}, {'lat': 42.5768582904225, 'lon': -82.9868946110187}, {'lat': 42.5872213754188, 'lon': -82.9916989082771}, {'lat': 42.5715499356101, 'lon': -82.9517771019881}, {'lat': 42.5992172904815, 'lon': -82.954730760593}, {'lat': 42.5841952774468, 'lon': -82.9510847232493}, {'lat': 42.5903481119295, 'lon': -82.9336456182833}, {'lat': 42.5989201121945, 'lon': -82.9376333322497}, {'lat': 42.6061752214264, 'lon': -82.9768515324492}, {'lat': 42.5917719193886, 'lon': -82.9746039398584}, {'lat': 42.6238401967956, 'lon': -82.9900647084419}, {'lat': 42.627523838725, 'lon': -82.9673924167222}, {'lat': 42.6251243423307, 'lon': -82.9502342122278}, {'lat': 42.6133950196915, 'lon': -82.9462054744}, {'lat': 42.5672969074654, 'lon': -82.9079957915006}, {'lat': 42.5607061548848, 'lon': -82.8970303042855}, {'lat': 42.5706983137954, 'lon': -82.8857762516172}, {'lat': 42.573674392182, 'lon': -82.8699051517006}, {'lat': 42.5847013009693, 'lon': -82.8499741627105}, {'lat': 42.5898019171077, 'lon': -82.8684423517044}, {'lat': 42.5892374163299, 'lon': -82.8823089529425}, {'lat': 42.5962501455701, 'lon': -82.9030856655607}, {'lat': 42.5992250044347, 'lon': -82.887214565644}, {'lat': 42.6021130133964, 'lon': -82.8722344266455}, {'lat': 42.6109637765472, 'lon': -82.8861855511661}, {'lat': 42.6097086583914, 'lon': -82.8700452068597}, {'lat': 42.6208612371415, 'lon': -82.8534526933104}, {'lat': 42.6272332425453, 'lon': -82.8722094477574}, {'lat': 42.6251978831257, 'lon': -82.8944133356276}, {'lat': 42.5447507121428, 'lon': -82.8561728215065}]}
"""
