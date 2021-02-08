// Initial By UE4ModuleCreator.
#pragma once
#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"
#include "Modules/ModuleInterface.h"

//该模块对外的公共接口
class I{ModuleName}Module : public IModuleInterface
{
public:
	//-----------------------------------------------------------------------------
	//需要暴露给外部的API定义


	//-----------------------------------------------------------------------------
public:
	//-----------------------------------------------------------------------------
	//一个模块只有一个实例，是很天然的单例，可以封装一个友好的获取方式
	//但是依然要注意，有可能在当作单例使用时，模块还未加载。（当然一般情况是不会出这种问题）
	//-----------------------------------------------------------------------------
	static inline I{ModuleName}Module& Get()
	{
		return FModuleManager::LoadModuleChecked< I{ModuleName}Module >( "{ModuleName}" );
	}
	//-----------------------------------------------------------------------------
	//当你使用单例时，如果不确定模块是否被加载，需要进行一次判定。（当然一般情况都是加载的）
	//-----------------------------------------------------------------------------
	static inline bool IsAvailable()
	{
		return FModuleManager::Get().IsModuleLoaded( "{ModuleName}" );
	}
};

