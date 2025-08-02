import json
import os
from datetime import datetime, date
from typing import Dict, List, Optional

class HabitTracker:
    def __init__(self, data_file: str = "habits.json"):
        self.data_file = data_file
        self.load_data()
    
    def load_data(self):
        """Load habit data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.data = {"users": {}, "habits": {}}
        else:
            self.data = {"users": {}, "habits": {}}
    
    def save_data(self):
        """Save habit data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def set_habit(self, user_id: str, habit_name: str, times_per_day: int) -> str:
        """Set a new habit for a user"""
        if user_id not in self.data["users"]:
            self.data["users"][user_id] = {}
        
        self.data["users"][user_id][habit_name] = {
            "times_per_day": times_per_day,
            "current_progress": 0,
            "last_reset_date": date.today().isoformat(),
            "created_date": date.today().isoformat()
        }
        
        self.save_data()
        return f"✅ Habit '{habit_name}' set! Goal: {times_per_day} times per day"
    
    def get_status(self, user_id: str) -> str:
        """Get current status of user's habits"""
        if user_id not in self.data["users"] or not self.data["users"][user_id]:
            return "❌ You haven't set any habits yet. Use `/sethabit [habit_name] [times_per_day]` to get started!"
        
        self._check_and_reset_daily(user_id)
        
        status_lines = ["📊 **Your Habit Status:**"]
        for habit_name, habit_data in self.data["users"][user_id].items():
            progress = habit_data["current_progress"]
            goal = habit_data["times_per_day"]
            percentage = min(100, (progress / goal) * 100)
            
            # Create progress bar
            filled = int(percentage / 10)
            progress_bar = "█" * filled + "░" * (10 - filled)
            
            status_lines.append(
                f"• **{habit_name}**: {progress}/{goal} ({percentage:.0f}%)\n"
                f"  {progress_bar}"
            )
        
        return "\n".join(status_lines)
    
    def increment_progress(self, user_id: str, habit_name: str) -> str:
        """Increment progress for a specific habit"""
        if user_id not in self.data["users"]:
            return "❌ You haven't set any habits yet!"
        
        if habit_name not in self.data["users"][user_id]:
            return f"❌ Habit '{habit_name}' not found! Use `/sethabit` to create it."
        
        self._check_and_reset_daily(user_id)
        
        habit_data = self.data["users"][user_id][habit_name]
        current_progress = habit_data["current_progress"]
        goal = habit_data["times_per_day"]
        
        if current_progress >= goal:
            return f"🎉 You've already completed your goal for '{habit_name}' today! Great job!"
        
        habit_data["current_progress"] += 1
        self.save_data()
        
        new_progress = habit_data["current_progress"]
        if new_progress >= goal:
            return f"🎉 **Congratulations!** You've completed your goal for '{habit_name}' today!"
        else:
            remaining = goal - new_progress
            return f"✅ Progress updated! '{habit_name}': {new_progress}/{goal} ({remaining} more to go!)"
    
    def send_motivation(self, user_id: str, habit_name: str) -> str:
        """Send motivational message for negative reactions"""
        if user_id not in self.data["users"] or habit_name not in self.data["users"][user_id]:
            return "💪 Keep going! Every small step counts towards your goals!"
        
        habit_data = self.data["users"][user_id][habit_name]
        current_progress = habit_data["current_progress"]
        goal = habit_data["times_per_day"]
        
        motivational_messages = [
            "💪 Don't give up! Tomorrow is a new day to crush your goals!",
            "🌟 Every expert was once a beginner. Keep pushing forward!",
            "🔥 Progress, not perfection! You're doing great!",
            "🚀 Small steps lead to big changes. You've got this!",
            "💎 Consistency beats intensity. Keep showing up!",
            "🌈 Every setback is a setup for a comeback!",
            "⚡ You're stronger than your excuses!",
            "🎯 Focus on progress, not perfection!",
            "💫 You have the power to change your habits!",
            "🌟 Believe in yourself and all that you are!"
        ]
        
        import random
        return random.choice(motivational_messages)
    
    def _check_and_reset_daily(self, user_id: str):
        """Check if it's a new day and reset progress if needed"""
        today = date.today().isoformat()
        
        if user_id in self.data["users"]:
            for habit_name, habit_data in self.data["users"][user_id].items():
                if habit_data["last_reset_date"] != today:
                    habit_data["current_progress"] = 0
                    habit_data["last_reset_date"] = today
            
            self.save_data()
    
    def get_user_habits(self, user_id: str) -> List[str]:
        """Get list of habit names for a user"""
        if user_id in self.data["users"]:
            return list(self.data["users"][user_id].keys())
        return [] 