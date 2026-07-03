# D:\YASH\Movie_Recommendation_System\backend\recommender.py

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dataset import MOVIES, SIMULATED_PERSONAS

class MovieRecommender:
    def __init__(self):
        self.movies = MOVIES
        self.movies_df = pd.DataFrame(MOVIES)
        self.personas = SIMULATED_PERSONAS
        self._prepare_cbf()

    def _prepare_cbf(self):
        """Prepare content-based filtering matrices."""
        # Create metadata soup: combine genres, director, cast, overview, and moods
        soup = []
        for _, movie in self.movies_df.iterrows():
            genres = " ".join(movie["genres"])
            director = movie["director"]
            cast = " ".join(movie["cast"])
            overview = movie["overview"]
            moods = " ".join(movie["moods"])
            # Weight genres, director, and moods heavily by repeating them
            item_soup = f"{genres} {genres} {director} {cast} {overview} {moods} {moods}"
            soup.append(item_soup.lower())
        
        self.movies_df["soup"] = soup
        
        # Compute TF-IDF Matrix
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.movies_df["soup"])
        
        # Pairwise cosine similarity matrix (for item-item lookups)
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def get_movie_by_id(self, movie_id):
        """Get movie metadata by ID."""
        match = self.movies_df[self.movies_df["id"] == movie_id]
        if not match.empty:
            return match.iloc[0].to_dict()
        return None

    def get_content_based_scores(self, user_ratings):
        """
        Compute content-based similarity scores for all movies based on user ratings.
        user_ratings: dict of {movie_id: rating_value} where rating_value is 1-5.
        """
        if not user_ratings:
            return np.zeros(len(self.movies))
            
        # Create a user profile vector
        user_profile = np.zeros(self.tfidf_matrix.shape[1])
        total_weight = 0
        
        for movie_id, rating in user_ratings.items():
            # Find the index of the movie in our dataframe
            idx_list = self.movies_df.index[self.movies_df["id"] == movie_id].tolist()
            if not idx_list:
                continue
            idx = idx_list[0]
            
            # Weight: ratings 4-5 are positive, 1-2 are negative, 3 is neutral
            weight = rating - 3.0
            if weight == 0:
                weight = 0.1 # slightly positive weight for just watching/rating 3 stars
                
            user_profile += self.tfidf_matrix[idx].toarray()[0] * weight
            total_weight += abs(weight)
            
        if total_weight > 0:
            user_profile = user_profile / total_weight
            
        # Calculate similarity of user profile with all movies
        scores = cosine_similarity(user_profile.reshape(1, -1), self.tfidf_matrix)[0]
        return scores

    def get_collaborative_filtering_scores(self, user_ratings):
        """
        Compute predicted movie ratings using User-User Collaborative Filtering.
        user_ratings: dict of {movie_id: rating_value}.
        """
        # Create a rating matrix for the personas + current user
        # Index: Personas, Columns: Movie IDs
        all_movie_ids = self.movies_df["id"].tolist()
        
        persona_ratings_list = []
        for p in self.personas:
            row = {m_id: np.nan for m_id in all_movie_ids}
            for m_id, rat in p["ratings"].items():
                if m_id in row:
                    row[m_id] = rat
            persona_ratings_list.append(row)
            
        ratings_df = pd.DataFrame(persona_ratings_list)
        
        # Add current user ratings
        user_row = {m_id: np.nan for m_id in all_movie_ids}
        for m_id, rat in user_ratings.items():
            if m_id in user_row:
                user_row[m_id] = rat
        
        user_df = pd.DataFrame([user_row])
        ratings_df = pd.concat([ratings_df, user_df], ignore_index=True)
        user_idx = len(ratings_df) - 1
        
        # Center ratings (subtract user mean) to compute Pearson-like similarity
        # Since matrix is very sparse, we can also use Cosine Similarity on filled values (defaulting nan to 0 or neutral 3)
        filled_ratings = ratings_df.fillna(3.0) # Assume neutral 3.0 for unrated
        
        # Calculate cosine similarity between current user and all personas
        user_sims = cosine_similarity(filled_ratings.iloc[[user_idx]], filled_ratings.iloc[:-1])[0]
        
        # Find top 3 most similar personas
        top_indices = np.argsort(user_sims)[-3:]
        top_sims = user_sims[top_indices]
        
        # If no positive similarity, return zeros
        if np.sum(np.abs(top_sims)) == 0:
            return np.zeros(len(self.movies))
            
        # Predict ratings for all movies using weighted average of these top 3 personas
        pred_scores = np.zeros(len(self.movies))
        for i, m_id in enumerate(all_movie_ids):
            # If user already rated the movie, we can skip or set score to 0
            if m_id in user_ratings:
                pred_scores[i] = 0
                continue
                
            weights_sum = 0
            weighted_ratings_sum = 0
            for idx_sim, sim in zip(top_indices, top_sims):
                persona_rating = ratings_df.iloc[idx_sim][m_id]
                if not np.isnan(persona_rating):
                    # Weight by similarity
                    weighted_ratings_sum += sim * persona_rating
                    weights_sum += sim
            
            if weights_sum > 0:
                # Normalize predicted rating (1 to 5 scale) to a 0 to 1 score
                predicted_val = weighted_ratings_sum / weights_sum
                pred_scores[i] = (predicted_val - 1.0) / 4.0 # Scale to [0, 1]
            else:
                pred_scores[i] = 0.0
                
        return pred_scores

    def get_hybrid_recommendations(self, user_ratings, preferred_mood=None, active_filters=None, top_n=10):
        """
        Generate hybrid recommendations.
        user_ratings: dict of {movie_id: rating}.
        preferred_mood: string, e.g. "Mind-bending".
        active_filters: dict with optional keys 'genre', 'language', 'rating_min', 'runtime_max'.
        """
        # 1. Content-based scores (scaled to 0-1)
        cb_scores = self.get_content_based_scores(user_ratings)
        if cb_scores.max() > 0:
            cb_scores = cb_scores / cb_scores.max()
            
        # 2. Collaborative filtering scores (already 0-1)
        cf_scores = self.get_collaborative_filtering_scores(user_ratings)
        
        # 3. Popularity score (scaled vote_count to 0-1)
        max_votes = self.movies_df["vote_count"].max()
        pop_scores = self.movies_df["vote_count"].values / max_votes
        
        # 4. Combine scores (50% Content, 40% Collaborative, 10% Popularity)
        hybrid_scores = 0.5 * cb_scores + 0.4 * cf_scores + 0.1 * pop_scores
        
        # Create recommendation results list
        recommendations = []
        for i, movie in self.movies_df.iterrows():
            m_id = movie["id"]
            
            # Skip if already rated (watched) by user
            if m_id in user_ratings:
                continue
                
            score = hybrid_scores[i]
            
            # Apply Mood Boost (+0.20 if matches preferred mood)
            mood_match = False
            if preferred_mood:
                if preferred_mood.lower() in [m.lower() for m in movie["moods"]]:
                    score += 0.20
                    mood_match = True
                    
            # Apply filter checks
            if active_filters:
                # Genre filter (multi-select or single)
                filter_genre = active_filters.get("genre")
                if filter_genre:
                    if isinstance(filter_genre, list):
                        if not any(g in movie["genres"] for g in filter_genre):
                            continue
                    elif filter_genre not in movie["genres"]:
                        continue
                        
                # Language filter
                filter_lang = active_filters.get("language")
                if filter_lang and movie["language"].lower() != filter_lang.lower():
                    continue
                    
                # Min rating filter
                filter_min_rating = active_filters.get("rating_min")
                if filter_min_rating and movie["rating"] < float(filter_min_rating):
                    continue
                    
                # Max runtime filter
                filter_max_runtime = active_filters.get("runtime_max")
                if filter_max_runtime and movie["runtime"] > int(filter_max_runtime):
                    continue
            
            # Cap score at 1.0
            score = min(score, 1.0)
            
            # Generate explanation for this recommendation
            explanation = self._generate_explanation(movie.to_dict(), user_ratings, cb_scores[i], cf_scores[i], mood_match, preferred_mood)
            
            recommendations.append({
                "movie": movie.to_dict(),
                "score": float(score),
                "match_percentage": int(score * 100),
                "explanation": explanation
            })
            
        # Sort recommendations by score descending
        recommendations = sorted(recommendations, key=lambda x: x["score"], reverse=True)
        return recommendations[:top_n]

    def get_surprise_recommendations(self, user_ratings, top_n=5):
        """
        Recommend movies outside the user's typical genres/moods but likely to interest them.
        """
        if not user_ratings:
            # If no history, suggest highly rated diverse movies
            diverse_movies = self.movies_df.sample(min(top_n, len(self.movies_df)))
            return [{
                "movie": m.to_dict(),
                "score": 0.8,
                "match_percentage": 80,
                "explanation": "A handpicked highly-rated film to expand your cinematic horizons!"
            } for _, m in diverse_movies.iterrows()]

        # Identify user's highly rated movies (4 or 5 stars)
        highly_rated_ids = [m_id for m_id, r in user_ratings.items() if r >= 4]
        if not highly_rated_ids:
            highly_rated_ids = list(user_ratings.keys())
            
        highly_rated_movies = self.movies_df[self.movies_df["id"].isin(highly_rated_ids)]
        
        # Find user's favorite genres
        favorite_genres = set()
        for _, m in highly_rated_movies.iterrows():
            favorite_genres.update(m["genres"])
            
        # Find movies outside these favorite genres
        outside_movies_df = self.movies_df[~self.movies_df["genres"].apply(lambda g_list: any(g in favorite_genres for g in g_list))]
        
        # If no movies outside, just use all unrated movies
        if outside_movies_df.empty:
            outside_movies_df = self.movies_df[~self.movies_df["id"].isin(user_ratings.keys())]
            
        # Compute hybrid recommendations on these outside movies
        # We want highly rated movies that similar users liked, despite the genre difference!
        cf_scores = self.get_collaborative_filtering_scores(user_ratings)
        
        surprise_list = []
        for idx, movie in outside_movies_df.iterrows():
            m_id = movie["id"]
            if m_id in user_ratings:
                continue
                
            # Use collaborative filtering score + movie rating to represent potential interest
            cf_score = cf_scores[idx]
            movie_rating_score = (movie["rating"] - 5.0) / 5.0 # normalized
            
            score = 0.6 * cf_score + 0.4 * movie_rating_score
            
            # Generate surprise explanation
            non_fav_genres = movie["genres"]
            explanation = f"Introducing you to {', '.join(non_fav_genres)}. Though it's outside your typical watch list, users with similar tastes rated it highly!"
            
            surprise_list.append({
                "movie": movie.to_dict(),
                "score": float(score),
                "match_percentage": int(max(score, 0.5) * 100),
                "explanation": explanation
            })
            
        surprise_list = sorted(surprise_list, key=lambda x: x["score"], reverse=True)
        return surprise_list[:top_n]

    def get_hidden_gems(self, user_ratings, top_n=5):
        """
        Recommend hidden gems: movies with rating >= 7.2 but low popularity (vote_count < 3500).
        """
        gems_df = self.movies_df[(self.movies_df["rating"] >= 7.2) & (self.movies_df["vote_count"] <= 3500)]
        
        # Calculate user similarity to these gems
        cb_scores = self.get_content_based_scores(user_ratings)
        cf_scores = self.get_collaborative_filtering_scores(user_ratings)
        
        gems_list = []
        for idx, movie in gems_df.iterrows():
            m_id = movie["id"]
            if m_id in user_ratings:
                continue
                
            score = 0.5 * cb_scores[idx] + 0.5 * cf_scores[idx]
            
            explanation = f"A hidden gem with an impressive {movie['rating']}/10 rating, but overlooked by mainstream audiences ({movie['vote_count']:,} ratings). It matches your taste profile perfectly!"
            
            gems_list.append({
                "movie": movie.to_dict(),
                "score": float(score),
                "match_percentage": int(max(score, 0.4) * 100),
                "explanation": explanation
            })
            
        gems_list = sorted(gems_list, key=lambda x: x["score"], reverse=True)
        return gems_list[:top_n]

    def _generate_explanation(self, movie, user_ratings, cb_score, cf_score, mood_match, preferred_mood):
        """Generate a user-friendly explanation of why a movie is suggested."""
        reasons = []
        
        # 1. Active Mood
        if mood_match and preferred_mood:
            reasons.append(f"matches your current mood for '{preferred_mood}' movies")
            
        # 2. Similar Movies
        if user_ratings and cb_score > 0.3:
            # Find the movie rated >= 4 with the highest similarity
            highly_rated_user_movies = [m_id for m_id, r in user_ratings.items() if r >= 4]
            if highly_rated_user_movies:
                best_sim = -1
                best_sim_movie_title = ""
                
                # Index of recommended movie
                rec_idx = self.movies_df.index[self.movies_df["id"] == movie["id"]].tolist()[0]
                
                for rated_id in highly_rated_user_movies:
                    rated_idx_list = self.movies_df.index[self.movies_df["id"] == rated_id].tolist()
                    if not rated_idx_list:
                        continue
                    rated_idx = rated_idx_list[0]
                    sim = self.cosine_sim[rec_idx, rated_idx]
                    if sim > best_sim:
                        best_sim = sim
                        best_sim_movie_title = self.movies_df.iloc[rated_idx]["title"]
                        
                if best_sim > 0.4:
                    reasons.append(f"similar plot, style, or themes to '{best_sim_movie_title}' which you enjoyed")
                    
        # 3. Favorite Cast or Director
        if user_ratings:
            highly_rated_ids = [m_id for m_id, r in user_ratings.items() if r >= 4]
            if highly_rated_ids:
                highly_rated_movies = self.movies_df[self.movies_df["id"].isin(highly_rated_ids)]
                
                # Check directors
                fav_directors = set(highly_rated_movies["director"].tolist())
                if movie["director"] in fav_directors:
                    reasons.append(f"directed by {movie['director']}, who directed other movies you rated highly")
                    
                # Check actors
                fav_actors = set()
                for _, m in highly_rated_movies.iterrows():
                    fav_actors.update(m["cast"])
                common_actors = set(movie["cast"]).intersection(fav_actors)
                if common_actors:
                    reasons.append(f"features {list(common_actors)[0]}, one of your favorite actors")
                    
        # 4. Similar user tastes (Collaborative)
        if cf_score > 0.5:
            reasons.append("popular among users with taste profiles very similar to yours")
            
        # Compile explanations
        if not reasons:
            # Fallback explanation
            matching_genres = movie["genres"]
            reasons.append(f"features a solid blend of your preferred elements in {', '.join(matching_genres)}")
            
        # Combine the reasons into a clean sentence
        if len(reasons) >= 2:
            explanation = "It " + reasons[0] + ", and it also " + reasons[1] + "."
        else:
            explanation = "It " + reasons[0] + "."
            
        return explanation
