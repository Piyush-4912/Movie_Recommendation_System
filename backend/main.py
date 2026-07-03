# D:\YASH\Movie_Recommendation_System\backend\main.py

import os
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dataset import MOVIES
from recommender import MovieRecommender

app = FastAPI(title="Movie Recommendation System API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recommender = MovieRecommender()

# Pydantic models
class FilterParams(BaseModel):
    genre: Optional[List[str]] = None
    language: Optional[str] = None
    rating_min: Optional[float] = None
    runtime_max: Optional[int] = None

class RecommendationRequest(BaseModel):
    ratings: Dict[int, int]  # movie_id -> rating (1-5)
    preferred_mood: Optional[str] = None
    filters: Optional[FilterParams] = None
    top_n: Optional[int] = 10

class ChatMessage(BaseModel):
    role: str  # "user" or "model" / "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    ratings: Dict[int, int]
    watchlist: List[int]
    api_key: Optional[str] = None

@app.get("/api/movies")
def get_movies(
    search: Optional[str] = None,
    genre: Optional[str] = None,
    mood: Optional[str] = None,
    language: Optional[str] = None,
    rating_min: Optional[float] = None,
    runtime_max: Optional[int] = None
):
    """Fetch all movies in the dataset with optional filtering."""
    filtered = MOVIES.copy()
    
    if search:
        search_lower = search.lower()
        filtered = [
            m for m in filtered
            if search_lower in m["title"].lower() 
            or search_lower in m["director"].lower()
            or any(search_lower in actor.lower() for actor in m["cast"])
        ]
        
    if genre:
        genre_list = [g.strip().lower() for g in genre.split(",")]
        filtered = [
            m for m in filtered
            if any(g in [mg.lower() for mg in m["genres"]] for g in genre_list)
        ]
        
    if mood:
        mood_list = [md.strip().lower() for md in mood.split(",")]
        filtered = [
            m for m in filtered
            if any(md in [mm.lower() for mm in m["moods"]] for md in mood_list)
        ]
        
    if language:
        filtered = [m for m in filtered if m["language"].lower() == language.lower()]
        
    if rating_min is not None:
        filtered = [m for m in filtered if m["rating"] >= rating_min]
        
    if runtime_max is not None:
        filtered = [m for m in filtered if m["runtime"] <= runtime_max]
        
    return filtered

@app.post("/api/recommendations")
def get_recommendations(req: RecommendationRequest):
    """Get personalized hybrid recommendations, surprise recommendations, and hidden gems."""
    # Convert Pydantic filters to dict
    filters_dict = None
    if req.filters:
        filters_dict = req.filters.dict(exclude_none=True)
        
    # Get standard hybrid recommendations
    recommendations = recommender.get_hybrid_recommendations(
        user_ratings=req.ratings,
        preferred_mood=req.preferred_mood,
        active_filters=filters_dict,
        top_n=req.top_n
    )
    
    # Get surprise recommendations
    surprise_recs = recommender.get_surprise_recommendations(
        user_ratings=req.ratings,
        top_n=5
    )
    
    # Get hidden gems
    hidden_gems = recommender.get_hidden_gems(
        user_ratings=req.ratings,
        top_n=5
    )
    
    return {
        "recommendations": recommendations,
        "surprise_recommendations": surprise_recs,
        "hidden_gems": hidden_gems
    }

@app.post("/api/chat")
async def chat_companion(req: ChatRequest):
    """
    Chat with the AI Movie Companion.
    If API Key is provided, use Google Gemini API.
    Otherwise, fall back to a local rule-based response.
    """
    # 1. Gather user profile details to insert into the prompt context
    watchlist_titles = []
    for m_id in req.watchlist:
        m = recommender.get_movie_by_id(m_id)
        if m:
            watchlist_titles.append(m["title"])
            
    liked_titles = []
    disliked_titles = []
    for m_id, r in req.ratings.items():
        m = recommender.get_movie_by_id(m_id)
        if m:
            if r >= 4:
                liked_titles.append(f"{m['title']} ({r} stars)")
            elif r <= 2:
                disliked_titles.append(f"{m['title']} ({r} stars)")

    profile_context = f"""
    USER TASTE PROFILE:
    - Highly Rated Movies (Likes): {', '.join(liked_titles) if liked_titles else 'None yet'}
    - Low Rated Movies (Dislikes): {', '.join(disliked_titles) if disliked_titles else 'None yet'}
    - Watchlist: {', '.join(watchlist_titles) if watchlist_titles else 'Empty'}
    """

    # 2. Extract last user message
    if not req.messages:
        raise HTTPException(status_code=400, detail="Empty messages list")
    
    last_user_message = req.messages[-1].content
    
    # Check if Gemini API Key is available
    api_key = req.api_key or os.environ.get("GEMINI_API_KEY")
    
    if api_key:
        try:
            import google.generativeai as genai
            
            # Configure Gemini API
            genai.configure(api_key=api_key)
            
            # Formulate System Instruction
            system_instruction = f"""
            You are CineCompanion, a warm, witty, and highly knowledgeable personal movie companion. Your goal is to guide the user in discovering movies they'll love, sharing interesting movie facts, and discussing cinema.
            
            Here is the user's taste profile to guide your suggestions:
            {profile_context}
            
            Here is our local catalog of available movies. Prioritize recommending movies from this list if they match the user's inquiry, as the user can add these directly to their watchlist:
            {[{'id': m['id'], 'title': m['title'], 'genres': m['genres'], 'director': m['director'], 'overview': m['overview'], 'moods': m['moods']} for m in MOVIES]}
            
            When suggesting movies:
            1. Suggest 2-3 titles maximum in a conversation step, explaining why (e.g. matching their likes, specific mood, director).
            2. For movies in our local catalog, mention them clearly.
            3. Keep your tone engaging, friendly, and conversational.
            4. Keep responses concise (under 250 words).
            """
            
            # Initialize Gemini model
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction
            )
            
            # Format chat history for Gemini API
            # Gemini expects history format: list of {'role': 'user'|'model', 'parts': [text]}
            gemini_history = []
            for msg in req.messages[:-1]:
                role = "user" if msg.role == "user" else "model"
                gemini_history.append({"role": role, "parts": [msg.content]})
                
            chat = model.start_chat(history=gemini_history)
            response = chat.send_message(last_user_message)
            
            return {"response": response.text}
            
        except Exception as e:
            # Fallback to local assistant if Gemini API call fails
            return {
                "response": f"🤖 *[CineCompanion is running in Offline Mode due to an API error]*\n\nI encountered an error connecting to Gemini, but I can still help! Based on your profile:\n\n" + 
                self_local_recommendation(last_user_message, req.ratings)
            }
    else:
        # Local Rule-based assistant fallback
        return {
            "response": self_local_recommendation(last_user_message, req.ratings)
        }

