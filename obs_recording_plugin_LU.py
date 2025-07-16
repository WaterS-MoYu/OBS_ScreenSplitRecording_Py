import os
import sys
import time
import json
import obspython as obs

message_file = "D:/MoCapTakeInfo.txt"
id_recording = "ID_Recording"
id_example = "ID1"
# below four are same
#JSON_DATA = '{"%s":[{"key":"OBS_KEY_F2"}],'% id_recording +'"%s":[{"key":"OBS_KEY_1"}]}' % id_example 
#JSON_DATA = '{"%s":[{"key":"OBS_KEY_F2"}],"%s":[{"key":"OBS_KEY_1"}]}' % (id_recording,id_example)
#JSON_DATA = '{{"{0}":[{{"key":"OBS_KEY_F2"}}],"{1}":[{{"key":"OBS_KEY_1"}}]}}'.format(id_recording,id_example)
#JSON_DATA = json.dumps({id_recording:[{"key":"OBS_KEY_F2"}],id_example:[{"key":"OBS_KEY_1"}]})

class ObsRecordingSetting:
    def __init__(self, source_name=None):
        self.source_name = source_name
        self.file_postfix = "CamB"
        #self.ep_scene_cam = "EP000_SC00_C000"
        #self.take_num = 1
        self.auto_read = True
        self.is_recording = False
    
    def update(self, settings):
        my_recording_setting.source_name = obs.obs_data_get_string(settings, "LIST_RecordingSource")
        my_recording_setting.file_postfix = obs.obs_data_get_string(settings, "TXT_FilePostfix")
        #my_recording_setting.auto_read = obs.obs_data_get_bool(settings, "BOOL_AutoReadMessage")
        #my_recording_setting.ep_scene_cam = obs.obs_data_get_string(settings, "TXT_EPSceneCam")
        #my_recording_setting.take_num = obs.obs_data_get_int(settings, "INT_TakeNum")
        return True

my_recording_setting = ObsRecordingSetting()

def rename_latest_recording(source_recording_file, new_filename):
    save_path = os.path.split(source_recording_file)[0] # 获取文件路径
    file_extension = os.path.splitext(source_recording_file)[1] # 获取文件后缀
    target_file = os.path.join(save_path, new_filename + file_extension)

    counter = 1
    while os.path.exists(target_file): # 重复 生成新名字
        new_name = new_filename + f"_{counter}" + file_extension
        target_file = os.path.join(save_path, new_name)
        counter += 1

    os.rename(source_recording_file, target_file)
    current_time = time.strftime("%Y-%M-%D_%H:%M:%S")
    print(f"Renamed {source_recording_file} to {target_file} at time {current_time}")


def switch_recording(pressed):
    if pressed:
        if my_recording_setting.is_recording:
            obs.obs_frontend_recording_stop()
            my_recording_setting.is_recording = False
        else:
            obs.obs_frontend_recording_start()
            my_recording_setting.is_recording = True

def recording_stopped_callback(event):
    if event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        my_recording_setting.is_recording = False

        if not my_recording_setting.auto_read:
            new_filename = f"{my_recording_setting.ep_scene_cam}_Take{my_recording_setting.take_num}_{my_recording_setting.file_postfix}"
            rename_latest_recording(obs.obs_frontend_get_last_recording(), new_filename)
        
        else:
            if not os.path.exists(message_file):
                print(f"Warning: {obs.obs_frontend_get_last_recording()} NOT Renamed Because NO message File Found")
                return
            with open(message_file, 'r') as file:
                messages = file.readlines()
                message = messages[-1].strip("\n")
                my_recording_setting.ep_scene_cam = message
                new_filename = f"{message}_{my_recording_setting.file_postfix}"
                rename_latest_recording(obs.obs_frontend_get_last_recording(), new_filename)

def recording_source_modify_callback(props, prop, settings, *args, **kwargs):
    my_recording_setting.update(settings)
    return True

def file_postfix_modify_callback(props, prop, settings, *args, **kwargs):
    my_recording_setting.update(settings)
    return True

def auto_read_message_modify_callback(props, prop, settings, *args, **kwargs):
    if obs.obs_data_get_bool(settings, "BOOL_AutoReadMessage"):
        p1 = obs.obs_properties_get(props, "TXT_EPSceneCam")
        obs.obs_property_set_visible(p1, False)
        p2 = obs.obs_properties_get(props, "INT_TakeNum")
        obs.obs_property_set_visible(p2, False)
    else:
        p1 = obs.obs_properties_get(props, "TXT_EPSceneCam")
        obs.obs_property_set_visible(p1, True)
        p2 = obs.obs_properties_get(props, "INT_TakeNum")
        obs.obs_property_set_visible(p2, True)
    my_recording_setting.update(settings)
    return True

