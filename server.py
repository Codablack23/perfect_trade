from dotenv import load_dotenv
load_dotenv()
from perfect_trade import app,database

if __name__ == "__main__":
    database.create_all()
    app.run(port=5001,debug=True)
     
