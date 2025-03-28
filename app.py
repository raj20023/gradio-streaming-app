import gradio as gr
import pandas as pd

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

def create_dataframe(data):
    df = pd.DataFrame(data)
    return df.style.highlight_max(color = 'lightgreen', axis = 0)

# Components
def create_video_player():
    youtube_embed = """
    <iframe width="100%" height="400" src="https://www.youtube.com/embed/4xDzrJKXOOY?si=aKjYZytqK1_eRVjQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
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
        gr.DataFrame(create_dataframe(STREAMER_PROFILE["past_streams"]))

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
            gr.DataFrame(create_dataframe(TRENDING_STREAMS))
            
        with gr.TabItem("Profile"):
            create_profile()

if __name__ == "__main__":
    demo.launch()
