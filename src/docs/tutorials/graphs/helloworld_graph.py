from typing import Dict, TypedDict
from langgraph.graph import StateGraph # framework that helps you design and manage the flow of tasks in your application using a graph structure

# We now create an AgentState - shared data structure that keeps track of information as your application runs. 
class AgentState(TypedDict): # Our state schema
    message : str 


def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a greeting message to the state""" # This is a docstring - it describes what the node does and is also used for llm to understand the node
    state['message'] = "Hey " + state["message"] + ", how is your day going?"
    return state 

graph = StateGraph(AgentState)
graph.add_node("greeter", greeting_node)
graph.set_entry_point("greeter") # set the entry point of the graph
graph.set_finish_point("greeter") # set the finish point of the graph
app = graph.compile() # compile the graph into a callable application

result = app.invoke({"message": "Bob"}) # invoke the graph with the initial state
print(result["message"]) # print the result

#Output: Hey Bob, how is your day going?






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

