#!/usr/bin/python3

#Made by Tom Gouville https://github.com/Any0ne22/

import subprocess
import os
import base64
import sys

purple='\033[1;35m'
nc='\033[0m'
dset= purple + "<" + nc + "dev$etup" + purple + ">"

def logo():
    print(purple)
    print("  __                     __            __                      \n /\\ \\                   /\\ \\_         /\\ \\__                   \n \\_\\ \\     __   __  __  \\/'__`\\     __\\ \\ ,_\\  __  __  _____   \n /'_` \\  /'__`\\/\\ \\/\\ \\ /\\ \\_\\_\\  /'__`\\ \\ \\/ /\\ \\/\\ \\/\\ '__`\\ \n/\\ \\L\\ \\/\\  __/\\ \\ \\_/ |\\ \\____ \\/\\  __/\\ \\ \\_\\ \\ \\_\\ \\ \\ \\L\\ \\\n\\ \\___,_\\ \\____\\\\ \\___/  \\/\\ \\_\\ \\ \\____\\\\ \\__\\\\ \\____/\\ \\ ,__/\n \\/__,_ /\\/____/ \\/__/    \\ `\\_ _/\\/____/ \\/__/ \\/___/  \\ \\ \\/ \n                           `\\_/\\_\\                       \\ \\_\\ \n                              \\/_/                        \\/_/ ")
    print(nc)

def isRoot():
    #Verify whether the user is root or not
    if subprocess.check_output("whoami").decode("utf-8") == "root\n":
        return True
    else:
        return False


def readFile(filename):
    paramFile = open(filename, "r")
    paramList = [x.replace("\n", "") for x in paramFile if (x!="" and x[0]!="#")]
    paramFile.close()
    return paramList

def writeFile(filename, data):
    paramFile = open(filename, "w")
    for x in data:
        paramFile.write(x + "\n")
    paramFile.close()
    subprocess.run("chmod -R 777 " + filename, shell=True)

def installAptitude(parameters):
    cmd = "apt-get install "
    for x in readFile(parameters.pkgsList):
        cmd += x + " "
    print(dset + purple + " Installing Aptitude packages" + nc)
    print(cmd)
    subprocess.run(cmd, shell=True)
    print("\n")

def updateAptitudePkgsList(parameters, merge=False):
    print(dset + purple + " Saving your Aptitude package list" + nc)
    pkgsList = subprocess.check_output(["apt", "list", "--installed"]).decode("utf-8")
    pkgsList = pkgsList.split("\n")[1:-1]
    newList = [x.split("/")[0].split(" ")[0] for x in pkgsList]
    if merge:
        #Merging the two lists into one
        return list(set(parameters.pkgsList + newList))
    else:
        return newList

def installPacman(parameters):
    cmd = "pacman -Sy "
    for x in readFile(parameters.pkgsList):
        cmd += x + " "
    print(dset + purple + " Installing Pacman packages" + nc)
    print(cmd)
    subprocess.run(cmd, shell=True)
    print("\n")

def updatePacmanPkgsList(parameters, merge=False):
    print(dset + purple + " Saving your Pacman package list" + nc)
    pkgsList = subprocess.check_output(["pacman", "-Qe"]).decode("utf-8")
    pkgsList = pkgsList.split("\n")[:-1]
    if merge:
        #Merging the two lists into one
        return list(set(parameters.pkgsList + pkgsList))
    else:
        return pkgsList

def installSnap(parameters):
    print(dset + purple + " Installing Snap packages" + nc)
    cmd = "snap install "
    for x in readFile(parameters.snapPkgs):
        print(cmd + x)
        subprocess.run(cmd, shell=True)
    print("\n")

def updateSnapPkgsList(parameters, merge=False):
    print(dset + purple + " Saving your Snap package list" + nc)
    pkgsList = subprocess.check_output(["snap", "list"]).decode("utf-8")
    pkgsList = pkgsList.split("\n")[1:-1]
    pkgsList = [x.split(" ")[0] for x in pkgsList]
    if merge:
        #Merging the two lists into one
        return list(set(parameters.pkgsList + pkgsList))
    else:
        return pkgsList

