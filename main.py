from fastapi import FastAPI, Form
import httpx
from decouple import config
import openai

app = FastAPI()

openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}


@app.post("/check-answer")
async def check_answer(question: str = Form(...), answer: str = Form(...)):
    openai_endpoint = "https://api.openai.com/v1/engines/davinci/completions"

    

    prompt = f"{question}\nDai a questa risposta un punteggio da 0 a 1: {answer}"

    user_message = {"role": "user", "content": prompt}


    try:
        formatted_messages = [{"role": user_message["role"], "content": user_message["content"]}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= formatted_messages
        )
        print(response)
        score = response["choices"][0]["message"]["content"]
        return {"score": score}
    except Exception as e:
        print(e)

    # Invia la richiesta a OpenAI
    #async with httpx.AsyncClient() as client:
    #    response = await client.post(
    #        openai_endpoint,
    #        headers={
    #            "Authorization": f"Bearer {OPEN_AI_KEY}",
    #            "Content-Type": "application/json",
    #        },
    #        json={
    #            "prompt": prompt,
    #            "max_tokens": 5,  # Sostituisci con il valore appropriato
    #        },
    #    )

    # Estrapola il punteggio dalla risposta di OpenAI
    #score = response.json()["choices"][0]["message"]["content"]

    # Restituisci il punteggio
    #return {"score": score}