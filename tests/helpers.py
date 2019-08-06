import subprocess


def run(args, **kwargs):
    return subprocess.check_output(["vvtool"] + list(args), **kwargs)
