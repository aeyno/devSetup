#!/bin/bash

#Made by Tom Gouville(https://github.com/Any0ne22)

#### PARAMETERS ####:
#Softwares to install
#aptitudes packages
aptitudepackages=( "wget" "snapd" "git" "vim" "zip" "unzip" "docker" "docker.io" "docker-compose" "python3" "python3-pip" "htop" "nodejs" "vlc")
#snapd packages
snappackages=( "code" "insomnia")
#Config files to replace (write the name of the file in the config folder and the place where it should be after the install separated by a space)
cfgfiles=("vimrc /etc/vim/vimrc")

#VSCODE extensions (commment the line if you don't use vscode)
vscodeext=("slevesque.vscode-hexdump" "ms-azuretools.vscode-docker" "ecmel.vscode-html-css" "mblode.twig-language-2" "leizongmin.node-module-intellisense" "GitHub.vscode-pull-request-github" "christian-kohler.path-intellisense" "itmcdev.node-extension-pack" "eg2.vscode-npm-script")



#Root check
if (( $EUID != 0 )); then
    echo "Please run dev\$etup as root"
    exit
fi

#UI elements
PURPLE='\033[1;35m'
NC='\033[0m'
dset="${PURPLE}<${NC}dev\$etup${PURPLE}>"

printf "${PURPLE}"
printf '%s\n' "  __                     __            __                      "
printf '%s\n' " /\\ \\                   /\\ \\_         /\\ \\__                   "
printf '%s\n' " \\_\\ \\     __   __  __  \\/'__\`\\     __\\ \\ ,_\\  __  __  _____   "
printf '%s\n' " /'_\` \\  /'__\`\\/\\ \\/\\ \\ /\\ \\_\\_\\  /'__\`\\ \\ \\/ /\\ \\/\\ \\/\\ '__\`\\ "
printf '%s\n' "/\\ \\L\\ \\/\\  __/\\ \\ \\_/ |\\ \\____ \\/\\  __/\\ \\ \\_\\ \\ \\_\\ \\ \\ \\L\\ \\"
printf '%s\n' "\\ \\___,_\\ \\____\\\\ \\___/  \\/\\ \\_\\ \\ \\____\\\\ \\__\\\\ \\____/\\ \\ ,__/"
printf '%s\n' " \\/__,_ /\\/____/ \\/__/    \\ \`\\_ _/\\/____/ \\/__/ \\/___/  \\ \\ \\/ "
printf '%s\n' "                           \`\\_/\\_\\                       \\ \\_\\ "
printf '%s\n' "                              \\/_/                        \\/_/ "
printf "${NC}\n\n"

echo -e "Bienvenue dans l'assistant d'installation d'environnement dev\$etup!\n(Si vous n'avez pas configuré la liste de vos packets pensez à éditer ce fichier)\n\n"


#Install
installcmd='apt-get install '
for i in "${aptitudepackages[@]}"
do
	installcmd=$installcmd$i" "
done

snapinstallcmd='snap install --classic '
echo -e "$dset${PURPLE} Installing Aptitude packages${NC}\n"
$installcmd
echo -e "\n\n$dset${PURPLE} Installing Snap packages${NC}\n"

for i in "${snappackages[@]}"
do
	$snapinstallcmd$i
done

echo -e "\n\n$dset${PURPLE} Installing configuration files${NC}\n"
for i in "${cfgfiles[@]}"
do
	cmd="cp ./config/$i"
	echo $cmd
	$cmd
done

if [ -z ${vscodeext+x} ]; 
then echo -e "\n\n$dset${PURPLE} No VScode extensions to install${NC}\n"; 
else echo -e "\n\n$dset${PURPLE} Installing VScode extensions${NC}\n"
	echo -e "$dset${PURPLE} Please enter the name of the user you want to install VScode extensions to:${NC}"
	read username
	if [$username -gt ""]
	then echo -e "${PURPLE}Invalid username${NC}"
		exit
	fi
	for i in "${vscodeext[@]}"
	do
		su $username -c "code --install-extension $i"
	done
fi
