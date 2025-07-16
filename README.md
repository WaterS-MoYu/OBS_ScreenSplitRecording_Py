# OBS_ScreenSplitRecording_Py
Python Script for multi OBS clients Screen Recording

# How to use
- Install Python with version >= 3.9, or conda create a virtual environment of python version >= 3.9
- Click Menu Tools(工具)-->Scripts(脚本), you can see a new window, click Python Settings(Python设置) tab, click Browse(浏览) button to choose your PC's python folder which contains python.exe, you can see "Loaded Python Version: 3.xx(已加载Python版本:3.xx)" below if it is loaded
  <https://github.com/WaterS-MoYu/OBS_ScreenSplitRecording_Py/blob/main/python%20setting.png>
- Click and back to the Scripts(脚本) tab, click the + button at the left-buttom corner, choose one of the python scripts of this project(such as obs_recording_plugin_LU.py), you can see several chinese parameters on the right
  - Note: the name of script indicates the area it will record: LU is Left Top 1/4 of screen, LD is Left bottom 1/4 of screen, RU and RD are right top/bottom 1/4 of screen, FULL is the whole screen
- Set the parameters
  -  the first 录制来源(source) is the source you want to record, for example a screen monitor source;
  -  the second 相机编号(Camera ID) is the id of this monitor screen, it will use camera id as a postfix added to recorded video files' name, for example, 2024-01-01.mp4 will be 2024-01-01_CamA.mp4
- After setting, click close button to quit scripts setting
- Open OBS Settings window, in Output(输出) tab, set your Recording Path(录像路径) of current OBS. Make sure if you use multi clients of obs, please set different save path for each one, otherwise they will try to rename same file at the same time
- The scripts will read the last line of file named "D:/MoCapTakeInfo.txt" in Disk D, the txt file records file name (like S001_C001_Take001) of each recording because my developed project will write recording takes names when a recording is started, you can modify those python scripts to change the file path, or use your own method to rename recorded videos
- The HotKeySetting.json file save the recording hotkey for OBS, in my project it is OBS_KEY_HOME, make sure your OBS setting and PC environment has no conflicts with this hotkey, you don't have to set recording hotkeys in OBS setting since the scripts have done that, and you can change the hotkey to any you want, for example, OBS_KEY_SPACE


# How to use multi OBS clients
- Go to your obs install path(like D:\obs-studio), copy the whole folder and rename as "obs-studio-new"
- Go to D:\obs-studio-new\bin\64bit, find obs64.exe and right click it and send to desktop as a windows shortcut
- Right click the new OBS desktop shortcut, select Properties(属性), at the Target(目标) box, add " --portable" after the D:\obs-studio-new\bin\64bit\obs64.exe path line, now you can double click it and use the second OBS at the same time

# Finally
If you can not understand, please see these png files of this project
