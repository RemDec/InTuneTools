#!/usr/bin/python3

from pathlib import Path
from uninstaller_list import UNINSTALLERS
import shutil
import argparse

dir_to_package = Path("./ToPackage")
dir_to_package.mkdir(exist_ok=True)

dir_standby = Path("./StandbyToCustom")
dir_standby.mkdir(exist_ok=True)

dir_history = Path("./PackagingHistory")
dir_history.mkdir(exist_ok=True)

dir_packaged = Path("./Packaged")
dir_packaged.mkdir(exist_ok=True)

def list_installers():
    exes = dir_to_package.glob('*.exe')
    msis = dir_to_package.glob('*.msi')
    return list(exes) + list(msis)

def install_cmd(software_name, installer_type):
    if installer_type == ".exe":
        return '"%%~dp0sources\%s%s" /S' % (software_name, installer_type)
    elif installer_type == ".msi":
        return 'MsiExec.exe /i "sources\%s%s" /qn' % (software_name, installer_type)

def uninstall_cmd(software_name, installer_type):
    uninst_by_file = UNINSTALLERS['files'].get(software_name)
    uninst_by_guid = UNINSTALLERS['guid'].get(software_name)
    if uninst_by_file:
        return r'"%s" /S' % uninst_by_file
    elif uninst_by_guid:
        return r'MsiExec /X "{%s}" /QN' % uninst_by_guid
    else:
        return r'"C:\Program Files (x86)\%s\uninst.exe" /S' % software_name

def detect_cmd(software_name):
    uninstaller = UNINSTALLERS['files'].get(software_name)
    if uninstaller:
        out_txt = "%s detected thanks to %s !" % (software_name, uninstaller)  # mandatory along with exit code
        return r'if ((Test-Path -Path "%s")) { write-output "%s"; exit 0 } else { exit 1 }' % (uninstaller, out_txt)
    return None


def package_cmd(dir_package, software_name, installer_target):
    copy_to_history = 'xcopy /e /v /y "%s" "%s";' % (dir_package, (dir_history / software_name))
    return copy_to_history + 'IntuneWinAppUtil.exe -c "%s" -s "%s" -o Packaged' % (dir_package, installer_target)

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
        package_script.write_text(package_cmd(dir_package, software_name, installer_target))
        # create the detection script to provide to InTune
        detect_command = detect_cmd(software_name)
        if detect_command:
            detection_script = Path(dir_packaged / ("DETECT_" + software_name + ".ps1"))
            detection_script.write_text(detect_command)


def clean_dirs():
    in_standby = list(dir_standby.glob('*/'))
    in_packaged_intunewin = list(dir_packaged.glob('*.intunewin'))
    in_packaged_ps1 = list(dir_packaged.glob('DETECT*.ps1'))
    pack_CMDs = list(Path('./').glob('PACK*.CMD'))
    print("Cleaning InStandby folder...")
    [shutil.rmtree(str(d)) for d in in_standby]

    print("Cleaning PACK_* snippet files ...")
    [f.unlink() for f in pack_CMDs]

    print("Cleaning resulting packaged files ...")
    [f.unlink() for f in in_packaged_ps1 + in_packaged_intunewin]


if __name__ == '__main__':
    desc = "InTune packager tool"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-c", "--clean", action="store_true", help="Clean the create files/directories after a run")

    args = parser.parse_args()
    if args.clean:
        clean_dirs()
    else:
        prepare_packages(list_installers())