def setConfigFiles(parameters):
    print(dset + purple + " Installing config files" + nc)
    for x in readFile(parameters.cfgList):
        [a, b]  = x.split(":")
        cmd = "cp -R ./config/" + a + " " + b.replace("$HOME", parameters.homeDirectory)
        print(cmd)
        subprocess.run(cmd, shell=True)
    print("\n")

def updateConfigFiles(parameters):
    print(dset + purple + " Updating the config files" + nc)
    for x in readFile(parameters.cfgList):
        [a, b]  = x.split(":")
        cmd = "cp -f " + b.replace("$HOME", parameters.homeDirectory) + " Profiles/" + parameters.profile + "/config/" + a
        print("Saving " + b.replace("$HOME", parameters.homeDirectory) + " as " + a)
        print(cmd)
        subprocess.run(cmd, shell=True)
    print("\n")

def installZipFiles(parameters):
    print(dset + purple + " Installing zip files" + nc)
    for x in readFile(parameters.zipList):
        [a, b]  = x.split(":")
        cmd = "unzip ./zip/" + a + " -d " + b.replace("$HOME", parameters.homeDirectory)
        print(cmd)
        subprocess.run(cmd, shell=True)
    print("\n")

def installVSCodeExtensions(parameters):
    print(dset + purple + " Installing VSCode extensions" + nc)
    for x in readFile(parameters.vsexts):
        cmd = "su " + parameters.homeDirectory[6:] + " -c \"code --install-extension " + x + "\""
        print(cmd)
        subprocess.run(cmd, shell=True)
    print("\n")

def updateVSCodeExtensions(parameters, merge=False):
    print(dset + purple + " Saving your VSCode extensions list" + nc)
    extsList = subprocess.check_output(["su", parameters.homeDirectory[6:],"-c","code --list-extensions"]).decode("utf-8")
    if merge:
        #Merging the two lists into one
        return list(set(parameters.vsexts + extsList.split("\n")[:-1]))
    else:
        return extsList.split("\n")[:-1]


#CLI commands
def command(args):
    cmdList = {"setprofile": set_profile, "install": install, "save": save, "add": add, "remove": remove, "help": helpcmd}
    if args[0] in cmdList:
        cmdList[args[0]](args[1:])
    else:
        print("Unknown command " + args[0])

def set_profile(args):
    if len(args) == 0:
        print("Error: you haven't specified a profile name")
        print("\n")
        return
    profile = args[0]
    if os.path.isdir("Profiles/" + profile):
        print(dset + purple + " Profile set to \"" + profile + "\"" + nc)
        p.setProfile(profile)
        return True
    else:
        print("Profile \"" + profile + "\" doesn't exist.")
        return False

def install(args):
    options = {"all": install_all, "packages": install_packages, "config": install_config, "zip": install_zip, "VSexts": install_VSCodeExts}
    if args[0] in options:
        options[args[0]](args[1:])
    else:
        print("Unknown option " + args[0])

def save(args):
    options = {"packages": save_packages, "config": save_config, "VSexts": save_VSCodeExts}
    if args[0] in options:
        options[args[0]](args[1:])
    else:
        print("Unknown option " + args[0])

def add(args):
    options = {"package": add_package, "snap": add_snap, "config": add_config, "zip": add_zip, "VSext": add_VSCodeExt, "profile": add_profile}
    if args[0] in options:
        options[args[0]](args[1:])
    else:
        print("Unknown option " + args[0])

def remove(args):
    options = {"package": remove_package, "snap": remove_snap, "config": remove_config, "zip": remove_zip, "VSext": remove_VSCodeExt, "profile": remove_profile}
    if args[0] in options:
        options[args[0]](args[1:])
    else:
        print("Unknown option " + args[0])

def helpcmd(args):
    print("Welcome to the help section, unfortunately it has not been created yet")

