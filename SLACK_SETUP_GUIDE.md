# 🚀 Slack Setup Guide - Habit Tracker Bot

## Step 1: Create Your Slack App

1. **Go to Slack API Console**
   - Visit: https://api.slack.com/apps
   - Click "Create New App"
   - Choose "From scratch"
   - Name: "Habit Tracker Bot" (or your preferred name)
   - Select your workspace

## Step 2: Configure Basic Information

1. **Add App Icon & Description**
   - Go to "Basic Information" in the sidebar
   - Upload an icon (optional but recommended)
   - Add description: "Track daily habits with emoji reactions"
   - **Save your Signing Secret** (you'll need this)

## Step 3: Enable Socket Mode

1. **Enable Socket Mode**
   - Go to "Socket Mode" in the sidebar
   - Toggle "Enable Socket Mode" to ON
   - Generate an App-Level Token:
     - Name: "habit-tracker-socket"
     - Add scope: `connections:write`
   - **Save your App Token** (starts with `xapp-`)

## Step 4: Configure OAuth & Permissions

1. **Add Bot Token Scopes**
   - Go to "OAuth & Permissions" in the sidebar
   - Scroll to "Scopes" → "Bot Token Scopes"
       - Add these scopes:
      - `chat:write` - Send messages
      - `commands` - Add slash commands
      - `reactions:read` - Read reactions
      - `channels:history` - Read channel messages
      - `channels:read` - Read channel information
      - `groups:read` - Read private channels
      - `mpim:read` - Read multi-person DMs
      - `im:read` - Read direct messages
      - `im:history` - Read DM message history
      - `app_mentions:read` - Read mentions

2. **Install App to Workspace**
   - Scroll to "OAuth Tokens for Your Workspace"
   - Click "Install to Workspace"
   - **Save your Bot User OAuth Token** (starts with `xoxb-`)

## Step 5: Configure Slash Commands

1. **Add /sethabit Command**
   - Go to "Slash Commands" in the sidebar
   - Click "Create New Command"
   - Command: `/sethabit`
   - Request URL: (leave empty for Socket Mode)
   - Short Description: "Set a daily habit goal"
   - Usage Hint: `[habit_name] [times_per_day]`

2. **Add /mystatus Command**
   - Click "Create New Command"
   - Command: `/mystatus`
   - Request URL: (leave empty for Socket Mode)
   - Short Description: "View your habit progress"
   - Usage Hint: (leave empty)

## Step 6: Configure Event Subscriptions

1. **Enable Events**
   - Go to "Event Subscriptions" in the sidebar
   - Toggle "Enable Events" to ON
   - Request URL: (leave empty for Socket Mode)

2. **Subscribe to Bot Events**
   - Scroll to "Subscribe to bot events"
   - Add these events:
     - `reaction_added`
     - `app_mention`
     - `message.im`

## Step 7: Configure Environment Variables

1. **Create .env File**
   ```bash
   cp env.example .env
   ```

2. **Edit .env File**
   ```env
   SLACK_BOT_TOKEN=xoxb-your-bot-token-here
   SLACK_SIGNING_SECRET=your-signing-secret-here
   SLACK_APP_TOKEN=xapp-your-app-token-here
   ```

## Step 8: Test Your Bot

1. **Run the Bot**
   ```bash
   python app.py
   ```

2. **Test in Slack**
   - Go to any channel in your workspace
   - Try: `/sethabit drink_water 3`
   - Try: `/mystatus`
   - Send a message: "I just drank water!"
   - React with ✅ to that message

## Troubleshooting

### Common Issues:

1. **"not_allowed_token_type" Error**
   - Make sure Socket Mode is enabled
   - Verify App Token has `connections:write` scope
   - Check that you're using the App Token (xapp-) not Bot Token (xoxb-)

2. **Commands Not Working**
   - Verify app is installed to workspace
   - Check bot token scopes
   - Ensure commands are properly configured

3. **Reactions Not Working**
   - Verify `reactions:read` scope is added
   - Check event subscriptions
   - Make sure habit names match exactly

### Token Types:
- **Bot Token** (xoxb-): Used for sending messages, reading channels
- **App Token** (xapp-): Used for Socket Mode connections
- **Signing Secret**: Used for verifying requests (not needed for Socket Mode)

## Testing Checklist

- [ ] App created and configured
- [ ] Socket Mode enabled
- [ ] All required scopes added
- [ ] Slash commands configured
- [ ] Event subscriptions enabled
- [ ] App installed to workspace
- [ ] Environment variables set
- [ ] Bot runs without errors
- [ ] Commands work in Slack
- [ ] Reactions work in Slack

## Next Steps

Once your bot is working:
1. Test with different habits
2. Try the motivational features
3. Check daily reset functionality
4. Deploy to Railway/Render for 24/7 operation 