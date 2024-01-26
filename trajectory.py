import math
import numpy as np
import matplotlib.pyplot as plt
import os


# added 
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation



# Define your delta robot

# R = 150        #Base Radius [mm]
# L = 206        #Bicep Length [mm]
# l = 480        #Forearm Length [mm]
# r = 50         #Platform Radius [mm]
# MAG = -30



# Real robot
R = 282.5  #Base Radius [mm]
L = 510  #Bicep Length [mm]
l = 1100  #Forearm Length [mm]
r = 80 #Platform Radius [mm]
MAG=-21.4



def IKinem(X, Y, Z):
    x0 = -X
    y0 = -Y
    z0 = Z
    theta1 = IKinemTh(x0, y0, z0)
    
    x0 = -X * math.cos(2 * math.pi / 3) + (-Y) * math.sin(2 * math.pi / 3)
    y0 = -Y * math.cos(2 * math.pi / 3) - (-X) * math.sin(2 * math.pi / 3)
    z0 = Z
    theta3 = IKinemTh(x0, y0, z0)
    
    x0 = -X * math.cos(2 * math.pi / 3) - (-Y) * math.sin(2 * math.pi / 3)
    y0 = -Y * math.cos(2 * math.pi / 3) + (-X) * math.sin(2 * math.pi / 3)
    z0 = Z
    theta2 = IKinemTh(x0, y0, z0)
    
    if not (math.isnan(theta1) or math.isnan(theta2) or math.isnan(theta3)):
        fl = 0
    else:
        fl = -1  # non-existing
 
    return math.radians(theta1), math.radians(theta2), math.radians(theta3)#, fl

def IKinemTh(x0, y0, z0):
    global r, R, l, L
    y1 = -R
    y0 = y0 - r  # shift center to edge
    
    a = (x0 ** 2 + y0 ** 2 + z0 ** 2 + L ** 2 - l ** 2 - y1 ** 2) / (2 * z0)
    b = (y1 - y0) / z0
    # discriminant
    D = -(a + b * y1) ** 2 + L ** 2 * (b ** 2 + 1)
    # print("D: ", D)
    if D < 0:
        theta = math.nan  # non-existing
    else:
        yj = (y1 - a * b - math.sqrt(D)) / (b ** 2 + 1)
        zj = a + b * yj
        theta = math.atan(-zj / (y1 - yj))
        if yj > y1:
            theta = theta + math.pi
        theta = math.degrees(theta)
    return theta





def cubic_trajectory(t, q0, qf, tf):
    """
    Generates a cubic polynomial trajectory.
    :param t: current time
    :param q0: start position
    :param qf: final position
    :param tf: total time for the movement
    :return: current position q(t) on the trajectory
    """
    a0 = q0
    a1 = 0
    a2 = (3 * (qf - q0)) / (tf ** 2)
    a3 = (-2 * (qf - q0)) / (tf ** 3)

    q_t = a0 + a1 * t + a2 * t ** 2 + a3 * t ** 3
    return q_t

def linear_trajectory(t, q0, qf, tf):
    """
    Generates a linear trajectory.
    :param t: current time
    :param q0: start position
    :param qf: final position
    :param tf: total time for the movement
    :return: current position q(t) on the trajectory
    """
    q_t = q0 + (t / tf) * (qf - q0)
    return q_t

def linear_trajectory_for_incremental(t, q0, qf, tf):
    """
    Generates a linear trajectory.
    :param t: current time
    :param q0: start position
    :param qf: final position
    :param tf: total time for the movement
    :return: current position q(t) on the trajectory
    """
    q_t = (t / tf) * (qf - q0)
    return q_t

