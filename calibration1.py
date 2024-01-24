

# calibration
# workspace = 920 * 920 * 510
# x = 460 ~ -460
# y = 460 ~ -460
# z = -700 ~ -1090 (연구실 컨베이어 기준) => 390

# 연구실 컨베이어
#   old_robot 
#
#    -y
# -x  +  +x     
#    +y
#
#  monitor

z = 900 # 칼리브레이션 z 높이 고정

left_up = (-460, -460 , z)
right_up = (460, -460, z)
left_down = (-460, 460, z)
right_down = (460, 460, z)

point_41 = zero = (0, 0, z) 

"""
calibration => 
L_up                  R_up
    1   3   5   7   9
    
    19  21  23  25  27
        
    37  39  41  43  45
    
    55  57  59  61  63

    73  75  77  79  81 
L_down                R_down
"""

point_1 = (-400, -400, z)
point_2 = (-400, -300, z)
point_3 = (-400, -200, z)
point_4 = (-400, -100, z)
point_5 = (-400, 0, z)
point_6 = (-400, 100, z)
point_7 = (-400, 200, z)
point_8 = (-400, 300, z)
point_9 = (-400, 400, z)

point_10 = (-300, -400, z)
point_11 = (-300, -300, z)
point_12 = (-300, -200, z)
point_13 = (-300, -100, z)
point_14 = (-300, 0, z)
point_15 = (-300, 100, z)
point_16 = (-300, 200, z)
point_17 = (-300, 300, z)
point_18 = (-300, 400, z)

point_19 = (-200, -400, z)
point_20 = (-200, -300, z)
point_21 = (-200, -200, z)
point_22 = (-200, -100, z)
point_23 = (-200, 0, z)
point_24 = (-200, 100, z)
point_25 = (-200, 200, z)
point_26 = (-200, 300, z)
point_27 = (-200, 400, z)

point_28 = (-100, -400, z)
point_29 = (-100, -300, z)
point_30 = (-100, -200, z)
point_31 = (-100, -100, z)
point_32 = (-100, 0, z)
point_33 = (-100, 100, z)
point_34 = (-100, 200, z)
point_35 = (-100, 300, z)
point_36 = (-100, 400, z)

point_37 = (0, -400, z)
point_38 = (0, -300, z)
point_39 = (0, -200, z)
point_40 = (0, -100, z)
point_41 = (0, 0, z)
point_42 = (0, 100, z)
point_43 = (0, 200, z)
point_44 = (0, 300, z)
point_45 = (0, 400, z)

point_46 = (100, -400, z)
point_47 = (100, -300, z)
point_48 = (100, -200, z)
point_49 = (100, -100, z)
point_50 = (100, 0, z)
point_51 = (100, 100, z)
point_52 = (100, 200, z)
point_53 = (100, 300, z)
point_54 = (100, 400, z)

point_55 = (200, -400, z)
point_56 = (200, -300, z)
point_57 = (200, -200, z)
point_58 = (200, -100, z)
point_59 = (200, 0, z)
point_60 = (200, 100, z)
point_61 = (200, 200, z)
point_62 = (200, 300, z)
point_63 = (200, 400, z)

point_64 = (300, -400, z)
point_65 = (300, -300, z)
point_66 = (300, -200, z)
point_67 = (300, -100, z)
point_68 = (300, 0, z)
point_69 = (300, 100, z)
point_70 = (300, 200, z)
point_71 = (300, 300, z)
point_72 = (300, 400, z)

point_73 = (400, -400, z)
point_74 = (400, -300, z)
point_75 = (400, -200, z)
point_76 = (400, -100, z)
point_77 = (400, 0, z)
point_78 = (400, 100, z)
point_79 = (400, 200, z)
point_80 = (400, 300, z)
point_81 = (400, 400, z)