#include "world.h"
#include "character.h"
#include "navmesh.h"
#include "logger.h"

#include <iostream>

using namespace std;

World::World()
{
	_nav_mesh=new NavMesh();
}

World::~World()
{
	Logger log(this);
	log.debug("destroying instance");
	//
	log.info("deleting navmesh...");
	delete _nav_mesh;
	//
	log.info("deleting characters...");
	for(std::list<Character*>::iterator _character=_characters.begin(); _character!=_characters.end(); ++_character){
		delete (*_character);
	}
}

//
Character* World::get_character(int index)
{
	if(index<0 || index>=_characters.size()){
		return 0;
	}
}

void World::add_character(Character* character)
{
	Logger log(this);
	if(character==0){
		log.error("trying to add a null pointer to a character");
		return;
	}
	log.info("add character and taking onwership; id="+std::to_string(character->getId()));
	for(std::list<Character*>::iterator _character=_characters.begin(); _character!=_characters.end(); ++_character){
		if((*_character)->getId()==character->getId()){
			log.warning("character already added");
			return;
		}
	}
	_characters.push_back(character);
}

void World::remove_character(Character* character)
{
	Logger log(this);
	if(character==0){
		log.error("trying to remove a null pointer to a character");
		return;
	}
	log.info("remove character id="+std::to_string(character->getId()));
	_characters.remove(character);
}

//
void World::update()
{
	for(std::list<Character*>::iterator character=_characters.begin(); character!=_characters.end(); ++character){
		(*character)->update();
	}
}
