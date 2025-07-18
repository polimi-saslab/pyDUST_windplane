def generate_reference(Omega, N_blades, Hub_offset,R_11,R_13,R_31,Rt_11,Rt_13,Rt_31):
    content = f'''
! Fix reference
reference_tag = Fix
parent_tag = 0  ! 0 : absolute reference frame
origin = (/0.,0.,0./)
orientation = (/1.,0.,0., 0.,1.,0., 0.,0.,1./)
multiple = F
moving = F
 
! Wing reference
reference_tag = Wing
parent_tag = Fix
origin = (/0.,0.,0./)
orientation = (/{R_11},0.,{R_13}, 0.,1.,0., {R_31},0.,{R_11}/)
multiple = F
moving = F
 
! Left Rotor reference
reference_tag = Hub_l
parent_tag = Wing
origin = (/-1.5,-5.2,0/)
orientation = (/{Rt_11},0.,{Rt_13}, 0.,1.,0., {Rt_31},0.,{Rt_11}/)
moving = F
multiple = T
multiplicity = {{
    mult_type = rotor
    n_blades = {N_blades}
    rot_axis = (/1., 0., 0./)
    rot_rate = {Omega} ! rad/s
    psi_0 = 0 ! rad
    hub_offset = {Hub_offset}
    n_dofs = 0
}}
 
! Right Rotor reference
reference_tag = Hub_r
parent_tag = Wing
origin = (/-1.5,5.2,0/) ! 1.32
orientation = (/{Rt_11},0.,{Rt_13}, 0.,1.,0., {Rt_31},0.,{Rt_11}/)
moving = F
multiple = T
multiplicity = {{
    mult_type = rotor
    n_blades = {N_blades}
    rot_axis = (/1., 0., 0./)
    rot_rate = -{Omega} ! rad/s (opposite direction for right rotor)
    psi_0 = 0 ! rad
    hub_offset = {Hub_offset}
    n_dofs = 0
}}
'''
    return content



def generate_dust(u_x,u_y,u_z,dt,tend,tout):
    content = f'''
    basename = ./output/test 
    geometry_file = geo_input.h5
    reference_file = references.in 

    ! free-stream condition 
    u_inf = (/{u_x} , {u_y} , {u_z}/)
    rho_inf = 1.225

    ! Timing 
    tstart = 0.
    tend = {tend}
    dt = {dt} 
    dt_out = {tout} 

    ! Model param 
    penetration_avoidance = T

    ! wake param 
    !rigid_wake = F
    n_wake_panels = 1
    n_wake_particles = 500000
    particles_box_min = (/  -150, -15, -5 /)
    particles_box_max = (/  5,  15,  5/)

    ! FMM 
    fmm = T
    vortstretch = F
    diffusion = F

    !! octree param 
    box_length = 10
    n_box = (/16, 2 , 2/)
    octree_origin = (/ -150, -10, -10/)


    !!
    n_octree_levels = 5
    min_octree_part =5
    multipole_degree = 2
    '''
    return content

def generate_dust_post(end_res):
    content = f'''
    data_basename = output/test 
    basename = postpro/test
    !
    ! Visualisation 
    analysis = {{
        type = viz
        name = visual 
        start_res = 1 
        end_res = {end_res}
        step_res = 1
        format = vtk ! tecplot  
        wake = T 
        !separate_wake = T 
        variable = vorticity_vector
        variable = vorticity
        variable = cp
        variable = pressure
    }}

    analysis = {{
        type = sectional_loads
        name = sec_wing
        start_res = 1
        end_res = {end_res}
        step_res = 1
        format = dat
        average = F
        component = Wing
        axis_nod = (/ 0.0, 0.0, 0.0 /)
        axis_dir = (/ 0.0, 1.0, 0.0 /)
        lifting_line_data = F
        vortex_lattice_data = T
    }}

    analysis = {{
        type = integral_loads
        name = int_wing
        start_res = 1
        end_res = {end_res}
        step_res = 1
        format = dat
        component = Wing
        reference_tag = 0
    }}


    analysis = {{
        type = sectional_loads
        name = sec_rot_left
        start_res = 1
        end_res = {end_res}
        step_res = 1
        format = dat
        average = F
        component = Rotorl__01
        axis_nod = (/ 0.0, 0.0, 0.0 /)
        axis_dir = (/ 0.0, 1.0, 0.0 /)
        lifting_line_data = T
        vortex_lattice_data = F
        reference_tag = Hub_l
    }}
    
    analysis = {{
        type = integral_loads
        name = int_rot_left
        start_res = 1
        end_res = {end_res}
        step_res = 1
        format = dat
        component = Rotorl
        average = F
        reference_tag = Hub_l
    }}

    analysis = {{
        type = sectional_loads
        name = sec_rot_right
        start_res = 1
        end_res = {end_res}
        step_res = 1
        format = dat
        average = F
        component = Rotorr__01
        axis_nod = (/ 0.0, 0.0, 0.0 /)
        axis_dir = (/ 0.0, 1.0, 0.0 /)
        lifting_line_data = T
        vortex_lattice_data = F
        reference_tag = Hub_r
    }}

    analysis = {{
        type = integral_loads
        name = int_rot_right
        start_res = 1
        end_res = {end_res}
        step_res = 1
        format = dat
        component = Rotorr
        average = F
        reference_tag = Hub_r
    }}
    '''
    return content


def save_to_file(content, file_path):
    with open(file_path, "w") as file:
        file.write(content)
    print(f"File '{file_path}' has been created.")
