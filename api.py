"""
API endpoints for the Discord bot
"""

from flask import request, jsonify
import asyncio

# Will be set by the main bot module
bot_instance = None


def set_bot(bot):
    """Set the bot instance for use by the API"""
    global bot_instance
    bot_instance = bot


def send_message():
    """
    Send a message to a Discord channel
    """
    data = request.get_json()
    channel_id = data.get('channel_id')
    message = data.get('message')
    
    if not channel_id or not message:
        return {"error": "Missing channel_id or message"}, 400
    
    if not bot_instance:
        return {"error": "Bot not initialized"}, 500

    try:
        channel = bot_instance.get_channel(int(channel_id))
        if not channel:
            return {"error": f"Channel {channel_id} not found"}, 404

        # Create a coroutine and run it in the bot's event loop
        coro = channel.send(message)
        future = asyncio.run_coroutine_threadsafe(coro, bot_instance.loop)
        msg = future.result()

        return {
            "status": "success",
            "message_id": msg.id,
            "channel_id": channel_id
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500


def send_dm():
    """
    Send a direct message to a Discord user
    """
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')
    
    if not user_id or not message:
        return {"error": "Missing user_id or message"}, 400
    
    if not bot_instance:
        return {"error": "Bot not initialized"}, 500

    try:
        user = bot_instance.get_user(int(user_id))
        if not user:
            return {"error": f"User {user_id} not found"}, 404

        # Create a coroutine and run it in the bot's event loop
        coro = user.send(message)
        future = asyncio.run_coroutine_threadsafe(coro, bot_instance.loop)
        msg = future.result()

        return {
            "status": "success",
            "message_id": msg.id,
            "user_id": user_id
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500


def get_status():
    """
    Get the current status of the bot
    """
    if not bot_instance:
        return {"status": "disconnected"}, 200

    return {
        "status": "connected" if bot_instance.is_ready() else "connecting",
        "bot_name": bot_instance.user.name if bot_instance.is_ready() else "Unknown",
        "latency": round(bot_instance.latency * 1000, 2)
    }, 200
