
import sys, csv, json, random, math
def dist(a,b): return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
def kmeans(points, k=3, iters=40):
    centroids = random.sample(points, k)
    for _ in range(iters):
        clusters = [[] for _ in range(k)]
        for p in points:
            idx = min(range(k), key=lambda i: dist(p, centroids[i]))
            clusters[idx].append(p)
        for i, c in enumerate(clusters):
            if c:
                centroids[i] = [sum(values)/len(values) for values in zip(*c)]
    labels = []
    for p in points:
        labels.append(min(range(k), key=lambda i: dist(p, centroids[i])))
    return labels

inp = sys.argv[1]; outp = sys.argv[2]
rows = list(csv.DictReader(open(inp)))
points = []
for r in rows:
    points.append([float(r.get("purchases",0)), float(r.get("visits",0)), float(r.get("spend",0))])
labels = kmeans(points, k=3)
output = []
for r, lab in zip(rows, labels):
    output.append({"id": int(r["id"]), "email": r["email"], "segment": lab})
open(outp, "w").write(json.dumps(output, indent=2))
print("OK")