def plot(results):
    (t_output, theta_output, thetadot_output, thetadotdot_output, thetadotdotdot_output) = results

    print("plot_results")
    fig = plt.figure()
    fig.set_figheight(15)
    fig.set_figwidth(10)

    # plot theta_t 
    plt.subplot(511)
    plt.grid(True)
    plt.plot(t_output, theta_output, label=['theta_1', 'theta_2', 'theta_3'], linewidth=3)
    plt.title("angle-time plot", fontsize=20)

    plt.legend()
    plt.xlabel("time (ms)", fontsize=15)
    plt.ylabel("angle (deg)", fontsize=15)

    # plot theta_dot_t
    plt.subplot(512)
    plt.grid(True)
    plt.plot(t_output, thetadot_output, label=['theta_dot_1', 'theta_dot_2', 'theta_dot_3'], linewidth=3)
    plt.title("angular velocity-time plot", fontsize=20)
    plt.legend()
    plt.xlabel("time (ms)", fontsize=15)
    plt.ylabel("angular velocity (deg/s)", fontsize=15)

    # plot theta_ddot_t 
    plt.subplot(513)
    plt.grid(True)
    plt.plot(t_output, thetadotdot_output, label=['x', 'y', 'z'], linewidth=3)
    plt.title("angular acceleration-time plot", fontsize=20)
    plt.legend()
    plt.xlabel("time (ms)", fontsize=15)
    plt.ylabel("angular acceleration (deg/s^2)", fontsize=15)

    # plot theta_dddot_t 
    plt.subplot(514)
    plt.grid(True)
    plt.plot(t_output, thetadotdotdot_output, label=['x', 'y', 'z'], linewidth=3)
    plt.title("angular jerk-time plot", fontsize=20)
    plt.legend()
    plt.xlabel("time (ms)", fontsize=15)
    plt.ylabel("angular jerk (deg/s^3)", fontsize=15)

    # # plot EE-position 
    # plt.subplot(515)
    # plt.grid(True)
    # plt.plot(t_output, ee_pos_output, label=['x', 'y', 'z'], linewidth=10)
    # plt.title("position-time plot", fontsize=20)
    # plt.legend()
    # plt.xlabel("time (ms)", fontsize=15)
    # plt.ylabel("EE position (m)", fontsize=15)


    plt.tight_layout()
    plt.savefig("cubic spline  method.png")
    plt.clf()


class Coeff:
    def __init__(self, points):

        # initialzing the postion, velocity and acceleration vectors 
        # all of the vectors are n*3 matrices (e.g: for v we have 3 components in x, y and z direction)
        self.points = np.array(points)
        self.t = np.zeros(self.points.shape)
        self.n = self.points.shape[0]

        # time value assignment, shape = n*3
        for i in [0, 1, 2]:
            self.t[:, i] = np.linspace(0, self.n, num=self.n) 
        # self.t[1] = 0.8
        # self.t[3] = 3.8
        # self.t[4] = 4.9
        
        # print("t",self.t) # 0 to 9 divide same interval

        # time intervals (T), shape = n-1*3
        self.T = self.t[1:self.n, :] - self.t[0:self.n-1, :]

    def velocity(self, initial_velo=[0, 0, 0], final_velo=[0, 0, 0]):
        # initializing c_prime and A_prime matrices (last dimension is for the x, y, z directions)
        A_prime = np.zeros((3, self.n-2, self.n-2))
        c_prime = np.zeros((self.n-2, 3))
        velocity_profile = np.zeros(self.points.shape)
        T = self.T
        # T[-1,:] += 15
        # T[-2,:] += 5
    
        # print("T", T) # time intervals 
        

        # makin the A_prime and c_prime matrices 
        for i in range(A_prime.shape[1]):
            if i != 0:
                A_prime[:, i, i-1] = T[i+1]
            A_prime[:, i, i] = 2*(T[i] + T[i+1])
            if i != A_prime.shape[1]-1:
                A_prime[:, i, i+1] = T[i]

        for i in range(A_prime.shape[1]):
            c_prime[i, :] = 3/(T[i]*T[i+1])*(T[i]**2*(self.points[i+2, :] - self.points[i+1, :]) + T[i+1]**2*(self.points[i+1, :] - self.points[i, :]))
            if i == 0:
                c_prime[i, :] -= T[i+1]*initial_velo
            elif i == A_prime.shape[1]-1:
                c_prime[i, :] -= T[i]*final_velo

        # calculating v vector from A_prime and C_prime matrices 
        v = np.zeros((self.n-2, 3))
        for i in [0, 1, 2]:
            M = np.linalg.inv(A_prime[i, :, :])
            N = c_prime[:, i]
            v[:, i] = np.matmul(M, N) 

        # v[-1,:] -=0.05

        velocity_profile[0, :] = initial_velo
        velocity_profile[self.n-1, :] = final_velo
        velocity_profile[1:self.n-1, :] = v
        # print("v",v)

        return velocity_profile

    def coeff_matrix(self, velocity_profile):
        # initializing the coefficient matrix 
        # dim 1 == number of polynomials 				--> k = 0, ..., n-2
        # dim 2 == number of x, y, z directions 		--> 3
        # dim 3 == number of coeff in the polynomial 	--> (e.g: a[k][0][m] that m=0,1,2,3 is for the k_th point in x direction)
        coeff = np.zeros((self.n-1, 3, 4)) 
        
        # assigning the values of wrt position and velocity
        coeff[:, :, 0] = self.points[0:self.n - 1, :]
        coeff[:, :, 1] = velocity_profile[0:self.n - 1, :] 
        coeff[:, :, 2] = 1/self.T*( 3*(self.points[1:self.n, :] - self.points[0:self.n-1, :])/self.T - 2*velocity_profile[0:self.n-1, :] - velocity_profile[1:self.n, :])
        coeff[:, :, 3] = 1/self.T**2*( 2*(- self.points[1:self.n, :] + self.points[0:self.n-1, :])/self.T + velocity_profile[0:self.n-1, :] + velocity_profile[1:self.n, :])
        
        return coeff

