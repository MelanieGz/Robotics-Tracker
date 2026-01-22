from fastapi import FastAPI
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
	dbname = "attendance",
	user = USER,
	password = PASSWORD,
	host = "localhost"
)

@app.post("/trackers")
def insert_person(data: dict):
   curr = conn.cursor()
   curr.execute(
      "INSERT INTO trackers (value) VALUES (%s)",
      (data["value"], )
   )
   conn.commit()
   curr.close()
   return {"status":"ok"}
