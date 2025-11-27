import pandas as pd 
import streamlit as st
import pickle
import requests



# Open pickle file  

with open("movie_recommender_system.pkl", "rb") as f:
    new_df = pickle.load(f)

with open('similarity.pkl','rb') as p:
    similarity = pickle.load(p)  

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
        url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT26E0j4RGENOtOUY_YdfqywB7_Vfjaqn2qadDCM282M6p3yKcVAGlfF3sbtdw32RuKmBk&usqp=CAU");
    background-size: 270px 270px;
    background-repeat: repeat;
    background-attachment: fixed;
}
</style>
"""

highlight_box = """
<style>
.content-box {
    background: rgba(30, 20, 100, 0.7);  /* semi-transparent dark green */
    padding: 32px;
    border-radius: 17px;
    color: white;
}
.content-box h1, .content-box h2, .content-box p {
    color: #ffffff;  /* white text */
}
</style>
"""

st.markdown(highlight_box, unsafe_allow_html=True)


st.sidebar.markdown(
    """
    <style>
    /* Sidebar background with gradient */
    [data-testid="stSidebar"] {
        background: rgba(30, 20, 100, 0.7);
        color: white;
        padding: 15px;
        border-radius: 12px;
    }

    /* Sidebar text color */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* App title styling */
    .stApp h1 {
        color: white;
        text-align: left;
        font-size: 2.2rem;
    }

    /* Movie titles */
    .stText {
        font-weight: bold;
        color: #022c22;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="content-box">
        <h1>🎬 Movie Recommender System </h1>
        <p>
       This is about a Movie Recommender System. It is designed to suggest movies to users based on their interests and viewing history. The system works by analyzing patterns, such as genres, ratings, and preferences, to provide personalized recommendations. By using techniques like content-based filtering the recommender helps users quickly discover new movies that match their taste. This makes the movie selection process easier, faster, and more enjoyable.
        </p>
         <h3>Algorithms Used:</h3>
        <ul>
            <li><b>NumPy</b> – Array's data collect and Display.</li>
	    <li><b>Pandas</b> – To execute the EDA and Handling the missing values.</li>	
        <li><b>NLTK</b> – Natural Language Toolkit (NLTK) library,Python library for text processing and natural language processing (NLP).</li>
	    <li><b>Feature Extraction</b> – Transform text data into vector data.</li>
	    <li><b>Content-based filtering</b> – Filtering the data according to content.</li>
        </ul>
         <div class="image-container">
    <img src="https://cdn.designcrowd.com/blog/2018/March/50-Typographic-Oscars-Film-Posters/GR_Typographic-Oscar-Film-Posters_Banner_828x300.jpg"
         alt="Collage Image">
  </div>
    </div>
    
    """,
    unsafe_allow_html=True
)

# Fetch movie Poster 

def fetch_poster(movie_id):
    url = url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    return  "https://image.tmdb.org/t/p/w500/" + data['poster_path']



# Recommendation function
def recommend(movie):
    movie_index  = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movie = []
    recommended_movie_posters =  []
    for i in movie_list: 
        movie_id = new_df.iloc[i[0]]["movie_id"]

        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie.append(new_df.iloc[i[0]].title)

    return recommended_movie, recommended_movie_posters

# Set the title of the wep 


st.sidebar.title("🎬 Movie Recommender System")
st.sidebar.image("https://images.thedirect.com/media/article_full/tony-stark-snap.jpg")
st.sidebar.markdown(page_bg,unsafe_allow_html=True)

# Extrat the name of movie list 
movie_list = new_df['title'].values

#  Create a Selectbox 
st.sidebar.subheader("Select Your Movie..")
selected_movie = st.sidebar.selectbox("Choose movie",movie_list) # Contain the name of the movie_list


if st.sidebar.button("Recommend"):
        st.title("Recommended movie--")
        recommended_movie,recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie[1])
            st.image(recommended_movie_posters[1])

        with col3:
            st.text(recommended_movie[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie[4])
            st.image(recommended_movie_posters[4])

        st.success("Preticted Movies..")
