import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from habit_tracker import HabitTracker

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Slack app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Initialize habit tracker
habit_tracker = HabitTracker()

@app.command("/sethabit")
def handle_sethabit(ack, command):
    """Handle /sethabit command"""
    ack()
    
    try:
        # Parse command text
        text = command.get("text", "").strip()
        if not text:
            app.client.chat_postEphemeral(
                channel=command["channel_id"],
                user=command["user_id"],
                text="❌ Please provide a habit name and frequency. Usage: `/sethabit [habit_name] [times_per_day]`\nExample: `/sethabit drink_water 3`"
            )
            return
        
        parts = text.split()
        if len(parts) < 2:
            app.client.chat_postEphemeral(
                channel=command["channel_id"],
                user=command["user_id"],
                text="❌ Please provide both habit name and frequency. Usage: `/sethabit [habit_name] [times_per_day]`"
            )
            return
        
        habit_name = parts[0]
        try:
            times_per_day = int(parts[1])
            if times_per_day <= 0:
                raise ValueError("Frequency must be positive")
        except ValueError:
            app.client.chat_postEphemeral(
                channel=command["channel_id"],
                user=command["user_id"],
                text="❌ Frequency must be a positive number. Example: `/sethabit drink_water 3`"
            )
            return
        
        # Set the habit
        response = habit_tracker.set_habit(command["user_id"], habit_name, times_per_day)
        
        try:
            app.client.chat_postEphemeral(
                channel=command["channel_id"],
                user=command["user_id"],
                text=response
            )
        except Exception as e:
            logger.error(f"Error sending ephemeral message: {e}")
            # Fallback: try to send a regular message
            try:
                app.client.chat_postMessage(
                    channel=command["channel_id"],
                    text=response
                )
            except Exception as e2:
                logger.error(f"Error sending regular message: {e2}")
        
    except Exception as e:
        logger.error(f"Error in sethabit command: {e}")
        try:
            app.client.chat_postEphemeral(
                channel=command["channel_id"],
                user=command["user_id"],
                text="❌ An error occurred while setting your habit. Please try again."
            )
        except Exception as e2:
            logger.error(f"Error sending error message: {e2}")

@app.command("/mystatus")
def handle_mystatus(ack, command):
    """Handle /mystatus command"""
    ack()
    
    try:
        response = habit_tracker.get_status(command["user_id"])
        
        try:
            app.client.chat_postEphemeral(
                channel=command["channel_id"],
                user=command["user_id"],
                text=response
            )
        except Exception as e:
            logger.error(f"Error sending ephemeral message: {e}")
            # Fallback: try to send a regular message
            try:
                app.client.chat_postMessage(
                    channel=command["channel_id"],
                    text=response
                )
            except Exception as e2:
                logger.error(f"Error sending regular message: {e2}")
        
    except Exception as e:
        logger.error(f"Error in mystatus command: {e}")
        try:
            app.client.chat_postEphemeral(
                channel=command["channel_id"],
                user=command["user_id"],
                text="❌ An error occurred while fetching your status. Please try again."
        )
        except Exception as e2:
            logger.error(f"Error sending error message: {e2}")

@app.event("reaction_added")
def handle_reaction_added(event, say):
    """Handle emoji reactions"""
    try:
        reaction = event.get("reaction")
        user_id = event.get("user")
        item = event.get("item", {})
        
        # Only handle reactions on messages
        if item.get("type") != "message":
            return
        
        # Get the message to extract habit name
        try:
            message_response = app.client.conversations_history(
                channel=item.get("channel"),
                latest=item.get("ts"),
                limit=1,
                inclusive=True
            )
            
            if not message_response["ok"] or not message_response["messages"]:
                return
            
            message = message_response["messages"][0]
            message_text = message.get("text", "").lower()
            
            # Check if message contains habit names
            user_habits = habit_tracker.get_user_habits(user_id)
            matched_habit = None
            
            for habit in user_habits:
                if habit.lower() in message_text:
                    matched_habit = habit
                    break
            
            if not matched_habit:
                return
            
            # Handle different reactions
            if reaction in ["white_check_mark", "heavy_check_mark"]:  # ✅
                response = habit_tracker.increment_progress(user_id, matched_habit)
                say(text=response, thread_ts=item.get("ts"))
                
            elif reaction in ["x", "negative_squared_cross_mark"]:  # ❌
                response = habit_tracker.send_motivation(user_id, matched_habit)
                say(text=response, thread_ts=item.get("ts"))
                
        except Exception as e:
            logger.error(f"Error processing reaction: {e}")
            
    except Exception as e:
        logger.error(f"Error in reaction handler: {e}")

@app.event("app_mention")
def handle_app_mention(event, say):
    """Handle when the bot is mentioned"""
    try:
        text = event.get("text", "").lower()
        
        if "help" in text or "commands" in text:
            help_text = """
🤖 **Habit Tracker Bot Commands:**

• `/sethabit [habit_name] [times_per_day]` - Set a new habit goal
  Example: `/sethabit drink_water 3`

• `/mystatus` - View your current progress

• React with ✅ to a message containing your habit name to mark progress
• React with ❌ to get motivational support

**Examples:**
- Set a habit: `/sethabit exercise 1`
- Check status: `/mystatus`
- Mark progress: React with ✅ to "I just exercised!"
            """
            say(text=help_text)
        else:
            say(text="👋 Hi! I'm your habit tracking assistant. Use `/sethabit` to get started or mention me with 'help' to see all commands!")
            
    except Exception as e:
        logger.error(f"Error in app mention handler: {e}")

@app.event("message")
def handle_message(event, say):
    """Handle direct messages to the bot"""
    try:
        # Only respond to direct messages
        if event.get("channel_type") != "im":
            return
        
        text = event.get("text", "").lower()
        
        if "help" in text or "commands" in text:
            help_text = """
🤖 **Habit Tracker Bot Commands:**

• `/sethabit [habit_name] [times_per_day]` - Set a new habit goal
  Example: `/sethabit drink_water 3`

• `/mystatus` - View your current progress

• React with ✅ to a message containing your habit name to mark progress
• React with ❌ to get motivational support

**Examples:**
- Set a habit: `/sethabit exercise 1`
- Check status: `/mystatus`
- Mark progress: React with ✅ to "I just exercised!"
            """
            say(text=help_text)
        else:
            say(text="👋 Hi! I'm your habit tracking assistant. Use `/sethabit` to get started or type 'help' to see all commands!")
            
    except Exception as e:
        logger.error(f"Error in message handler: {e}")

if __name__ == "__main__":
    # Check for required environment variables
    required_vars = ["SLACK_BOT_TOKEN", "SLACK_SIGNING_SECRET", "SLACK_APP_TOKEN"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set them in your .env file or environment.")
        exit(1)
    
    # Start the app
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    print("🚀 Habit Tracker Bot is starting...")
    handler.start() 