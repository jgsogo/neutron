// CrossPlatformService.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

#include "Poco/Util/ServerApplication.h"

class MyServerApplication : public Poco::Util::ServerApplication {
	public:

};

int main(int argc, char** argv)
{
	MyServerApplication app;
	return app.run(argc, argv);
}