def cubic_spline(path_criteria, max_velo):
    FREQUENCY = 800
    # print("path_criteria1:",path_criteria)
    path_criteria_tp = np.transpose(np.array(path_criteria))
    path_criteria_x = np.array(path_criteria[0])
    path_criteria_y = np.array(path_criteria[1])
    path_criteria_z = np.array(path_criteria[2])
    n = path_criteria_x.shape[0] - 1
    # print("path_criteria",path_criteria_tp)
    # print("path_criteria[0]",path_criteria_tp[0])

    # find overall T_total
    d = 0 # rough distance
    for i in range(1, n+1):
        d += ((path_criteria_x[i] - path_criteria_x[i-1])**2 + (path_criteria_y[i] - path_criteria_y[i-1])**2 + (path_criteria_z[i] - path_criteria_z[i-1])**2)**0.5
    d = d*1.5

    T_total = d/max_velo

    # calculating IK for path criteria
    theta = np.zeros(path_criteria_tp.shape)

    for idx, i in enumerate(path_criteria_tp): #path_criteria_tp: [[x,y,z],[x,y,z],[x,y,z]...]
        # print("i", i)
        x,y,z = i

        theta[idx] = IKinem(x,y,z)
        # print("IKinem(x,y,z)",IKinem(x,y,z))

        q_end = tuple(x_rad * MAG for x_rad in theta[idx])
        theta[idx] = tuple(sum(elem) for elem in zip(q_end, (4.41710, 3.73270, 6.14191)))

        # print("theta[idx]",theta[idx])


        # theta[idx] = IKinem(x,y,z)# IKinem(x,y,z)

    # find the coeff matrix
    coeff = Coeff(theta) 	# initializing the coeff class (for interpolating theta profile)
    velocity_profile = coeff.velocity() 	# calculating velocity profile
    coeff_matrix = coeff.coeff_matrix(velocity_profile) 	# calculating coefficient matrix of a_ij

    t =  coeff.t.transpose()[0]

    # print("t",t) # [0.    1.125 2.25  3.375 4.5   5.625 6.75  7.875 9.   ]



    # getting the outputs (inputs of the stepper motor)
    t_output = np.arange(0, math.ceil(T_total*FREQUENCY))

    # build T vector for using on coeff matrix 
    T_output = np.arange(0, math.ceil(T_total*FREQUENCY))/math.ceil(T_total*FREQUENCY)*t[-1]
    T_old = np.copy(T_output) # not important 
    # print("T_old",T_old) # 0 to point num(9). interval = tick
    counter = 1
    for idx, i in enumerate(T_output):
        try:
            if i>= t[counter+1]:
                counter += 1
        except: 
            pass 
        if i >= t[counter]:
            T_output[idx] = T_output[idx] - t[counter]
    
    # print("T_output", T_output) # here the interval of each line.

    T_output = np.transpose(np.array([T_output, T_output, T_output]))

    # get final profile outputs of position, velocity, acceleration, jerk
    theta_output 			= np.zeros((t_output.shape[0], 3))
    thetadot_output 		= np.zeros((t_output.shape[0], 3))
    thetadotdot_output 		= np.zeros((t_output.shape[0], 3))
    thetadotdotdot_output   = np.zeros((t_output.shape[0], 3))
    # print("t_output", t_output)
    # print("T_output:", T_output)
    counter = 0 
    # print(T_old)
    
    for i in t_output: # all ticks . counter is the line num.
        try:
            if T_old[i] >= t[counter+1]:
                counter += 1
        except: 
            pass 

        theta_output[i] = (np.transpose(coeff_matrix[counter])[0] + \
                                        np.transpose(coeff_matrix[counter])[1]*T_output[i] + \
                                        np.transpose(coeff_matrix[counter])[2]*T_output[i]**2 + \
                                        np.transpose(coeff_matrix[counter])[3]*T_output[i]**3) # * MAG
        # print("theta_output[i]", theta_output[i])

        # 각 곡선의 다항식을 구함.
        
        thetadot_output[i] = np.transpose(coeff_matrix[counter])[1] + \
                                        np.transpose(coeff_matrix[counter])[2]*T_output[i]*2 + \
                                        np.transpose(coeff_matrix[counter])[3]*T_output[i]**2*3
        
        thetadotdot_output[i] = np.transpose(coeff_matrix[counter])[2]*2 + \
                                        np.transpose(coeff_matrix[counter])[3]*T_output[i]*6
        
        thetadotdotdot_output[i] = np.transpose(coeff_matrix[counter])[3]*6


    # ee_pos_output = np.zeros(theta_output.shape)
    # print(theta_output.shape)
    # for idx, i in enumerate(theta_output):
    #     ee_pos_output[idx] = robot.forward_kin(theta_output[idx])



    t_output = np.transpose(np.array([t_output, t_output, t_output]))

    theta_output = theta_output.tolist()

    return (t_output, theta_output, thetadot_output, thetadotdot_output, thetadotdotdot_output)





