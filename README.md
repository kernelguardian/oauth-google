# Getting Started
- Clone this repo
- Generate google credetials
    - Client Secret
    - Client ID
- Generate a random secret key
- Create a new file named .env with the same format of .example.env and update with the values generated in the above step
- Install python dependencies by running the command `pip install -r requirements.txt`
- Start the server by running the command `uvicorn main:app --reload`
- In your browser open http://127.0.0.1:8000/login and you will be greeted with Google Oauth Screen.
- Voila

