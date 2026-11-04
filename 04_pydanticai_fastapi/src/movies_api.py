from data_models import Movie, Prompt
from dotenv import load_dotenv
from fastapi import FastAPI
from model import nvidia_model
from pydantic_ai import Agent
from utils import query_duckdb

load_dotenv()

agent = Agent(
    model=nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b"),
)

app = FastAPI()


@app.get("/movies")
async def read_movies():
    movies = query_duckdb("FROM movies;")
    return movies.to_dict(orient="records")


@app.post("/movie")
async def create_movie(query: Prompt):
    result = await agent.run(query.prompt, output_type=Movie)
    movie = result.output

    query_duckdb(
        "INSERT INTO movies VALUES (?,?,?,?)",
        parameters=(movie.title, movie.year, movie.genre, movie.rating),
    )
    return movie
