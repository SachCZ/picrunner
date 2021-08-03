def write_control(grid, final_time, opened_file):
    opened_file.write("begin:control\n")
    opened_file.write("    nx = {}\n".format(int(grid.nx + 1)))
    opened_file.write("    ny = {}\n".format(int(grid.ny + 1)))
    opened_file.write("    t_end = {}\n".format(final_time))
    opened_file.write("    x_min = {}\n".format(grid.xmin))
    opened_file.write("    x_max = {}\n".format(grid.xmax))
    opened_file.write("    y_min = {}\n".format(grid.ymin))
    opened_file.write("    y_max = {}\n".format(grid.ymax))
    opened_file.write("end:control\n\n")

def write_boundary(grid, opened_file):
    opened_file.write("begin:boundaries\n")
    opened_file.write("    bc_x_min = {}\n".format(grid.bc_xmin))
    opened_file.write("    bc_x_max = {}\n".format(grid.bc_xmax))
    opened_file.write("    bc_y_min = {}\n".format(grid.bc_ymin))
    opened_file.write("    bc_y_max = {}\n".format(grid.bc_ymax))
    opened_file.write("end:boundaries\n\n")
