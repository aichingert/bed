import sys
import subprocess

# TODO: define structure which holds system calls with values for the tests

def main():
    sys.argv.pop(0)
    assert len(sys.argv) == 1, "error [gtes]: expected a `test_file.byl`"

    subprocess.call(["../code/./bylc"])

    cmd = ["strace", "../code/./byl", sys.argv[0]]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    o, e = proc.communicate(1000)
    aout = e.decode("ascii")
    print(aout)
    line = aout.split("\n")
    [print("'", x, "'") for x in line]


if __name__ == "__main__":
    main()

