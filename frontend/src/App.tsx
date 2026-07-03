// D:\YASH\Movie_Recommendation_System\frontend\src\App.tsx

import React, { useState, useEffect, useRef } from 'react';
import { 
  Film, Search, Heart, Sparkles, Settings, MessageSquare, Send, 
  Star, Plus, Check, Trash, Info, Compass, Activity, 
  ChevronRight, RefreshCw, BarChart2, Trophy
} from 'lucide-react';
import './App.css';

interface Movie {
  id: number;
  title: string;
  year: number;
  genres: string[];
  director: string;
  cast: string[];
  runtime: number;
  language: string;
  rating: number;
  vote_count: number;
  overview: string;
  moods: string[];
  poster_path: string;
}

interface RecResult {
  movie: Movie;
  score: number;
  match_percentage: number;
  explanation: string;
}

interface ChatMessage {
  role: 'user' | 'model' | 'assistant';
  content: string;
}

const API_BASE_URL = 'http://127.0.0.1:8000';

const MOODS_LIST = ["Mind-bending", "Relaxing", "Funny", "Emotional", "Spooky", "Action-packed", "Inspirational", "Romantic", "Suspenseful"];
const GENRES_LIST = ["Sci-Fi", "Action", "Thriller", "Drama", "Romance", "Comedy", "Mystery", "Horror", "Fantasy", "Animation", "Family", "Music"];
const LANGUAGES_LIST = ["English", "French", "Spanish", "Japanese", "Korean"];

