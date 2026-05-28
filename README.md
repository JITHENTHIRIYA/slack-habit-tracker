# Slack Habit Tracker Bot

A Slack bot for tracking daily habits using slash commands and emoji reactions. No paid API keys required — runs entirely on free-tier infrastructure.

## Features

- **Set habits**: `/sethabit [habit_name] [times_per_day]` — define a daily habit with a target count
- **Check progress**: `/mystatus` — view progress for all your habits with visual progress bars
- **Emoji reactions**:
  - React with ✅ on a message containing a habit name to increment progress
  - React with ❌ to receive a motivational nudge
- **Daily reset**: Progress resets automatically each day based on the current date
- **Local storage**: All data persisted in a `habits.json` file

## Tech Stack

- **Language**: Python 3.8+
- **Framework**: [Slack Bolt for Python](https://slack.dev/bolt-python/)
- **Transport**: Socket Mode (no public URL required)
- **Storage**: Local JSON file

## Setup

### 1. Install dependencies

```bash
git clone <your-repo>
cd slack-habit-tracker
pip install -r requirements.txt
cp env.example .env
```

### 2. Create a Slack app

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create New App** → **From scratch**
3. Name your app and select your workspace

### 3. Configure the Slack app

#### OAuth & Permissions

Add the following **Bot Token Scopes**:

| Scope | Purpose |
|-------|---------|
| `chat:write` | Send messages |
| `commands` | Register slash commands |
| `reactions:read` | Listen to emoji reactions |
| `channels:history` | Read channel messages |
| `im:history` | Read direct messages |
| `app_mentions:read` | Respond to mentions |

#### Slash Commands

Add these two commands (Request URL can be left empty when using Socket Mode):

| Command | Description | Usage Hint |
|---------|-------------|------------|
| `/sethabit` | Set a daily habit goal | `[habit_name] [times_per_day]` |
| `/mystatus` | View habit progress | — |

#### Event Subscriptions

Subscribe to the following bot events:

- `reaction_added`
- `app_mention`
- `message.im`

#### Socket Mode

1. Enable **Socket Mode** in app settings
2. Generate an **App-Level Token** with the `connections:write` scope
3. Save the token — it starts with `xapp-`

### 4. Install the app to your workspace

1. Go to **Install App** in the sidebar
2. Click **Install to Workspace**
3. Copy the **Bot User OAuth Token** — it starts with `xoxb-`

### 5. Configure environment variables

Edit `.env` with your tokens:

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
SLACK_APP_TOKEN=xapp-your-app-token-here
```

### 6. Run the bot

```bash
python app.py
```

## Usage

### Setting habits

```
/sethabit drink_water 3
/sethabit exercise 1
/sethabit read 30
```

### Checking status

```
/mystatus
```

Output example:
```
drink_water: 2/3 (67%)
  ████████░░
```

### Tracking progress

1. Send a message mentioning a habit name: `"I just drank water!"`
2. React with ✅ to increment the count for that habit
3. React with ❌ for a motivational message

### Getting help

- Mention the bot: `@HabitTracker help`
- Send it a direct message: `help`

## Deployment

### Railway (recommended)

1. Fork this repository
2. Go to [railway.app](https://railway.app) and connect your GitHub account
3. Create a new project from your forked repo
4. Add the environment variables in the Railway dashboard
5. Deploy

### Render

1. Fork this repository
2. Go to [render.com](https://render.com) and create a new **Web Service**
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python app.py`
6. Add environment variables and deploy

### Replit

1. Create a new Python repl at [replit.com](https://replit.com)
2. Upload your project files
3. Add environment variables under the **Secrets** tab
4. Run the bot

## Project Structure

```
slack-habit-tracker/
├── app.py                # Slack bot entry point and event handlers
├── habit_tracker.py      # Habit tracking logic and data management
├── requirements.txt      # Python dependencies
├── env.example           # Environment variable template
├── SLACK_SETUP_GUIDE.md  # Extended Slack app configuration guide
└── habits.json           # User data (auto-created on first run)
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SLACK_BOT_TOKEN` | Bot User OAuth Token (`xoxb-...`) | Yes |
| `SLACK_SIGNING_SECRET` | App Signing Secret | Yes |
| `SLACK_APP_TOKEN` | App-Level Token (`xapp-...`) | Yes |
| `PORT` | HTTP port (only needed for HTTP mode) | No |

## Data Storage

User habit data is stored in `habits.json`:

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
  }
}
```

## Troubleshooting

**Bot not responding to slash commands**
- Confirm slash commands are configured in your Slack app settings
- Verify the bot token has all required scopes
- Check that the app is installed to the workspace

**Reactions not tracked**
- Confirm the `reactions:read` scope is present
- Ensure the message you reacted to contains a habit name recognized by the bot

**Environment variables not loading**
- Verify the `.env` file exists in the project root
- Check that variable names match exactly
- Restart the bot after any changes to `.env`

**Enable debug logging**

```python
# In app.py
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes and test thoroughly
4. Open a pull request

## License

MIT License. See [LICENSE](LICENSE) for details.
