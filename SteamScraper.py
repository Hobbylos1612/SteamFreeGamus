import requests
from bs4 import BeautifulSoup
import webbrowser

BASE_STORE = "https://store.steampowered.com"

# Debug game for testing
DEBUG_GAME = {
    "title": "Health Insurance Claim Denier",
    "appid": "3451060",
    "link": f"{BASE_STORE}/app/3451060",
    "header_img": f"https://cdn.akamai.steamstatic.com/steam/apps/3451060/header.jpg"
}

# Toggle for debug mode
DEBUG_MODE = False  # Set to False to disable the debug game

def get_games(debug=DEBUG_MODE):
    url = f"{BASE_STORE}/search/?maxprice=free&specials=1"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    games = []
    search_rows = soup.find("div", id="search_resultsRows")
    if search_rows:
        for row in search_rows.find_all("a", class_="search_result_row"):
            href = row.get("href", "")
            parts = href.split("/")
            if len(parts) < 5:
                continue
            appid = parts[4]

            title = row.find("span", class_="title").text.strip() if row.find("span", class_="title") else ""
            link = f"{BASE_STORE}/app/{appid}"
            header_img = f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg"

            games.append({
                "title": title,
                "appid": appid,
                "link": link,
                "header_img": header_img
            })

    # Add debug game manually if debug mode is on
    if debug:
        games.append(DEBUG_GAME)

    return games

def get_images(appid):
    url = f"{BASE_STORE}/app/{appid}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    images = []

    highlight_strip = soup.find(id="highlight_strip")
    if highlight_strip:
        for img_div in highlight_strip.find_all("div", class_="highlight_strip_screenshot"):
            img_tag = img_div.find("img")
            if img_tag and img_tag.get("src"):
                # Remove the small thumbnail sizing
                img_url = img_tag["src"].replace(".116x65", "")
                images.append(img_url)

    return images

def get_free_promotions(debug=DEBUG_MODE):
    games = get_games(debug)
    free_games = []

    for game in games:
        images = get_images(game["appid"])
        free_games.append({
            "name": game["title"],
            "link": game["link"],
            "header": game["header_img"],
            "images": images
        })

    return free_games

# Example usage
if __name__ == "__main__":
    free_games = get_free_promotions()
    for g in free_games:
        print(f"{g['name']}")
        print(f"Link: {g['link']}")
        print(f"Header: {g['header']}")
        print(f"Images: {len(g['images'])} screenshots")
        print("-" * 50)
        webbrowser.open(g['link'])
