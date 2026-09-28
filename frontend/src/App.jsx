import PredictionForm from "./components/predictionForm";
import MetricsDashboard from "./components/MetricsDashboard";
import "./index.css";

export default function App() {
  return (
    <div className="app-shell">
      <header className="page-header">
        <p className="eyebrow">Machine Learning in Production</p>
        <h1>Interactive House Price Prediction App</h1>
        <p className="page-subtitle">
          Predict property prices, collect feedback, retrain the model, and
          track performance over time.
        </p>
      </header>

      <main className="dashboard-grid">
        <PredictionForm />
        <MetricsDashboard />
      </main>
    </div>
  );
}