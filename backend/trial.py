# from datetime import datetime, timedelta
# from app.models import User

# def send_reminders():
#     inactive_users = get_inactive_users()
#     print("INACTIVE USERS:")
#     for user in inactive_users:
#         print("SENDING REMINDER TO:", user.username)

# def get_inactive_users():
#     # Define the timeframe for considering a user as inactive (e.g., 5 seconds)
#     inactive_threshold = datetime.now() - timedelta(seconds=5)

#     # Query the database to retrieve users who haven't visited the app within the specified timeframe
#     inactive_users = User.query.filter(User.last_login < inactive_threshold).all()

#     return inactive_users

# if __name__ == "__main__":
#     send_reminders()
