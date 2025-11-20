
const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

const app = express();
app.use(bodyParser.json());
app.use("/", express.static(path.join(__dirname, "..", "frontend")));

const DB = path.join(__dirname, "db.json");

function readDB() {
  return JSON.parse(fs.readFileSync(DB, "utf-8"));
}
function writeDB(db) {
  fs.writeFileSync(DB, JSON.stringify(db, null, 2));
}

// Users endpoints
app.get("/api/users", (req, res) => res.json(readDB().users));
app.post("/api/users", (req, res) => {
  const db = readDB();
  const user = req.body;
  user.id = Date.now();
  db.users.push(user);
  writeDB(db);
  res.json(user);
});

// Segmentation (same as before)
app.post("/api/segment", (req, res) => {
  const db = readDB();
  const csvPath = path.join(__dirname, "users.csv");
  let csv = "id,email,purchases,visits,spend,category_interest\n";
  db.users.forEach(u => {
    csv += `${u.id},${u.email},${u.purchases || 0},${u.visits || 0},${u.spend || 0},${u.category_interest || ''}\n`;
  });
  fs.writeFileSync(csvPath, csv);
  const py = spawn("python3", [path.join(__dirname, "ml", "segment.py"), csvPath, path.join(__dirname, "segments.json")]);
  let err = "";
  py.stderr.on("data", d => err += d.toString());
  py.on("close", code => {
    if (code !== 0) return res.status(500).json({ error: err });
    const segments = JSON.parse(fs.readFileSync(path.join(__dirname, "segments.json")));
    res.json(segments);
  });
});

// Email generation (template or LLM placeholder)
app.post("/api/generate-email", (req, res) => {
  const { segment, topic, name } = req.body;
  const py = spawn("python3", [path.join(__dirname, "ml", "email_gen.py"), String(segment || 0), topic || "Special Offer", name || "Customer"]);
  let out = "";
  py.stdout.on("data", d => out += d.toString());
  py.on("close", () => res.json({ email: out }));
});

// Collaborative filtering recommendations (user-based simple)
app.post("/api/recommend-collab", (req, res) => {
  // expects { user_id: <id>, top_k: 5 }
  const { user_id, top_k } = req.body || {};
  const py = spawn("python3", [path.join(__dirname, "ml", "recommend_collab.py"), String(user_id || 1), String(top_k || 5)]);
  let out = "", err = "";
  py.stdout.on("data", d => out += d.toString());
  py.stderr.on("data", d => err += d.toString());
  py.on("close", code => {
    if (code !== 0) return res.status(500).json({ error: err });
    res.json(JSON.parse(out));
  });
});

// Complementary add-on recommendations
app.post("/api/recommend-addon", (req, res) => {
  const { product_id } = req.body || {};
  const py = spawn("python3", [path.join(__dirname, "ml", "addon_reco.py"), String(product_id || 1)]);
  let out = "", err = "";
  py.stdout.on("data", d => out += d.toString());
  py.stderr.on("data", d => err += d.toString());
  py.on("close", code => {
    if (code !== 0) return res.status(500).json({ error: err });
    res.json(JSON.parse(out));
  });
});

// TF-IDF similar products
app.post("/api/similar-products", (req, res) => {
  const { description, top_k } = req.body || {};
  const py = spawn("python3", [path.join(__dirname, "ml", "tfidf_sim.py"), description || "", String(top_k || 5)]);
  let out = "", err = "";
  py.stdout.on("data", d => out += d.toString());
  py.stderr.on("data", d => err += d.toString());
  py.on("close", code => {
    if (code !== 0) return res.status(500).json({ error: err });
    res.json(JSON.parse(out));
  });
});

// Mock Mailchimp send (placeholder)
app.post("/api/send", (req, res) => {
  const { email, subject, body } = req.body;
  // In production, implement Mailchimp API here using API key in env var
  console.log("Mock send:", email, subject);
  res.json({ status: "sent", email });
});

app.listen(5000, () => console.log("Server running at http://localhost:5000"));
