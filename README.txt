
Enhanced AI for Automated Email Marketing - Project Bundle
---------------------------------------------------------

This enhanced package integrates features from your project document:
- Intelligent segmentation (KMeans)
- Personalized email generation (templates + product injection)
- Collaborative-filtering recommendations
- Complementary add-on recommendations
- TF-IDF based product similarity (requires scikit-learn)
- Mock Mailchimp send endpoint (replace with real Mailchimp API in production)

Prerequisites:
- Node.js and npm
- Python 3
- For TF-IDF similarity: pip install scikit-learn numpy pandas

How to run:
1. cd backend
2. npm install
3. npm start
4. Open http://localhost:5000

Python scripts are in backend/ml. They are called by backend server when you use the frontend UI.

Notes:
- This demo uses a JSON file (db.json) as a lightweight data store. Replace with MongoDB/Postgres for production.
- To integrate Mailchimp, implement API calls in /api/send using MAILCHIMP_API_KEY environment variable.
