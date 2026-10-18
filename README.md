# Library thing

A CLI for signing up, issuing books, returning them, and checking who's got what.

## Start it

1. Start MySQL Server.
2. Add a `.env` file with your database details:

   ```env
   DB_USER=your_mysql_user
   DB_PASSWORD=your_mysql_password
   DB_NAME=library
   ```

3. Install the dependencies and run it:

   ```bash
   pip install -r requirements.txt
   python main.py
   ```

There you go. Follow the promts.