def self_local_recommendation(message: str, ratings: Dict[int, int]) -> str:
    """A rule-based local fallback helper to answer inquiries when Gemini is unavailable."""
    msg = message.lower()
    
    # 1. Check for greetings
    if any(greet in msg for greet in ["hello", "hi", "hey", "greetings"]):
        return (
            "Hello! I am your CineCompanion. 👋\n\n"
            "I'm currently running in **Local Mode**. To unlock my advanced AI capabilities (where we can chat about characters, film theory, and complex queries), please add your **Gemini API Key** in the **Settings** panel!\n\n"
            "In the meantime, you can ask me to: \n"
            "- *Recommend a movie*\n"
            "- *Find a comedy/sci-fi/drama movie*\n"
            "- *Suggest a mood (e.g., mind-bending, funny, spooky, emotional)*"
        )
        
    # 2. Check for mood inquiries
    detected_mood = None
    for mood in ["mind-bending", "relaxing", "funny", "emotional", "spooky", "action-packed", "inspirational", "romantic", "suspenseful"]:
        if mood in msg:
            detected_mood = mood
            break
            
    # 3. Check for genre inquiries
    detected_genre = None
    for genre in ["sci-fi", "action", "thriller", "drama", "romance", "comedy", "mystery", "horror", "fantasy", "animation"]:
        if genre in msg:
            detected_genre = genre.capitalize()
            # handle sci-fi casing
            if genre == "sci-fi":
                detected_genre = "Sci-Fi"
            break

    # Get local recommendations
    filters = {}
    if detected_genre:
        filters["genre"] = [detected_genre]
        
    recs = recommender.get_hybrid_recommendations(
        user_ratings=ratings,
        preferred_mood=detected_mood,
        active_filters=filters,
        top_n=3
    )
    
    if not recs:
        return "I couldn't find any direct matches in our catalog. Try adjusting your request or rate a few more movies so I can understand your taste better!"
        
    response_text = ""
    if detected_mood:
        response_text += f"Here are a few **{detected_mood}** recommendations tailored for you:\n\n"
    elif detected_genre:
        response_text += f"Here are a few **{detected_genre}** movies from our catalog:\n\n"
    else:
        response_text += "Based on your watch history and ratings, here are a few movies I recommend:\n\n"
        
    for r in recs:
        m = r["movie"]
        response_text += f"🎥 **{m['title']}** ({m['year']}) — *{r['match_percentage']}% Match*\n"
        response_text += f"• **Genres**: {', '.join(m['genres'])} | **Director**: {m['director']}\n"
        response_text += f"• **Why?** {r['explanation']}\n\n"
        
    if not os.environ.get("GEMINI_API_KEY"):
        response_text += "\n*Tip: Connect your Gemini API Key in Settings to enable deep conversations!*"
        
    return response_text

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
