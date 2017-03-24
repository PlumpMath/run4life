#ifndef _NAVMESH_H_
#define _NAVMESH_H_

#include "object.h"
#include "lpoint3.h"
#include "node.h"

#include <vector>
#include <string>

class A: public std::vector<int>
{
};

class NavMesh: public Object
{
public:
	GET_CLASS_NAME("NavMesh")
	NavMesh();
	virtual ~NavMesh();

	bool load_file(const std::string& file_path);

	inline void doA(std::vector<int> a) {}

	Node* node_from_line(const std::string& line);
	
	const int get_num_nodes() const {return _nodes.size();}
	Node* get_node(int i);
	
	int find_closest_node(const LPoint3f& point);
	//int find_closest_node(const LPoint3f& point, const std::vector<Node*>& nodes);
	
	void find_path_nodes(const LPoint3f& source, const LPoint3f& target);

private:
	std::string _file_path;
	std::vector<Node*> _nodes;

private:
	class NodeCost
	{
	public:
		NodeCost(const int& node_index, const float& cost) : node_index(node_index), cost(cost) {}
		int node_index;
		float cost;
	};
	class NodeCostComparator
	{
	public:
		inline bool operator () (NodeCost& n1, NodeCost& n2) {return n1.cost>n2.cost;}
	};
};
	
#endif
