# Karta: musikquizet (main, 17 nov)

## Helheten
Kaggle-data
  → dlt/load_data.py              laddar in rådata i DuckDB
  → dbt/models/staging/           städar: stg_tracks, stg_artists, stg_albums, stg_track_artists
  → dbt/models/marts/quiz_tracks  EN rad per låt, färdig för quizet
  → duckdb/warehouse.duckdb       databasfilen där allt ligger
  → backend/api.py                läser marts.quiz_tracks EN gång → df
  → frontend/app.py               Streamlit-sidan användaren ser

## backend/api.py – tre endpoints
| Endpoint | In | Ut | Använder |
|---|---|---|---|
| GET /filter | – | årtionden, genrer, antal | utils/filter_decades, filter_genres |
| GET /tracks | antal, årtionden, genrer | lista med låtar (MusicData) | utils/num_tracks |
| POST /generated_quiz | lista med låtar | en följdfråga per låt | agent/agent.py |

## backend/agent/ – vad varje fil gör
| Fil | Innehåller | Kort sagt |
|---|---|---|
| deps.py | MusicData, FollowUps | Mallarna. MusicData = en låt (namn, artist, år, genrer …). FollowUps = svaret: fråga, alternativ, rätt svar |
| model.py | nvidia_model() | Kopplar till AI-modellen via NVIDIA. Läser NVIDIA_API från .env |
| prompts.py | get_prompt() | Hämtar agentens instruktioner från Logfire |
| tools.py | search_wikipedia(query) | Verktyget: söker på Wikipedia, returnerar artikeltext (str) |
| agent.py | music_agent | Sätter ihop allt: modell + mallar + instruktioner + verktyg |

## Så skapas en följdfråga
1. Frontend skickar låtarna till POST /generated_quiz
2. För varje låt: music_agent.run(..., deps=låten)
3. track_context() i agent.py lägger till låtens fakta i instruktionerna
4. Agenten anropar search_wikipedia med en sökning den själv väljer
5. Agenten skriver frågan → måste passa mallen FollowUps
6. Svaret går tillbaka till frontend och visas

## Snabbsvar
- Var finns MusicData? → backend/agent/deps.py
- Varför tar agenten in en låt (deps)? → för att veta vilken låt frågan gäller
- Var läses tabellen in? → backend/api.py, en gång vid start
- Var filtreras låtarna? → backend/utils/