import asyncio
from database.supabase_client import supabase_client

async def get_all_categories():

    try:
        categories = await supabase_client.get_all_categories()
        print("All available categories in your database:")
        for i, cat in enumerate(categories, 1):
            print(f"{i:2d}. {cat.get('name', 'No name')}")
        return categories
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    asyncio.run(get_all_categories())
