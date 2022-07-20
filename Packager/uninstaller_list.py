UNINSTALLERS = {
    'files': {
        "7-Zip": r'C:\Program Files\7-Zip\Uninstall.exe',
        "Git": r'C:\Program Files\Git\unins000.exe',
        "KeePass": r'C:\Program Files\KeePass Password Safe 2\unins000.exe',
        "MOBIB_Reader": None, # C:\Users\decocqr\AppData\Local\Programs\MOBIB_Reader\unins000.exe
        "Notepad++": r'C:\Program Files\Notepad++\uninstall.exe',
        "Postman": None, # Squirrel installation -> use special cmd Update.exe --uninstall
        "WinSCP": r'C:\Program Files (x86)\WinSCP\unins000.exe',
        "Tricentis Tosca": r'C:\Program Files (x86)\TRICENTIS\Tosca Testsuite\intune_installer.exe',  # Uninstall can only be done from original installer
        "Azure Storage Explorer": r'C:\Program Files (x86)\Microsoft Azure Storage Explorer\unins000.exe',
    },
    'guid': {
        "PuTTY": r'E078C644-A120-4668-AD62-02E9FD530190',
        "Adobe Acrobat DC": r'AC76BA86-1033-1033-7760-BC15014EA700',
        "Belgium Identity Card": r'DB942AEA-93D6-4FE4-8862-180D35A75498',
        "Altitude uAgent": r'50cee41d-446f-4f52-916e-e070e3f79a92',
        "Avaya IX Workplace": r'7BE3AB6A-04A5-4C2C-A23A-942CCBFE0F43',
        "Phish Alert": r'F3E990F3-6238-4294-97E6-DD252C1F2BCB',
        "LogMeInRescueTechnicianConsole": r'A2AF44DC-528E-4A70-A3D6-8C4C4AEDDB7C',
        "Tricentis Tosca": r'271A70F0-5455-46E3-ADD8-83254D249DE0',  # For detection only, because the intune_installer isn't removed at uninstall so not good candidate
        "Azure CLI": r'229AC774-AB39-4D59-9BD1-87E5BD6DB346',
        "Azure Storage Emulator": r'41AC2282-F083-4495-8306-2D6ABC7D5CA2',
    }
}
