# 📸 TextOnPhoto

Telegram bot for adding custom text to images.

The bot allows a user to send a photo, choose where the text should appear, enter custom text, and receive a processed image with the text overlay. The user can also adjust the result by changing text size, color, position, or text content.

## Features

- Accepts images from Telegram users
- Adds custom text to images
- Lets the user choose text position: top or bottom
- Supports editing the generated result:
  - change font size
  - change text color
  - switch text position
  - edit text
- Uses inline buttons for interaction
- Processes images with Pillow
- Stores configuration separately via `.env`

## Tech Stack

- Python
- pyTelegramBotAPI
- Pillow
- python-dotenv

## Project Structure

```
LDTBot/
│
├── handlers/ # Message and callback handlers
│ ├── init.py
│ ├── messages.py
│ └── callbacks.py
│
├── keyboards/ # Inline keyboards
│ ├── init.py
│ └── inline.py
│
├── services/ # Business logic and services
│ ├── init.py
│ ├── image_service.py
│ └── state_service.py
│
├── generated/ # Generated images (ignored by Git)
│
├── .env.example # Example environment variables
├── .gitignore
├── config.py # Configuration loader
├── main.py # Bot entry point
├── requirements.txt # Project dependencies
├── README.md
└── CactusClassicalSerif-Regular.ttf # Font used for text rendering
```

## Installation

Clone the repository:

```bash
git clone https://github.com/KulikovaSasha/LDTBot.git
cd LDTBot
```

Create and activate a virtual environment:

### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
TG_TOKEN=your_telegram_bot_token_here
```

You can get a bot token from @BotFather in Telegram.

An example configuration file is available in `.env.example`.

## Run the bot

```bash
python main.py
```

## How it works

1. The user sends a photo to the bot  
2. The bot asks where to place the text  
3. The user sends the text  
4. The bot generates a new image with text overlay  
5. The user can accept the result or edit it:
   - font size  
   - text color  
   - text position  
   - text content  

## Implemented Logic

- multi-step user interaction  
- inline keyboard callbacks  
- image processing  
- text placement on images  
- automatic line splitting based on image width  
- user state handling  
- project configuration through environment variables  

## Notes

- Do not commit your real `.env` file to GitHub  
- Make sure the font file is present in the project root  
- A stable internet connection is required for Telegram Bot API access  

## Possible Improvements

- move handlers into separate modules  
- add logging  
- improve error handling  
- support multiple fonts  
- support manual text positioning  
- add Docker support  
- deploy to a cloud platform  

## Author

Sasha Kulikova  

GitHub: https://github.com/KulikovaSasha