def higher_order_poly_3pt(q0, q1, q2): # thi will only work if you have 3 points to interpolate 
    FREQUENCY = 5000
    
    x0,y0,z0 = q0
    x1,y1,z1 = q1
    x2,y2,z2 = q2


    q0 = np.array(IKinem(x0,y0,z0))
    # print("IKinem",IKinem(x0,y0,z0))
    q1 = np.array(IKinem(x1,y1,z1))
    q2 = np.array(IKinem(x2,y2,z2))

    a0 = q0
    a1 = np.array([0, 0, 0])
    a2 = np.array([0, 0, 0])
    a3 = np.array([0, 0, 0])
    a4 = 256*q1 - 163*q0 - 93*q2
    a5 = 596*q0 - 1024*q1 + 428*q2
    a6 = 1536*q1 - 838*q0 - 698*q2
    a7 = 532*q0 - 1024*q1 + 492*q2
    a8 = 256*q1 - 128*q0 - 128*q2

    t = np.array(range(FREQUENCY))/FREQUENCY
    q_t = np.zeros((FREQUENCY, 3))
    qdot_t = np.zeros((FREQUENCY, 3))
    qddot_t = np.zeros((FREQUENCY, 3))
    qdddot_t = np.zeros((FREQUENCY, 3))


    for i in range(FREQUENCY):
        q_t[i] = (a8*t[i]**8 + a7*t[i]**7 + a6*t[i]**6 + a5*t[i]**5 + a4*t[i]**4 + a3*t[i]**3 + a2*t[i]**2 + a1*t[i] + a0)* MAG
        qdot_t[i] = 8*a8*t[i]**7 + 7*a7*t[i]**6 + 6*a6*t[i]**5 + 5*a5*t[i]**4 + 4*a4*t[i]**3 + 3*a3*t[i]**2 + 2*a2*t[i] + a1 
        qddot_t[i] = 56*a8*t[i]**6 + 42*a7*t[i]**5 + 30*a6*t[i]**4 + 20*a5*t[i]**3 + 12*a4*t[i]**2 + 6*a3*t[i] + 2*a2
        qdddot_t[i] = 336*a8*t[i]**5 + 210*a7*t[i]**4 + 120*a6*t[i]**3 + 60*a5*t[i]**2 + 24*a4*t[i] + 6*a3
        # print("q_t[i]",q_t[i])

    # temp_t = 1
    # temp  = a8*temp_t**8 + a7*temp_t**7 + a6*temp_t**6 + a5*temp_t**5 + a4*temp_t**4 + a3*temp_t**3 + a2*temp_t**2 + a1*temp_t + a0
    # print(temp)

    # ee_pos = np.zeros((FREQUENCY, 3))
    # for idx, i in enumerate(np.array(q_t)):
    #     ee_pos[idx] = robot.forward_kin(q_t[idx])

    q_t = q_t.tolist()
    results = (t, q_t, qdot_t, qddot_t, qdddot_t)

    return results

