def add_log(msg):
    path = "log.txt"
    N = 1
    with open(path,"r",encoding="utf-8") as f:
        for line in f:
            if line != "":
                N+=1
    with open(path,"a",encoding="utf-8") as f:
        f.write(f"第{N}条:{msg}\n")
add_log("用户登录")
add_log("用户退出")