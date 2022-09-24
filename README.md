**How to Run the App**
1. Clone the repository
    ``` 
      $ git clone https://github.com/Josh596/HackerNews.git 
    ```
2. Create and activate the virtual environment. From the terminal:
   - Mac 
      ```bash
      $ python3 -m venv env
      $ source env/bin/activate
      ```
   - Windows
     ```bash
      $ python -m venv env
      $ env\Scripts\activate
     ``` 
3. Install the required python libraries
   ```bash
   (env) $ pip install -r requirements.txt
   ``` 
4. Install Redis to act as a broker with Celery
   - Mac
      ```bash
      (env) $ brew install redis
      ```
   - Windows: (https://redis.io/docs/getting-started/installation/install-redis-on-windows/)
5. Load the env variables
   ```bash
      (env) $ touch .env
   ```
   - Open the .env file and add a SECRET_KEY variable. The file should look like this
   ```
   SECRET_KEY = 'random_key'
   ```
6. Run database migrations: 
    ```bash
      # This might take some time, to get the latest 100 posts
      (env) $ python manage.py makemigrations
      (env) $ python manage.py migrate
    ```

7. Start celery and redis:
   - Mac
      ```bash
      (env) $ celery -A core worker -B -l info --logfile=celery.log --detach
      (env) $ redis-server
      ```
   - Windows:
      ```bash
      (env) $ celery -A core worker -l info --logfile=celery.log
      ```
      ### Then follow the instructions on
      - (https://redis.io/docs/getting-started/installation/install-redis-on-windows/)
8. Start the web application: `python manage.py runserver`

