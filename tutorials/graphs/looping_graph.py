from langgraph.graph import StateGraph, END
import random
from typing import Dict, List, TypedDict

class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int

def greeting_node(state: AgentState) -> AgentState:
    """Greeting Node which says hi to the person"""
    state["name"] = f"Hi there, {state['name']}"
    state["counter"] = 0 

    return state

def random_node(state: AgentState) -> AgentState:
    """Generates a random number from 0 to 10"""
    state["number"].append(random.randint(0, 10))
    state["counter"] += 1

    return state


def should_continue(state: AgentState) -> AgentState:
    """Function to decide what to do next"""
    if state["counter"] < 5:
        print("ENTERING LOOP", state["counter"])
        return "loop"  # Continue looping
    else:
        return "exit"  # Exit the loop

# greeting → random → random → random → random → random → END

graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge("greeting", "random")


graph.add_conditional_edges(
    "random",     # Source node
    should_continue, # Action
    {
        "loop": "random",  
        "exit": END          
    }
)

graph.set_entry_point("greeting")

app = graph.compile()

result = app.invoke({"name":"Vaibhav", "number":[], "counter":-100})
print(result)

# Output: {'name': 'Hi there, Vaibhav', 'number': [10, 10, 10, 10, 10], 'counter': 5}


# Get the PNG data
png_data = app.get_graph().draw_mermaid_png()
# Save the graph image to current directory
import os
# Get the current filename without extension
current_filename = os.path.splitext(os.path.basename(__file__))[0]
image_filename = f"{current_filename}.png"
# Save the PNG data to file
with open(image_filename, 'wb') as f:
    f.write(png_data)
print(f"Graph image saved as: {image_filename}")