def generate_mltp(point0, point1, point2):

  
    results = higher_order_poly_3pt(point0, point1, point2)

    (t_output, theta_output, thetadot_output, thetadotdot_output, thetadotdotdot_output) = results
    plot(results)
    print("done?")
    

    return theta_output

def generate_cubic_spline(pre_place, pick, place, traj_configs=[]):

    pick_value = traj_configs[0] # a1
    total_vel = int(float(traj_configs[1])) # a2
    place_value = traj_configs[2] # a3
    pick_curve= int(float(traj_configs[3])) # b
    place_curve = traj_configs[4] # c
    pick_depth = traj_configs[5] # d
    place_depth = traj_configs[6] # e
    # points=[[-100,200,-320],
    #     [-100,200,-340],
    #     [-100,200,-380],
    #     [-100,200,-400]]
    
    # pick and pick
    # points=[[-100,200,-400],  
    #     [-100,200,-360],
    #     [-100,190,-310],
    #     [-100,100,-300],
    #     [-100,0,-300],
    #     [-100,-100,-300],
    #     [-100,-190,-310],
    #     [-100,-200,-360],
    #     [-100,-200,-400],
    #     ]


    # points=[[-100,0,-300],
    #    [-100,100,-300],
    #     [-100,190,-310],
    #     [-100,200,-325],
    #     [-100,200,-345],
    #     [-100,200,-360]
    #     ]
    print("traj_configs", traj_configs)

    pre_place_x=pre_place[0]
    pre_place_y=pre_place[1]
    pre_place_z=pre_place[2]
    pick_x = pick[0]
    pick_y = pick[1]
    pick_z = pick[2]
    place_x=place[0]
    place_y=place[1]
    place_z=place[2]

    # x1 = (pick_x + pre_place_x) / 2
    # y1 = (pick_y + pre_place_y) / 2

   
    
    x1 = (pick_x*3 + pre_place_x) / 4
    y1 = (pick_y*3 + pre_place_y) / 4

    # x0 = (pre_place_x + x1 )/2
    # y0 = (pre_place_y + y1 )/2


    x2 = (pick_x*(40-pick_curve) + pre_place_x) / 40
    y2 = (pick_y*(40-pick_curve) + pre_place_y) / 40

    x3 = (pick_x*(40-pick_curve) + place_x) / 40
    y3 = (pick_y*(40-pick_curve) + place_y) / 40

    # x4 = (pick_x + place_x) / 2
    # y4 = (pick_y + place_y) / 2 

    x4 = (pick_x*3 + place_x) / 4
    y4 = (pick_y*3 + place_y) / 4

    # x5 = ( place_x + x4 ) /2
    # y5 = ( place_y + y4 ) /2
    
    pick_curve_z = math.sqrt((int(pick_x-x2))**2 + (int(pick_y - y2))**2)
    print("int(pick_x-x2",int(pick_x-x2),int(pick_y - y2), pick_curve_z  )

    if (pre_place_z - pick_curve_z) > pick_z:
        points=[[pre_place_x, pre_place_y, pre_place_z],
        # [x0, y0, pre_place_z ],
        [x1, y1, pre_place_z],
        # [x2, y2, pre_place_z - pick_curve_z],
        [pick_x, pick_y, pick_z],
        # [x3,y3,place_z-pick_curve_z],
        [x4, y4, place_z],
        # [x5, y5, place_z],
        [place_x, place_y, place_z]
        ]


    # points = [[pre_place_x,pre_place_y,pre_place_z],
    # [pick_x,pick_y,pick_z],
    # [place_x,place_y,place_z]]

    ## Testing
    # points=[[0,0,-800],
    #    [200,0,-800],
    #    [0,0,-800],
    #     ]

    ##  Set pick values
    pick_value = int(float(pick_value))  # Convert the first element to an integer

    # Calculate the number of additional points to insert
    num_points_to_insert = pick_value if pick_value >= 1 else 0

    # Calculate the interval between points
    if num_points_to_insert > 0:
        distance_between_points = (pick_z - (pre_place_z - 10)) / (num_points_to_insert+1)
        print("distance_between_points",distance_between_points)

    # Insert points with equal intervals between pick_z and pre_place_z-10
    if num_points_to_insert > 0:
        for i in range(num_points_to_insert):
            new_z = pre_place_z - pick_curve_z+ (i + 1) * distance_between_points
            points.insert(2 + i, [pick_x, pick_y, new_z])
            points.insert(4 + i, [pick_x, pick_y, new_z])
            

    # Print the updated points list
    for i, point in enumerate(points):
        print(f"Point {i+1}: {point}")

    print("trajectory spot",points)

    

    path_criteria=[list(pair) for pair in zip(*points)]
    max_velo=total_vel #900

    cubic_spline_results = cubic_spline(path_criteria,max_velo)
    (t_output, theta_output, thetadot_output, thetadotdot_output, thetadotdotdot_output) = cubic_spline_results
    # plot(cubic_spline_results)
    # path_plot(path_criteria, points)
    

    # print("Final output: ",theta_output)
    # print("theta_output",theta_output)

    return theta_output


