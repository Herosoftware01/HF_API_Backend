from mcp.server.fastmcp import FastMCP
import api_service
import json

# Initialize FastMCP server
mcp = FastMCP("hero-fashion-mcp")

@mcp.tool()
async def get_buyers(query: str = None) -> str:
    """Fetch all buyers from Hero Fashion API. Optionally filter by any field."""
    try:
        data = await api_service.get_buyers()
        
        if query:
            query_lower = str(query).lower()
            def match_buyer(b):
                if not isinstance(b, dict): return False
                return any(query_lower in str(v).lower() for v in b.values() if v is not None)
                
            if isinstance(data, list):
                data = [b for b in data if match_buyer(b)]
            elif isinstance(data, dict) and "results" in data:
                data["results"] = [b for b in data["results"] if match_buyer(b)]
                
        return json.dumps(data)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def create_buyer(name: str, email: str, phone: str = "") -> str:
    """Create a new buyer in Hero Fashion API."""
    try:
        data = {"name": name, "email": email, "phone": phone}
        result = await api_service.create_buyer(data)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def update_buyer(buyer_id: str, name: str = None, email: str = None, phone: str = None) -> str:
    """Update an existing buyer in Hero Fashion API."""
    try:
        data = {}
        if name: data["name"] = name
        if email: data["email"] = email
        if phone: data["phone"] = phone
        result = await api_service.update_buyer(buyer_id, data)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def get_orders() -> str:
    """Fetch all orders from Hero Fashion API."""
    try:
        data = await api_service.get_orders()
        return json.dumps(data)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def create_order(buyer_id: str, product: str, quantity: int) -> str:
    """Create a new order in Hero Fashion API."""
    try:
        data = {"buyer_id": buyer_id, "product": product, "quantity": quantity}
        result = await api_service.create_order(data)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def update_order(order_id: str, status: str) -> str:
    """Update an existing order in Hero Fashion API."""
    try:
        data = {"status": status}
        result = await api_service.update_order(order_id, data)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def analyze_sales_data() -> str:
    """Analyze orders data and return sales statistics."""
    try:
        orders = await api_service.get_orders()
        if not isinstance(orders, list):
            orders = orders.get("results", orders) if isinstance(orders, dict) else []
            
        total_orders = len(orders)
        status_counts = {}
        product_quantities = {}
        
        for order in orders:
            status = order.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
            
            product = order.get("product", "unknown")
            try:
                quantity = int(order.get("quantity", 1))
            except (ValueError, TypeError):
                quantity = 1
            product_quantities[product] = product_quantities.get(product, 0) + quantity
            
        stats = {
            "Total Orders": total_orders,
            "Orders by Status": status_counts,
            "Product Quantities Sold": product_quantities
        }
        
        return json.dumps(stats)
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    # Run the server with SSE or stdio (default is stdio)
    mcp.run()