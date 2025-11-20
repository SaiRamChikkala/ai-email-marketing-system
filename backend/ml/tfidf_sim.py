
# TF-IDF based product similarity.
# Requires scikit-learn, numpy, pandas. Usage: python3 tfidf_sim.py "<description>" <top_k>
import sys, json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

db = json.load(open('../db.json'))
docs = [p['description'] for p in db['products']]

vec = TfidfVectorizer()
tfidf = vec.fit_transform(docs)

desc = sys.argv[1] if len(sys.argv)>1 else ""
top_k = int(sys.argv[2]) if len(sys.argv)>2 else 5

if not desc:
    # return top products
    out = [p for p in db['products']][:top_k]
    print(json.dumps(out))
    sys.exit(0)

query_vec = vec.transform([desc])
sims = cosine_similarity(query_vec, tfidf)[0]
pairs = list(enumerate(sims))
pairs = sorted(pairs, key=lambda x: x[1], reverse=True)[:top_k]
result = [db['products'][idx] for idx,_ in pairs]
print(json.dumps(result))
