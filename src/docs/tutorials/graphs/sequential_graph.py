from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: str
    final: str

def first_node(state:AgentState) -> AgentState:
    """This is the first node of our sequence"""
    state["final"] = f"Hi {state['name']}!"
    return state

def second_node(state:AgentState) -> AgentState:
    """This is the second node of our sequence"""
    state["final"] = state["final"] + f" You are {state['age']} years old!"
    return state

graph = StateGraph(AgentState)

graph.add_node("first_node", first_node) # add the first node to the graph
graph.add_node("second_node", second_node) # add the second node to the graph

graph.set_entry_point("first_node") # set the entry point of the graph
graph.add_edge("first_node", "second_node") # add an edge between the first and second node
graph.set_finish_point("second_node") # set the finish point of the graph
app = graph.compile() # compile the graph into a callable application

result = app.invoke({"name": "Charlie", "age": 20}) # invoke the graph with the initial state
print(result)
# Output: {'name': 'Charlie', 'age': '20', 'final': 'Hi Charlie! You are 20 years old!'}



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