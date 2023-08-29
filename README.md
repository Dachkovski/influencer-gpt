# Influencer GPT 🐦

Influencer GPT is a Streamlit application designed to assist influencers and content creators. It leverages OpenAI's GPT-3.5 Turbo model to search for trends, generate video scripts, and offers the possibility to post videos to platforms like YouTube, Instagram, and TikTok.

## Features

- **Trend Search**: Discover the latest trends using Twitter or GPT-3.
- **Video Script Generation**: Automatically generate video scripts based on the selected trend.
- **Video Creation**: Produce videos using either D-ID or HeyGen.
- **Video Posting**: (Coming Soon) Post videos to YouTube, Instagram, and TikTok with auto-generated metadata (title, description, hashtags).

## Prerequisites

- Python 3.7+
- OpenAI API key
- Twitter API credentials
- D-ID API key
- HeyGen API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/influencer-gpt.git
   cd influencer-gpt
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API keys and credentials:
   - Open the `settings.py` file and configure the API keys and credentials for OpenAI, Twitter, D-ID, and HeyGen.

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Start the application and navigate to the provided localhost URL.
2. Enter your research goal in the text input.
3. Select a trend from the generated list.
4. Edit the generated video script if needed.
5. Confirm and generate the video.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)