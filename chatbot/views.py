from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import json
from asgiref.sync import async_to_sync

from .serializers import ChatRequestSerializer
from .services import ai_service
# from .services.mcp_client import call_mcp_tool

def index(request):
    """Serve the frontend chat UI."""
    return render(request, 'chatbot.html')

class ChatAPIView(APIView):
    """
    API View to handle incoming chat messages, use Gemini for intent parsing, 
    call MCP tools, and use Gemini to generate a response.
    """
    def post(self, request, *args, **kwargs):
        serializer = ChatRequestSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data['message']
            
            # Use Gemini AI to parse intent
            tool_name, arguments = ai_service.select_mcp_tool(message)
            print("TOOL:", tool_name)
            print("ARGS:", arguments)
            
            if not tool_name:
                # Fallbacks in case Gemini API is blocked by rate limits
                msg_lower = message.lower().strip()
                if msg_lower == "show buyers":
                    tool_name = "get_buyers"
                    arguments = {}
                elif msg_lower == "show all buyers":
                    tool_name = "get_buyers"
                    arguments = {}
                elif "order" in msg_lower and len(msg_lower.split()) <= 2:
                    tool_name = "get_orders"
                    arguments = {}
                elif msg_lower not in ["hi", "hello", "hey"] and len(msg_lower) < 20:
                    # Treat short unmatched messages as a general search query
                    tool_name = "get_buyers"
                    arguments = {"query": message.strip()}
                else:
                    return Response({
                        "reply": "My AI is currently hitting API quota limits. But you can still try typing 'Show buyers', a date, or an order number directly."
                    }, status=status.HTTP_200_OK)
                
            if tool_name == "chat":
                reply_message = arguments.get(
                    "message",
                    "Hello! 👋 I can help you with buyers, orders, and sales data."
                )

                return Response({
                    "reply": reply_message
                }, status=status.HTTP_200_OK)
                
            ALLOWED_TOOLS = [
                "get_buyers",
                "create_buyer",
                "update_buyer",
                "get_orders",
                "create_order",
                "update_order",
                "analyze_sales_data"
            ]
            
            if tool_name not in ALLOWED_TOOLS:
                return Response({
                    "reply": "Invalid tool request"
                }, status=status.HTTP_200_OK)
            
            # Call MCP Server tool synchronously using async_to_sync
            try:
                mcp_result = async_to_sync(call_mcp_tool)(tool_name, arguments)
                
                # Attempt to parse result as JSON
                try:
                    data_payload = json.loads(mcp_result)
                    
                    # Generate a human-friendly response using Gemini
                    human_reply = ai_service.generate_human_response(tool_name, data_payload)
                    
                    if isinstance(data_payload, str):
                        return Response({
                            "reply": human_reply,
                            "data": None
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            "reply": human_reply,
                            "data": data_payload
                        }, status=status.HTTP_200_OK)
                        
                except json.JSONDecodeError:
                    # Result is a plain string
                    human_reply = ai_service.generate_human_response(tool_name, {"result": mcp_result})
                    return Response({
                        "reply": human_reply,
                        "data": None
                    }, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response({
                    "reply": f"Error interacting with MCP tools: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
