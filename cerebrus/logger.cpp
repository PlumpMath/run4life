#include "logger.h"
#include "object.h"

using namespace std;

Logger::Logger(Object* owner) : _owner(owner)
{
}

Logger::~Logger()
{
}

void Logger::debug(const std::string& message, const std::string& function)
{
	_message("DEBUG",message,function);
}

void Logger::info(const std::string& message, const std::string& function)
{
	_message("INFO",message,function);
}

void Logger::warning(const std::string& message, const std::string& function)
{
	_message("WARNING",message,function);
}

void Logger::error(const std::string& message, const std::string& function)
{
	_message("ERROR",message,function);
}

void Logger::exception(const std::string& message, const std::string& function)
{
	_message("EXCEPTION",message,function);
}

void Logger::_message(const std::string& type, const std::string& message, const std::string& function)
{
	std::string msg;
	//
	msg="Cerebrus|";
	msg+=type;
	msg+="|";
	//
	if(_owner){
		msg+=_owner->getClassName();
		msg+="[";
		msg+=std::to_string(_owner->getId());
		msg+="]";
	} else {
		msg+="Logger[]";
	}
	//
	if(function!=""){
		msg+=".";
		msg+=function;
		msg+="():";
	}
	//
	msg+=" ";
	msg+=message;
	//
	std::cout << msg << std::endl;
}
