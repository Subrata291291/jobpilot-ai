import { useState } from "react";
import {
  BriefcaseBusiness,
  MapPin,
  Upload,
  Sparkles,
  FileText,
  ExternalLink,
  LoaderCircle,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";

import { recommendJobsFromCV } from "./services/api";

function App() {
  const [file, setFile] = useState(null);

  // Keep role empty so backend can use the CV role
  // when the user does not provide a preferred role.
  const [role, setRole] = useState("");

  const [location, setLocation] = useState("Kolkata");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  // Number of jobs currently visible
  const [visibleJobs, setVisibleJobs] = useState(3);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    setError("");
    setResult(null);
    setVisibleJobs(3);

    if (selectedFile.size > 5 * 1024 * 1024) {
      setFile(null);
      setError("CV size must not exceed 5 MB.");
      return;
    }

    const allowedTypes = [".pdf", ".docx"];
    const filename = selectedFile.name.toLowerCase();

    const isAllowed = allowedTypes.some((extension) =>
      filename.endsWith(extension)
    );

    if (!isAllowed) {
      setFile(null);
      setError("Only PDF and DOCX files are supported.");
      return;
    }

    setFile(selectedFile);
  };

  const handleFindJobs = async () => {
    setError("");
    setResult(null);
    setVisibleJobs(3);

    if (!file) {
      setError("Please upload your CV first.");
      return;
    }

    try {
      setLoading(true);

      const data = await recommendJobsFromCV({
        file,
        preferredRole: role,
        preferredLocation: location,
      });

      setResult(data);

      // Always start by showing first 3 jobs
      setVisibleJobs(3);
    } catch (err) {
      console.error(err);

      const message =
        err?.response?.data?.detail ||
        "Something went wrong while finding jobs.";

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleLoadMore = () => {
    setVisibleJobs((current) =>
      Math.min(current + 3, result?.jobs?.length || 0)
    );
  };

  const handleNewSearch = () => {
    setResult(null);
    setError("");
    setVisibleJobs(3);
  };

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">
            <Sparkles size={20} />
          </div>

          <span>JobPilot AI</span>
        </div>

        <div className="navbar-badge">
          AI-Powered Job Search
        </div>
      </header>

      <main className="hero">
        {!result && (
          <section className="hero-content">
            <div className="hero-badge">
              <Sparkles size={16} />
              Intelligent Job Matching
            </div>

            <h1>
              Find jobs that
              <span> match your skills.</span>
            </h1>

            <p className="hero-description">
              Upload your CV and let AI analyze your experience,
              search current job opportunities, and find roles that
              match your profile.
            </p>
          </section>
        )}

        {!result && (
          <section className="search-card">
            <div className="card-header">
              <div>
                <h2>Find Your Next Job</h2>

                <p>
                  Upload your CV and tell us what you're looking for.
                </p>
              </div>
            </div>

            <div className="form-section">
              <label>Upload your CV</label>

              <label className="upload-box">
                <input
                  type="file"
                  accept=".pdf,.docx"
                  onChange={handleFileChange}
                />

                <div className="upload-icon">
                  {file ? (
                    <FileText size={28} />
                  ) : (
                    <Upload size={28} />
                  )}
                </div>

                {file ? (
                  <>
                    <strong>{file.name}</strong>

                    <span>
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </span>
                  </>
                ) : (
                  <>
                    <strong>Drop your CV here</strong>

                    <span>
                      PDF or DOCX · Maximum 5 MB
                    </span>
                  </>
                )}
              </label>
            </div>

            <div className="form-grid">
              <div className="form-field">
                <label htmlFor="role">
                  <BriefcaseBusiness size={16} />
                  Preferred Role
                </label>

                <input
                  id="role"
                  type="text"
                  value={role}
                  onChange={(event) =>
                    setRole(event.target.value)
                  }
                  placeholder="e.g. Frontend Developer"
                />
              </div>

              <div className="form-field">
                <label htmlFor="location">
                  <MapPin size={16} />
                  Preferred Location
                </label>

                <input
                  id="location"
                  type="text"
                  value={location}
                  onChange={(event) =>
                    setLocation(event.target.value)
                  }
                  placeholder="e.g. Kolkata"
                />
              </div>
            </div>

            {error && (
              <div className="error-message">
                <AlertCircle size={17} />
                {error}
              </div>
            )}

            <button
              className="search-button"
              type="button"
              onClick={handleFindJobs}
              disabled={loading}
            >
              {loading ? (
                <>
                  <LoaderCircle
                    size={18}
                    className="spin"
                  />
                  Finding Matching Jobs...
                </>
              ) : (
                <>
                  <Sparkles size={18} />
                  Find Matching Jobs
                </>
              )}
            </button>

            <p className="privacy-note">
              Your CV is used to analyze your profile and find
              relevant opportunities.
            </p>
          </section>
        )}

        {loading && (
          <section className="loading-card">
            <LoaderCircle size={34} className="spin" />

            <h2>Finding your matching jobs...</h2>

            <p>
              AI is analyzing your CV and searching for relevant
              opportunities.
            </p>
          </section>
        )}

        {result && !loading && (
          <section className="results-section">
            <div className="results-header">
              <div>
                <div className="success-badge">
                  <CheckCircle2 size={16} />
                  Search completed
                </div>

                <h2>
                  Jobs matching your profile
                </h2>

                <p>
                  Found {result.total_jobs} matching opportunities.
                </p>
              </div>

              <button
                className="new-search-button"
                onClick={handleNewSearch}
              >
                New Search
              </button>
            </div>

            {result.candidate && (
              <div className="candidate-card">
                <div className="candidate-info">
                  <div className="candidate-avatar">
                    {result.candidate.name
                      ?.charAt(0)
                      ?.toUpperCase() || "U"}
                  </div>

                  <div>
                    <h3>{result.candidate.name}</h3>

                    <p>
                      {result.candidate.current_role}
                      {" · "}
                      {result.candidate.experience_years} years
                      experience
                    </p>
                  </div>
                </div>

                <div className="skills-list">
                  {result.candidate.skills
                    ?.slice(0, 10)
                    .map((skill) => (
                      <span key={skill}>
                        {skill}
                      </span>
                    ))}
                </div>
              </div>
            )}

            <div className="jobs-list">
              {result.jobs
                ?.slice(0, visibleJobs)
                .map((job, index) => (
                  <article
                    className="job-card"
                    key={`${job.company}-${job.title}-${index}`}
                  >
                    <div className="job-card-top">
                      <div>
                        <h3>{job.title}</h3>

                        <p className="company-name">
                          {job.company}
                        </p>

                        <p className="job-location">
                          <MapPin size={15} />
                          {job.location || "Location not specified"}
                        </p>
                      </div>

                      <div className="match-score">
                        <strong>
                          {Math.round(job.match_score)}%
                        </strong>

                        <span>Match</span>
                      </div>
                    </div>

                    <div className="job-skills">
                      {job.skills?.slice(0, 7).map((skill) => (
                        <span key={skill}>
                          {skill}
                        </span>
                      ))}
                    </div>

                    <div className="score-breakdown">
                      <div>
                        <span>Skills</span>
                        <strong>{job.skill_score}%</strong>
                      </div>

                      <div>
                        <span>Role</span>
                        <strong>{job.role_score}%</strong>
                      </div>

                      <div>
                        <span>Location</span>
                        <strong>{job.location_score}%</strong>
                      </div>

                      <div>
                        <span>Experience</span>
                        <strong>{job.experience_score}%</strong>
                      </div>
                    </div>

                    {job.experience && (
                      <p className="experience-text">
                        Experience: {job.experience}
                      </p>
                    )}

                    {job.url ? (
                      <a
                        className="view-job-button"
                        href={job.url}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        View Job
                        <ExternalLink size={16} />
                      </a>
                    ) : (
                      <span className="job-link-unavailable">
                        Job link unavailable
                      </span>
                    )}
                  </article>
                ))}
            </div>

            {/* Load More */}
            {result.jobs &&
              visibleJobs < result.jobs.length && (
                <div className="load-more-container">
                  <button
                    className="load-more-button"
                    onClick={handleLoadMore}
                  >
                    Load More
                  </button>
                </div>
              )}

            {/* All jobs have been displayed */}
            {result.jobs &&
              result.jobs.length > 0 &&
              visibleJobs >= result.jobs.length && (
                <p className="all-jobs-message">
                  You have reached the end of the search results.
                </p>
              )}

            {result.jobs && result.jobs.length === 0 && (
              <p className="all-jobs-message">
                No matching jobs were found.
              </p>
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;