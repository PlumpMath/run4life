#include "object.h"
#include "logger.h"

using namespace std;

int Object::_idCounter(0);

Object::Object()
{
	_idCounter++;
	_id=_idCounter;
}

Object::~Object()
{
}
