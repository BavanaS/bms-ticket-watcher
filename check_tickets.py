import sys
import requests

NTFY_TOPIC = "bavana-bms-doomsday-alert"
NOTIFICATION_TITLE = "Ticket Alert Dec 17"
BMS_COIMBATORE_URL = "https://in.bookmyshow.com/explore/movies-coimbatore"

TARGET_THEATRES = [
    "Miraj",
    "Cinépolis",
    "Karpagam Grandplex",
    "LUXON",
    "PVR",
    "Alveal",
    "Fun Republic",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def send_phone_alert(message: str):
  """Sends push notification directly to the ntfy app."""
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
  print("Checking BookMyShow Coimbatore for 'Avengers: Doomsday'...")
  try:
    res = requests.get(BMS_COIMBATORE_URL, headers=HEADERS, timeout=20)
    page_text = res.text

    # 1. Check if the movie is listed
    if (
        "Avengers: Doomsday" not in page_text
        and "Avengers Doomsday" not in page_text
    ):
      print("Status: 'Avengers: Doomsday' is not listed yet.")
      return

    print("Movie listing detected! Checking for open booking dates...")

    # 2. Check if Dec 17 bookings are open
    if "17 Dec" in page_text or "Dec 17" in page_text or "17-12-2026" in page_text:
      # Check which target theatres are mentioned
      matched_theatres = [t for t in TARGET_THEATRES if t.lower() in page_text.lower()]
      theatre_str = ", ".join(matched_theatres) if matched_theatres else "Target Theatres"
      
      alert_msg = f"Avengers Doomsday Dec 17 bookings OPEN! Seen at: {theatre_str}. Book now on BookMyShow!"
      send_phone_alert(alert_msg)
    else:
      print("Movie listed, but Dec 17 date tab is not bookable yet.")

  except Exception as e:
    print(f"Error during check: {e}")
    sys.exit(0)  # Exit 0 so GitHub Actions doesn't flag unnecessary failure alerts


if __name__ == "__main__":
  main()
