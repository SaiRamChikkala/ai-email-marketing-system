
import sys, json
seg = sys.argv[1] if len(sys.argv)>1 else '0'
topic = sys.argv[2] if len(sys.argv)>2 else 'Special Offer'
name = sys.argv[3] if len(sys.argv)>3 else 'Customer'
templates = {
    "0": "Hello {name},\n\nBased on your interests, we thought you'd like our {topic}. Here are some picks: {reco}\n\nRegards, Team",
    "1": "Hi {name},\n\nAs a premium user, enjoy exclusive {topic}. Recommended for you: {reco}\n\nCheers, Team",
    "2": "Hey {name},\n\nDon't miss {topic} tailored for your needs. Take a look: {reco}\n\nThanks, Team"
}
db = json.load(open('../db.json'))
# simple top products from same category as segment mapping
seg_map = {"0":"electronics","1":"fashion","2":"groceries"}
cat = seg_map.get(str(seg),"electronics")
# pick top 3 products in that category
reco = [p['title'] for p in db['products'] if p['category']==cat][:3]
msg = templates.get(str(seg), templates['0']).format(name=name, topic=topic, reco=", ".join(reco))
print(msg)