def install_all(args):
    if len(args) > 0:
        if not set_profile(args): return
    install_packages(['auto'])
    install_config([])
    install_zip([])
    install_VSCodeExts([])

def install_packages(args):
    options = {"auto": install_packages_auto, "aptitude": installAptitude, "pacman": installPacman, "snap": installSnap}
    if args[0] in options:
        option = args.pop(0)
        if len(args) > 0:
            if not set_profile(args): return
        options[option](p)
    else:
        print("Unknown option " + args[0])

def install_packages_auto(parameters):
    if subprocess.check_output(["whereis","apt-get"]).decode("utf-8") != "apt-get:\n":
        #If Aptitude is installed
        installAptitude(parameters)
    elif subprocess.check_output(["whereis","pacman"]).decode("utf-8") != "pacman:\n":
        #If Pacman is installed
        installPacman(parameters)
    if subprocess.check_output(["whereis","snap"]).decode("utf-8") != "snap:\n":
        #If Snap is installed
        installSnap(parameters)

def install_config(args):
    setConfigFiles(p)

def install_zip(args):
    installZipFiles(p)

def install_VSCodeExts(args):
    installVSCodeExtensions(p)

def save_packages(args):
    options = {"auto": save_packages_auto, "aptitude": save_aptitude, "pacman": save_pacman, "snap": save_snap}
    if args[0] in options:
        options[args[0]](args[1:])
    else:
        print("Unknown option " + args[0])

def save_packages_auto(args):
    if subprocess.check_output(["whereis","apt-get"]).decode("utf-8") != "apt-get:\n":
        #If Aptitude is installed
        save_aptitude([])
    elif subprocess.check_output(["whereis","pacman"]).decode("utf-8") != "pacman:\n":
        #If Pacman is installed
        save_pacman([])
    if subprocess.check_output(["whereis","snap"]).decode("utf-8") != "snap:\n":
        #If Snap is installed
        save_snap([])

def update_parameters(updateFunction, fileName, interactive, merge):
    pkgs = []
    if merge:
        pkgs = updateFunction(p, True)
    else:
        pkgs = updateFunction(p, False)
    writeFile(fileName, pkgs)
    if interactive:
        print("Would you like to edit the list? (y/N)")
        if input("> ") == "y":
            subprocess.run("editor " + fileName, shell=True)
    print("\n")

def save_aptitude(args):
    merge = False
    if len(args) > 0 and args[0] == "merge":
        args.pop(0)
        merge = True
    if len(args) > 0:
        if not set_profile(args): return
    update_parameters(updateAptitudePkgsList, p.pkgsList, p.interactive, merge)

def save_pacman(args):
    merge = False
    if len(args) > 0 and args[0] == "merge":
        args.pop(0)
        merge = True
    if len(args) > 0:
        if not set_profile(args): return
    update_parameters(updatePacmanPkgsList, p.pkgsList, p.interactive, merge)

def save_snap(args):
    merge = False
    if len(args) > 0 and args[0] == "merge":
        args.pop(0)
        merge = True
    if len(args) > 0:
        if not set_profile(args): return
    update_parameters(updateSnapPkgsList, p.snapPkgs, p.interactive, merge)

def save_config(args):
    if len(args) > 0:
        if not set_profile(args): return
    updateConfigFiles(p)

def save_VSCodeExts(args):
    merge = False
    if len(args) > 0 and args[0] == "merge":
        args.pop(0)
        merge = True
    if len(args) > 0:
        if not set_profile(args): return
    update_parameters(updateVSCodeExtensions, p.vsexts, p.interactive, merge)

def add_package(args):
    if len(args) == 0:
        print("You haven't specified a package name")
        print("\n")
    else:
        package = args.pop(0)
        if len(args) > 0:
            if not set_profile(args): return
        print(dset + purple + " Adding \"" + package + "\" to your package list" + nc)
        f = open(p.pkgsList, "a")  
        f.writelines(package)
        f.close
        print("\n")

