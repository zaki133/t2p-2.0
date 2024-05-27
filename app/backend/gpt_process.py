import openai
import json
from xml_parser import json_to_bpmn

class ApiCaller:
    def __init__(self, api_key):
        # Initialize the OpenAI client with the provided API key
        self.client = openai.OpenAI(api_key=api_key)

    def call_api(self, system_prompt, user_text):
        try:
            # Ensure the system prompt is set and then followed by the user's specific input
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ],
                temperature=0,
                model="gpt-4-turbo",
                max_tokens=4096
            )
            response_text = chat_completion.choices[0].message.content.strip()
            print("AI Response:", response_text)  # Debug print
            return response_text
        except Exception as e:
            return f"An error occurred: {str(e)}"
#
    def conversion_pipeline(self, process_description):

        prompt = self.generate_first_prompt()
        
        response_text = self.call_api(prompt, user_text= process_description)
        print("hello")
        json_data = self.generate_bpmn_json(response_text)
        json_to_bpmn(json.loads(json_data))

        return json_data


    @staticmethod
    def generate_first_prompt():
        # Construct the prompt to ask for detailed business process elements with explicit formatting
        prompt = (
                """You are an assistant for breaking down complex process descriptions into BPMN 2.0 elements. Your task is to provide a detailed and accurate breakdown of the business process in a structured format. Ensure that the process flow is clearly delineated, and all decision points are systematically resolved as per BPMN standards.

                Details to include:

                Events:
                - Start Event: Describe the initial event that triggers the process.
                - Intermediate Events: List any intermediate events that occur during the process.
                - End Event: Describe the final event that concludes the process.

                Tasks/Activities:
                - List all tasks and activities involved in the process along with a brief description of each.

                Gateways (Decision Points):
                - Opening Gateways: Describe any decision points within the process, including the conditions that guide the decisions.
                - Closing Gateways: Ensure each gateway opened in the process is correspondingly closed. Provide details on how each decision point is resolved, maintaining the logical flow of the process.

                Flows:
                - Sequence Flows: Detail all sequence flows, explaining how tasks and events are interconnected. Ensure accurate representation of the flow, maintaining the order of activities as described. Confirm that each element is connected with at least one sequence flow, paying special attention to intermediate events.
                - Message Flows: Detail all message flows between participants.

                Participants (Pools, Lanes):
                - Identify all participants involved in the process, and specify their roles within pools and lanes.

                Ensure that the information is comprehensive and precisely corresponds to the elements required for a BPMN 2.0 diagram. Your output should form a complete, executable BPMN diagram that accurately reflects the described process."""
        )
        return prompt
    


    def generate_bpmn_json(self, detailed_summary):
        # Generate a prompt to transform detailed summary into JSON structure suitable for BPMN XML conversion
        system_prompt = (
            "Based on the following detailed summary of a business process, create a structured JSON output "
            "that conforms to the following schema suitable for BPMN XML conversion. Please format the output "
            "as JSON with the following keys: 'events', 'tasks', 'gateways', 'flows', and 'participants'. Only return the JSON text, avoid markdown formatting or formatting of any king. Each "
            "key should contain a list of elements, each with properties that define their roles in the BPMN diagram. "
            "For example, tasks should include 'id', 'name', and 'type'; flows should include 'source', 'target', and 'type'; "
            "and events should include 'id', 'type', and 'name'. Regard opening gateways as SPLITS and closing gateways as JOINS."
            "Expected JSON structure example (please generate content accordingly):\n\n"
            "{\n"
            "  'events': [\n"
            "    {'id': 'startEvent1', 'type': 'Start', 'name': 'Process Start'},\n"
            "    {'id': 'endEvent1', 'type': 'End', 'name': 'Process End'}\n"
            "  ],\n"
            "  'tasks': [\n"
            "    {'id': 'task1', 'name': 'Check Outage', 'type': 'UserTask'},\n"
            "    {'id': 'task2', 'name': 'Inform Customer', 'type': 'ServiceTask'}\n"
            "  ],\n"
            "  'gateways': [\n"
            "    {'id': 'gateway1', 'name': 'Outage Decision', 'type': 'ExclusiveGateway'}\n"
            "  ],\n"
            "  'flows': [\n"
            "    {'id': 'flow1','source': 'startEvent1', 'target': 'task1', 'type': 'SequenceFlow'},\n"
            "    {'id': 'flow2','source': 'task1', 'target': 'gateway1', 'type': 'SequenceFlow'},\n"
            "    {'id': 'flow3','source': 'gateway1', 'target': 'task2', 'type': 'SequenceFlow'},\n"
            "    {'id': 'flow4','source': 'task2', 'target': 'endEvent1', 'type': 'SequenceFlow'}\n"
            "  ],\n"
            "  'participants': [\n"
            "    {'id': 'lane1', 'name': 'Customer Service', 'type': 'Lane'}\n"
            "  ]\n"
            "}\n"
        )
        # Call the 'run' method with the generated prompt and return the result
        json_output = self.call_api(system_prompt=system_prompt, user_text=detailed_summary)
        return json_output

