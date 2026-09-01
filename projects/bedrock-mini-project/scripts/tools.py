"""
Stretch tier — tool definitions.

Define one or more tools your agent can call. The model never executes these;
it requests them by name and your code dispatches.

Pattern: function + schema + dispatch table.

For the Stretch tier, you only need ONE tool. Pick one from your template,
or invent one. Mock the data — no need for a real backend.
"""

from datetime import datetime, timedelta
from typing import Any


# ===== Tool implementations (just normal Python functions) =====

def get_vacation_balance(employee_id: str) -> dict:
    """Return remaining vacation days for an employee.
    
    In a real app, this would call your HR system / Workday / etc.
    Here, we mock it.
    """
    # Mocked data — return realistic-looking values
    mock_data = {
        "E001": {"name": "Alex Kim", "days_remaining": 12, "days_taken": 8},
        "E002": {"name": "Priya Singh", "days_remaining": 18, "days_taken": 2},
        "E003": {"name": "Marcus Chen", "days_remaining": 5, "days_taken": 15},
    }
    if employee_id not in mock_data:
        return {"error": f"Employee {employee_id} not found"}
    return {
        "employee_id": employee_id,
        **mock_data[employee_id],
        "as_of_date": datetime.utcnow().date().isoformat(),
    }


def check_order_status(order_id: str) -> dict:
    """Return order status for a customer support bot."""
    # Mocked
    mock_orders = {
        "ORD-100": {"status": "Delivered", "delivered_on": "2026-05-10"},
        "ORD-101": {"status": "In transit", "expected": "2026-05-16"},
        "ORD-102": {"status": "Processing", "placed_on": "2026-05-13"},
    }
    if order_id not in mock_orders:
        return {"error": f"Order {order_id} not found"}
    return {"order_id": order_id, **mock_orders[order_id]}


def get_current_date() -> dict:
    """Return today's date — useful for research/analysis assistant."""
    today = datetime.utcnow().date()
    return {
        "today": today.isoformat(),
        "weekday": today.strftime("%A"),
        "iso_week": today.isocalendar().week,
    }


# ===== Tool schemas (what the model sees) =====

TOOL_CONFIG = {
    "tools": [
        {
            "toolSpec": {
                "name": "get_vacation_balance",
                "description": (
                    "Return remaining vacation days for a specific employee. "
                    "Use ONLY when a user asks about their own or a colleague's vacation balance. "
                    "Requires the employee ID (format: E001, E002, …)."
                ),
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "employee_id": {
                                "type": "string",
                                "description": "Employee ID, e.g. 'E001'.",
                            },
                        },
                        "required": ["employee_id"],
                    }
                },
            }
        },
        # Add more toolSpec entries here if you have more tools.
        # For Stretch, ONE tool is enough.
    ]
}


# ===== Dispatch table =====

TOOL_FUNCTIONS = {
    "get_vacation_balance": get_vacation_balance,
    "check_order_status": check_order_status,
    "get_current_date": get_current_date,
}


def run_tool(tool_name: str, tool_input: dict) -> Any:
    """Look up and execute a tool by name."""
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return {"error": f"Unknown tool: {tool_name}"}
    try:
        return func(**tool_input)
    except TypeError as e:
        return {"error": f"Bad tool input: {e}"}
    except Exception as e:
        return {"error": f"Tool execution failed: {e}"}
