#!/usr/bin/env python3
"""在独立会话里启动一个命令（双 fork + setsid），并把它写进 pidfile。

普通 `nohup cmd &` 只是忽略 SIGHUP，进程仍然留在调用方的进程组 / 会话里；
调用方（agent run、CI shell）结束时按进程组清理，服务会被一起带走。
这里双 fork + setsid 让服务脱离原会话，父进程退出后由 init/launchd 收养，
调用方怎么退出都影响不到它。

用法：
  python3 scripts/daemonize.py --pidfile .preview/hugo.pid --log .preview/hugo.log -- hugo server ...
"""

import argparse
import os
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description="启动一个完全脱离调用方的后台进程")
    ap.add_argument("--pidfile", required=True, help="把子进程 PID 写到这个文件")
    ap.add_argument("--log", required=True, help="stdout/stderr 追加到这个文件")
    ap.add_argument("cmd", nargs=argparse.REMAINDER, help="要执行的命令（放在 -- 之后）")
    args = ap.parse_args()

    cmd = args.cmd
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        print("!! 没有要执行的命令", file=sys.stderr)
        return 2

    pidfile = os.path.abspath(args.pidfile)
    logfile = os.path.abspath(args.log)
    os.makedirs(os.path.dirname(pidfile), exist_ok=True)
    os.makedirs(os.path.dirname(logfile), exist_ok=True)

    first = os.fork()
    if first > 0:
        os.waitpid(first, 0)
        return 0

    os.setsid()

    second = os.fork()
    if second > 0:
        with open(pidfile, "w", encoding="utf-8") as fh:
            fh.write(f"{second}\n")
        os._exit(0)

    # 孙进程：新会话首领，父进程已退出，由 init 收养
    devnull = os.open(os.devnull, os.O_RDONLY)
    os.dup2(devnull, 0)
    log_fd = os.open(logfile, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    os.dup2(log_fd, 1)
    os.dup2(log_fd, 2)
    try:
        os.execvp(cmd[0], cmd)
    except OSError as exc:  # pragma: no cover
        print(f"!! exec 失败：{exc}", file=sys.stderr)
        os._exit(127)


if __name__ == "__main__":
    raise SystemExit(main())
