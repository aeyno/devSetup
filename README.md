```
  __                     __            __                      
 /\ \                   /\ \_         /\ \__                   
 \_\ \     __   __  __  \/'__`\     __\ \ ,_\  __  __  _____   
 /'_` \  /'__`\/\ \/\ \ /\ \_\_\  /'__`\ \ \/ /\ \/\ \/\ '__`\ 
/\ \L\ \/\  __/\ \ \_/ |\ \____ \/\  __/\ \ \_\ \ \_\ \ \ \L\ \
\ \___,_\ \____\\ \___/  \/\ \_\ \ \____\\ \__\\ \____/\ \ ,__/
 \/__,_ /\/____/ \/__/    \ `\_ _/\/____/ \/__/ \/___/  \ \ \/ 
                           `\_/\_\                       \ \_\ 
                              \/_/                        \/_/ 
```

**dev$etup** is a simple CLI tool to automatically install all your developpement environnement on a new linux environnement by installing Aptitude or Pacman packages, Snap packages, your custom config files and also your VScode extensions if you use it.

## Installation
Make sur to have python 3 and download  **devsetup.py**

## Usage

Lauching the tool in interactive mode (In this mode you can type your commands without exiting the program) :
```
python3 devsetup.py
```

You can also type directly your command after the name of the file. In this mode the program will quit after the command is executed. Example for the commmand "install config":
```
python3 devsetup install config
```

## How it works ?

### Packages
You can use **dev$etup** to install a specific package list automaticaly using aptitude or pacman depending on your Linux Distro. The package list is stored in *Profiles/[ProfileName]/packages.txt* (one package per line, the lines beginning with # are ignored) or *Profiles/[ProfileName]/SnapPackages.txt* (for the Snap packages).
For instance to install the packages from the profile *profile1* using Aptitude:
```
> install packages aptitude profile1
```
**dev$etup** also supports Pacman and Snap

You can exports all the packages installed with your package manager to have a backup. eg: to backup all your Snap packages to your profile *Default*:
```
> save packages Snap Default
```

To add a package to the list:
```
> add package packageName profileName
```

To remove a package from the list:
```
> remove package packageName profileName
```

### Configuration files
You can use **dev$etup** to install your custom configuration files. The configuration files are stored in *Profiles/[ProfileName]/config/* and their installation paths in *Profiles/[ProfileName]/configFiles.txt* (one package per line with the following formatting: `filename:$HOME/path/to/install/file` the lines beginning with # are ignored) or *Profiles/[ProfileName]/SnapPackages.txt* (for the Snap packages).

To install all your config files from the profile *Profile1*:
```
> install config Profile1
```

To backup all your config files from your system to a profile:
```
> save config profileName
```

### Profiles
The profile system allows you to organise your packages/config/VS Extensions list in differents categories. For example your can create a `dev` profile for your developement tools, a `dotfiles` profile to store your configuration files for your window manager, a `backup` profile to backup your package list and config files everyday using for example a cron task...

To add a profile:
```
> add profile profileName
```
To remove a profile:
```
> remove profile profileName
```

In interactive mode the current profile is always the last used since you've lauched the CLI. If your are not using the interactive mode you need to always give the profile you want to use at the end of the command else it will use the `default` profile.

## Exhaustive command list 
```
cli commands
│
└───install
│   │
|   └───all [profileName] : install packages, config, zip and VSexts from the current profile
|   |
|   └───packages
|   |   |
|   |   └───aptitude [profileName] : install the packages list from the current profile using aptitude
|   |   |
|   |   └───pacman [profileName] : install the packages list from the current profile using pacman
|   |   |
|   |   └───snap [profileName] : install the snap packages from the current profile
|   |   |
|   |   └───auto [profileName] : let the tool decide whether to install the packages from the current profile with aptitude or pacman
|   |
|   └───config [profileName] : copy the config files from the current profile to their path
|   |
|   └───zip [profileName] : extract the zip files from the current profile to their path
|   |
|   └───VSexts [profileName] : install the VS Code extensions for the current user
|
└───save
│   |
|   └───packages
|   |   |
|   |   └───aptitude [merge] [profileName] : export the packages currently installed with aptitude to the current profile
|   |   |
|   |   └───pacman [merge] [profileName] : export the packages currently installed with pacman to the current profile
|   |   |
|   |   └───snap [merge] [profileName] : export the packages currently installed with snap to the current profile
|   |
|   └───config [profileName] : backup the config files to the current profile
|   |
|   └───VSexts [merge] [profileName] : export the VS Code extensions to the current profile
│   
└───add
│   |
|   └───package packageName [profileName] : add package packageName to the packages list
|   |
|   └───snap packageName [profileName] : add package packageName to the snap packages list
|   |
|   └───zip fileName extractionPath [profileName] : add the zip file fileName in the zip folder of the current profile and give its extraction path
|   |
|   └───config fileName location [profileName] : add the config file fileName to the current profile (use "save config" to backup the file)
|   |
|   └───VSexts extensionName [profileName] : add the extension extensionName to the current profile
|   |
|   └───profile profileName : create a new profile with name profileName
│   
└───remove
│   |
|   └───package packageName [profileName] : remove the package packageName from the current profile
|   |
|   └───snap packageName [profileName] : remove the snap package packageName from the current profile
|   |
|   └───zip fileName [profileName] : remove the zip fileName from the current profile
|   |
|   └───config fileName [profileName] : remove config file fileName from current profile
|   |
|   └───VSexts extensionName [profileName] : remove extensionName from current profile
|   |
|   └───profile profileName : remove the profile profileName
│   
└───help : show the help
│   
└───exit : exit the CLI
```
