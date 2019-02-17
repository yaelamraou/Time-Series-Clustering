import numpy as np
import matplotlib.pyplot as plt
class neighboors():
    def __init__(self,Id,distance):
        self.Id = Id
        self.distance = distance

class Data_point():
    def __init__(self,Id,timeSerie,distances) :
        self.visited = 0
        self.Id = Id
        self.clust_id = None
        self.timeSerie = timeSerie
        self.distances = sorted(distances, key = lambda neigh : neigh.distance)
        #self.isCorePt = False
        self.inRange = []
        self.label = None

    def inRangeNeigh(self , eps , min_pts ) :
        cpt = 1
        for elem in self.distances :
            if (elem.distance <= eps) :
                self.inRange.append(elem)
                cpt += 1
            else :
                break
        return cpt
    
class DbCluster() : 
    def __init__(self,id) :
        self.id = id
        self.Cseries = []
    def addSerie(self , Data_point ) :
        Data_point.clust_id = self.id
        self.Cseries.append(Data_point.timeSerie)
    
#add id in dist list
class TimeSerieDbScan() :
    def __init__(self,DistMatrix,eps,min_pts):
        self.DistMatrix = DistMatrix
        self.Distances_list = []
        self.clusters = []
        self.eps = eps
        self.min_pts = min_pts
        self.DataSet = []
        self.Noise = []


    def BuildDistances (self) :
        for i in range(0,len(DistMatrix)) : 
            neigh = []
            for j in range (i+1,len(DistMatrix)) :
               neigh.append(neighboors(j,DistMatrix[i][j]))
            for j in range(0,i):
                neigh.append(neighboors(j,DistMatrix[j][i]))
            self.Distances_list.append(neigh)
        

    def  BuildDataPts(self,series):
        id = 0
        for elem in self.Distances_list :
            self.DataSet.append(Data_point(id,series[id],elem))
            id += 1

    
    def expand_cluster(self,point,clust):
        clust.addSerie(point)
        point.label = 'Clustered'
        i = 0 
        condition = i < len(point.inRange)
        while condition :
            if point.Id == 3:
                print( 'i = '  + str(i))
            p = point.inRange[i]
            if self.DataSet[p.Id].visited == False :
                
                self.DataSet[p.Id].visited = True
                if self.DataSet[p.Id].inRangeNeigh(eps,min_pts) >= min_pts : 
                    point.inRange = point.inRange + self.DataSet[p.Id].inRange
                    clust.addSerie(self.DataSet[p.Id])
            else :
                if self.DataSet[p.Id].label == 'Noise' :
                    self.DataSet[p.Id].label = 'Clustered'
                    clust.addSerie(self.DataSet[p.Id])
            i += 1
            condition = i < len(point.inRange)

    def fit(self,series) :
        self.BuildDistances()
        self.BuildDataPts(series)
        clustID = 0
        for p in self.DataSet : 
            if p.visited == False : 
                p.visited = True
                if p.inRangeNeigh(eps,min_pts) < min_pts :
                    p.label = 'Noise'
                else :
                    newClust = DbCluster(clustID)
                    self.expand_cluster(p,newClust)
                    self.clusters.append(newClust)
                    clustID +=1
        for p in self.DataSet : 
            if p.label == 'Noise' :
                self.Noise.append(self.DataSet[p.Id])
        

def log(show, data):
        if show:
            print(data)

series = np.genfromtxt("series_trace.csv",delimiter=",")
DistMatrix = np.genfromtxt("dist_matrix_trace.csv",delimiter=",")
eps = 5
min_pts = 8
model = TimeSerieDbScan(DistMatrix,eps,min_pts)
model.fit(series)
for yi in range (0,len(model.clusters)):
    for ss in model.clusters :
        print(len(ss.Cseries))
        for s in ss.Cseries :
            plt.plot(s)
        plt.show()


# for elem in model.DataSet : 
#     print('======================')
#     print(elem.Id)
#     print("##################")
#     for el in elem.inRange :
#         print (el.Id)
# for elem in model.clusters :
#     #print(elem.Cseries)'''