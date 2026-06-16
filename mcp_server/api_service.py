import httpx
from typing import Dict, Any, List

BASE_URL = "https://app.herofashion.com"

async def get_buyers() -> Any:
    """Fetch all buyers."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{BASE_URL}/web_socket/")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP Error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

async def create_buyer(data: Dict[str, Any]) -> Any:
    """Create a new buyer."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{BASE_URL}/create_buyer/", json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP Error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

async def update_buyer(buyer_id: str, data: Dict[str, Any]) -> Any:
    """Update an existing buyer."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.put(f"{BASE_URL}/update_buyer/{buyer_id}/", json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP Error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

async def get_orders() -> Any:
    """Fetch all orders."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{BASE_URL}/torder/")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP Error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

async def create_order(data: Dict[str, Any]) -> Any:
    """Create a new order."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{BASE_URL}/create_torder/", json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP Error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

async def update_order(order_id: str, data: Dict[str, Any]) -> Any:
    """Update an existing order."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.put(f"{BASE_URL}/update_torder/{order_id}/", json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP Error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}
