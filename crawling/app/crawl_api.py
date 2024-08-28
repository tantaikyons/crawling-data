import os
import requests
import json
import google.generativeai as genai
from fastapi  import  APIRouter,FastAPI
from crawling.data import CrawlService
os.environ["GEMINI_API_KEY"] = "AIzaSyDa4RWRs9co9CadhWhv5buaCU1pMVPBjMU"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# Create the model
generation_config = {
"temperature": 1,
"top_p": 0.95,
"top_k": 64,
"max_output_tokens": 8192,
"response_mime_type": "text/plain",
}
router = FastAPI()


@router.post("/api/query")
async def retrival(query_user: str) -> dict:
    """
    Retrieves data based on a query from a server.

    Args:
        query_user (str): The query to retrieve data.

    Returns:
        dict: The retrieved data.
    """
    X_API_KEY = "sdb-dev-JoZuQ76ekjNXfpC94Mhc8Yc2hHzdZrjt"
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    res = requests.post(
        'https://sm-api-dev.kyons.vn/api/xe-dien-PztvU/points/query',
        headers={"X-API-Key": X_API_KEY},
        json={
            "text": f"{query_user}",
            "query_filter": {},
            "limit": 100
        },
    )

    data_res = []
    res = json.loads(res.text)
    for i in range(len(res)):
        if res[i]["score"] >= 0.45:
            data_res.append(res[i])

    body_query = str(data_res)
    chat_session = model.start_chat(history=[])
    body_title = """{
        "title": 1 list of related titles (enclosed in []),
        "url": 1 list of related urls (enclosed in [])
    }"""
    response = chat_session.send_message(
        f"Based on the information:\n{body_query}\n\nQuestion: {query_user}\nPlease answer succinctly.")
    response_title_url = chat_session.send_message(
        f"Based on the information:\n{body_query}\n\nAnd the information:\n{response.text}\nPlease create a dictionary following the format below:\n{body_title}")
    response_title_url = "{" + response_title_url.text.split("{")[-1].split("}")[0] + "}"
    response_title_url = eval(response_title_url)
    title = response_title_url["title"]
    url = response_title_url["url"]
    return {
        "text": response.text,
        "candidates": [
            {
                "title": title,
                "url": url
            }
        ]
    }

@router.post("/api/crawl")
async  def crawling(user_text: str) -> dict:
    """
    Crawls a website based on a given user input.

    Args:
        user_text (str): The user input for the website to crawl.

    Returns:
        dict: The crawled data from the website.
    """
    return CrawlService.crawl_website(user_text)

@router.post("/api/upload_data")
async def post_data_to_server(url: str, data: list) -> None:
    """
    Posts data to a server.

    Args:
        url (str): The URL to post the data to.
        _data (list): The data to be posted.

    Returns:
        None
    """
    X_API_KEY = "sdb-dev-JoZuQ76ekjNXfpC94Mhc8Yc2hHzdZrjt"
    headers = {"X-API-KEY": X_API_KEY}

    for i in range(len(data)):
        data_json = {"data": [
            {
                "id": i,
                "text": "base url: http://sieuxedien.vn//",
                "payload": {
                    "url": data[i]["url"],
                    "title": data[i]["title"],
                    "body": data[i]["body"]
                }
            }
        ]
        }
        json_data = json.dumps(data_json)
        response = requests.post(url,
                                data=json_data,
                                headers=headers)

        if response.status_code == 201:
            print("Data has been successfully sent!")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