def path_plot(path_criteria, points):
    # print("path_criteria", path_criteria)
    
    # DRAW INITIAL AND FINAL STATE
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot initial and final states
    ax.scatter(path_criteria[0], path_criteria[1], path_criteria[2], color='blue', label='Initial/Final State')

    # ANIMATION
    def update(num, data, line):
        line.set_data(data[:2, :num])
        line.set_3d_properties(data[2, :num])

    ee_pos_t = np.transpose(points)
    N = ee_pos_t.shape[1]
    print("N",N)

    line, = ax.plot(ee_pos_t[0, :1], ee_pos_t[1, :1], ee_pos_t[2, :1], 'b')  # Initialize the line

    ani = animation.FuncAnimation(fig, update, N, fargs=(ee_pos_t, line), interval=10000/N, blit=False)
    ani.save('animation.gif',writer='pillow', fps=15)

    




def generate_trajectory(q_start, q_end, tf, dt):
    """
    Generates a trajectory for the delta robot from start to end positions using cubic interpolation.
    :param q_start: start joint angles (theta1, theta2, theta3)
    :param q_end: end joint angles (theta1, theta2, theta3)
    :param tf: total time for the movement
    :param dt: time step
    :return: a list of joint angles for each time step
    """
    trajectory = []
    t = 0

    # q_end = np.array(q_end).dot(M)
    

    # Under line is for calibration of control and real radian value.

    # print(q_start, q_end)
    q_start = tuple(x_rad for x_rad in q_start)
    #q_end = tuple(x_rad for x_rad in q_end)
    q_end = tuple(x_rad * MAG for x_rad in q_end)
    # print("q_end",q_end)
    q_end = tuple(sum(elem) for elem in zip(q_end, (4.41710, 3.73270, 6.14191)))
    print("q_end", q_end)

    while t <= tf:
        q_t = [linear_trajectory(t,   q_start[i], q_end[i], tf) for i in range(3)]
        #q_t = [linear_trajectory_for_incremental(dt,   q_start[i], q_end[i], tf) for i in range(3)]
        trajectory.append(q_t)
        t += dt

    return trajectory


