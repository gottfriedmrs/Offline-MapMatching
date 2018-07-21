from qgis.analysis import *
from qgis.core import *

class Network:
    
    def __init__(self, linestring_layer):
        self.vector_layer = linestring_layer
    
    def routing(self, start, end):
        #create director and strategy
        director = QgsVectorLayerDirector(self.vector_layer, -1, '', '', '', 2)
        strategy = QgsNetworkDistanceStrategy()
        director.addStrategy(strategy)
        
        #buildiung the graph
        builder = QgsGraphBuilder(self.vector_layer.sourceCrs())
        tied_points = director.makeGraph(builder, [start, end])
        graph = builder.graph()
        start_id = graph.findVertex(tied_points[0])
        end_id = graph.findVertex(tied_points[1])
        
        #start routing
        (tree, cost) = QgsGraphAnalyzer.dijkstra(graph, start_id, 0)
        if tree[end_id] == -1:
            return -1
        else:
            points = {}
            cur_pos = end_id
            
            while cur_pos != start_id:
                #extract the indices and points of the current edge
                from_vertex_id = str(graph.edge(tree[cur_pos]).fromVertex())
                from_vertex_point = graph.vertex(graph.edge(tree[cur_pos]).fromVertex()).point()
                to_vertex_id = str(graph.edge(tree[cur_pos]).toVertex())
                to_vertex_point = graph.vertex(graph.edge(tree[cur_pos]).toVertex()).point()
                
                #add the extracted information to the dictionary
                points.update({from_vertex_id : from_vertex_point})
                points.update({to_vertex_id : to_vertex_point})
                
                #set the cur_pos for the next loop
                if cur_pos != graph.edge(tree[cur_pos]).toVertex():
                    cur_pos = graph.edge(tree[cur_pos]).toVertex()
                else:
                    cur_pos = graph.edge(tree[cur_pos]).fromVertex()
        
            #return the values of the dictionary only
            return list(points.values())
    
    def distanceOnNetwork(self, start, end):
        #get all vertices from the routing result
        vertices = self.routing(start, end)
        
        #points == -1, if routing was not possible
        if vertices == -1:
            print(start)
            print(end)
            return vertices
        else:
            distance = 0
            for i, vertex in enumerate(vertices):
                
                #get the distance between the current vertice and the next vertice
                if len(vertices) > (i + 1):
                    distance = distance + vertex.distance(vertices[i + 1].x(), vertices[i + 1].y())
                else:
                    return distance
            return distance
    
