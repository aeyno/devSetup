```  __                     __            __                      
 /\ \                   /\ \_         /\ \__                   
 \_\ \     __   __  __  \/'__`\     __\ \ ,_\  __  __  _____   
 /'_` \  /'__`\/\ \/\ \ /\ \_\_\  /'__`\ \ \/ /\ \/\ \/\ '__`\ 
/\ \L\ \/\  __/\ \ \_/ |\ \____ \/\  __/\ \ \_\ \ \_\ \ \ \L\ \
\ \___,_\ \____\\ \___/  \/\ \_\ \ \____\\ \__\\ \____/\ \ ,__/
 \/__,_ /\/____/ \/__/    \ `\_ _/\/____/ \/__/ \/___/  \ \ \/ 
                           `\_/\_\                       \ \_\ 
                              \/_/                        \/_/ ```

dev$etup is a simple script to automatically install all your developpement environnement on a new linux environnement by installing Aptitude packages, Snap packages, your custom config files and also your VScode extensions if you use it.

## Usage

When your dev$etup script is set, open your terminal and type ```./devSetup.sh```

## Configuration

To configure dev$etup use your text editor to edit ```devSetup.sh```

### Packages installation

You can specify your package by modifying the **aptitudepackages** and **snappackages** arrays

*Example packages list:*
```
aptitudepackages=( "snapd" "git" "vim" "docker" "docker.io" "docker-compose" "python3" "python3-pip" "nodejs")
snappackages=( "vscode" "insomnia")
```

### Configuration files installation

It is also possible to set a list of configuration files to install after the package installation is complete by modifiying the **cfgfiles** array: you need to put your config file in the **config** directory and add `"yourconfigfile /absolute/path/where/to/install/yourconfigfile"`

*Example configuration file install for vim:*
```
cfgfiles=("vimrc /etc/vim/vimrc")
```

### VScode extensions installation

If you use VScode you can install your extensions by adding them in the **vscodeext** array. If you don't use VScode just comment the line.

*Example configuration for VScode extension:*
```
vscodeext=( "ms-azuretools.vscode-docker" "ecmel.vscode-html-css" "mblode.twig-language-2" "GitHub.vscode-pull-request-github" "christian-kohler.path-intellisense" )
```