def add_snap(args):
    if len(args) == 0:
        print("You haven't specified a package name")
        print("\n")
    else:
        package = args.pop(0)
        if len(args) > 0:
            if not set_profile(args): return
        print(dset + purple + " Adding \"" + package + "\" to your Snap packages" + nc)
        f = open(p.snapPkgs, "a")
        f.writelines(package)
        f.close
        print("\n")

def add_config(args):
    if len(args) == 0:
        print("You haven't specified a configuration file")
        print("\n")
    else:
        configFile = args.pop(0)
        filename = ""
        if len(args) == 2:
            filename = args.pop(0)
            if not set_profile(args): return
        elif len(args) == 1:
            if not set_profile(args): return
            filename = configFile.split("/")[-1]
        else:
            filename = configFile.split("/")[-1]
        print(dset + purple + " Adding \"" + configFile + "\" as \"" + filename + "\" to your configuration files" + nc)
        if os.path.isfile(configFile):
            f = open(p.cfgList, "a")
            f.writelines(filename + ":" + configFile.replace("~", "$HOME"))
            f.close
            print("Please use \"save config\" to make a copy of this config file")
        else:
            print("Error: file " + configFile + " doesn't exist")
        print("\n")

def add_zip(args):
    if len(args) == 0:
        print("You haven't specified a zip file")
        print("\n")
    else:
        filename = args.pop(0)
        path = ""
        if len(args) == 2:
            path = args.pop(0)
            if not set_profile(args): return
        elif len(args) == 1:
            path = args[0]
        else:
            print("You haven't specified the extraction path")
            print("\n")
            return
        print(dset + purple + " Adding \"" + filename + "\" to your zip files" + nc)
        if os.path.isfile("Profiles/" + p.profile + "/zip/" + filename):
            f = open(p.zipList, "a")
            f.writelines(filename + ":" + path.replace("~", "$HOME"))
            f.close
        else:
            print("Error: file " + filename + " not found in Profiles/" + p.profile + "/zip/")
        print("\n")

def add_VSCodeExt(args):
    if len(args) == 0:
        print("You haven't specified an extension name")
        print("\n")
    else:
        ext = args.pop(0)
        if len(args) > 0:
            if not set_profile(args): return
        print(dset + purple + " Adding \"" + ext + "\" to your VSCode extensions" + nc)
        f = open(p.vsexts, "a")  
        f.writelines(ext)
        f.close
        print("\n")

def add_profile(args):
    if len(args) == 0:
        print("Error: you haven't specified a profile name")
        print("\n")
        return
    profile = args[0]
    print(dset + purple + " Creating profile \"" + profile + "\"" + nc)
    if os.path.isdir("Profiles/" + profile):
        print("Profile \"" + profile + "\" already exists.")
    else:
        os.mkdir("Profiles/" + profile)
        os.mkdir("Profiles/" + profile + "/config")
        os.mkdir("Profiles/" + profile + "/zip")
        open("Profiles/" + profile + "/packages.txt", "a").close()
        open("Profiles/" + profile + "/snapPackages.txt", "a").close()
        open("Profiles/" + profile + "/configfiles.txt", "a").close()
        open("Profiles/" + profile + "/vscodeextensions.txt", "a").close()
        open("Profiles/" + profile + "/zip.txt", "a").close()
        subprocess.run("chmod -R 777 " + "Profiles/" + profile, shell=True)
        print("Profile \"" + profile + "\" successfully created.")
    print("\n")

def remove_package(args):
    if len(args) == 0:
        print("You haven't specified a package name")
        print("\n")
    else:
        package = args.pop(0)
        if len(args) > 0:
            if not set_profile(args): return
        print(dset + purple + " Removing \"" + package + "\" from your package list" + nc)
        packages = readFile(p.pkgsList)
        try:
            packages.remove(package)
        except:
            pass
        writeFile(p.pkgsList, packages)
        print("\n")

