#!/usr/bin/python3

from pathlib import Path
from uninstaller_list import UNINSTALLERS

dir_to_package = Path("./ToPackage")
dir_to_package.mkdir(exist_ok=True)

dir_standby = Path("./StandbyToCustom")
dir_to_package.mkdir(exist_ok=True)

dir_packaged = Path("./Packaged")
dir_packaged.mkdir(exist_ok=True)

def list_installers():
    exes = dir_to_package.glob('*.exe')
    msis = dir_to_package.glob('*.msi')
    return list(exes) + list(msis)

def install_cmd(software_name, installer_type):
    if installer_type == ".exe":
        return '"%%~dp0sources\%s%s" /s' % (software_name, installer_type)
    elif installer_type == ".msi":
        return 'MsiExec.exe /i "sources\%s%s" /qn' % (software_name, installer_type)

def uninstall_cmd(software_name, installer_type):
    uninstall_info = UNINSTALLERS.get(software_name)
    if installer_type == ".exe":
        if uninstall_info:
            return r'"%s" /S' % uninstall_info
        return r'"C:\Program Files (x86)\%s\uninst.exe" /S' % software_name
    elif installer_type == ".msi":
        if uninstall_info:
            return r'MsiExec /x "{%s}" /qn' % uninstall_info
        return 'MsiExec /x "{GUID}" /qn'

def detect_cmd(software_name):
    uninstaller = UNINSTALLERS.get(software_name)
    if uninstaller:
        return r'if ((Test-Path -Path "%s")) { exit 0 } else { exit 1 }' % uninstaller
    return None


def package_cmd(dir_package, installer_target):
    return 'IntuneWinAppUtil.exe -c "%s" -s "%s" -o Packaged' % (dir_package, installer_target)

def prepare_packages(installers):
    for installer in installers:
        print("\nFound installer to treat : ", installer)
        software_name = installer.stem
        installer_type = installer.suffix
        # create directory structure
        dir_package = dir_standby / software_name
        dir_package.mkdir(exist_ok=True)
        dir_src = dir_package / "sources"
        dir_src.mkdir(exist_ok=True)
        # move the software installer to a fixed relative path
        installer_target = dir_src / (software_name + installer_type)
        installer.replace(installer_target)
        # create and fill in (un)install scripts with default commands
        install_script = dir_package / "Install.CMD"
        uninstall_script = dir_package / "UnInstall.CMD"
        install_script.write_text(install_cmd(software_name, installer_type))
        uninstall_script.write_text(uninstall_cmd(software_name, installer_type))
        # create the snippet to launch later after finetuning to package towards .intunewin
        package_script = Path("PACK_" + software_name + ".CMD")
        package_script.write_text(package_cmd(dir_package, installer_target))
        # create the detection script to provide to InTune
        detect_command = detect_cmd(software_name)
        if detect_command:
            detection_script = Path(dir_packaged / ("DETECT_" + software_name + ".ps1"))
            detection_script.write_text(detect_command)


if __name__ == '__main__':
    prepare_packages(list_installers())
