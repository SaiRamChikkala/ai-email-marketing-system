
# Rule-based complementary add-on recommendations for a product id.
# Usage: python3 addon_reco.py <product_id>
import sys, json
prod_id = int(sys.argv[1]) if len(sys.argv)>1 else 1
db = json.load(open('../db.json'))

# simple mapping (would be learned in production)
addon_map = {
    1: [3], # earbuds -> power bank
    2: [1,3], # smartwatch -> earbuds, power bank
    3: [1], # power bank -> earbuds
    4: [5], # tshirt -> sneakers
    6: [7]  # honey -> dry fruits
}
addons = addon_map.get(prod_id, [])
res = []
for a in addons:
    p = next((x for x in db['products'] if x['id']==a), None)
    if p:
        res.append(p)
print(json.dumps(res))
