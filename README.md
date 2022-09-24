**How to Run the App**
1. Clone the repository
    ``` 
      $ git clone https:// 
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
5. Run database migrations: 
    ```bash
      # This might take some time, to get the latest 100 posts
      (env) $ python manage.py makemigrations
      (env) $ python manage.py migrate
    ```

6. Start celery and redis:
   ```bash
    (env) $ celery -A core worker -B -l info --logfile=celery.log --detach
    (env) $ redis-server
   ```
7. Start the web application: `python manage.py runserver`

