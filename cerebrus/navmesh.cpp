#include "navmesh.h"
#include "node.h"
#include "edge.h"
#include "logger.h"

#include <fstream>
#include <sstream>
#include <exception>
#include <queue>

using namespace std;

NavMesh::NavMesh() : _file_path("")
{
}

NavMesh::~NavMesh()
{
}

bool NavMesh::load_file(const string& file_path)
{
	Logger log(this);
	log.info("load file "+file_path);
	if(_file_path!=""){
		log.error("a file has already been loaded");
		return false;
	}
	//
	ifstream ifs;
	ifs.open(file_path, ifstream::in);
	if(!ifs.is_open()){
		log.error("the file has not been open");
		return false;
	}
	//
	Node* node(0);
	while(!ifs.eof()){
		char* line=new char[128];
		ifs.getline(line,128);
		string line_s(line);
		delete line;
		//
		if(line_s!="") node=node_from_line(line_s);
		if(node) _nodes.push_back(node);
	}
	//
	ifs.close();
	//
	log.info("loaded "+std::to_string(_nodes.size())+" nodes");
	return true;
}

Node* NavMesh::node_from_line(const string& line)
{
	Node* node(0);
	Logger log(this);
	if(line==""){
		log.error("empty line");
		return node;
	}
	//
	istringstream iss(line);
	try {
		node=new Node();
		char dummy;
		float x,y,z;
		iss >> node->index >> dummy >> node->is_valid >> dummy >> x >> dummy >> y >> dummy >> z >> dummy;
		node->pos.set_x(x);
		node->pos.set_y(y);
		node->pos.set_z(z);
		int i(0);
		int idx_neighbor;
		while(!iss.eof() && i<Node::NUM_NEIGHBORS){
			iss >> idx_neighbor >> dummy;
			node->neighbors[i]=idx_neighbor;
			i++;
		}
		//log.debug("index="+std::to_string(x));
	} catch(exception& e) {
		log.exception(string(e.what()));
		delete node;
		node=0;
	}
	return node;
}

Node* NavMesh::get_node(int i)
{
	Node* n(0);
	try {
		n=_nodes[i];
	} catch(exception& e){
		Logger log(this);
		log.exception(string(e.what()),"get_node");
	}
	return n;
}


int NavMesh::find_closest_node(const LPoint3f& point)
{
	//return find_closest_node(point, _nodes);
}

/*
int NavMesh::find_closest_node(const LPoint3f& point, const std::vector<Node*>& nodes)
{
	if(nodes.size()==0){
		return -1;
	}
	//Logger log(this);
	//log.debug("point ("+std::to_string(point.get_x())+","+std::to_string(point.get_y())+","+std::to_string(point.get_z())+")");
	float distances[nodes.size()];
	float dx,dy,dz;
	for(int i=0;i<nodes.size();++i){
		Node* node=nodes[i];
		dx=point.get_x()-node->pos.get_x();
		dy=point.get_y()-node->pos.get_y();
		dz=point.get_z()-node->pos.get_z();
		if(dx==0) dx=0.0000000001;
		if(dy==0) dy=0.0000000001;
		if(dz==0) dz=0.0000000001;
		distances[i]=abs(dx*dy*dz);
		//log.debug(std::to_string(i)+"->"+std::to_string(abs(dx*dy*dz))+" ("+std::to_string(node->pos.get_x())+","+std::to_string(node->pos.get_y())+","+std::to_string(node->pos.get_z())+")("+std::to_string(dx)+","+std::to_string(dy)+","+std::to_string(dz)+")");
	}
	int idx_node(Node::INDEX_INVALID);
	float idx_min(1000000000);
	for(int i=0;i<nodes.size();++i){
		if(distances[i]<idx_min){
			idx_min=distances[i];
			idx_node=i;
			//log.debug("minimum: "+std::to_string(idx_node)+"->"+std::to_string(idx_min));
		}
	}
	return idx_node;
}
*/

void NavMesh::find_path_nodes(const LPoint3f& source, const LPoint3f& target)
{
	Logger log(this);
	stringstream ss;
	ss << source.get_x()<<"," << source.get_y()<<"," << source.get_z()<<"->" << target.get_x()<<"," << target.get_y()<<"," << target.get_z();
	log.debug("find path "+ss.str());
	//vector<Node*> path;
	//
	int idx_source=find_closest_node(source);
	if(idx_source<0) return;
	Node* sourceNode=_nodes[idx_source];
	int idx_target=find_closest_node(target);
	if(idx_target<0) return;
	Node* targetNode=_nodes[idx_target];
	// A*
	std::vector<float> GCosts(_nodes.size(),0.0);
	std::vector<float> FCosts(_nodes.size(),0.0);
	std::vector<const Edge*> spt(_nodes.size(),0);
	std::vector<const Edge*> frontier(_nodes.size(),0);
	std::priority_queue<NodeCost, std::vector<NodeCost>, NodeCostComparator> pq;
	pq.push(NodeCost(0,123));
	pq.push(NodeCost(0,43));
	pq.push(NodeCost(0,567));
	pq.push(NodeCost(0,11));
	pq.push(NodeCost(0,9));
	while(!pq.empty()){
		NodeCost nc=pq.top();
		log.debug("element with cost="+std::to_string(nc.cost));
		pq.pop();
	}
	//
	return;
}
