import sys
import subprocess

PAGE_SIZE = 4096

def helper_align_to_page_size(n):
    return ((n + PAGE_SIZE - 1) & (~(PAGE_SIZE - 1)))

def helper_parse_args(call, name, n):
    args = call[len(name) + 1:].split(',')
    assert len(args) == n, "error [gtes]: expected {0} arguments for {1}".format(n, name)
    return args

def test_sys_read(line, fd, count):
    call, call_ret = line.split('=')
    assert call.startswith("read"), "error [gtes]: expected sys read but got `{0}`".format(call)

    args = helper_parse_args(call[:call.find('"')] + call[call.rfind('"') + 1:], "read", 3)
    size = int(args[2].rstrip()[:-1])

    assert fd == int(args[0]),  "error [gtes]: expected fd to be the same as received by open"
    assert count == size, "error [gtes]: expected to read `{0}` bytes but got `{1}`".format(count, size)
    size = int(call_ret)
    assert count == size, "error [gtes]: expected to read `{0}` bytes but got `{1}`".format(count, size)

def test_sys_open(line, name):
    call, call_ret = line.split('=')
    s_open, file_name, s_open_mode = call.split('"')
    assert s_open.startswith("open"), "error [gtes]: expected compiler to open the input file"
    assert file_name == name, "error [gtes]: expected compiler to open the provided file"
    return int(call_ret)

def test_sys_close(line, fd):
    call, call_ret = line.split('=')

    assert call.startswith("close"), "error [gtes]: expected sys close but got `{0}`".format(call)
    args = helper_parse_args(call, "close", 1)
    assert int(args[0].rstrip()[:-1]) == fd, "error [gtes]: closing wrong fd"
    assert int(call_ret) == 0, "error [gtes]: failed to close file"

def test_sys_lseek(line, fd, mode, byts):
    call, call_ret = line.split('=')
    size = int(call_ret)

    assert call.startswith("lseek"), "error [gtes]: expected compiler to seek the size"
    args = helper_parse_args(call, "lseek", 3)
    assert fd == int(args[0]),  "error [gtes]: expected fd to be the same as received by open"
    assert args[2].lstrip().startswith(mode), "error [gtes]: does not seek until the end"
    assert byts == size, "error [gtes]: expected to read `{0}` bytes but got `{1}`".format(byts, size)

def test_sys_mmap(line, byts):
    call, _ = line.split('=')
    assert call.startswith("mmap"), "error [gtes]: expected sys mmap but got `{0}`".format(call)
    args = helper_parse_args(call, "mmap", 6)
    size = int(args[1])
    assert size == byts, "error [gtes]: allocating `{0}` instead of `{1}` bytes".format(size, byts)

def test_sys_exit(line, code):
    call, _ = line.split('=')
    assert call.startswith("exit"), "error [gtes]: expected sys exit but got `{0}`".format(call)
    args = helper_parse_args(call, "exit", 1)
    exit_code = int(args[0].rstrip()[:-1]) 
    assert exit_code == code, "error [gtes]: bylc exited with `{0}` but should have with `{1}`".format(exit_code, code)

def main():
    sys.argv.pop(0)
    assert len(sys.argv) == 1, "error [gtes]: expected a `test_file.byl`"

    subprocess.call(["../code/./bylc"])

    cmd = ["strace", "../code/./byl", sys.argv[0]]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    name = sys.argv[0]
    file = open(name, "r")
    read = file.read()
    byts = len(read)
    file.close()

    o, e = proc.communicate()
    aout = e.decode("ascii")
    line = aout.split("\n")
    line = line[1:len(line) - 2]

    [print(x) for x in line]
    assert len(line) >= 6, "error [gtes]: expected compiler to make at least 6 syscalls"
    fd = test_sys_open(line[0], name)
    test_sys_lseek(line[1], fd, "SEEK_END", byts)
    test_sys_lseek(line[2], fd, "SEEK_SET", 0)
    test_sys_mmap(line[3], helper_align_to_page_size(byts))
    test_sys_read(line[4], fd, byts)
    test_sys_close(line[5], fd)
    test_sys_exit(line[6], 0)

if __name__ == "__main__":
    main()

