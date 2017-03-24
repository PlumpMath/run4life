#ifndef _NODE_H_
#define _NODE_H_

#include "object.h"
#include "lpoint3.h"

#include <string>
#include <vector>

class Node: public Object
{
public:
	GET_CLASS_NAME("Node")
	Node();
	virtual ~Node();

	static const long INDEX_INVALID;
	static const long NUM_NEIGHBORS;
	static const std::string semicolon;
	static const std::string comma;

	long index;
	bool is_valid;
	LPoint3f pos;
	long neighbors[8];

	std::string to_string();

};

#endif
