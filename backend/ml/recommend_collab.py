
# Simple item-based collaborative filtering using ratings.
# Usage: python3 recommend_collab.py <user_id> <top_k>
import sys, json, math
from collections import defaultdict

db = json.load(open('../db.json'))

user_id = int(sys.argv[1]) if len(sys.argv)>1 else 1
top_k = int(sys.argv[2]) if len(sys.argv)>2 else 5

# build item-user ratings
item_users = defaultdict(dict)
user_items = defaultdict(dict)
for r in db['ratings']:
    item_users[r['product_id']][r['user_id']] = r['rating']
    user_items[r['user_id']][r['product_id']] = r['rating']

# compute simple item similarity (cosine on rating vectors)
def cosine(a,b):
    common = set(a.keys()) & set(b.keys())
    if not common: return 0.0
    num = sum(a[u]*b[u] for u in common)
    den1 = math.sqrt(sum(v*v for v in a.values()))
    den2 = math.sqrt(sum(v*v for v in b.values()))
    if den1==0 or den2==0: return 0.0
    return num/(den1*den2)

# create similarity matrix for items
items = list({p['id'] for p in db['products']})
sim = {i:{} for i in items}
for i in items:
    for j in items:
        if i==j: continue
        sim[i][j] = cosine(item_users.get(i,{}), item_users.get(j,{}))

# score candidate items for user based on items they've rated
scores = {}
user_rated = user_items.get(user_id,{})
for candidate in items:
    if candidate in user_rated: continue
    score = 0.0
    for rated_item, rating in user_rated.items():
        score += sim.get(candidate,{}).get(rated_item,0.0) * rating
    scores[candidate] = score

# top k
top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
result = []
for pid, sc in top:
    prod = next((p for p in db['products'] if p['id']==pid), None)
    if prod:
        result.append({"product": prod, "score": sc})

print(json.dumps(result))
