# 각종 세팅값을 설정
import yaml

yaml_file_path = '../move/config.yaml'  
with open(yaml_file_path, 'r') as file:
    # YAML 파일을 읽고 파싱하여 Python 딕셔너리로 변환
    config = yaml.safe_load(file)

# class set_delta():
#     def xyz_origin(self):

# 현재 좌표 값 받아오기
x = 0
y = 0
z = -850

# 한계 설정
x_max = config['move']['max_x_area'] #  460
x_min = config['move']['min_x_area'] # -460 

y_max = config['move']['max_y_area'] # 460
y_min = config['move']['min_y_area'] # -460

z_max = config['move']['max_z_area'] # -700
z_min = config['move']['min_z_area'] # -1090

# 토픽 연속 값 주기 (1000ms = 1초)
ms = config['manual']['ms']  # 100

# move 한계값
round = config['trajectory']['curve_r']

path_speed_max = config['trajectory']['path_speed_max'] # 2000
path_speed_min = config['trajectory']['path_speed_min'] # 0
bending_max = config['trajectory']['bending_max'] # 90
bending_min = config['trajectory']['bending_min'] # 0
Deceleration_max = config['trajectory']['deceleration_max'] # 1.0
Deceleration_min = config['trajectory']['deceleration_min'] # 0
sync_max = config['trajectory']['sync_max'] # 30
sync_min = config['trajectory']['sync_min'] # 0
pick_sync = config['trajectory']['pick_sync']
place_sync = config['trajectory']['place_sync']


# import yaml

# # Function to read and parse the YAML file
# def load_config(file_path):
#     with open(file_path, 'r') as file:
#         return yaml.safe_load(file)

# # Path to the YAML file
# config_path = 'config.yaml'

# # Load the contents of config.yaml
# config = load_config(config_path)

# # Variables related to the 'move' section
# x_min = config['move']['min_x_area']
# x_max = config['move']['max_x_area']
# y_min = config['move']['min_y_area']
# y_max = config['move']['max_y_area']
# z_min = config['move']['min_z_area']
# z_max = config['move']['max_z_area']

# up_position = config['move']['up']
# pick_position = config['move']['pick']
# place_x = config['move']['place_x']
# place_y = config['move']['place_y']
# y_offset = config['move']['y_offset']
# x_offset = config['move']['x_offset']

# # Variables related to the camera
# cam2robot = config['move']['cam2robot']
# cam_min_x = config['move']['cam_min_x']
# cam_max_x = config['move']['cam_max_x']
# conveyor_width = config['move']['conveyor_width']
# cam_y_mm = config['move']['cam_y_mm']
# cam_y_pixel = config['move']['cam_y_pixel']
# x_ratio = config['move']['x_ratio']
# y_ratio = config['move']['y_ratio']

# # Variables related to home positions
# home1 = {'label': config['move']['home1']['label'], 'x': config['move']['home1']['x'], 'y': config['move']['home1']['y'], 'z': config['move']['home1']['z']}
# home2 = {'label': config['move']['home2']['label'], 'x': config['move']['home2']['x'], 'y': config['move']['home2']['y'], 'z': config['move']['home2']['z']}
# home3 = {'label': config['move']['home3']['label'], 'x': config['move']['home3']['x'], 'y': config['move']['home3']['y'], 'z': config['move']['home3']['z']}
# home4 = {'label': config['move']['home4']['label'], 'x': config['move']['home4']['x'], 'y': config['move']['home4']['y'], 'z': config['move']['home4']['z']}

# # Variables related to the 'trajectory' section
# trajectory_up = config['trajectory']['up']
# pick_z = config['trajectory']['pick_z']
# trajectory_speed = config['trajectory']['speed']
# curve_r = config['trajectory']['curve_r']
# pick_decel = config['trajectory']['pick_decel']
# place_decel = config['trajectory']['place_decel']
# decel_start = config['trajectory']['decel_start']
# place_down_mode = config['trajectory']['place_down_mode']

# # Variables related to the 'manual' section
# manual_ms = config['manual']['ms']