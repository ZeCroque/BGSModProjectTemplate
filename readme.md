[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)

# Overview

A template project for BGS modding using VSCode, with default files and integrating a release pipeline system (more info on the latter [here](https://github.com/ZeCroque/BGSModPackagingScripts)).

# Usage

1. Install [copier](https://copier.readthedocs.io/en/stable/#quick-start)
2. Run `copier https://github.com/ZeCroque/BGSModProjectTemplate.git path/to/destination`

# Generated project features

The generated project will be git initialized and will have the release pipeline scripts added as a submodule in the `CIScripts` subfolder.

A `.code_workspace` will be generated, containing the game's base script folder, the git repository root, the papyrus log folder (inside the `My Games` folder) and finally a "notepad" folder, meant to contain your TODO list and some notes (automatically created) and/or other design documents. All these folder are created/added based on the answers you gave when launching the copier command.

A `task.json` file is also created in the `.vscode` subfolder, with the following tasks:
- `Papyrus Compile` and `Papyrus Compile (Release)` will compile the scripts based on the build description in the corresponding `.ppj` file. The project also has some default code that is templated and this script will fill those templates with info from the `preset.json` file and will also change the output of the `IsAchievementFriendly()` method.
- `Format Readme` will parse the `readme.md` file inside the `ModPage` subfolder and create different texts for all platforms in the `output` subfolder. It will also update the readme at root. See the *Readme formatting* section of the pipeline scripts' readme for more info.
- `Package` will first prompt if you want to localize the plugin file and will trigger the official localization process if appropriate (more info in the *Localization Process* section of the pipeline scripts' readme). When done, you will be given the opportunity to make an archive for NexusMods, the Creations store and/or an Achievement friendly package. This process will first run the compiling tasks in release mode, then create the mod archives, then format the templated readme in the `ModPage` subfolder, and finally output a `.zip` file in the `output` folder. Here's the output zip file structure:
    - Nexus:
        - The `.esm`, `.esp` or `esl` file(s), depending on the game and the chosen mod size
        - The main `.ba2` or `.bsa` archive, depending on the game
        - Additional voice archives (for instance `ModName - Voices_fr.ba2`) if you chose to localize the voices (only Starfield/FO4) and even an alternative `_NO_AI` archive file if you added AI/spliced voices to your project and want to add this option to your FOMOD. See the *Optional files* section of the pipeline scripts' readme for more info.
        - The "readme.md" file
        - A "FOMOD" folder if there's one in the project repository
        - The thumbnail image if there's an image named `ShortName_Thumbnail.png` in the project repository, meant to be used by the FOMOD mainly
    - Creations:
        - The `.esm`, `.esp` or `esl` file(s), depending on the game and the chosen mod size
        - The main `.ba2` or `.bsa` archives, depending on the game (for PC, Xbox and PC) 
    - Achievement-Friendly:
        - Same as the above but with the appropriate compilation option.
    
    The files generated for the Creations platform are also copied to the main `./Data` folder for uploading with the CK (because that folder is integrated with MO2, see below). The archives for the Creation platform are meant for testing purpose, because the archives in the mod working folder are otherwise superseded by the spare files.
- `Add Strings to achlist` will append the string files for every supported languages to the `modShortName_Main.achlist` file.
- For Skyrim only, `Generate SEQ` will generate the SEQ file required to make quests start on load

You will also find a `build.py` file that simply runs the `Package` task.

A `extensions.json` file is also created in the `.vscode` subfolder, to help you use the proper extensions for each games via recommendations.

There's some starting content as well, here's a list:
- A basic `.esp` plugin containing an update quest with the appropriate update script attached, relying on the `buildCode` field of the `preset.json` file to trigger mod updating logic if needed. For Starfield only, there's also a templated gameplay option group containing a `Mod Version` gameplay option.
- Some basic scripts in a `modShortName` namespace
    - The quest script for the updating logic
    - An utility global script: `modShortName:Utility:ModInfo` which return the `buildCode` and has the `IsAchievementFriendly()` predicate
    - For Skyrim there's also a default `.seq` file to make the update quest start upon loading

If you indicated your mod will contain voices, the `Data/Sound/Voice/ModName.esp` folder will be created, along with a folder junction pointing to it named `Data/Sound/Voice/ModName.esm` for Starfield or  `Data/Sound/Voice/ModName.esl` elsewise (if you chose the "small" mod size).

For Starfield, a folder junction to the `Data/Scripts/Source` folder is also created in the game base script folder to make sure the official Papyrus extensions works properly.

Finally, there's also a GPL3 license file and a basic `.gitignore` file.

# MO2 Integration

This template relies on MO2 to setup a proper workflow without dirtying the game folder. It requires that the mod instance that manages you game have a `ZZZ_Dev` profile, with no mods activated or only development ones (script extender plugins...). That profile will be duplicated to create a new `ZZZ_ModName` profile that activates a mod named `ModNameWIP`, which is in fact a folder junction to your repository's `Data` subfolder. The profile will also redirect the output of the `Creation Kit`, `SF1Edit`/`FO4Edit`/`SSEEdit` and `xTranslator` shortcuts to that "mod" instead of the default `overwrite` folder.

MO2 is also used to run some tasks of the packaging scripts. (localization, SEQ generation) 