export default function App() {
  // --- STATE ---
  const [movies, setMovies] = useState<Movie[]>([]);
  const [recommendations, setRecommendations] = useState<RecResult[]>([]);
  const [surpriseRecs, setSurpriseRecs] = useState<RecResult[]>([]);
  const [hiddenGems, setHiddenGems] = useState<RecResult[]>([]);
  
  // Onboarding taste profile
  const [onboardingStep, setOnboardingStep] = useState<number | null>(null);
  const [onboardingGenres, setOnboardingGenres] = useState<string[]>([]);
  const [onboardingMoods, setOnboardingMoods] = useState<string[]>([]);
  const [onboardingRatings, setOnboardingRatings] = useState<Record<number, number>>({});
  
  // User profile
  const [ratings, setRatings] = useState<Record<number, number>>({});
  const [watchlist, setWatchlist] = useState<number[]>([]);
  const [preferredMood, setPreferredMood] = useState<string>("");
  
  // Navigation & UI
  const [currentTab, setCurrentTab] = useState<string>('discover');
  const [activeMovieDetail, setActiveMovieDetail] = useState<Movie | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [recsLoading, setRecsLoading] = useState<boolean>(false);
  
  // Filters
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [filterGenre, setFilterGenre] = useState<string>("");
  const [filterLanguage, setFilterLanguage] = useState<string>("");
  const [filterRatingMin, setFilterRatingMin] = useState<number>(0);
  const [filterRuntimeMax, setFilterRuntimeMax] = useState<number>(180);
  
  // Chat Companion
  const [chatCollapsed, setChatCollapsed] = useState<boolean>(true);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState<string>("");
  const [chatLoading, setChatLoading] = useState<boolean>(false);
  const [geminiApiKey, setGeminiApiKey] = useState<string>("");

  const chatEndRef = useRef<HTMLDivElement>(null);

  // --- INITIAL LOAD ---
  useEffect(() => {
    // Load local storage states
    const storedRatings = localStorage.getItem('movie_ratings');
    const storedWatchlist = localStorage.getItem('movie_watchlist');
    const storedApiKey = localStorage.getItem('gemini_api_key');
    const storedOnboard = localStorage.getItem('onboarding_completed');
    
    if (storedRatings) setRatings(JSON.parse(storedRatings));
    if (storedWatchlist) setWatchlist(JSON.parse(storedWatchlist));
    if (storedApiKey) setGeminiApiKey(storedApiKey);
    
    // Fetch catalog movies
    fetchMovies();
    
    if (storedOnboard !== 'true') {
      setOnboardingStep(1); // Trigger onboarding if not completed
    } else {
      // Chat greeting
      setChatMessages([
        { role: 'model', content: "Welcome back! 🎬 I'm CineCompanion, your personal AI movie assistant. Let me know what you're in the mood for, or ask me for a recommendation!" }
      ]);
    }
  }, []);

  // Update recommendations whenever ratings or preferred mood changes
  useEffect(() => {
    if (Object.keys(ratings).length > 0 && onboardingStep === null) {
      fetchRecommendations();
    }
  }, [ratings, preferredMood, onboardingStep]);

  // Scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages, chatLoading]);

  // --- API CALLS ---
  const fetchMovies = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/movies`);
      if (res.ok) {
        const data = await res.json();
        setMovies(data);
      }
    } catch (err) {
      console.error("Error fetching movies:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchRecommendations = async () => {
    setRecsLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/recommendations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ratings: ratings,
          preferred_mood: preferredMood || null,
          filters: null,
          top_n: 12
        })
      });
      if (res.ok) {
        const data = await res.json();
        setRecommendations(data.recommendations);
        setSurpriseRecs(data.surprise_recommendations);
        setHiddenGems(data.hidden_gems);
      }
    } catch (err) {
      console.error("Error fetching recommendations:", err);
    } finally {
      setRecsLoading(false);
    }
  };

  const handleSendChatMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const userMsg = chatInput.trim();
    setChatInput("");
    
    // Add user message to state
    const newMessages = [...chatMessages, { role: 'user' as const, content: userMsg }];
    setChatMessages(newMessages);
    setChatLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: newMessages.map(m => ({ role: m.role === 'assistant' ? 'model' : m.role, content: m.content })),
          ratings: ratings,
          watchlist: watchlist,
          api_key: geminiApiKey || null
        })
      });
      
      if (res.ok) {
        const data = await res.json();
        setChatMessages(prev => [...prev, { role: 'model', content: data.response }]);
      } else {
        const errorData = await res.json();
        setChatMessages(prev => [...prev, { role: 'model', content: `Error: ${errorData.detail || 'Could not communicate with the companion.'}` }]);
      }
    } catch (err) {
      console.error("Error chatting:", err);
      setChatMessages(prev => [...prev, { role: 'model', content: "Sorry, I couldn't reach the backend server. Please make sure the backend is running!" }]);
    } finally {
      setChatLoading(false);
    }
  };

  // --- ACTIONS ---
  const handleRateMovie = (movieId: number, rating: number) => {
    const updatedRatings = { ...ratings, [movieId]: rating };
    setRatings(updatedRatings);
    localStorage.setItem('movie_ratings', JSON.stringify(updatedRatings));
  };

  const handleToggleWatchlist = (movieId: number) => {
    let updated;
    if (watchlist.includes(movieId)) {
      updated = watchlist.filter(id => id !== movieId);
    } else {
      updated = [...watchlist, movieId];
    }
    setWatchlist(updated);
    localStorage.setItem('movie_watchlist', JSON.stringify(updated));
  };

  const handleRemoveRating = (movieId: number) => {
    const updatedRatings = { ...ratings };
    delete updatedRatings[movieId];
    setRatings(updatedRatings);
    localStorage.setItem('movie_ratings', JSON.stringify(updatedRatings));
  };

  // --- ONBOARDING ACTIONS ---
  const handleToggleOnboardingGenre = (genre: string) => {
    setOnboardingGenres(prev => 
      prev.includes(genre) ? prev.filter(g => g !== genre) : [...prev, genre]
    );
  };

  const handleToggleOnboardingMood = (mood: string) => {
    setOnboardingMoods(prev => 
      prev.includes(mood) ? prev.filter(m => m !== mood) : [...prev, mood]
    );
  };

  const handleOnboardingRate = (movieId: number, rating: number) => {
    setOnboardingRatings(prev => ({ ...prev, [movieId]: rating }));
  };

  const handleFinishOnboarding = () => {
    // Save ratings & complete onboarding
    setRatings(onboardingRatings);
    localStorage.setItem('movie_ratings', JSON.stringify(onboardingRatings));
    localStorage.setItem('onboarding_completed', 'true');
    
    // Set some sample user watchlist based on genre preferences
    const sampledWatchlist: number[] = [];
    movies.forEach(m => {
      if (m.genres.some(g => onboardingGenres.includes(g)) && sampledWatchlist.length < 3) {
        if (!onboardingRatings[m.id]) {
          sampledWatchlist.push(m.id);
        }
      }
    });
    if (sampledWatchlist.length > 0) {
      setWatchlist(sampledWatchlist);
      localStorage.setItem('movie_watchlist', JSON.stringify(sampledWatchlist));
    }
    
    setOnboardingStep(null);
    
    // Generate AI response greeting
    const welcomeMsg = `Thanks for sharing your taste! 🍿 Based on your selection of **${onboardingGenres.join(', ')}** and liking movies like **${
      movies.filter(m => onboardingRatings[m.id] >= 4).map(m => m.title).join(', ') || 'your rated movies'
    }**, I've calibrated your personalized dashboard.\n\nI also populated a smart watchlist for you! Let me know what you want to watch next.`;
    
    setChatMessages([
      { role: 'model', content: welcomeMsg }
    ]);
  };

  const handleSaveApiKey = (key: string) => {
    setGeminiApiKey(key);
    localStorage.setItem('gemini_api_key', key);
    alert("Gemini API Key saved successfully!");
  };

  const handleResetApp = () => {
    if (window.confirm("Are you sure you want to reset your taste profile, watchlist, and ratings?")) {
      localStorage.clear();
      setRatings({});
      setWatchlist([]);
      setPreferredMood("");
      setOnboardingStep(1);
      setOnboardingGenres([]);
      setOnboardingMoods([]);
      setOnboardingRatings({});
      setRecommendations([]);
      setSurpriseRecs([]);
      setHiddenGems([]);
      setChatMessages([
        { role: 'model', content: "Taste profile reset. Let's rebuild it together! Select your favorite genres to begin." }
      ]);
    }
  };

  // --- STATS COMPUTATION ---
  const getStats = () => {
    const totalRated = Object.keys(ratings).length;
    const totalWatchlist = watchlist.length;
    
    // Total watch time
    let totalWatchTimeMinutes = 0;
    Object.keys(ratings).forEach(id => {
      const m = movies.find(movie => movie.id === parseInt(id));
      if (m) totalWatchTimeMinutes += m.runtime;
    });
    const watchTimeHours = Math.round(totalWatchTimeMinutes / 60);

    // Genre distribution
    const genreCounts: Record<string, number> = {};
    Object.keys(ratings).forEach(id => {
      const m = movies.find(movie => movie.id === parseInt(id));
      if (m) {
        m.genres.forEach(g => {
          genreCounts[g] = (genreCounts[g] || 0) + 1;
        });
      }
    });

    // Rating distribution
    const ratingDistribution = { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 };
    Object.values(ratings).forEach(r => {
      const key = r as 1 | 2 | 3 | 4 | 5;
      if (key in ratingDistribution) {
        ratingDistribution[key]++;
      }
    });

    const sortedGenres = Object.entries(genreCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5);

    return {
      totalRated,
      totalWatchlist,
      watchTimeHours,
      sortedGenres,
      ratingDistribution
    };
  };

  const stats = getStats();

  // --- MOVIE FILTERING (CLIENT-SIDE FOR SEARCH TAB) ---
  const getFilteredMovies = () => {
    return movies.filter(m => {
      // Search query
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        const matchesTitle = m.title.toLowerCase().includes(query);
        const matchesDirector = m.director.toLowerCase().includes(query);
        const matchesCast = m.cast.some(actor => actor.toLowerCase().includes(query));
        if (!matchesTitle && !matchesDirector && !matchesCast) return false;
      }
      // Genre filter
      if (filterGenre && !m.genres.includes(filterGenre)) return false;
      // Language filter
      if (filterLanguage && m.language.toLowerCase() !== filterLanguage.toLowerCase()) return false;
      // Rating filter
      if (filterRatingMin > 0 && m.rating < filterRatingMin) return false;
      // Runtime filter
      if (filterRuntimeMax < 180 && m.runtime > filterRuntimeMax) return false;
      
      return true;
    });
  };

  const filteredMoviesList = getFilteredMovies();

  // --- MOVIE POSTER PATH UTILITY ---
  const getPosterUrl = (movie: Movie) => {
    // If we have a TMDB poster path, load it. Otherwise, return null (renders fallback CSS)
    if (movie.poster_path && movie.poster_path.startsWith('/')) {
      return `https://image.tmdb.org/t/p/w500${movie.poster_path}`;
    }
    return null;
  };

  if (loading && movies.length === 0) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', background: 'var(--bg-primary)' }}>
        <RefreshCw size={48} className="animate-spin" style={{ color: 'var(--accent-purple)', marginBottom: '15px' }} />
        <h2 style={{ fontSize: '1.2rem', fontWeight: 600 }}>CineCompanion is preparing...</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '5px' }}>Loading catalog database</p>
      </div>
    );
  }

  return (
    <div className="app-container">
      
      {/* --- ONBOARDING TASTE PROFILE OVERLAY --- */}
      {onboardingStep !== null && (
        <div className="onboarding-overlay">
          <div className="onboarding-card glass-panel animate-fade-in">
            <div className="onboarding-header">
              <h1>CineCompanion</h1>
              <p className="section-subtitle">Let's craft your personalized movie companion dashboard</p>
            </div>
            
            <div className="onboarding-step-indicator">
              <div className={`step-dot ${onboardingStep === 1 ? 'active' : ''}`} />
              <div className={`step-dot ${onboardingStep === 2 ? 'active' : ''}`} />
              <div className={`step-dot ${onboardingStep === 3 ? 'active' : ''}`} />
            </div>

            {/* STEP 1: Select Genres */}
            {onboardingStep === 1 && (
              <div className="animate-fade-in">
                <h3 style={{ marginBottom: '20px', textAlign: 'center' }}>Which movie genres do you enjoy most?</h3>
                <div className="selection-grid">
                  {GENRES_LIST.map(genre => (
                    <div 
                      key={genre} 
                      className={`onboard-item ${onboardingGenres.includes(genre) ? 'selected' : ''}`}
                      onClick={() => handleToggleOnboardingGenre(genre)}
                    >
                      {genre}
                    </div>
                  ))}
                </div>
                <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '20px' }}>
                  <button 
                    className="btn-primary" 
                    disabled={onboardingGenres.length === 0}
                    onClick={() => setOnboardingStep(2)}
                  >
                    Next Step <ChevronRight size={18} />
                  </button>
                </div>
              </div>
            )}

            {/* STEP 2: Select Moods */}
            {onboardingStep === 2 && (
              <div className="animate-fade-in">
                <h3 style={{ marginBottom: '20px', textAlign: 'center' }}>Select moods you often watch movies for</h3>
                <div className="selection-grid">
                  {MOODS_LIST.map(mood => (
                    <div 
                      key={mood} 
                      className={`onboard-item ${onboardingMoods.includes(mood) ? 'selected' : ''}`}
                      onClick={() => handleToggleOnboardingMood(mood)}
                    >
                      {mood}
                    </div>
                  ))}
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
                  <button className="btn-secondary" onClick={() => setOnboardingStep(1)}>
                    Back
                  </button>
                  <button 
                    className="btn-primary" 
                    disabled={onboardingMoods.length === 0}
                    onClick={() => setOnboardingStep(3)}
                  >
                    Next Step <ChevronRight size={18} />
                  </button>
                </div>
              </div>
            )}

            {/* STEP 3: Rate 3 movies */}
            {onboardingStep === 3 && (
              <div className="animate-fade-in">
                <h3 style={{ marginBottom: '10px', textAlign: 'center' }}>Rate some popular films you have seen</h3>
                <p className="section-subtitle" style={{ textAlign: 'center', marginBottom: '25px' }}>
                  Rate at least 3 movies so we can calibrate your content similarity profile.
                  ({Object.keys(onboardingRatings).length}/3 rated)
                </p>
                
                <div className="onboarding-movies-grid">
                  {movies.slice(0, 8).map(movie => {
                    const posterUrl = getPosterUrl(movie);
                    const currentRating = onboardingRatings[movie.id] || 0;
                    
                    return (
                      <div key={movie.id} className="glass-card" style={{ padding: '12px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        <div style={{ height: '140px', background: '#1b192e', borderRadius: '8px', overflow: 'hidden' }}>
                          {posterUrl ? (
                            <img src={posterUrl} alt={movie.title} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                          ) : (
                            <div className="movie-poster-placeholder" style={{ fontSize: '0.8rem', padding: '10px' }}>{movie.title}</div>
                          )}
                        </div>
                        <div style={{ fontWeight: 600, fontSize: '0.9rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                          {movie.title}
                        </div>
                        <div className="star-rating-widget" style={{ justifyContent: 'center' }}>
                          {[1, 2, 3, 4, 5].map(star => (
                            <button 
                              key={star} 
                              className={star <= currentRating ? 'filled' : ''}
                              onClick={() => handleOnboardingRate(movie.id, star)}
                            >
                              <Star size={16} fill={star <= currentRating ? '#fbbf24' : 'none'} />
                            </button>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
                
                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
                  <button className="btn-secondary" onClick={() => setOnboardingStep(2)}>
                    Back
                  </button>
                  <button 
                    className="btn-primary" 
                    disabled={Object.keys(onboardingRatings).length < 3}
                    onClick={handleFinishOnboarding}
                  >
                    Enter CineCompanion
                  </button>
                </div>
              </div>
            )}

          </div>
        </div>
      )}

      {/* --- SIDEBAR --- */}
      <aside className="sidebar">
        <div className="logo-section">
          <Film size={26} color="#d946ef" style={{ strokeWidth: 2.5 }} />
          <span>CineCompanion</span>
        </div>
        
        <nav className="nav-links">
          <button 
            className={`nav-link ${currentTab === 'discover' ? 'active' : ''}`}
            onClick={() => setCurrentTab('discover')}
          >
            <Compass size={20} />
            <span>Discover</span>
          </button>
          
          <button 
            className={`nav-link ${currentTab === 'search' ? 'active' : ''}`}
            onClick={() => setCurrentTab('search')}
          >
            <Search size={20} />
            <span>Search & Filters</span>
          </button>
          
          <button 
            className={`nav-link ${currentTab === 'watchlist' ? 'active' : ''}`}
            onClick={() => setCurrentTab('watchlist')}
          >
            <Heart size={20} />
            <span>Smart Watchlist</span>
          </button>
          
          <button 
            className={`nav-link ${currentTab === 'stats' ? 'active' : ''}`}
            onClick={() => setCurrentTab('stats')}
          >
            <BarChart2 size={20} />
            <span>My Taste Stats</span>
          </button>
          
          <button 
            className={`nav-link ${currentTab === 'settings' ? 'active' : ''}`}
            onClick={() => setCurrentTab('settings')}
          >
            <Settings size={20} />
            <span>Settings</span>
          </button>
        </nav>
        
        <div className="sidebar-footer">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            <Activity size={14} color="#10b981" />
            <span>AI Model Running</span>
          </div>
        </div>
      </aside>

      {/* --- MAIN DISPLAY --- */}
      <main className="main-content">
        
        {/* --- DISCOVER TAB --- */}
        {currentTab === 'discover' && (
          <div className="animate-fade-in">
            <div className="section-header">
              <div>
                <h2 className="section-title">Personalized Recommendations</h2>
                <p className="section-subtitle">Highly tailored matches based on your taste profile</p>
              </div>
              <button 
                className="btn-secondary" 
                onClick={fetchRecommendations} 
                disabled={recsLoading}
                style={{ gap: '6px' }}
              >
                <RefreshCw size={14} className={recsLoading ? 'animate-spin' : ''} /> Refresh Matcher
              </button>
            </div>

            {/* Mood selector chip list */}
            <div style={{ marginBottom: '10px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
              What mood are you in? Select one to adjust recommendations:
            </div>
            <div className="mood-chips-container">
              <button 
                className={`mood-chip ${preferredMood === "" ? 'active' : ''}`}
                onClick={() => setPreferredMood("")}
              >
                🎯 All Matches
              </button>
              {MOODS_LIST.map(mood => (
                <button 
                  key={mood} 
                  className={`mood-chip ${preferredMood === mood ? 'active' : ''}`}
                  onClick={() => setPreferredMood(mood)}
                >
                  {mood}
                </button>
              ))}
            </div>

            {recsLoading ? (
              <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-secondary)' }}>
                <RefreshCw size={40} className="animate-spin" style={{ margin: '0 auto 15px auto', color: 'var(--accent-purple)' }} />
                <p>Analyzing ratings and recalculating vectors...</p>
              </div>
            ) : recommendations.length === 0 ? (
              <div className="glass-panel" style={{ padding: '40px', textAlignment: 'center' } as any}>
                <p style={{ marginBottom: '20px' }}>You haven't rated enough movies yet. Go to Search to rate movies or reset the app to restart onboarding!</p>
                <button className="btn-primary" onClick={() => setCurrentTab('search')}>Go to Search</button>
              </div>
            ) : (
              <>
                {/* Main recommendations grid */}
                <div className="movie-grid">
                  {recommendations.map(res => {
                    const movie = res.movie;
                    const posterUrl = getPosterUrl(movie);
                    const isWatchlisted = watchlist.includes(movie.id);
                    
                    return (
                      <div key={movie.id} className="movie-card glass-panel animate-fade-in">
                        <div className="match-badge">{res.match_percentage}% Match</div>
                        
                        {isWatchlisted && (
                          <div className="watchlist-badge">
                            <Check size={12} /> Watchlist
                          </div>
                        )}
                        
                        <div className="movie-poster-wrapper">
                          {posterUrl ? (
                            <img src={posterUrl} alt={movie.title} className="movie-poster" />
                          ) : (
                            <div className="movie-poster-placeholder">
                              <span>{movie.title}</span>
                              <div className="poster-genres">{movie.genres.slice(0, 2).join(', ')}</div>
                            </div>
                          )}
                          
                          {/* Hover action overlay */}
                          <div className="movie-card-hover-actions">
                            <button 
                              className={`hover-btn ${isWatchlisted ? 'active' : ''}`}
                              title={isWatchlisted ? "Remove from watchlist" : "Add to watchlist"}
                              onClick={() => handleToggleWatchlist(movie.id)}
                            >
                              <Heart size={20} fill={isWatchlisted ? "white" : "none"} />
                            </button>
                            <button 
                              className="hover-btn"
                              title="View details & rate"
                              onClick={() => setActiveMovieDetail(movie)}
                            >
                              <Info size={20} />
                            </button>
                          </div>
                        </div>
                        
                        <div className="movie-card-info">
                          <h4 className="movie-card-title">{movie.title}</h4>
                          <div className="movie-card-meta">
                            <span>{movie.year} • {movie.runtime}m</span>
                            <div className="movie-rating">
                              <Star size={14} fill="#fbbf24" stroke="#fbbf24" />
                              <span>{movie.rating}</span>
                            </div>
                          </div>
                          
                          <div className="explanation-bar" title={res.explanation}>
                            💡 {res.explanation}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* Surprise me section */}
                <div style={{ marginTop: '50px' }}>
                  <div className="section-header">
                    <div>
                      <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Sparkles size={24} color="#d946ef" /> Surprise Recommendations
                      </h2>
                      <p className="section-subtitle">Expanding your tastes with films outside your usual genres</p>
                    </div>
                  </div>
                  <div className="carousel-container">
                    {surpriseRecs.map(res => {
                      const movie = res.movie;
                      const posterUrl = getPosterUrl(movie);
                      const isWatchlisted = watchlist.includes(movie.id);
                      
                      return (
                        <div key={movie.id} className="carousel-card glass-panel">
                          <div style={{ position: 'relative' }}>
                            {posterUrl ? (
                              <img src={posterUrl} alt={movie.title} className="carousel-poster" />
                            ) : (
                              <div className="movie-poster-placeholder" style={{ height: '160px' }}>{movie.title}</div>
                            )}
                            <button 
                              className="hover-btn" 
                              style={{ position: 'absolute', right: '10px', bottom: '-15px', zIndex: 5, width: '36px', height: '36px' }}
                              onClick={() => handleToggleWatchlist(movie.id)}
                            >
                              {isWatchlisted ? <Check size={16} /> : <Plus size={16} />}
                            </button>
                          </div>
                          <div className="carousel-content">
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, width: '80%', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                {movie.title}
                              </h4>
                              <span style={{ fontSize: '0.8rem', color: '#fbbf24', fontWeight: 700 }}>★ {movie.rating}</span>
                            </div>
                            <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden', height: '48px', lineHeight: '1.4' }}>
                              {movie.overview}
                            </p>
                            <div style={{ fontSize: '0.7rem', color: 'var(--accent-pink)', borderTop: '1px solid rgba(255,255,255,0.03)', paddingTop: '8px', fontStyle: 'italic' }}>
                              💡 {res.explanation}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Hidden gems section */}
                <div style={{ marginTop: '30px' }}>
                  <div className="section-header">
                    <div>
                      <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Trophy size={24} color="#3b82f6" /> Hidden Gems
                      </h2>
                      <p className="section-subtitle">Highly rated movies you may have missed, matching your interests</p>
                    </div>
                  </div>
                  <div className="carousel-container">
                    {hiddenGems.map(res => {
                      const movie = res.movie;
                      const posterUrl = getPosterUrl(movie);
                      const isWatchlisted = watchlist.includes(movie.id);
                      
                      return (
                        <div key={movie.id} className="carousel-card glass-panel">
                          <div style={{ position: 'relative' }}>
                            {posterUrl ? (
                              <img src={posterUrl} alt={movie.title} className="carousel-poster" />
                            ) : (
                              <div className="movie-poster-placeholder" style={{ height: '160px' }}>{movie.title}</div>
                            )}
                            <button 
                              className="hover-btn" 
                              style={{ position: 'absolute', right: '10px', bottom: '-15px', zIndex: 5, width: '36px', height: '36px' }}
                              onClick={() => handleToggleWatchlist(movie.id)}
                            >
                              {isWatchlisted ? <Check size={16} /> : <Plus size={16} />}
                            </button>
                          </div>
                          <div className="carousel-content">
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, width: '80%', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                {movie.title}
                              </h4>
                              <span style={{ fontSize: '0.8rem', color: '#fbbf24', fontWeight: 700 }}>★ {movie.rating}</span>
                            </div>
                            <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden', height: '48px', lineHeight: '1.4' }}>
                              {movie.overview}
                            </p>
                            <div style={{ fontSize: '0.7rem', color: 'var(--accent-purple)', borderTop: '1px solid rgba(255,255,255,0.03)', paddingTop: '8px', fontStyle: 'italic' }}>
                              💡 {res.explanation}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </>
            )}
          </div>
        )}

        {/* --- SEARCH & FILTERS TAB --- */}
        {currentTab === 'search' && (
          <div className="animate-fade-in">
            <div className="section-header">
              <div>
                <h2 className="section-title">Catalog Explorer</h2>
                <p className="section-subtitle">Search, filter, and rate movies to improve recommendations</p>
              </div>
            </div>

            {/* Filter Bar */}
            <div className="filter-bar glass-panel">
              <div className="filter-row">
                <div className="search-input-wrapper">
                  <Search size={18} className="search-icon" />
                  <input 
                    type="text" 
                    placeholder="Search by movie title, actor, director..." 
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                </div>
                
                <select 
                  className="filter-select"
                  value={filterGenre}
                  onChange={(e) => setFilterGenre(e.target.value)}
                >
                  <option value="">All Genres</option>
                  {GENRES_LIST.map(g => <option key={g} value={g}>{g}</option>)}
                </select>

                <select 
                  className="filter-select"
                  value={filterLanguage}
                  onChange={(e) => setFilterLanguage(e.target.value)}
                >
                  <option value="">All Languages</option>
                  {LANGUAGES_LIST.map(l => <option key={l} value={l}>{l}</option>)}
                </select>
              </div>

              <div className="filter-row">
                <div className="slider-group">
                  <label>Min Rating: {filterRatingMin > 0 ? `${filterRatingMin} ★` : 'Any'}</label>
                  <input 
                    type="range" 
                    min="0" 
                    max="9" 
                    step="0.5"
                    value={filterRatingMin} 
                    onChange={(e) => setFilterRatingMin(parseFloat(e.target.value))}
                  />
                </div>

                <div className="slider-group">
                  <label>Max Runtime: {filterRuntimeMax < 180 ? `${filterRuntimeMax} min` : 'Any'}</label>
                  <input 
                    type="range" 
                    min="70" 
                    max="180" 
                    step="5"
                    value={filterRuntimeMax} 
                    onChange={(e) => setFilterRuntimeMax(parseInt(e.target.value))}
                  />
                </div>

                <button 
                  className="btn-secondary"
                  onClick={() => {
                    setSearchQuery("");
                    setFilterGenre("");
                    setFilterLanguage("");
                    setFilterRatingMin(0);
                    setFilterRuntimeMax(180);
                  }}
                >
                  Clear Filters
                </button>
              </div>
            </div>

            {/* Results Grid */}
            {filteredMoviesList.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '50px 0', color: 'var(--text-secondary)' }}>
                <p>No movies matched your filters. Try widening your criteria!</p>
              </div>
            ) : (
              <div className="movie-grid">
                {filteredMoviesList.map(movie => {
                  const posterUrl = getPosterUrl(movie);
                  const isWatchlisted = watchlist.includes(movie.id);
                  const userRating = ratings[movie.id] || 0;
                  
                  return (
                    <div key={movie.id} className="movie-card glass-panel">
                      {isWatchlisted && (
                        <div className="watchlist-badge">
                          <Check size={12} /> Watchlist
                        </div>
                      )}
                      
                      {userRating > 0 && (
                        <div className="match-badge" style={{ borderColor: '#fbbf24', color: '#fbbf24' }}>
                          Rated {userRating} ★
                        </div>
                      )}

                      <div className="movie-poster-wrapper">
                        {posterUrl ? (
                          <img src={posterUrl} alt={movie.title} className="movie-poster" />
                        ) : (
                          <div className="movie-poster-placeholder">
                            <span>{movie.title}</span>
                            <div className="poster-genres">{movie.genres.slice(0, 2).join(', ')}</div>
                          </div>
                        )}
                        
                        {/* Hover action overlay */}
                        <div className="movie-card-hover-actions">
                          <button 
                            className={`hover-btn ${isWatchlisted ? 'active' : ''}`}
                            title={isWatchlisted ? "Remove from watchlist" : "Add to watchlist"}
                            onClick={() => handleToggleWatchlist(movie.id)}
                          >
                            <Heart size={20} fill={isWatchlisted ? "white" : "none"} />
                          </button>
                          <button 
                            className="hover-btn"
                            title="View details & rate"
                            onClick={() => setActiveMovieDetail(movie)}
                          >
                            <Info size={20} />
                          </button>
                        </div>
                      </div>
                      
                      <div className="movie-card-info">
                        <h4 className="movie-card-title">{movie.title}</h4>
                        <div className="movie-card-meta">
                          <span>{movie.year} • {movie.runtime}m</span>
                          <div className="movie-rating">
                            <Star size={14} fill="#fbbf24" stroke="#fbbf24" />
                            <span>{movie.rating}</span>
                          </div>
                        </div>
                        <div style={{ marginTop: 'auto', display: 'flex', gap: '3px', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                          {movie.genres.slice(0, 3).join(' • ')}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* --- WATCHLIST TAB --- */}
        {currentTab === 'watchlist' && (
          <div className="animate-fade-in">
            <div className="section-header">
              <div>
                <h2 className="section-title">My Smart Watchlist</h2>
                <p className="section-subtitle">Tracked movies you intend to watch. Companion provides custom recs from this list!</p>
              </div>
            </div>

            {watchlist.length === 0 ? (
              <div className="glass-panel" style={{ padding: '60px', textAlignment: 'center' } as any}>
                <Heart size={44} color="var(--text-muted)" style={{ margin: '0 auto 15px auto', display: 'block' }} />
                <p style={{ color: 'var(--text-secondary)', marginBottom: '20px' }}>Your watchlist is currently empty. Explore the catalog and click the Heart icon to populate it!</p>
                <button className="btn-primary" onClick={() => setCurrentTab('discover')}>Explore Suggestions</button>
              </div>
            ) : (
              <div className="watchlist-grid">
                {watchlist.map(movieId => {
                  const movie = movies.find(m => m.id === movieId);
                  if (!movie) return null;
                  const posterUrl = getPosterUrl(movie);
                  
                  return (
                    <div key={movie.id} className="watchlist-item glass-panel animate-fade-in">
                      {posterUrl ? (
                        <img src={posterUrl} alt={movie.title} className="watchlist-item-poster" />
                      ) : (
                        <div className="watchlist-item-poster" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#1b192e', fontSize: '0.7rem', padding: '5px' }}>{movie.title}</div>
                      )}
                      
                      <div className="watchlist-item-details">
                        <div>
                          <h4 className="watchlist-item-title">{movie.title}</h4>
                          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{movie.year} • {movie.runtime}m</span>
                        </div>
                        
                        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                          <button 
                            className="btn-secondary" 
                            style={{ padding: '5px 10px', fontSize: '0.8rem' }}
                            onClick={() => setActiveMovieDetail(movie)}
                          >
                            Details & Rate
                          </button>
                        </div>
                      </div>
                      
                      <button 
                        className="watchlist-remove-btn" 
                        onClick={() => handleToggleWatchlist(movie.id)}
                        title="Remove from watchlist"
                      >
                        <Trash size={16} />
                      </button>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* --- STATS TAB --- */}
        {currentTab === 'stats' && (
          <div className="animate-fade-in">
            <div className="section-header">
              <div>
                <h2 className="section-title">My Taste Dashboard</h2>
                <p className="section-subtitle">Visual analytics generated from your rating metrics</p>
              </div>
            </div>

            <div className="stats-summary-row">
              <div className="stat-item glass-panel">
                <div className="stat-val">{stats.totalRated}</div>
                <div className="stat-lbl">Movies Rated</div>
              </div>
              <div className="stat-item glass-panel">
                <div className="stat-val">{stats.totalWatchlist}</div>
                <div className="stat-lbl">In Watchlist</div>
              </div>
              <div className="stat-item glass-panel">
                <div className="stat-val">{stats.watchTimeHours}h</div>
                <div className="stat-lbl">Total Screen Time</div>
              </div>
            </div>

            <div className="stats-container">
              
              {/* Genre Distribution Chart */}
              <div className="stats-card glass-panel">
                <h3 style={{ marginBottom: '20px', fontSize: '1.1rem', fontWeight: 700 }}>Top Genres</h3>
                {stats.sortedGenres.length === 0 ? (
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Rate movies to see your favorite genre distribution!</p>
                ) : (
                  stats.sortedGenres.map(([genre, count]) => {
                    const maxVal = stats.sortedGenres[0][1];
                    const percent = maxVal > 0 ? (count / maxVal) * 100 : 0;
                    return (
                      <div key={genre} className="chart-bar-row">
                        <span className="chart-bar-label">{genre}</span>
                        <div className="chart-bar-track">
                          <div className="chart-bar-fill" style={{ width: `${percent}%` }} />
                        </div>
                        <span className="chart-bar-val">{count}</span>
                      </div>
                    );
                  })
                )}
              </div>

              {/* Rating Distribution Chart */}
              <div className="stats-card glass-panel">
                <h3 style={{ marginBottom: '20px', fontSize: '1.1rem', fontWeight: 700 }}>Ratings Breakdown</h3>
                {stats.totalRated === 0 ? (
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Rate movies to view ratings distribution!</p>
                ) : (
                  Object.entries(stats.ratingDistribution).reverse().map(([rating, count]) => {
                    const maxCount = Math.max(...Object.values(stats.ratingDistribution));
                    const percent = maxCount > 0 ? (count / maxCount) * 100 : 0;
                    return (
                      <div key={rating} className="chart-bar-row">
                        <span className="chart-bar-label" style={{ width: '60px' }}>{rating} Stars</span>
                        <div className="chart-bar-track">
                          <div className="chart-bar-fill" style={{ width: `${percent}%`, background: 'linear-gradient(to right, #fbbf24, #f59e0b)' }} />
                        </div>
                        <span className="chart-bar-val">{count}</span>
                      </div>
                    );
                  })
                )}
              </div>

            </div>

            {/* List of rated movies */}
            <div className="glass-panel stats-card" style={{ marginTop: '30px' }}>
              <h3 style={{ marginBottom: '20px', fontSize: '1.1rem', fontWeight: 700 }}>Rated Movie History</h3>
              {Object.keys(ratings).length === 0 ? (
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>You haven't rated any movies yet.</p>
              ) : (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                  {Object.entries(ratings).map(([idStr, rating]) => {
                    const id = parseInt(idStr);
                    const movie = movies.find(m => m.id === id);
                    if (!movie) return null;
                    return (
                      <div key={id} style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'rgba(255,255,255,0.03)', padding: '6px 12px', borderRadius: '20px', border: '1px solid rgba(255,255,255,0.05)', fontSize: '0.85rem' }}>
                        <span>{movie.title}</span>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '2px', color: '#fbbf24', fontWeight: 700 }}>
                          ★ {rating}
                        </span>
                        <button 
                          style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', display: 'flex', alignItems: 'center' }}
                          onClick={() => handleRemoveRating(movie.id)}
                          title="Remove rating"
                        >
                          ×
                        </button>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

          </div>
        )}

        {/* --- SETTINGS TAB --- */}
        {currentTab === 'settings' && (
          <div className="animate-fade-in">
            <div className="section-header">
              <div>
                <h2 className="section-title">Application Settings</h2>
                <p className="section-subtitle">Manage AI integration keys and local profiles</p>
              </div>
            </div>

            <div className="glass-panel settings-panel" style={{ padding: '30px' }}>
              
              <div className="form-group">
                <label>Google Gemini API Key</label>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <input 
                    type="password" 
                    placeholder={geminiApiKey ? "••••••••••••••••••••••••••••••••" : "Enter your Gemini API key..."}
                    value={geminiApiKey}
                    onChange={(e) => setGeminiApiKey(e.target.value)}
                  />
                  <button 
                    className="btn-primary"
                    onClick={() => handleSaveApiKey(geminiApiKey)}
                  >
                    Save Key
                  </button>
                </div>
                <p className="help-text">
                  CineCompanion uses Google's <code>gemini-1.5-flash</code> model to provide deep conversational movie matching. 
                  Get a free key from the Google AI Studio. 
                  <strong> If left blank, the chatbot falls back to our smart offline matching rules.</strong>
                </p>
              </div>

              <div style={{ borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '25px', marginTop: '25px' }}>
                <h4 style={{ color: 'var(--accent-pink)', marginBottom: '10px', fontWeight: 700 }}>Danger Zone</h4>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '15px', lineHeight: '1.4' }}>
                  Resetting clears your ratings matrix, onboarding choices, watchlist registry, and cached API credentials.
                </p>
                <button className="btn-secondary" style={{ borderColor: 'rgba(239, 68, 68, 0.4)', color: '#ef4444' }} onClick={handleResetApp}>
                  Reset Taste Profile & Keys
                </button>
              </div>

            </div>
          </div>
        )}

      </main>

      {/* --- FLOATING AI CHAT COMPANION --- */}
      <div className={`chat-drawer glass-panel ${chatCollapsed ? 'collapsed' : ''}`}>
        
        {chatCollapsed ? (
          <button className="chat-trigger-btn" onClick={() => setChatCollapsed(false)}>
            <MessageSquare size={20} />
            <span>AI Companion</span>
          </button>
        ) : (
          <>
            <div className="chat-header">
              <div className="chat-title-row">
                <MessageSquare size={18} color="#c084fc" />
                <div style={{ display: 'flex', flexDirection: 'column' }}>
                  <span style={{ fontSize: '0.9rem', fontWeight: 700 }}>CineCompanion</span>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <div className={`chat-dot ${geminiApiKey ? '' : 'offline'}`} />
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>
                      {geminiApiKey ? 'Gemini AI Mode' : 'Local Rule Mode'}
                    </span>
                  </div>
                </div>
              </div>
              <button className="chat-close-btn" onClick={() => setChatCollapsed(true)}>
                ×
              </button>
            </div>
            
            <div className="chat-messages">
              {chatMessages.map((msg, index) => (
                <div key={index} className={`chat-bubble ${msg.role}`}>
                  {msg.content.split('\n').map((line, idx) => (
                    <p key={idx} style={{ marginBottom: line.trim() === '' ? '10px' : '4px' }}>{line}</p>
                  ))}
                </div>
              ))}
              
              {chatLoading && (
                <div className="chat-typing-indicator">
                  <div className="chat-dot-anim" />
                  <div className="chat-dot-anim" />
                  <div className="chat-dot-anim" />
                </div>
              )}
              
              <div ref={chatEndRef} />
            </div>
            
            <form className="chat-input-area" onSubmit={handleSendChatMessage}>
              <input 
                type="text" 
                placeholder="Ask for details, specific moods, or actors..."
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                disabled={chatLoading}
              />
              <button className="chat-send-btn" type="submit" disabled={!chatInput.trim() || chatLoading}>
                <Send size={16} />
              </button>
            </form>
          </>
        )}

      </div>

      {/* --- DETAILS & RATINGS MODAL --- */}
      {activeMovieDetail && (
        <div className="modal-overlay" onClick={() => setActiveMovieDetail(null)}>
          <div className="modal-content glass-panel animate-fade-in" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setActiveMovieDetail(null)}>
              ×
            </button>
            
            {getPosterUrl(activeMovieDetail) ? (
              <img src={getPosterUrl(activeMovieDetail)!} alt={activeMovieDetail.title} className="modal-poster" />
            ) : (
              <div className="modal-poster" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#1b192e', padding: '20px', textAlign: 'center' }}>
                <span style={{ fontSize: '1.2rem', fontWeight: 800 }}>{activeMovieDetail.title}</span>
                <span style={{ fontSize: '0.8rem', color: 'var(--accent-pink)', marginTop: '10px' }}>{activeMovieDetail.genres.join(', ')}</span>
              </div>
            )}
            
            <div className="modal-body">
              <div>
                <h3 className="modal-title">{activeMovieDetail.title}</h3>
                <div className="modal-meta-row" style={{ marginTop: '5px' }}>
                  <span>{activeMovieDetail.year}</span>
                  <span>•</span>
                  <span>{activeMovieDetail.runtime} min</span>
                  <span>•</span>
                  <span>{activeMovieDetail.language}</span>
                  <span>•</span>
                  <span style={{ color: '#fbbf24', fontWeight: 600 }}>★ {activeMovieDetail.rating} ({activeMovieDetail.vote_count.toLocaleString()} votes)</span>
                </div>
              </div>
              
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                {activeMovieDetail.genres.map(g => (
                  <span key={g} style={{ fontSize: '0.75rem', background: 'rgba(139, 92, 246, 0.15)', border: '1px solid rgba(139, 92, 246, 0.3)', padding: '4px 10px', borderRadius: '15px', color: '#c084fc' }}>
                    {g}
                  </span>
                ))}
                {activeMovieDetail.moods.map(m => (
                  <span key={m} style={{ fontSize: '0.75rem', background: 'rgba(217, 70, 239, 0.15)', border: '1px solid rgba(217, 70, 239, 0.3)', padding: '4px 10px', borderRadius: '15px', color: '#f472b6' }}>
                    🎭 {m}
                  </span>
                ))}
              </div>

              <div>
                <h5 style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '4px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Overview</h5>
                <p style={{ fontSize: '0.9rem', lineHeight: '1.5', color: 'var(--text-primary)' }}>
                  {activeMovieDetail.overview}
                </p>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                <div>
                  <h5 style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '2px', textTransform: 'uppercase' }}>Director</h5>
                  <span style={{ fontSize: '0.9rem', fontWeight: 500 }}>{activeMovieDetail.director}</span>
                </div>
                <div>
                  <h5 style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '2px', textTransform: 'uppercase' }}>Key Cast</h5>
                  <span style={{ fontSize: '0.9rem', fontWeight: 500 }}>{activeMovieDetail.cast.join(', ')}</span>
                </div>
              </div>

              <div className="modal-interactive">
                <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Your Rating:</span>
                  <div className="star-rating-widget">
                    {[1, 2, 3, 4, 5].map(star => {
                      const currentRating = ratings[activeMovieDetail.id] || 0;
                      return (
                        <button 
                          key={star} 
                          className={star <= currentRating ? 'filled' : ''}
                          onClick={() => handleRateMovie(activeMovieDetail.id, star)}
                        >
                          <Star size={24} fill={star <= currentRating ? '#fbbf24' : 'none'} />
                        </button>
                      );
                    })}
                  </div>
                </div>

                <div style={{ marginLeft: 'auto' }}>
                  <button 
                    className={watchlist.includes(activeMovieDetail.id) ? 'btn-secondary' : 'btn-primary'}
                    onClick={() => handleToggleWatchlist(activeMovieDetail.id)}
                  >
                    {watchlist.includes(activeMovieDetail.id) ? (
                      <>
                        <Check size={16} /> In Watchlist
                      </>
                    ) : (
                      <>
                        <Plus size={16} /> Add to Watchlist
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
