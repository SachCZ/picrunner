import subprocess



def main():
    epoch_exe = "/home/martin/CLionProjects/epoch-4.17.14/epoch2d/bin/epoch2d"
    with subprocess.Popen(
            ["mpirun", "-np", "4", epoch_exe],
            stdin=subprocess.PIPE
    ) as proc:
        proc.communicate(b"cone")


if __name__ == '__main__':
    main()