def ep_scenen_cam_modify_callback(props, prop, settings, *args, **kwargs):
    my_recording_setting.update(settings)
    return True

def take_num_modify_callback(props, prop, settings, *args, **kwargs):
    my_recording_setting.update(settings)
    return True

def script_description():
    return "虚拍动捕obs录屏插件-左上角1/4屏"

def script_properties():
    props = obs.obs_properties_create()

    RecordingSource = obs.obs_properties_add_list(props,"LIST_RecordingSource","录制来源",obs.OBS_COMBO_TYPE_LIST,obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            name = obs.obs_source_get_name(source)
            obs.obs_property_list_add_string(RecordingSource, name, name)
        obs.source_list_release(sources)

    FilePostfix = obs.obs_properties_add_list(props,"TXT_FilePostfix","相机编号",obs.OBS_COMBO_TYPE_EDITABLE,obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_list_add_string(FilePostfix, "CamA", "CamA")
    obs.obs_property_list_add_string(FilePostfix, "CamB", "CamB")
    obs.obs_property_list_add_string(FilePostfix, "CamC", "CamC")
    obs.obs_property_list_add_string(FilePostfix, "CamD", "CamD")
    obs.obs_property_list_add_string(FilePostfix, "CamE", "CamE")

    #AutoReadMessage = obs.obs_properties_add_bool(props, "BOOL_AutoReadMessage", "开启自动读取场次镜头号")
    #EPSceneCam = obs.obs_properties_add_text(props, "TXT_EPSceneCam", "场次镜头", obs.OBS_TEXT_DEFAULT)
    #TakeXXX = obs.obs_properties_add_int(props,"INT_TakeNum","Take",1,999,1)

    obs.obs_property_set_modified_callback(RecordingSource, recording_source_modify_callback)
    obs.obs_property_set_modified_callback(FilePostfix, file_postfix_modify_callback)
    #obs.obs_property_set_modified_callback(AutoReadMessage, auto_read_message_modify_callback)
    #obs.obs_property_set_modified_callback(EPSceneCam, ep_scenen_cam_modify_callback)
    #obs.obs_property_set_modified_callback(TakeXXX, take_num_modify_callback)
    return props

def script_update(settings):
    my_recording_setting.source_name = obs.obs_data_get_string(settings, "LIST_RecordingSource")
    current_scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())
    scene_item = obs.obs_scene_find_source(current_scene, my_recording_setting.source_name)

    pos = obs.vec2()
    pos.x, pos.y = 0, 0
    obs.obs_sceneitem_set_pos(scene_item, pos)
    obs.obs_sceneitem_set_rot(scene_item, 0)

    scale = obs.vec2()
    scale.x, scale.y = 2, 2
    obs.obs_sceneitem_set_scale(scene_item, scale)

    # 5|4|6      0101|0100|0110
    # 1|0|2   =  0001|0000|0010
    # 9|8|10     1001|1000|1010
    # OBS_ALIGN_CENTER 0 0000
    # OBS_ALIGN_LEFT   1 0001
    # OBS_ALIGN_RIGHT  2 0010
    # OBS_ALIGN_TOP    4 0100
    # OBS_ALIGN_BOTTOM 8 1000
    obs.obs_sceneitem_set_alignment(scene_item,5)

    obs.obs_sceneitem_set_bounds_type(scene_item, obs.OBS_BOUNDS_NONE)

def script_load(settings):
    my_recording_setting.update(settings)
    print(f"1 {my_recording_setting.source_name} 2 {my_recording_setting.file_postfix} 3 {my_recording_setting.auto_read}")
    obs.obs_frontend_add_event_callback(recording_stopped_callback)

    hotkeys_json_file = obs.obs_data_create_from_json_file(script_path() + "HotKeySetting.json")
    hotkeys_json_string = obs.obs_data_get_json(hotkeys_json_file)
    hotkeys_json = obs.obs_data_create_from_json(hotkeys_json_string)

    array_recording = obs.obs_data_get_array(hotkeys_json, id_recording)
    hotkey_recording = obs.obs_hotkey_register_frontend(id_recording, "Switch Recording State", switch_recording)
    obs.obs_hotkey_load(hotkey_recording, array_recording)
    obs.obs_data_array_release(array_recording)

    obs.obs_data_release(hotkeys_json)
    obs.obs_data_release(hotkeys_json_file)