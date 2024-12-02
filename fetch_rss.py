import feedparser
import yaml
from notion_client import Client
import os
from datetime import datetime

def load_feeds(feeds_file):
    with open(feeds_file, 'r') as file:
        return yaml.safe_load(file)['feeds']

def fetch_rss_items(feed_url):
    feed = feedparser.parse(feed_url)
    return feed.entries

def create_notion_page(notion, database_id, title, content, link):
    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {  # Adjust if your database uses a different title column
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "URL": {
                "url": link
            }
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content,
                                "link": {"url": link}
                            }
                        }
                    ]
                }
            }
        ]
    )

def main():
    # Load Notion credentials from environment variables
    notion_token = os.environ.get('NOTION_KEY')
    notion_database_id = os.environ.get('NOTION_DATABASE_ID')

    if not notion_token or not notion_database_id:
        print("Notion Key or Database ID not set in environment variables")
        return

    # Initialize Notion client
    notion = Client(auth=notion_token)

    # Load feeds from YAML
    feeds = load_feeds('feeds.yml')

    # Process each feed
    for feed_config in feeds:
        feed_name = feed_config['name']
        feed_url = feed_config['url']

        # Fetch RSS items
        items = fetch_rss_items(feed_url)

        # Post each item to Notion
        for item in items:
            create_notion_page(
                notion, 
                notion_database_id, 
                f"{feed_name}: {item.get('title', 'Untitled')}", 
                item.get('summary', 'No summary available'),
                item.get('link', '')
            )

        print(f"Processed {len(items)} items from {feed_name}")

if __name__ == "__main__":
    main()
