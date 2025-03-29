
from uagents import Agent, Context, Protocol, Model

class BudgetQuery(Model):
    total_spent: float
    budget_limit: float

class BudgetResponse(Model):
    message: str

budget_agent = Agent(name="budget-agent", seed="budget-agent-secret")

budget_protocol = Protocol("BudgetProtocol")

@budget_protocol.on_message(model=BudgetQuery)
async def handle_query(ctx: Context, sender: str, query: BudgetQuery):
    if query.total_spent > query.budget_limit:
        diff = query.total_spent - query.budget_limit
        message = f"⚠️ Budget exceeded by ₹{diff:.2f}"
    else:
        diff = query.budget_limit - query.total_spent
        message = f"✅ Within budget. ₹{diff:.2f} remaining"

    await ctx.send(sender, BudgetResponse(message=message))

budget_agent.include(budget_protocol)

if __name__ == "__main__":
    budget_agent.run()
