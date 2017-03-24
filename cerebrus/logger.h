#ifndef _LOGGER_H_
#define _LOGGER_H_

#include <iostream>

class Object;

class Logger
{
public:
	Logger(Object* owner=0);
	~Logger();
	
	void debug(const std::string& message, const std::string& function="");
	void info(const std::string& message, const std::string& function="");
	void warning(const std::string& message, const std::string& function="");
	void error(const std::string& message, const std::string& function="");
	void exception(const std::string& message, const std::string& function="");

private:
	void _message(const std::string& type, const std::string& message, const std::string& function);
	
private:
	Object* _owner;
};

#endif
