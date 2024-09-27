import requests
import urllib.parse
from typing import List
from termcolor import colored

def search_for_stock_videos(query: str, api_key: str, it: int, min_dur: int) -> List[str]:
    """
    Searches for stock videos based on a query.

    Args:
        query (str): The query to search for.
        api_key (str): The API key to use.

    Returns:
        List[str]: A list of stock videos.
    """

    base_url = 'https://api.pexels.com/videos/'
    
    # Build headers
    headers = {
        "Authorization": api_key,
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
    }

    params = {'query': query, 'per_page': it}

    r  = requests.get(base_url + 'search', headers=headers, params=params)

    if r.status_code == 200:
        response = r.json()
    else:
        print("faile to fetch the images", response.status_code)
        return []

    # Build URL
    # encoded_query = urllib.parse.quote(query)
    # qurl = f"{base_url}/videos/search?query={query.encode()}&per_page={it}"

    # Send the request
    # r = requests.get(qurl, headers=headers)

    # Parse the response
    response = r.json()

    # Parse each video
    raw_urls = []
    video_url = []
    video_res = 0
    try:
        # loop through each video in the result
        for i in range(it):
            #check if video has desired minimum duration
            if response["videos"][i]["duration"] < min_dur:
                continue
            raw_urls = response["videos"][i]["video_files"]
            temp_video_url = ""
            
            # loop through each url to determine the best quality
            for video in raw_urls:
                # Check if video has a valid download link
                if ".com/video-files" in video["link"]:
                    # Only save the URL with the largest resolution
                    if (video["width"]*video["height"]) > video_res:
                        temp_video_url = video["link"]
                        video_res = video["width"]*video["height"]
                        
            # add the url to the return list if it's not empty
            if temp_video_url != "":
                video_url.append(temp_video_url)
                
    except Exception as e:
        print(colored("[-] No Videos found.", "red"))
        print(colored(e, "red"))

    # Let user know
    print(colored(f"\t=> \"{query}\" found {len(video_url)} Videos", "cyan"))

    # Return the video url
    return video_url
