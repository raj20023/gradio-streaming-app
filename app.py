import gradio as gr
from google_auth_oauthlib.flow import InstalledAppFlow
import os

def authenticate_youtube():
    client_config = {
        "web": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
            "auth_uri": os.environ.get("GOOGLE_AUTH_URI"),
            "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
            "redirect_uris": os.environ.get("GOOGLE_REDIRECT_URIS").split(","),
            "javascript_origins": os.environ.get("GOOGLE_JAVASCRIPT_ORIGINS").split(","),
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, ['https://www.googleapis.com/auth/youtube.readonly'])
    
    auth_url, _ = flow.authorization_url()
    print(f"Please visit this URL to authorize the application: {auth_url}")

    # Manually enter the authorization code
    auth_code = input("Enter the authorization code: ").strip()

    creds = flow.fetch_token(code=auth_code)
    return creds

youtube = authenticate_youtube()

def get_live_stream():
    request = youtube.search().list(
        part="snippet",
        eventType="live",
        type="video",
        q="tech live stream"  # Customize this query
    )
    response = request.execute()
    
    if response["items"]:
        video_id = response["items"][0]["id"]["videoId"]
        return f"https://www.youtube.com/embed/{video_id}"
    else:
        return "No live streams found."

live_stream_url = get_live_stream()


# Mock Data
STREAMER_PROFILE = {
    "name": "StreamMaster42",
    "followers": "12.4K",
    "total_streams": 45,
    "categories": ["Gaming", "Tech Talks", "Coding"],
    "past_streams": [
        {"title": "Python Deep Dive", "views": "2.3K", "date": "2025-03-25"},
        {"title": "Gaming Marathon", "views": "5.1K", "date": "2025-03-24"}
    ]
}

MOCK_CHAT = [
    ("User1", "Awesome stream! 👏"),
    ("User2", "What game is this? 🎮")
]

TRENDING_STREAMS = [
    {"title": "Epic Gaming Session", "viewers": "8.2K", "category": "Gaming"},
    {"title": "AI Workshop Live", "viewers": "4.7K", "category": "Tech"}
]

# Components
def create_video_player():
    live_url = get_live_stream()
    youtube_embed = f"""
    <iframe width="100%" height="400" src="{live_url}" title="YouTube Live Stream" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
    """
    return gr.HTML(youtube_embed)


def create_chat_interface():
    with gr.Blocks() as chat:
        chatbot = gr.Chatbot(value=MOCK_CHAT, label="Live Chat")
        msg = gr.Textbox(label="Send Message")
        clear = gr.Button("Send")
        
        def respond(message, chat_history):
            chat_history.append(("You", message))
            return "", chat_history
        
        clear.click(respond, [msg, chatbot], [msg, chatbot])
    return chat

def create_reactions():
    emojis = ["🔥", "❤️", "🎉", "🚀", "👏"]
    with gr.Row():
        for emoji in emojis:
            btn = gr.Button(emoji)
            btn.click(lambda e=emoji: gr.Info(f"Sent {e} reaction!"), inputs=btn)
    return gr.Row()

def create_profile():
    with gr.Column():
        gr.Markdown(f"## {STREAMER_PROFILE['name']}")
        gr.Markdown(f"**Followers:** {STREAMER_PROFILE['followers']}")
        gr.Markdown(f"**Total Streams:** {STREAMER_PROFILE['total_streams']}")
        gr.DataFrame(
            value=STREAMER_PROFILE["past_streams"],
            headers=["Title", "Views", "Date"],
            row_count=2
        )

def create_donation():
    with gr.Group():  # Modern alternative
        gr.Markdown("### Support the Streamer")
        amount = gr.Number(label="Amount ($)")
        donate_btn = gr.Button("Donate 💸")
        donation_msg = gr.Textbox(visible=False)
        
        def mock_donate(amt):
            return f"🎉 Thank you for donating ${amt}! (Mock transaction)"
        
        donate_btn.click(
            mock_donate, 
            inputs=amount, 
            outputs=donation_msg
        )

# App Layout
with gr.Blocks(theme=gr.themes.Soft(), title="StreamLive 2025") as demo:
    gr.Markdown("# 🎥 StreamLive 2025")
    
    with gr.Tabs():
        with gr.TabItem("Live Stream"):
            with gr.Row():
                with gr.Column(scale=3):
                    create_video_player()
                    create_reactions()
                    create_donation()
                with gr.Column(scale=1):
                    create_chat_interface()
            
        with gr.TabItem("Trending"):
            gr.DataFrame(
                value=TRENDING_STREAMS,
                headers=["Title", "Viewers", "Category"],
                row_count=2
            )
            
        with gr.TabItem("Profile"):
            create_profile()

app = gr.Interface(fn=demo, inputs="text", outputs="text")
_, port, _ = app.launch(server_name="localhost", server_port=5000, share=False)

print(f"Use this Redirect URI in Google Cloud: http://localhost:{port}/")

