; my_project.iss
[Setup]
; Basic setup information
AppName=NCM App
AppVersion=1.0
DefaultDirName={userdocs}\NCM App
DefaultGroupName=NCM App
OutputDir=.
OutputBaseFilename=ncm_app_installer

[Files]
; Main executable
Source: "dist\main\main.exe"; DestDir: "{app}"; Flags: ignoreversion
; Include the entire _internal directory
Source: "dist\main\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs
; Config files
Source: "config\saved_colors.csv"; DestDir: "{app}\config"; Flags: ignoreversion
Source: "config\selected_colors.csv"; DestDir: "{app}\config"; Flags: ignoreversion
Source: "config\settings.json"; DestDir: "{app}\config"; Flags: ignoreversion
; Assets
Source: "assets\color_converter_dark.png"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\color_converter_light.png"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\color_gear_dark.png"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\color_gear_light.png"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\color_grab_dark.png"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\color_grab_light.png"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\icon.ico"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\ncm_app_dark.png"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\ncm_app_light.png"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\settings.png"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\tutorials.png"; DestDir: "{app}\assets"; Flags: ignoreversion

[Icons]
; Shortcut in Start Menu
Name: "{group}\NCM App"; Filename: "{app}\main.exe"
