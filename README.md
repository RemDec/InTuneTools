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
