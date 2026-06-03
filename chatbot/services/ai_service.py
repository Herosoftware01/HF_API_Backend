# import os
# import re
# import json
# # import google.generativeai as genai
# # from dotenv import load_dotenv

# load_dotenv()

# # Configure Gemini
# api_key = os.getenv("GEMINI_API_KEY")

# genai.configure(api_key=api_key)

# # Gemini model
# model = genai.GenerativeModel("gemini-2.5-flash")


# TOOL_DESCRIPTIONS = """
# Available Tools:

# 1. get_buyers()
# - Fetch all buyers
# - Show buyers
# - Customer list
# - Buyer list
# - Total buyers
# - How many buyers
# - IMPORTANT: If the user provides a specific search term (like a name, date, or order number), extract it and pass it as the "query" argument (e.g., {"query": "Murthy"} or {"query": "2025-12-19"}).

# 2. get_orders()
# - Fetch all orders
# - Show orders
# - Order list
# - Total orders
# - How many orders

# 3. analyze_sales_data()
# - Sales summary
# - Product analysis
# - Sales statistics
# - Which product sold most

# 4. chat(message)
# Use this for:
# - hi
# - hii
# - hello
# - hey
# - good morning
# - good evening
# - how are you
# - thank you
# - casual conversation

# Return a friendly response.

# JSON format:

# {
#     "tool": "tool_name",
#     "arguments": {}
# }

# For greetings:

# {
#     "tool": "chat",
#     "arguments": {
#         "message":
#         "Hello! 👋 I can help you with buyers, orders, and sales data."
#     }
# }

# If no tool matches:

# {
#     "tool": null,
#     "arguments": {}
# }
# """


# def select_mcp_tool(
#     user_message: str
# ):
#     """
#     Select MCP tool
#     from user message.
#     """

#     prompt = f"""
# {TOOL_DESCRIPTIONS}

# User message:
# {user_message}

# Determine the correct tool.

# Return ONLY valid JSON.

# Do not explain.
# Do not use markdown.
# Only JSON.
# """

#     try:

#         response = model.generate_content(
#             prompt,
#             generation_config=
#             genai.GenerationConfig(
#                 response_mime_type=
#                 "application/json"
#             )
#         )

#         text = response.text.strip()

#         print(
#             "Gemini Response:",
#             text
#         )

#         match = re.search(r"\{.*\}", text, re.DOTALL)
#         parsed = json.loads(match.group()) if match else None

#         tool_name = parsed.get(
#             "tool"
#         )

#         arguments = parsed.get(
#             "arguments",
#             {}
#         )

#         if not isinstance(
#             arguments,
#             dict
#         ):
#             arguments = {}

#         return (
#             tool_name,
#             arguments
#         )

#     except Exception as e:

#         print(
#             "Error in select_mcp_tool:",
#             str(e)
#         )

#         return (
#             None,
#             {}
#         )


# def generate_human_response(
#     tool_name: str,
#     mcp_result
# ):
#     """
#     Convert MCP result
#     into human response.
#     """

#     # Greeting chat response
#     if tool_name == "chat":

#         if isinstance(
#             mcp_result,
#             dict
#         ):
#             return mcp_result.get(
#                 "message",
#                 "Hello! 👋"
#             )

#         return str(mcp_result)

#     prompt = f"""
# Tool used:
# {tool_name}

# Returned data:
# {json.dumps(mcp_result)}

# Write a short,
# friendly response.

# Rules:
# - Keep response short
# - No raw JSON
# - Be conversational
# - Summarize data

# Examples:

# "There are 120 buyers."

# "I found 84 orders."

# "Sales analysis completed."

# "Top selling product is shirt."
# """

#     try:

#         response = model.generate_content(
#             prompt
#         )

#         return response.text.strip()

#     except Exception as e:

#         print(
#             "Error in generate_human_response:",
#             str(e)
#         )

#         return (
#             "Action completed successfully."
#         )