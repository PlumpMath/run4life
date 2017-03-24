#ifndef _EDGE_H_
#define _EDGE_H_

#include "object.h"

class Edge: public Object
{
public:
	Edge(const int& index_source, const int& index_target);
	virtual ~Edge();
	
	int index_source;
	int index_target;
	
};

#endif
