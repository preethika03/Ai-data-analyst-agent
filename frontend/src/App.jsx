
import './App.css'

function App() {
  return (
    <div className="app">
      <aside className="sidebar">
        <h2 className="brand">✦ DataPilot</h2>
        <p className="menu-label">WORKSPACE</p>

        <nav>
          <a className="nav-item active" href="#overview">▦ Overview</a>
          <a className="nav-item" href="#upload">↑ Upload Dataset</a>
          <a className="nav-item" href="#analysis">◈ Data Analysis</a>
          <a className="nav-item" href="#assistant">✧ AI Assistant</a>
        </nav>

        <div className="sidebar-bottom">
          <div className="avatar">DP</div>
          <div>
            <strong>Data Analyst</strong>
            <p>Workspace</p>
          </div>
        </div>
      </aside>

      <main className="main-content" id="overview">
        <header className="topbar">
          <span>Workspace / Overview</span>
          <span className="status">● System ready</span>
        </header>

        <section className="welcome">
          <div>
            <p className="eyebrow">YOUR INTELLIGENT DATA WORKSPACE</p>
            <h1>Make your data <span>make sense.</span></h1>
            <p className="subtitle">
              Upload your dataset, uncover patterns, and turn numbers into insights.
            </p>
          </div>
          <div className="hero-symbol">✳</div>
        </section>

        <section className="upload-panel" id="upload">
          <div className="upload-icon">↑</div>
          <h2>Start with your dataset</h2>
          <p>Upload a CSV file to begin exploring your data.</p>

          <label className="upload-button">
            <input
              type="file"
              accept=".csv,text/csv"
              onChange={(event) => {
                const file = event.target.files?.[0]
                if (file) alert(`Selected: ${file.name}`)
              }}
            />
            ↑ Choose CSV file
          </label>

          <p className="file-note">CSV files only · Maximum size depends on server configuration</p>
        </section>

        <section className="section-heading" id="analysis">
          <div>
            <h2>Your analysis workspace</h2>
            <p>Your insights will appear here after uploading a dataset.</p>
          </div>
          <span className="demo-badge">Preview</span>
        </section>

        <section className="stats-grid">
          <article className="stat-card">
            <div className="stat-top"><span>Rows analyzed</span><span>▤</span></div>
            <h3>—</h3>
            <p>Waiting for dataset</p>
          </article>

          <article className="stat-card">
            <div className="stat-top"><span>Columns detected</span><span>▥</span></div>
            <h3>—</h3>
            <p>Your variables, at a glance</p>
          </article>

          <article className="stat-card">
            <div className="stat-top"><span>Data quality</span><span>◇</span></div>
            <h3>—</h3>
            <p>Ready for inspection</p>
          </article>
        </section>

        <section className="assistant-card" id="assistant">
          <div className="assistant-icon">✧</div>
          <div>
            <h2>Meet your AI analyst</h2>
            <p>Ask questions about your data and get explanations in plain English.</p>
          </div>
          <button onClick={() => alert('We will connect the AI assistant to the backend next!')}>
            Explore assistant →
          </button>
        </section>

        <footer>DataPilot · AI-powered data exploration</footer>
      </main>
    </div>
  )
}

export default App
