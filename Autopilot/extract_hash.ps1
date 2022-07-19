$DestPath = "D:\Autopilots\"
if (!(Test-Path -Path $DestPath)) {
	New-Item -Type Directory -Path $DestPath
}
Set-Location -Path $DestPath
$env:Path += ";C:\Program Files\WindowsPowerShell\Scripts"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force
Install-Script -Name Get-WindowsAutopilotInfo -Force
$SN = (Get-WmiObject -class win32_bios).SerialNumber
Get-WindowsAutopilotInfo -OutputFile "PP-${SN}.csv"
