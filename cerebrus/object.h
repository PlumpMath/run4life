#ifndef _OBJECT_H_
#define _OBJECT_H_

#include <string>

#define GET_CLASS_NAME(NAME) const std::string getClassName() {return std::string(NAME);}

class Object
{
public:
	virtual const std::string getClassName() = 0;

private:
	static int _idCounter;
	
protected:
	Object();
	virtual ~Object();

public:
	inline int getId() const {return _id;}
	
private:
	int _id;
};
	
#endif
