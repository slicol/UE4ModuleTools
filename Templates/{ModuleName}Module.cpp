// Initial By UE4ModuleCreator.
#include "{ModuleName}Module.h"

DEFINE_LOG_CATEGORY_STATIC(Log{ModuleName}, Log, All);

class F{ModuleName}Module : public I{ModuleName}Module
{
public:
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;

public:
	//-----------------------------------------------------------------------------
	//需要暴露给外部的API的实现

};
//-----------------------------------------------------------------------------
IMPLEMENT_GAME_MODULE(F{ModuleName}Module, {ModuleName});
//-----------------------------------------------------------------------------


//-----------------------------------------------------------------------------
void F{ModuleName}Module::StartupModule()
{
	//TODO
}

void F{ModuleName}Module::ShutdownModule()
{
	//TODO
}


//-----------------------------------------------------------------------------
//需要暴露给外部的API的实现
//TODO
