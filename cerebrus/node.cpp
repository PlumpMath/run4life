#include "node.h"

#include <sstream>

using namespace std;

const long Node::INDEX_INVALID(-1);
const long Node::NUM_NEIGHBORS(8);
const string Node::semicolon(";");
const string Node::comma(",");

Node::Node() : index(INDEX_INVALID), is_valid(false)
{
	for(int i=0; i<NUM_NEIGHBORS; ++i){
		neighbors[i]=INDEX_INVALID;
	}
}

Node::~Node()
{
}

string Node::to_string()
{
	ostringstream oss(std::ostringstream::ate);
	oss << index << semicolon << is_valid << semicolon << pos.get_x() << semicolon << pos.get_y() << semicolon << pos.get_z() << semicolon;
	for(int i=0; i<NUM_NEIGHBORS; ++i){
		if(neighbors[i]==INDEX_INVALID) break;
		if(i>0) oss << comma;
		oss << neighbors[i];
	}
	return oss.str();
}
