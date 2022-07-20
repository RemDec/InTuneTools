# InTuneTools
Diverse InTune-related tools/snippets to manage the Microsoft solution.

## Autopilot

Scripts to allow quick registration of Windows devices in InTune (meaning computing the hash of the machines in an uploadable CSV), easing the manual steps described [here](https://docs.microsoft.com/en-us/mem/autopilot/add-devices) to do it from an USB stick. So it takes less than 2 minutes by machine, we plug in each time the same USB key that gathers up the hashes in individual CSV files. Once done, the merger script can be launched, it will compile all the hashes in one CSV that we can upload in the Intune's portal (`Devices > Device enrollment > Windows enrollment > Devices`).

1. Spin up the new endpoint, proceed the first Windows setup steps until the network connection page (language, keyboard, ...).
1. Once connected, plug in the USB stick containing the snippets
1. Open up a terminal with Shift + F10
1. Type `D:\intune.CMD` (or replace with the USB drive letter)
1. In the popped up explorer, you can browse the USB to see an `Autopilot` directory with the CSV containing the generated hash in
1. Eject the USB key (right click on drive > eject)
1. Shutdown the machine (`shutdown /p`)
2. Repeat the operation for each machine in your batch to register

Once done, plug in the USB in any usable machine, open up a powershell and `cd D:\`, then launch the script `merger.ps1`. In the same directory, the final file `MergedAutopilots.csv` is generated, you can upload it to Intune.

## Packager

Python >= 3.5 workflow to ease and semi-automate the process of packaging batch of applications for InTune.
- [IntuneWinAppUtil.exe](Packager/IntuneWinAppUtil.exe) : the [Win32 Content Prep Tool](https://github.com/Microsoft/Microsoft-Win32-Content-Prep-Tool) written by Microsoft to wrap up sources
- [uninstaller.py](Packager/uninstaller.py) : a registry for uninstallation techniques specific to each software you want to package (either by uninstaller file or by software GUID) that will help to pre-generate stuff to wrap up
- [packager.py](Packager/packager.py) : the tool to launch once you've put all your installers (`.exe`, `.msi`) in the directory `ToPackage`, will pre-generate stuff to wrap up later in a directory `StandbyToCustom` (package structure, scripts)

Of course, before packaging an app you should test (un)installation manually and be aware of its specificities. Once done, proceed to the following steps :

1. [Pre-step] Test a manual install of the softwares to package, provide in the config file [uninstaller.py](Packager/uninstaller.py) the way to uninstall it (either by GUID or directly pointing to the uninstaller file). If you don't know, put `None` but you'll loose part of automation. Put a key mapping exactly the name of the installer.

1. Put all the installers (`.exe`/`.msi`) you want to package in the directory `ToPackage\` with an explicit name (try to use the same than when installed on the system in the `C:\Program Files\SoftwareName` if possible) mapping a key in [uninstaller.py](Packager/uninstaller.py)

1. Launch the [packager.py](Packager/packager.py) that will create a `PACK_SoftwareName.CMD` script in current directory and under the directory   `StandbyToCustom\` a new named directory for every installer, with the pre-filled package structure and scripts in it

1. For the next package you want to wrap up, browse the created package structure and test the `(Un)Install.CMD` scripts (as admin), tweak them if necessary. For example, an `.exe` installation isn't standardized, to install silenlty as InTune requires you may put a flag that can be `/S`, `/VERYSILENT`, `/QUIET`, ... edit the `.CMD` files in consequence, don't hesitate to launch it to test

1. Once (un)install works, wrap up the software by launching `PACK_SoftwareName.CMD`, then a `SoftwareName.intunewin` archive is created under `Packaged\` along with a `DETECT_SoftwareName.ps1` script potentially uploadable to InTune (may be to tweak as well)

Now you should create a new app in the InTune portal and upload the generated `.intunewin`, in the install/uninstall command fields put `Install.CMD` and `UnInstall.CMD`. You may use `DETECT_SoftwareName.ps1` for detecting rule if needed.
