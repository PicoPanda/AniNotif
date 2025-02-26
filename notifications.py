# ======================================================================
# File: notifications.py
# Description: This file contains functions to send notifications to the user.
#
# How the module works:
#
# create_notification(title='Notification', subtitle=None, text=None, icon=None, sound=None, delay=timedelta(), action_button_str=None, action_callback=None, reply_button_str=None, reply_callback=None, snooze_button_str=None)
#
# - title: The title of the notification.
# - subtitle: The subtitle of the notification.
# - text: The text of the notification.
# - icon: The icon of the notification.
# - sound: The sound of the notification.
# ======================================================================


from mac_notifications import client


def release_notification(anime_title: str, episode: int, time: str) -> bool: # Returns True if the notification was sent, False otherwise
    """Send a notification to the user."""
    title = f"{anime_title} - Episode {episode}"
    subtitle = f"Releases at {time}"
    message = f"New {anime_title} episode, EP - {episode} available at {time}"
    try:
        client.create_notification(title=title, subtitle=subtitle, text=message)
        return True
    except Exception as e:
        print(f"Error sending notification: {e}")
        return False


if __name__ == '__main__':
    release_notification(anime_title="Test", episode=1, time="10:00")
