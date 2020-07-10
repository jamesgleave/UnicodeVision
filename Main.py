from Converter import Converter
from subprocess import Popen,PIPE


def lives_stream(*kwargs):
    p1 = Popen("echo hello", stdout=PIPE)
    streamer = Converter()
    streamer.live_stream()


def subprocess_cmd(dr,cmd1,cmd2):
    p1 = Popen(cmd1.split(),stdout=PIPE,cwd=dr)
    p2 = Popen(cmd2.split(),stdin=p1.stdout,stdout=PIPE,cwd=dr)
    p1.stdout.close()
    return p2.communicate()[0]


subprocess_cmd('/Users/martingleave/Desktop/Coding Projects 2020 /UnicodeVision/Assets/src/', 'open -a Terminal', 'python3 Converter.py')