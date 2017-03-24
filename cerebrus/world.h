#ifndef _WORLD_H_
#define _WORLD_H_

#include "object.h"

#include <list>
#include <string>

class NavMesh;
class Character;

class World: public Object
{
public:
	GET_CLASS_NAME("World")
	World();
	virtual ~World();
	
	// navmesh
	inline NavMesh* get_nav_mesh() {return _nav_mesh;}
	
	// characters
	inline int get_num_characters() const {return _characters.size();}
	Character* get_character(int index);
	void add_character(Character* character);
	void remove_character(Character* character);
	
	// world
	void update();
	
private:
	std::list<Character*> _characters;
	NavMesh* _nav_mesh;
};

#endif
