// Initial By UE4ModuleCreator.
using UnrealBuildTool;
using Tools.DotNETCommon;
using System.Collections.Generic;

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


	//如果你的模块有分层的概念，你有可能需要获取指定层的所有模块名
 	public List<string> GetModuleNamesOfLayer(string LayerName)
    {
        string Path = this.Target.ProjectFile.Directory.FullName + "/Source/" + LayerName;
        System.IO.DirectoryInfo DirInfo = new System.IO.DirectoryInfo(Path);
        System.IO.DirectoryInfo[] SubDirInfos = DirInfo.GetDirectories();

        List<string> Result = new List<string>();
        for (int i = 0; i < SubDirInfos.Length; ++i)
        {
            Result.Add(SubDirInfos[i].Name);
        }
        return Result;
    }

}
