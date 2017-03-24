#!/usr/bin/python2

from panda3d.core import *
from panda3d.egg import *
import os, os.path
import argparse
import logging

log=logging.getLogger("navmesh")

def nodeFromText(line):
    node=Node()
    parts=line.split(";")
    if len(parts)==5:
        node.index=int(parts[0])
        node.is_valid=bool(int(parts[1]))
        node.x=float(parts[2])
        node.y=float(parts[3])
        node.z=float(parts[4])
        node.neighbors=[int(x) for x in parts[5].split(",")]
    else:
        log.error("wrong text: %s"%line)
    return node

class Node:
    
    INVALID_INDEX=-1
    
    def __init__(self, vertex=None, polygons=None):
        self.is_valid=True
        #
        self.index=Node.INVALID_INDEX
        self.x=0.0
        self.y=0.0
        self.z=0.0
        self.neighbors=[] # [idx_node, ...]
        #
        if vertex!=None:
            self.index=vertex.getIndex()
            pos=vertex.getPos3()
            self.x=float(pos.getX())
            self.y=float(pos.getY())
            self.z=float(pos.getZ())
            #
            if polygon!=None:
                for polygon in polygons:
                    for i_vertex in range(polygon.getNumVertices()):
                        vertex=polygon.getVertex(i_vertex)
                        if not vertex.getIndex() in self.neighbors and vertex.getIndex()!=self.index:
                            self.neighbors.append(vertex.getIndex())
    
    def is_same_position(self, vertex):
        pos=vertex.getPos3()
        return self.x==float(pos.getX()) and self.y==float(pos.getY()) and self.z==float(pos.getZ())

    def __str__(self):
        #  index,x,y,z,[idx_neighb, ..., 7]
        return "%i;%i;%f;%f;%f;%s\n"%(node.index, 1 if node.is_valid else 0,  node.x, node.y, node.z, str(",").join([str(x) for x in node.neighbors]))


class Generator:
    
    def __init__(self, file_full_path, file_collision_path, full_mesh_name, coll_mesh_name, out_file):
        #
        self.file_full_path=file_full_path
        self.file_collision_path=file_collision_path
        self.full_mesh_name=full_mesh_name
        self.coll_mesh_name=coll_mesh_name
        self.out_file=out_file
        #
        self.vertices=[] # [EggVertex, ...]
        self.polygonsForVertex={} # {vertex_index:[EggPolygon, ...], ...}
        #
        self.nodes=[]
    
    def execute(self):
        # process full mesh
        self.processFullMeshFile()
        # process collision mesh
        self.processCollisionMeshFile()
        # write file
        self.writeFile()

    def processFile(self, file_path, mesh_name): # -> (vertex_pool, polygons)
        # open file
        fn=Filename(file_path)
        # read egg data
        log.info("read %s..."%file_path)
        egg=EggData()
        egg.read(fn)
        log.info("get mesh %s"%mesh_name)
        mesh=egg.findChild(mesh_name)
        vertex_pool=None
        polygons=[]
        for child in mesh.getChildren():
            if child.getType()==EggVertexPool:
                vertex_pool=child
            if child.getType()==EggPolygon:
                polygons.append(child)
        log.info("ok, got %i vertices and %i polygons"%(len(vertex_pool), len(polygons)))
        return (vertex_pool, polygons)

    def processFullMeshFile(self):
        log.info("Processing full mesh file:")
        vertex_pool, polygons=self.processFile(self.file_full_path, self.full_mesh_name)
        #
        log.info("sorting vertices into vertices list...")
        for vertex in vertex_pool:
            self.vertices.append(vertex)
        self.vertices.sort(key=lambda x:x.getIndex())
        #
        log.info("mapping polygons to vertices...")
        for polygon in polygons:
            for i_vertex in range(polygon.getNumVertices()):
                vertex=polygon.getVertex(i_vertex)
                if not vertex.getIndex() in self.polygonsForVertex:
                    self.polygonsForVertex[vertex.getIndex()]=[]
                self.polygonsForVertex[vertex.getIndex()].append(polygon)
        #
        log.info("generating nodes...")
        for vertex in self.vertices:
            node=Node(vertex, self.polygonsForVertex[vertex.getIndex()])
            self.nodes.append(node)
        log.info("%i nodes generated"%len(self.nodes))
    
    def processCollisionMeshFile(self):
        log.info("Processing collision mesh file:")
        cmn="%s.Coll"%self.full_mesh_name if self.coll_mesh_name==None else self.coll_mesh_name
        vertex_pool, polygons=self.processFile(self.file_collision_path, cmn)
        #
        log.info("invalidating nodes not found in collision mesh...")
        validated_count=0
        checked=[False for x in range(len(self.nodes))]
        for node in self.nodes:
            node.is_valid=False
        for vertex in vertex_pool:
            for i in range(len(self.nodes)):
                if checked[i]:
                    continue
                if self.nodes[i].is_same_position(vertex):
                    checked[i]=True
                    self.nodes[i].is_valid=True
                    validated_count+=1
        log.info("%i nodes validated"%validated_count)
    
    def writeFile(self):
        fn="navmesh.dat" if self.out_file==None else self.out_file
        if os.path.exists(fn):
            os.remove(fn)
        with open(fn, "w") as f:
            for node in self.nodes:
                f.write(str(node))
        
if __name__=="__main__":
    #
    logging.basicConfig(level=logging.DEBUG)
    #
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="file_full_path", help="the full mesh file path")
    parser.add_argument("-c", dest="file_collision_path",  required=False, help="the collision mesh file path")
    parser.add_argument("-mf", dest="full_mesh_name",  required=True, help="the name of the full mesh to use")
    parser.add_argument("-mc", dest="coll_mesh_name",  required=False, help="the name of the collision mesh to use")
    parser.add_argument("-o", dest="out_file",  required=False, help="path to output file")
    args = parser.parse_args()
    #
    gen=Generator(args.file_full_path, args.file_collision_path, args.full_mesh_name, args.coll_mesh_name, args.out_file)
    gen.execute()
