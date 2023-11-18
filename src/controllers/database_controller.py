import psycopg2
from src.config.config import host, user, password, database


def connect_to_database():
    try:
        return psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=database
        )
    except Exception as e:
        print("Database connection failed:", e)
        # Optionally, re-raise the exception to halt the program if the database connection is essential
        raise


def setup_database():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS users (
          user_id VARCHAR(255) PRIMARY KEY,
          xp INT,
          level INT,
          rank VARCHAR(255)
      )
  """)
    conn.commit()
    cursor.close()
    conn.close()


def calculate_level(xp):
    # Define your logic to calculate level based on XP
    # Assuming each rank is a level, you can use the same logic as calculate_rank
    if xp <= 250:
        level = 1  # Bot 🤖
    elif xp <= 700:
        level = 2  # Alcoholic 🍺
    elif xp <= 1200:
        level = 3  # MethHead 💊
    elif xp <= 2000:
        level = 4  # Rockstar 🎸
    elif xp <= 4000:
        level = 5  # Heisenberg 👨‍🔬
    else:
        level = 6  # KURWAMACH 💥
    return level


def calculate_rank(xp):
    # Define your logic to calculate rank based on XP
    if xp < 250:
        rank = "Bot"
    elif xp < 700:
        rank = "Alcoholic"
    elif xp < 1200:
        rank = "MethHead"
    elif xp < 2000:
        rank = "Rockstar"
    elif xp < 4000:
        rank = "Heisenberg"
    else:
        rank = "KURWAMACH"
    return rank


async def update_xp(user_id, xp_gain):
    conn = connect_to_database()
    c = conn.cursor()

    # Use %s as placeholders for PostgreSQL
    c.execute("SELECT xp, level, rank FROM users WHERE user_id = %s", (user_id,))
    user = c.fetchone()

    if user:
        new_xp = user[0] + xp_gain
        new_level = calculate_level(new_xp)
        new_rank = calculate_rank(new_xp)
        # Update placeholders to %s for PostgreSQL
        c.execute("UPDATE users SET xp = %s, level = %s, rank = %s WHERE user_id = %s",
                  (new_xp, new_level, new_rank, user_id))
    else:
        # Insert new user with placeholders as %s
        c.execute("INSERT INTO users (user_id, xp, level, rank) VALUES (%s, %s, %s,%s)",
                  (user_id, xp_gain, 1, "BOT"))

    conn.commit()
    conn.close()

