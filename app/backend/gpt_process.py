import openai
import json
import requests
import json
from xml_parser import json_to_bpmn

class ApiCaller:
    def __init__(self, api_key):
        self.api_key = api_key
        self.flask_app_url = "someurlIDK/call_openai" #!!!!!!!!!!!!!!!SET THIS WHEN DEPLOYED!!!!!!!!!!!!!!

    def call_api(self, system_prompt, user_text):
        # Construct the data payload to send to the Flask API
        data_payload = {
            "api_key": self.api_key,
            "system_prompt": system_prompt,
            "user_text": user_text
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            # Make a POST request to the other API
            response = requests.post(self.flask_api_url, headers=headers, json=data_payload)
            if response.status_code == 200:
                # Process the response from your Flask API
                response_data = response.json()
                return response_data['message']  
            else:
                return f"An error occurred: {response.text}"
            
        except Exception as e:
            return f"An exception occurred: {str(e)}"
            
    def conversion_pipeline(self, process_description):
        
        try:
            json_data = self.generate_bpmn_json(process_description)
            xml_data = json_to_bpmn(json.loads(json_data))
            return xml_data
        except Exception as e:
            return f"An error occurred: {str(e)}"
        
    # @staticmethod
    # def generate_first_prompt():
    #     # Construct the prompt to ask for detailed business process elements with explicit formatting
    #     prompt = (
    #             """You are an assistant for breaking down complex process descriptions into BPMN 2.0 elements. Your task is to provide a detailed and accurate breakdown of the business process in a structured format. Ensure that the process flow is clearly delineated, and all decision points are systematically resolved as per BPMN standards.

    #             Details to include, only if present in the process description (ommiting elements if fine):

    #             Events:
    #             - Start Event: Describe the initial event that triggers the process.
    #             - End Event: Describe the final event that concludes the process.

    #             Tasks/Activities:
    #             - List all tasks and activities involved in the process along with a brief description of each.

    #             Gateways (Decision Points):
    #             - Opening Gateways: Describe any decision points within the process, including the conditions that guide the decisions.
    #             - Closing Gateways: Ensure each gateway opened in the process is correspondingly closed. Provide details on how each decision point is resolved, maintaining the logical flow of the process.

    #             Flows:
    #             - Sequence Flows: Detail all sequence flows, explaining how tasks and events are interconnected. Ensure accurate representation of the flow, maintaining the order of activities as described. Confirm that each element is connected with at EXACTLY two sequence flows, apart from start-events, end-events and gateways.  

    #             Ensure that the information is comprehensive and precisely corresponds to the elements required for a BPMN 2.0 diagram. Your output should form a complete, executable BPMN diagram that accurately reflects the described process."""
    #     )
    #     original_prompt = """
    #             You are an assistant for breaking down complex process descriptions into BPMN 2.0 elements. Your task is to provide a detailed and accurate breakdown of the business process in a structured format. Ensure that the process flow is clearly delineated, and all decision points are systematically resolved as per BPMN standards.

    #             Details to include:

    #             Events:
    #             - Start Event: Describe the initial event that triggers the process.
    #             - Intermediate Events: List any intermediate events that occur during the process.
    #             - End Event: Describe the final event that concludes the process.

    #             Tasks/Activities:
    #             - List all tasks and activities involved in the process along with a brief description of each.

    #             Gateways (Decision Points):
    #             - Opening Gateways: Describe any decision points within the process, including the conditions that guide the decisions.
    #             - Closing Gateways: Ensure each gateway opened in the process is correspondingly closed. Provide details on how each decision point is resolved, maintaining the logical flow of the process.

    #             Flows:
    #             - Sequence Flows: Detail all sequence flows, explaining how tasks and events are interconnected. Ensure accurate representation of the flow, maintaining the order of activities as described. Confirm that each element is connected with at least one sequence flow, paying special attention to intermediate events.
    #             - Message Flows: Detail all message flows between participants.

    #             Participants (Pools, Lanes):
    #             - Identify all participants involved in the process, and specify their roles within pools and lanes.

    #             Ensure that the information is comprehensive and precisely corresponds to the elements required for a BPMN 2.0 diagram. Your output should form a complete, executable BPMN diagram that accurately reflects the described process."""
        
    #     return prompt
    


    def generate_bpmn_json(self, user_description):
        # Generate a prompt to transform detailed summary into JSON structure suitable for BPMN XML conversion
        system_prompt = (
            """You are an assistant for breaking down complex process descriptions into BPMN 2.0 elements. Your task is to provide a detailed and accurate breakdown of the business process in a structured format. Ensure that the process flow is clearly delineated, and all decision points are systematically resolved as per BPMN standards.

                Details to include:

                Events:
                - Start Event: Describe the initial event that triggers the process.
                - End Event: Describe the final event that concludes the process.

                Tasks/Activities:
                - List all tasks and activities involved in the process along with a brief description of each.

                Gateways (Splitting/Joining Points):
                - Exclusive Gateways: Describe any points within the process where the flow can ONLY go in ONE direction, including the conditions that determine the direction the flow needs to take.
                - Parallel Gateways: Describe any points within the process where the flow MUST go in MULTIPLE directions.
                Note: Ensure each gateway opened in the process is correspondingly closed, exclusive splits must eventually meet in exclusive joins (with ending process within a direction of exclusive gateway being the only exception), and parallel splits must meet with parralel joins.

                Flows:
                - Sequence Flows: Detail all sequence flows, explaining how tasks and events are interconnected. Ensure accurate representation of the flow, maintaining the order of activities as described. Confirm that each element is connected with only two sequence flows, except for end events and start events, these have only one sequence flow. Flows arent allowed to bi-directional, so there has to be a check exclusive gateway if a recurring activity is needed to be done"""

            "Create a structured JSON output that conforms to the following schema suitable for BPMN XML conversion. Please format the output "
            "as JSON with the following keys: 'events', 'tasks', 'gateways', and 'flows'. "
            "Only return the JSON text, avoid markdown formatting or formatting of any king. Each "
            "key should contain a list of elements, each with properties that define their roles in the BPMN diagram. "
            "For example, tasks should include 'id', 'name', and 'type'; flows should include 'source', 'target', and 'type'; "
            "and events should include 'id', 'type', and 'name'. Regard opening gateways as SPLITS and closing gateways as JOINS."
            "Expected JSON structure example (only generate the relevant content, not all elements need to be used):\n\n"
            "{\n"
            "  'events': [\n"
            "    {'id': 'startEvent1', 'type': 'Start', 'name': ''},\n"
            "    {'id': 'endEvent1', 'type': 'End', 'name': ''}\n"
            "  ],\n"
            "  'tasks': [\n"
            "    {'id': 'task1', 'type': 'UserTask', 'name': 'Check Outage'},\n"
            "    {'id': 'task2', 'type': 'ServiceTask'}, 'name': 'Inform Customer'\n"
            "  ],\n"
            "  'gateways': [\n"
            "    {'id': 'gateway1', 'type': 'ExclusiveGateway', 'name': 'Split1'}\n"
            "    {'id': 'gateway2', 'type': 'ParallelGateway', 'name': 'ParallelSplit1'}"
            "  ],\n"
            "  'flows': [\n"
            "    {'id': 'flow1', 'type': 'SequenceFlow','source': 'startEvent1', 'target': 'task1'},\n"
            "    {'id': 'flow2', 'type': 'SequenceFlow','source': 'task1', 'target': 'gateway1'},\n"
            "    {'id': 'flow3', 'type': 'SequenceFlow','source': 'gateway1', 'target': 'task2'},\n"
            "    {'id': 'flow4', 'type': 'SequenceFlow','source': 'task2', 'target': 'endEvent1'}\n"
            "  ],\n"
            "}\n"
            f"Here is the process description again, for clarification: {user_description}"
        )
        # Call the 'run' method with the generated prompt and return the result
        json_output = self.call_api(system_prompt=system_prompt, user_text="")
        return json_output

