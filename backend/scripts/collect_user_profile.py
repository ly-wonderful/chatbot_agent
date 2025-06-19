import asyncio
from app.models.schemas import UserProfile
from app.database.supabase_client import supabase_client
import logging
from typing import List, Dict, Any
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import radiolist_dialog, checkboxlist_dialog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_valid_age() -> int:
    while True:
        try:
            age = int(input("Enter child's age (4-18): ").strip())
            if 4 <= age <= 18:
                return age
            print("❌ Age must be between 4 and 18.")
        except ValueError:
            print("❌ Please enter a valid number.")

def get_valid_grade(min_grade: int, max_grade: int) -> int:
    while True:
        try:
            grade = int(input(f"Enter child's grade level ({min_grade}-{max_grade}): ").strip())
            if min_grade <= grade <= max_grade:
                return grade
            print(f"❌ Grade must be between {min_grade} and {max_grade}.")
        except ValueError:
            print("❌ Please enter a valid number.")

def get_valid_distance() -> float:
    while True:
        try:
            distance = float(input("Enter maximum driving distance in miles: ").strip())
            if distance > 0:
                return distance
            print("❌ Distance must be greater than 0.")
        except ValueError:
            print("❌ Please enter a valid number.")

def get_interests() -> List[str]:
    print("\nEnter child's interests (one per line, press Enter twice to finish):")
    interests = []
    while True:
        interest = input().strip()
        if not interest:
            if not interests:
                print("❌ Please enter at least one interest.")
                continue
            break
        interests.append(interest)
    return interests

async def select_location() -> str:
    """Let user select a location from the database"""
    locations = await supabase_client.get_unique_locations()
    if not locations:
        return input("Enter your home address: ").strip()
    
    # Create location options
    location_options = [(f"{loc['city']}, {loc['state']}", f"{loc['city']}, {loc['state']}") 
                       for loc in locations]
    location_options.append(("other", "Other (Enter custom address)"))
    
    # Show location selection dialog
    result = radiolist_dialog(
        title="Select Location",
        text="Choose your location or enter a custom address:",
        values=location_options
    ).run()
    
    if result == "other":
        return input("Enter your home address: ").strip()
    return result

async def select_categories() -> List[str]:
    """Let user select camp categories from the database"""
    categories = await supabase_client.get_unique_categories()
    if not categories:
        return []
    
    # Create category options
    category_options = [(cat, cat) for cat in categories]
    
    # Show category selection dialog
    result = checkboxlist_dialog(
        title="Select Camp Categories",
        text="Choose preferred camp categories (use space to select, enter to confirm):",
        values=category_options
    ).run()
    
    return result if result else []

async def collect_user_profile() -> UserProfile:
    """Interactive function to collect user profile information"""
    
    print("\n👋 Welcome to Camp Search!")
    print("Let's get to know you and your child better.")
    print("----------------------------------------")
    
    # Collect parent/guardian information
    name = input("\nWhat's your name? ").strip()
    while not name:
        print("❌ Name cannot be empty.")
        name = input("What's your name? ").strip()
    
    # Collect child information
    child_name = input("\nWhat's your child's name? ").strip()
    while not child_name:
        print("❌ Child's name cannot be empty.")
        child_name = input("What's your child's name? ").strip()
    
    child_age = get_valid_age()
    
    # Get grade range from database
    grade_range = await supabase_client.get_grade_range()
    child_grade = get_valid_grade(grade_range["min"], grade_range["max"])
    
    # Collect interests
    print("\nWhat are your child's interests?")
    print("(Examples: sports, arts, science, music, etc.)")
    interests = get_interests()
    
    # Collect location information
    print("\nWhere are you located?")
    address = await select_location()
    while not address:
        print("❌ Address cannot be empty.")
        address = await select_location()
    
    max_distance = get_valid_distance()
    
    # Collect special needs information
    print("\nDoes your child have any special needs or require accommodations?")
    print("(Press Enter to skip if none)")
    special_needs = input().strip()
    
    # Collect preferred categories
    print("\nSelect preferred camp categories:")
    preferred_categories = await select_categories()
    
    # Create and return user profile
    profile = UserProfile(
        name=name,
        child_name=child_name,
        child_age=child_age,
        child_grade=child_grade,
        interests=interests,
        address=address,
        max_distance_miles=max_distance,
        special_needs=special_needs if special_needs else None,
        preferred_categories=preferred_categories if preferred_categories else None
    )
    
    # Display summary
    print("\n📋 Profile Summary:")
    print("------------------")
    print(f"Parent/Guardian: {profile.name}")
    print(f"Child: {profile.child_name} (Age: {profile.child_age}, Grade: {profile.child_grade})")
    print(f"Interests: {', '.join(profile.interests)}")
    print(f"Location: {profile.address}")
    print(f"Maximum Distance: {profile.max_distance_miles} miles")
    if profile.special_needs:
        print(f"Special Needs: {profile.special_needs}")
    if profile.preferred_categories:
        print(f"Preferred Categories: {', '.join(profile.preferred_categories)}")
    
    return profile

if __name__ == "__main__":
    asyncio.run(collect_user_profile()) 