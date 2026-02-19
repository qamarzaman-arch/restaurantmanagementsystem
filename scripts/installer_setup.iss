; Inno Setup Script for RestaurantOS
#define MyAppName "Restaurant Management System"
#define MyAppVersion "1.0"
#define MyAppPublisher "Your Restaurant OS"
#define MyAppExeName "RestaurantOS.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Use a valid GUID (hex digits only) wrapped in double braces
AppId={{D3B2A1E9-4C5D-4E3F-8A7B-9C0D1E2F3A4B}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Remove the following line to run in administrative install mode (install for all users).
PrivilegesRequired=lowest
OutputDir=..\installer
OutputBaseFilename=RestaurantOS_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\RestaurantOS\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\RestaurantOS\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