def generate_trajectory_xyz_M(start, end, tf, dt, M):
    

    trajectory = []
    t = 0
    trajectory_xyz = []

    while t<= tf:
        x,y,z = [cubic_trajectory(t, start[i], end[i], tf) for i in range(3)]

        # for plot
        trajectory_xyz.append((x,y,z))


        # get theta 
        # t1, t2, t3 = IKinem(x,y,z)

        theta = np.array(IKinem(x,y,z))
        
        t1, t2, t3 = theta.dot(M)

        
        # Under line is for calibration of control and real radian value.

        # print(q_start, q_end)
        q = (t1*MAG, t2*MAG, t3*MAG)
        # print("q",q)



        trajectory.append(q)
        t += dt
    return trajectory, trajectory_xyz # trajectory xyz for plot


def generate_trajectory_xyz(start, end, tf, dt):
    trajectory = []
    t = 0
    trajectory_xyz = []



    while t<= tf:
        x,y,z = [linear_trajectory(t, start[i], end[i], tf) for i in range(3)]
        # print("xyz", x,y,z)
        
    
        # trajectory_xyz.append((x,y,z))

        t1, t2, t3 = IKinem(x,y,z)

        q = (t1*MAG, t2*MAG, t3*MAG)

        q_end = tuple(sum(elem) for elem in zip(q, (4.41710, 3.73270, 6.14191)))
        
        trajectory.append(q_end)
        t += dt

    print("trajectory", trajectory)
    return trajectory



def calibration(q_value):
    # Under line is for calibration of control and real radian value.

    # print(q_start, q_end)
    q_value = list(x_rad*MAG for x_rad in q_value)
    return q_value

def get_distance(start_pos, end_pos):
    if start_pos == end_pos:
        return 0

    tdiff = 0
    for start_k, end_k in zip(start_pos, end_pos):
        diff = abs(start_k-end_k)
        tdiff += diff**2
    
    return math.sqrt(tdiff)

def helix_curve():
    # Parameters
    R = 100
    a = (380 - 530) / (8 * np.pi)  # Adjust pitch for new Z range
    b = -380  # Start at -380 for Z

    # Generate parameter values within a suitable range
    t = np.linspace(0, 8 * np.pi, 200)

    # Calculate coordinates using helix equations
    x = R * np.cos(t)
    y = R * np.sin(t)
    z = a * t + b

    # Filter points within specified ranges
    filtered_points = []
    for xi, yi, zi in zip(x, y, z):
        if -200 <= xi <= 200 and -200 <= yi <= 200 and -530 <= zi <= -380:
            filtered_points.append((xi, yi, zi))

    # print(len(filtered_points))
    return filtered_points
    # # Display the filtered points
    # for point in filtered_points:
    #     print(point)

def trajectory_config(move_list_path):
    with open(move_list_path,'r') as file:
        for line in file:
            parts = line.split()
            break    
        print("traj_configs",parts)
    
    return parts


if __name__ == '__main__':
    # Boundary
    '''
    X: -200 ~ 200
    Y: -200 ~ 200
    Z: -378 ~ -538
    '''
    # Test
    # start_pos = (0, 0, -350)
    # end_pos = (0, 0, -500)
    # print(get_distance(start_pos, end_pos))
    # theta_start = IKinem(*start_pos)
    # theta_end = IKinem(*end_pos)

    # move_vel = 100 # mm/s
    # move_time = get_distance(start_pos, end_pos) / move_vel
    result0= generate_trajectory_xyz((0, 0, -900), 
                                                (100,0,-900),
                                                3,
                                                0.0005)

    # Read coordinates from the file
    current_dir = os.path.dirname(os.path.realpath(__file__))
    move_list_path = os.path.join(current_dir, "../pyqt_delta/document/move_list.txt" )

    traj_configs = trajectory_config(move_list_path)

    generate_cubic_spline((0,0,-800), (200,200,-900),(-200, 0, -800), traj_configs)


    # exit()
    # trajectory = generate_trajectory(theta_start, theta_end, tf=move_time, dt=0.1)
    # print(len(trajectory))
    # for point in trajectory:
    #     print(point)