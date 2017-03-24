#ifndef _CHARACTER_H_
#define _CHARACTER_H_

#include "object.h"

class World;

class Character: public Object
{
public:
	GET_CLASS_NAME("Character")
	Character();
	virtual ~Character();
	
	void update();
	
private:
	World* _world;
};

#endif
