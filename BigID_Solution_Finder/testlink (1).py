import gradio as gr
import requests
import re
import urllib.parse
import json

API_TOKEN = "YXZvZGFsYUBiaWdpZC5jb206QVRBVFQzeEZmR0YwMW9JbV9NbmdxZEJuNnJndlFheEJ3TTBUS0t3WF9KVDFpZlJJeWk4c3BNRVhyUmR0YUVVWDBrZVNMOHg2d0c4S3E3WnVEUDVaRnJRdHF4OHc1WXU2Q2sxLVc3S2p2d1IzTzg1RDdvWjJ3Rm1oZWh4UXFrSkdLbXFlczZyMG9jQmRLS3hZQjY3ckZGWGdlWFEyXzdoQ2FocUpndHMzWDVLZFpmLVJqd1gzVHBnPUM5QjE4QUYx"

def clean_text(text):
    """Removes special characters and unnecessary symbols."""
    if not text:
        return "No excerpt available."
    text = re.sub(r'@@@.*?@@@', '', text)  # Remove highlight markers
    text = re.sub(r'[\n\r]+', ' ', text)  # Remove excessive new lines
    text = re.sub(r'&amp;', '&', text)  # Replace &amp; with &
    return text.strip()

def get_data_from_local_db(user_input=""):
    url = "http://localhost:8000/api/items"
    #url = "http://localhost:8000/api/items?que_description={user_input}"

    payload = {}
    headers = {}

    response = requests.get(url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()


    print(data)
    for item in data:
        que_exp_ans = item.get("que_exp_ans")
        print(f"que_exp_ans: {que_exp_ans}")
     
    return que_exp_ans


def call_confluence_api(user_input, history):
    """Fetches search results and appends a Markdown link for feedback switching."""
    url = f'https://bigidio.atlassian.net/wiki/rest/api/search?cql=text~"{user_input}"&limit=5'
    
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'X-APOLLO-OPERATION-NAME': 'ConfluenceQuickSearchQuery',
        'Authorization': f"Basic {API_TOKEN}"
    }

    excerpts = []
    db_response = get_data_from_local_db()

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        if "results" in data and data["results"]:
            formatted_responses=[]
            for result in data["results"]:
                title_raw = result.get("title", "Untitled Page")  
                excerpt_raw = result.get("excerpt", "No excerpt available")  
                page_url_raw = result.get("url", "")

                if page_url_raw.startswith("http"):
                    page_url = page_url_raw
                else:
                    page_url = f"https://bigidio.atlassian.net/wiki{urllib.parse.unquote_plus(page_url_raw)}"

                title = clean_text(title_raw)
                excerpt = clean_text(excerpt_raw)
                excerpts.append(excerpt)
                
                link = f'<a href="{page_url}" target="_blank" style="color: blue; font-weight: bold; text-decoration: underline;">{title}</a>' if page_url else f"{title}"
                formatted_responses.append(f"{link}  \n{excerpt}")
            
            formatted_output = "\n\n".join(formatted_responses)
            excerpts_output = "\n\n".join(excerpts)
            with open("/Users/hkarri/python_local/BigID_Solution_Finder/output.txt", "w") as file:
                file.write(excerpts_output)
        else:
            formatted_output = "❌ No results found."
    else:
        formatted_output = f"⚠️ Error: Request failed with status code {response.status_code}"

    db_message = "Our recommended result"
    search_res = "Here are the top 5 search results:"
    message = "If any of the search results worked for you, please provide your problem and the solution that worked for you."
    return f"{db_message}\n\n{db_response}\n\n{search_res}\n\n{formatted_output}\n\n{message}"

def submit_feedback(problem, solution):
    """Handles feedback submission and sends it to the API."""
    api_url = "http://localhost:8000/api/items/"
    payload = json.dumps({
        "category_name": "Connectors2",  # This can be adjusted as needed
        "que_description": problem,
        "que_exp_ans": solution,
        "exp_ans": 1
    })
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(api_url, headers=headers, data=payload)
    
    if response.status_code == 201:
        return f"✅ Thank you for your feedback!\n\nProblem: {problem}\nSolution: {solution}"
    else:
        return f"⚠️ Error submitting feedback. Please try again. ({response.status_code})"

def switch_to_feedback():
    """Updates the radio button to 'Feedback' when the user clicks Provide Feedback."""
    return gr.update(value="Feedback")

with gr.Blocks() as interface:
    choice = gr.Radio(["Search", "Feedback"], label="Select an Option", value="Search")
    chatbot_container = gr.Group(visible=True)
    feedback_container = gr.Group(visible=False)

    # Chatbot Interface
    with chatbot_container:
        chatbot = gr.ChatInterface(fn=call_confluence_api, title="🔍 Bigid Solution Finder")

        # Feedback Button
        feedback_button = gr.Button("📩 Feedback", visible=True)
        feedback_button.click(switch_to_feedback, inputs=[], outputs=[choice])

    # Feedback Interface
    with feedback_container:
        gr.Markdown(
            """<h2 style='text-align: center;'>📢 Feedback Form</h2>
            <p style='text-align: center;'>Tell us about your issue and how it was solved! Your feedback helps us improve.</p>"""
        )
        solution_choices = []
        try:
            #/Users/hkarri/python_local/BigID_Solution_Finder/testlink.py
            with open("/Users/hkarri/python_local/BigID_Solution_Finder/output.txt", "r") as file:
                content = file.read()  # Read the entire content of the file
                print("File content read successfully:")
                print(content)
                solution_choices = content.split("\n\n")
                print(solution_choices)
                print(len(solution_choices))
        except FileNotFoundError:
            print("The file 'output.txt' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        problem_input = gr.Textbox(label="🛠 Problem", placeholder="Describe the issue in detail...", lines=3)
        solution_input = gr.Dropdown(choices=solution_choices, label= "solution",value="", allow_custom_value=True)
        
        submit_button = gr.Button("🚀 Submit Feedback", variant="primary")
        output_text = gr.Text(label="Submission Status", interactive=False, visible=False)

        def handle_submit(problem, solution):
            response = submit_feedback(problem, solution)
            return gr.update(value=response, visible=True)

        submit_button.click(
            handle_submit, 
            inputs=[problem_input, solution_input], 
            outputs=[output_text]
        )

    # Handle switching between Chatbot and Feedback interface
    choice.change(
        lambda x: (gr.update(visible=x == "Search"), gr.update(visible=x == "Feedback")), 
        inputs=[choice], 
        outputs=[chatbot_container, feedback_container]
    )

# Launch the interface
interface.launch()