def remove_snap(args):
    if len(args) == 0:
        print("You haven't specified a package name")
        print("\n")
    else:
        package = args.pop(0)
        if len(args) > 0:
            if not set_profile(args): return
        print(dset + purple + " Removing \"" + package + "\" from your snap package list" + nc)
        packages = readFile(p.snapPkgs)
        try:
            packages.remove(package)
        except:
            pass
        writeFile(p.snapPkgs, packages)
        print("\n")

def remove_config(args):
    if len(args) == 0:
        print("You haven't specified a config file name")
        print("\n")
    else:
        filename = args.pop(0)
        if len(args) > 0:
            if not set_profile(args): return
        print(dset + purple + " Removing \"" + filename + "\" from your config file list" + nc)
        configs = readFile(p.cfgList)
        for i in range(len(configs)):
            if configs[i].split(":")[0] == filename:
                configs.pop(i)
                os.remove("Profiles/" + p.profile + "/config/" + filename)
                break
        writeFile(p.cfgList, configs)
        print("\n")

def remove_zip(args):
    if len(args) == 0:
        print("You haven't specified a zip file name")
        print("\n")
    else:
        filename = args.pop(0)
        if len(args) > 0:
            if not set_profile(args): return
        print(dset + purple + " Removing \"" + filename + "\" from your zip files list" + nc)
        zips = readFile(p.cfgList)
        for i in range(len(zips)):
            if zips[i].split(":")[0] == filename:
                zips.pop(i)
                os.remove("Profiles/" + p.profile + "/zip/" + filename)
                break
        writeFile(p.cfgList, zips)
        print("\n")

def remove_VSCodeExt(args):
    if len(args) == 0:
        print("You haven't specified an extension name")
        print("\n")
    else:
        ext = args.pop(0)
        if len(args) > 0:
            if not set_profile(args): return
        print(dset + purple + " Removing \"" + ext + "\" from your VS Code extensions list" + nc)
        exts = readFile(p.vsexts)
        try:
            exts.remove(ext)
        except:
            pass
        writeFile(p.vsexts, exts)
        print("\n")

def remove_profile(args):
    if len(args) == 0:
        print("Error: you haven't specified a profile name")
        print("\n")
        return
    profile = args[0]
    print(dset + purple + " Removing profile \"" + profile + "\"" + nc)
    if not os.path.isdir("Profiles/" + profile):
        print("Profile \"" + profile + "\" doesn't exist. Nothing to do.")
    else:
        for root, dirs, files in os.walk("Profiles/" + profile, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir("Profiles/" + profile)
        print("Profile \"" + profile + "\" successfully removed.")
    print("\n")


class Parameters:
    def __init__(self):
        if not os.path.isdir("Profiles/Default"):
            add_profile(["Default"])
        self.profile = "Default"
        self.homeDirectory = os.environ.get('HOME')
        self.pkgsList = "Profiles/Default/packages.txt"
        self.snapPkgs = "Profiles/Default/snapPackages.txt"
        self.cfgList = "Profiles/Default/configfiles.txt"
        self.vsexts = "Profiles/Default/vscodeextensions.txt"
        self.zipList = "Profiles/Default/zip.txt"
        self.interactive = False
    
    def setProfile(self, profileName):
        self.profile = profileName
        self.pkgsList = "Profiles/" + profileName + "/packages.txt"
        self.snapPkgs = "Profiles/" + profileName + "/snapPackages.txt"
        self.cfgList = "Profiles/" + profileName + "/configfiles.txt"
        self.vsexts = "Profiles/" + profileName + "/vscodeextensions.txt"
        self.zipList = "Profiles/" + profileName + "/zip.txt"



if __name__ == '__main__':
    
    if not isRoot():
        print("please run as root")
        exit()

    if not os.path.isdir("Profiles/"):
        os.mkdir("Profiles/")
    
    global p
    p = Parameters()
    logo()

    if len(sys.argv) > 1:
        args = sys.argv[1:]
        #print(args)
        command(args)
    else:
        #Interactive mode
        p.interactive = True
        while 1:
            cmd = input("> ")
            args = cmd.split(" ")
            #print(args)
            if args[0] == "exit":
                print("Goodbye!")
                exit()
            else:
                command(args)