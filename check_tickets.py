import requests

NTFY_TOPIC = "bavana-bms-doomsday-alert"
NOTIFICATION_TITLE = "Ticket Alert Dec 17"


def send_phone_alert(message: str):
  url = f"https://ntfy.sh/{NTFY_TOPIC}"
  headers = {
      "Title": NOTIFICATION_TITLE,
      "Priority": "urgent",
      "Tags": "ticket,loudspeaker",
  }
  response = requests.post(
      url, data=message.encode("utf-8"), headers=headers, timeout=15
  )
  if response.status_code == 200:
    print(f"✅ Notification sent: {message}")
  else:
    print(f"❌ Failed to send notification: {response.status_code}")


def main():
  print("Sending immediate test alert to phone...")
  send_phone_alert("Test Alert: Your phone notification setup is working!")


if __name__ == "__main__":
  main()
