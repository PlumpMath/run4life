#include "character.h"
#include "logger.h"

using namespace std;

Character::Character()
{
}

Character::~Character()
{
	Logger(this).debug("destroying instance");
}

void Character::update()
{
	Logger log(this);
	log.info("character update","update");
}
