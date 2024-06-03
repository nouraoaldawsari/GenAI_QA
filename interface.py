import gradio as gr
from vector_database import VectorDatabase  # hypothetical module for vector database operations
from llm_interface import LLMInterface  # hypothetical module for interacting with LLMs

# Initialize the vector database
vector_db = VectorDatabase()

# Initialize the LLM interface
llm_interface = LLMInterface(models=["gpt-3.5-turbo", "gpt-4", "Llama-2-70b-chat", "Falcon-40b-instruct"])

def evaluate_models(prompt):
    # Query the vector database with the user's prompt
    search_results = vector_db.query(prompt)
    
    # Generate a new prompt that includes the search results and the original user prompt
    new_prompt = f"{prompt}\n\nSearch Results:\n{search_results}"
    
    # Query each LLM with the new prompt
    responses = llm_interface.query_all(new_prompt)
    
    # Return the responses from each LLM
    return responses

# Create the Gradio interface
iface = gr.Interface(
    fn=evaluate_models,
    inputs=gr.inputs.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs=gr.outputs.Textbox(),
)

# Launch the app
iface.launch()
