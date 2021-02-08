// Initial By UE4ModuleCreator.
using UnrealBuildTool;
public class {ModuleName} : ModuleRules
{
	public {ModuleName}(ReadOnlyTargetRules Target): base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
		
		//---------------------------------------------------------------------
		//对UnrealEngine的依赖
		PublicDependencyModuleNames.AddRange(new string[]{
			"Core",
			"Engine",
			"CoreUObject"
		});

		PrivateDependencyModuleNames.AddRange(new string[]{

        });
		//---------------------------------------------------------------------

		//---------------------------------------------------------------------
		//对Foundations/GPFramework/DFMGameCore的依赖
		//---------------------------------------------------------------------
		PublicDependencyModuleNames.AddRange(new string[]{
			"GameCore"
		});

		PrivateDependencyModuleNames.AddRange(new string[]{

        });
		//---------------------------------------------------------------------

		//---------------------------------------------------------------------
		//！！！不要包含其它模块的路径！！！
		//---------------------------------------------------------------------
		PublicIncludePaths.AddRange(new string[]{"{ModuleDirectory}/Public"});
		PrivateIncludePaths.AddRange(new string[]{"{ModuleDirectory}/Private"});
		//---------------------------------------------------------------------


		//---------------------------------------------------------------------
		//如果这个模块原本不是Editor模块，但是【不得不】用到一些Ed的特性，需要单独增加Ed的依赖
		if (Target.Type == TargetRules.TargetType.Editor)
		{
			PrivateDependencyModuleNames.Add("UnrealEd");
            PrivateDependencyModuleNames.Add("ApplicationCore");
		}
	}
}
