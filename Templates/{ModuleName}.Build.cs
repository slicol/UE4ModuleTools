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
		//对游戏模块的依赖
		//---------------------------------------------------------------------
		PublicDependencyModuleNames.AddRange(new string[]{
		});

		PrivateDependencyModuleNames.AddRange(new string[]{

        });
		//---------------------------------------------------------------------

		//---------------------------------------------------------------------
		//！！！不要包含其它模块的路径！！！
		//---------------------------------------------------------------------
		PublicIncludePaths.AddRange(new string[]
		{
			ModuleDirectory,
			ModuleDirectory + "/Public",
		});
		PrivateIncludePaths.AddRange(new string[]
		{
			ModuleDirectory + "/Private",
		});
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
    public System.Collections.Generic.List<string> GetModuleNamesOfLayer(string LayerName, string Excludes = "")
    {
        string LayerPath = "";
        //LayerPath = this.Target.ProjectFile.Directory.FullName + "/Source/" + LayerName;

        Tools.DotNETCommon.FileReference ProjectFile = null;
        System.Reflection.FieldInfo info = this.GetType().GetField("ProjectFile");
        if (info == null)
        {
            var Target = this.GetType().GetField("Target").GetValue(this);
            System.Reflection.PropertyInfo pinfo = Target.GetType().GetProperty("ProjectFile");
            ProjectFile = pinfo.GetValue(Target) as Tools.DotNETCommon.FileReference;
        }
        else
        {
            ProjectFile = info.GetValue(this) as Tools.DotNETCommon.FileReference;
        }
        LayerPath = ProjectFile.Directory.FullName + "/Source/" + LayerName;
        System.IO.DirectoryInfo DirInfo = new System.IO.DirectoryInfo(LayerPath);
        System.IO.DirectoryInfo[] SubDirInfos = DirInfo.GetDirectories();

        System.Collections.Generic.List<string> Result = new System.Collections.Generic.List<string>();
        for (int i = 0; i < SubDirInfos.Length; ++i)
        {
            string Item = SubDirInfos[i].Name;
            if (!Excludes.Contains(Item) && Item != this.Name)
            {
                Result.Add(Item);
            }
        }
        return Result;
    }

}
