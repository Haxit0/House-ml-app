const API_BASE = "http://127.0.0.1:8000";

export async function predictHouse(data) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    throw new Error("Prediction request failed");
  }

  return res.json();
}

export async function submitFeedback(data) {
  const res = await fetch(`${API_BASE}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    throw new Error("Feedback request failed");
  }

  return res.json();
}

export async function fetchMetrics() {
  const res = await fetch(`${API_BASE}/metrics`);

  if (!res.ok) {
    throw new Error("Metrics request failed");
  }

  return res.json();
}

export async function retrainModel() {
  const res = await fetch(`${API_BASE}/retrain`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Retrain request failed");
  }

  return res.json();
}