import subprocess


def run(args, **kwargs):
    return subprocess.check_output(["vvcli"] + list(args), **kwargs)
