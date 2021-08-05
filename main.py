import subprocess
from urllib.parse import urlparse


def ping(server="azat.ai", count=1, wait_sec=1):
    """

    :rtype: dict or None
    """
    cmd = "ping -c {} -W {} {}".format(count, wait_sec, server).split(" ")
    try:
        output = subprocess.check_output(cmd).decode().strip()
        lines = output.split("\n")
        total = lines[-2].split(",")[3].split()[1]
        loss = lines[-2].split(",")[2].split()[0]
        timing = lines[-1].split()[3].split("/")
        return {
            "type": "rtt",
            "min": timing[0],
            "avg": timing[1],
            "max": timing[2],
            "mdev": timing[3],
            "total": total,
            "loss": loss,
        }
    except Exception as e:
        print(e)
        return None


with open("mirrors.txt", mode="r") as f:
    data = f.read()
    _list = data.strip("\n").split(",")
    pure_list = []
    for each in _list:
        if each == "":
            pass
        elif each == "\n":
            pass
        else:
            pure_list.append(each.strip("\n").strip(" "))

    domains = []
    for each in pure_list:
        domain = urlparse(each).netloc
        domains.append(domain)

    min_ref = ""
    min_time = 1000
    for each in domains:
        res = ping(server=each)
        print(res)
        c_ref = each
        try:
            c_time = float(res["max"])
        except:
            c_time = 1000

        if c_time <= min_time:
            min_ref = c_ref
            min_time = c_time

        print(c_ref, c_time)

    print(f"final: {min_ref}, {min_time}")
