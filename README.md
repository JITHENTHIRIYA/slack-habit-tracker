# 🚀 Slack Habit Tracker Bot

A free Slack bot that helps users track daily habits using simple emoji reactions. No paid API keys required!

## ✨ Features

- **Set Habits**: `/sethabit [habit_name] [times_per_day]` - Create daily habit goals
- **Track Progress**: `/mystatus` - View your current progress with visual progress bars
- **Emoji Reactions**: 
  - ✅ (white_check_mark) - Increment progress
  - ❌ (x) - Get motivational support
- **Daily Reset**: Progress automatically resets each day
- **Local Storage**: All data stored in `habits.json` file
- **Free Deployment**: Deploy on Railway, Render, or Replit

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Slack SDK**: `slack-bolt`
- **Storage**: Local JSON file
- **Environment**: `.env` file for secure configuration

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd slack-habit-tracker
pip install -r requirements.txt
cp env.example .env
```

### 2. Create Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Name your app (e.g., "Habit Tracker Bot")
4. Select your workspace

### 3. Configure Slack App

#### Basic Information
- Add app icon and description
- Note your **Signing Secret** (you'll need this)

#### OAuth & Permissions
- Add these **Bot Token Scopes**:
  - `chat:write` - Send messages
  - `commands` - Add slash commands
  - `reactions:read` - Read reactions
  - `channels:history` - Read channel messages
  - `im:history` - Read DM messages
  - `app_mentions:read` - Read mentions

#### Slash Commands
Add these commands:
- **Command**: `/sethabit`
  - **Request URL**: `https://your-domain.com/slack/events` (for HTTP mode) or leave empty for Socket Mode
  - **Short Description**: Set a daily habit goal
  - **Usage Hint**: `[habit_name] [times_per_day]`

- **Command**: `/mystatus`
  - **Request URL**: Same as above
  - **Short Description**: View your habit progress
  - **Usage Hint**: (leave empty)

#### Event Subscriptions
- **Request URL**: `https://your-domain.com/slack/events` (for HTTP mode) or leave empty for Socket Mode
- **Subscribe to bot events**:
  - `reaction_added`
  - `app_mention`
  - `message.im`

#### Socket Mode
- Enable Socket Mode
- Generate an **App-Level Token** with `connections:write` scope
- Note the **App Token** (starts with `xapp-`)

### 4. Install App to Workspace

1. Go to "Install App" in the sidebar
2. Click "Install to Workspace"
3. Note your **Bot User OAuth Token** (starts with `xoxb-`)

### 5. Environment Setup

Edit `.env` with your Slack tokens:
```env
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
SLACK_APP_TOKEN=xapp-your-app-token-here
```

### 6. Run the Bot

```bash
python app.py
```

You should see: `🚀 Habit Tracker Bot is starting...`

## 📖 Usage

### Setting Habits
```
/sethabit drink_water 3
/sethabit exercise 1
/sethabit read 30
```

### Checking Status
```
/mystatus
```

### Tracking Progress
1. Send a message containing your habit name: "I just drank water!"
2. React with ✅ to increment progress
3. React with ❌ for motivation

### Getting Help
- Mention the bot: `@HabitTracker help`
- Send a DM to the bot: `help`

## 🚀 Deployment

### Railway (Recommended)

1. Fork this repository
2. Go to [railway.app](https://railway.app)
3. Connect your GitHub account
4. Create new project from GitHub repo
5. Add environment variables in Railway dashboard
6. Deploy!

### Render

1. Fork this repository
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Connect your GitHub repo
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `python app.py`
7. Add environment variables
8. Deploy!

### Replit

1. Go to [replit.com](https://replit.com)
2. Create new Python repl
3. Upload your files
4. Add environment variables in Secrets tab
5. Run the bot

## 📁 Project Structure

```
slack-habit-tracker/
├── app.py              # Main Slack bot application
├── habit_tracker.py    # Habit tracking logic
├── requirements.txt    # Python dependencies
├── env.example        # Environment variables template
├── SLACK_SETUP_GUIDE.md # Detailed Slack app setup instructions
├── habits.json        # User data storage (created automatically)
└── README.md          # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SLACK_BOT_TOKEN` | Bot User OAuth Token (xoxb-...) | Yes |
| `SLACK_SIGNING_SECRET` | App Signing Secret | Yes |
| `SLACK_APP_TOKEN` | App-Level Token (xapp-...) | Yes |
| `PORT` | Port for HTTP mode (optional) | No |

### Data Storage

The bot stores all user data in `habits.json`:

```json
{
  "users": {
    "U1234567890": {
      "drink_water": {
        "times_per_day": 3,
        "current_progress": 2,
        "last_reset_date": "2024-01-15",
        "created_date": "2024-01-15"
      }
    }
  },
  "habits": {}
}
```

## 🎯 Features in Detail

### Daily Reset
Progress automatically resets at midnight based on the user's timezone. The bot compares the current date with the last reset date.

### Progress Bars
Visual progress bars show completion percentage:
```
• drink_water: 2/3 (67%)
  ████████░░
```

### Motivational Messages
When users react with ❌, they get random motivational messages:
- "💪 Don't give up! Tomorrow is a new day to crush your goals!"
- "🌟 Every expert was once a beginner. Keep pushing forward!"
- "🔥 Progress, not perfection! You're doing great!"

### Smart Habit Matching
The bot intelligently matches habit names in messages:
- Message: "I just exercised!"
- Habit: "exercise" → Match found!

## 🐛 Troubleshooting

### Common Issues

1. **Bot not responding to commands**
   - Check if slash commands are properly configured
   - Verify bot token has correct scopes
   - Ensure app is installed to workspace

2. **Reactions not working**
   - Verify `reactions:read` scope is added
   - Check if habit names match exactly
   - Ensure bot can read channel messages

3. **Environment variables not loading**
   - Check `.env` file exists and is in correct location
   - Verify variable names match exactly
   - Restart the bot after changing environment variables

### Debug Mode

Enable debug logging by modifying `app.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [Slack Bolt for Python](https://slack.dev/bolt-python/)
- Inspired by the need for simple, free habit tracking tools
- Thanks to the Slack API team for excellent documentation

---

**Happy habit tracking! 🎉** 