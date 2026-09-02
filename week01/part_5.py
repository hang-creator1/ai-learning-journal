def save_scores(scores):
    return scores
path =  "scores.txt"
scores = save_scores({"小明": 90, "小红": 58})
with open(path,"w",encoding = "utf-8") as f:
    for key,value in scores.items():
        f.write(f"{key}:{value}\n")
with open(path,"r",encoding="utf-8") as f:
    for line in f:
        print(f"{line.strip()}\n")