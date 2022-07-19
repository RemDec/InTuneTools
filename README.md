# InTuneTools
Diverse InTune-related tools/snippets to manage the Microsoft solution.

## Autopilot

Scripts to allow quick registration of devices in InTune, easing the manual steps described [here](https://docs.microsoft.com/en-us/mem/autopilot/add-devices) to do it from an USB stick.
1. Spin up the new endpoint, proceed the first Windows setup steps until the network connection page.
1. Once connected, plug in the USB stick containing the snippets
1. Open up a terminal with Shift + F10
1. Type `D:\intune.CMD` (or replace with the USB drive letter)
1. In the popped up explorer, you can browse the USB to see an `Autopilot` directory with the CSV containing your hash in
1. Eject the USB key (right click on drive > eject)
1. Shutdown the machine (`shutdown /p`)
