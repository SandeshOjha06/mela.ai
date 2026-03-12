"""
LangGraph Graph Compilation — assembles the Swarm execution graph.

Builds a StateGraph with the Supervisor as the hub and 6 worker agents
as spokes. Uses conditional edges for dynamic routing based on the
Supervisor's decision.
"""

from langgraph.graph import END, StateGraph

from app.swarm.agents import (
    budget_finance_agent,
    email_agent,
    emergency_info_agent,
    marketing_agent,
    problem_solver_agent,
    scheduler_agent,
)
from app.swarm.state import EventState
from app.swarm.supervisor import (
    BUDGET_FINANCE,
    EMAIL,
    EMERGENCY_INFO,
    MARKETING,
    PROBLEM_SOLVER,
    SCHEDULER,
    route_from_supervisor,
    supervisor_node,
)

# Node name constant for the supervisor
SUPERVISOR = "supervisor"


def build_swarm_graph() -> StateGraph:
    """
    Construct and compile the LangGraph StateGraph for the Event
    Command Center Swarm.

    The graph follows a Star Topology:
      - Entry → Supervisor
      - Supervisor → (conditional) → Worker Agent
      - Worker Agent → Supervisor (loop back)
      - Supervisor → END (when pipeline is complete)

    Returns:
        A compiled LangGraph StateGraph ready for invocation.
    """
    graph = StateGraph(EventState)

    # --- Add Nodes ---
    graph.add_node(SUPERVISOR, supervisor_node)
    graph.add_node(PROBLEM_SOLVER, problem_solver_agent)
    graph.add_node(MARKETING, marketing_agent)
    graph.add_node(SCHEDULER, scheduler_agent)
    graph.add_node(EMAIL, email_agent)
    graph.add_node(EMERGENCY_INFO, emergency_info_agent)
    graph.add_node(BUDGET_FINANCE, budget_finance_agent)

    # --- Set Entry Point ---
    graph.set_entry_point(SUPERVISOR)

    # --- Conditional Edges from Supervisor ---
    # The Supervisor decides the next node; route_from_supervisor
    # reads state["next_agent"] and returns the node name.
    graph.add_conditional_edges(
        SUPERVISOR,
        route_from_supervisor,
        {
            PROBLEM_SOLVER: PROBLEM_SOLVER,
            MARKETING: MARKETING,
            SCHEDULER: SCHEDULER,
            EMAIL: EMAIL,
            EMERGENCY_INFO: EMERGENCY_INFO,
            BUDGET_FINANCE: BUDGET_FINANCE,
            "end": END,
        },
    )

    # --- Worker Agents → back to Supervisor ---
    # After each worker completes, control returns to the Supervisor
    # for the next routing decision.
    graph.add_edge(PROBLEM_SOLVER, SUPERVISOR)
    graph.add_edge(MARKETING, SUPERVISOR)
    graph.add_edge(SCHEDULER, SUPERVISOR)
    graph.add_edge(EMAIL, SUPERVISOR)
    graph.add_edge(EMERGENCY_INFO, SUPERVISOR)
    graph.add_edge(BUDGET_FINANCE, SUPERVISOR)

    # --- Compile ---
    compiled_graph = graph.compile()
    return compiled_graph


# Pre-compiled singleton graph instance
swarm_graph = build_swarm_graph()
