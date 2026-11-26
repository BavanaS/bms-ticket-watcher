import sys
import requests

NTFY_TOPIC = "bavana-bms-doomsday-alert"
NOTIFICATION_TITLE = "Ticket Alert Dec 17"
BMS_COIMBATORE_URL = "https://in.bookmyshow.com/explore/movies-coimbatore"

TARGET_THEATRES = [
    "Miraj Cinemas – SRK Mall",
    "Cinépolis – Fun Republic Mall",
    "Karpagam Grandplex",
    "LUXON",
    "PVR – Alveal Fun Savvy Mall",
]

# Keywords to match the theatres in BookMyShow HTML
THEATRE_KEYWORDS = {
    "Miraj": "Miraj Cinemas (SRK Mall)",
    "Cinépolis": "Cinépolis (Fun Republic Mall)",
    "Cinepolis": "Cinépolis (Fun Republic Mall)",
    "Karpagam": "Karpagam Grandplex (LUXON LED)",
    "LUXON": "Karpagam Grandplex (LUXON LED)",
    "Alveal": "PVR (Alveal Fun Savvy Mall)",
    "Savvy": "PVR (Alveal Fun Savvy Mall)",
    "PVR": "PVR Cinemas",
}

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
  """Sends urgent push notification to the phone via ntfy."""
  url = f"https://ntfy.sh/{NTFY_TOPIC}"
  headers = {
      "Title": NOTIFICATION_TITLE,
      "Priority": "urgent",
      "Tags": "ticket,loudspeaker,fire",
  }
  try:
    response = requests.post(
        url, data=message.encode("utf-8"), headers=headers, timeout=15
    )
    if response.status_code == 200:
      print(f"✅ Notification successfully sent to phone: {message}")
    else:
      print(f"❌ Failed to send alert, HTTP status: {response.status_code}")
  except Exception as e:
    print(f"Error dispatching notification: {e}")


def main():
  print("Checking BookMyShow Coimbatore for 'Avengers: Doomsday'...")

  try:
    response = requests.get(BMS_COIMBATORE_URL, headers=HEADERS, timeout=20)
    page_text = response.text

    # 1. Check if the movie is listed at all on BookMyShow Coimbatore
    is_movie_listed = (
        "Avengers: Doomsday" in page_text or "Avengers Doomsday" in page_text
    )

    if not is_movie_listed:
      print("Status: 'Avengers: Doomsday' is not listed yet in Coimbatore.")
      return

    print("Movie listing detected on BookMyShow! Checking for 17 Dec dates...")

    # 2. Check if 17 Dec booking tab/date is active
    date_indicators = [
        "17 Dec",
        "Dec 17",
        "17-12-2026",
        "20261217",
        "17th Dec",
        "DEC 17",
    ]
    is_date_open = any(indicator in page_text for indicator in date_indicators)

    if is_date_open:
      # Identify which target theatres have matches on page
      found_theatres = set()
      for keyword, name in THEATRE_KEYWORDS.items():
        if keyword.lower() in page_text.lower():
          found_theatres.add(name)

      theatres_str = (
          ", ".join(found_theatres)
          if found_theatres
          else "Target Coimbatore Theatres"
      )
      alert_message = (
          f"Avengers: Doomsday bookings OPEN for Dec 17 at: {theatres_str}! "
          f"Open BookMyShow now."
      )

      # Send phone notification
      send_phone_alert(alert_message)
    else:
      print(
          "Movie is listed on BookMyShow, but Dec 17 date tab is not bookable"
          " yet."
      )

  except Exception as err:
    print(f"Transient error during check: {err}")
    sys.exit(0)  # Exit cleanly so GitHub doesn't trigger false error emails


if __name__ == "__main__":
  main()
