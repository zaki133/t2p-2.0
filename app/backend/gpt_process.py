import requests
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
                model="gpt-4o",
                max_tokens=4096
            )
            response_text = chat_completion.choices[0].message.content.strip()
            print("AI Response:", response_text)  # Debug print
            return response_text
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    #Edited by Felix Lange

    
            
            
    def conversion_pipeline(self, process_description):
        prompt_activities = f"""
            Considering the context of Business Process Management and process modelling and the following definitions:

            Activity:
            An activity is a unit of work that can be performed by an individual or a group. It is a specific step in the process.

            Consider the following process:
            The customer data is received by customer service and based on this data a customer data object is entered into the CRM system.
            After customer data has been entered it should then be compared with the internal customer data base and checked for completeness and plausibility.
            In case of any errors these should be corrected on the basis of a simple error list.
            The comparison of data is done to prevent individual customer data being stored multiple times.
            In case the customer does not exist in the customer data base, a new customer object is being created which will remain the data object of interest during the rest of the process flow.
            This object consists of data elements such as the customer's name and address and the assigned power gauge.
            The generated customer object is then used, in combination with other customer data to prepare the contract documents for the power supplier switch (including data such as bank connection, information on the selected rate, requested date of switch-over).
            In the following an automated check of the contract documents is carried out within the CIS (customer information system) in order to confirm their successful generation.
            In case of a negative response, i.e. the contract documents are not (or incorrectly) generated, the causing issues are being analyzed and resolved.
            Subsequently the contract documents are generated once again.
            In case of a positive response a confirmation document is sent out to the customer stating that the switch-over to the new supplier can be executed.
            A request to the grid operator is automatically sent out by the CIS.
            It puts the question whether the customer may be supplied by the selected supplier in the future.
            The switch-over request is checked by the grid operator for supplier concurrence, and the grid operator transmits a response comment.
            In the case of supplier concurrence the grid operator would inform all involved suppliers and demand the resolution of the conflict.
            The grid operator communicates with the old supplier and carries out the termination of the sales agreement between the customer and the old supplier (i.e. the customer service (of the new supplier) does not have to interact with the old supplier regarding termination).
            If there are not any objections by the grid operator (i.e. no supplier concurrence), customer service creates a CIS contract.
            The customer then has the chance to check the contract details and based on this check may decide to either withdraw from the switch contract or confirm it.
            Depending on the customer's acceptance/rejection the process flow at customer service either ends (in case of withdrawal) or continues (in case of a confirmation).
            An additional constraint is that the customer can only withdraw from the offered contract within 7 days after the 7th day the contract will be regarded as accepted and the process continues.
            The confirmation message by the customer is therefore not absolutely necessary (as it will count as accepted after 7 days in any way) but it can speed up the switch process.
            On the switch-date, but no later than 10 days after power supply has begun, the grid operator transmits the power meter data to the customer service and the old supplier via messages containing a services consumption report.
            At the same time, the grid operator computes the final billing based on the meter data and sends it to the old supplier.
            Likewise the old supplier creates and sends the final billing to the customer.

            Q:  lists the activities of the process
            A:
            - receive customer data
            - enter customer data object into the CRM system
            - compare customer data with the internal customer data base
            - check for completeness and plausibility
            - correct errors
            - create a new customer object
            - prepare the contract documents for the power supplier switch
            - check contract documents
            - analyse causing issues
            - resolve causing issues
            - generate contract documents
            - send out confirmation document
            - send out request
            - check switch-over request
            - transmit response comment
            - inform involved supplier
            - demand resolution of conflict
            - communicate with the old supplier
            - carry out the termination of the sales agreement
            - create CIS contract
            - check contract details
            - withdraw switch contract
            - confirm switch contract
            - transmit power meter data
            - compute final billing
            - send final billing
            - create final billing
            - send final billing

            Consider the following process:

            The SP/PU/GO request changes of the MPO or the MPO himself causes a change.
            The MPO reviews the change request.
            The MPO rejects the change of the measuring point by the SP/PU/GO or the MPO confirms the request of the SP/PU/GO.
            The MPO performs the measuring point change.
            The MPO reports the implementation to the SP/PU/GO or notifies the SP/PU/GO about the failure of the changes.


            Q:  lists the activities of the process
            A:
            - request change
            - cause change
            - review change request
            - reject the change of the measuring point by the SP/PU/GO
            - confirm the request of the SP/PU/GO
            - perform measuring point change
            - report implementation
            - notify about the failure of the change

            Consider the following process:
            
            {process_description} 
            Q:  lists the activities of the process
            A:"""

        gpt4_response_activities = self.call_api(prompt_activities, "")


        prompt_participants = f"""
            Considering the context of Business Process Management and process modelling and the following definitions:

            Process Participant:
            A process participant is any individual or entity that participates in a business process. This could include individuals who initiate the process, those who respond to it, or those who are affected by it.

            Activity:
            An activity is a unit of work that can be performed by an individual or a group. It is a specific step in the process.

            Consider the following process:

            A customer brings in a defective computer and the CRS checks the defect and hands out a repair cost calculation back.
            If the customer decides that the costs are acceptable, the process continues, otherwise she takes her computer home unrepaired.
            The ongoing repair consists of two activities, which are executed, in an arbitrary order.
            The first activity is to check and repair the hardware, whereas the second activity checks and configures the software.
            After each of these activities, the proper system functionality is tested.
            If an error is detected another arbitrary repair activity is executed, otherwise the repair is finished.


            Q: For each activity in this list, who is the participant performing it?
            - 'bring in a defective computer'
            - 'check the defect'
            - 'hand out a repair cost calculation'
            - 'take computer home unrepaired'
            - 'check and repair the hardware'
            - 'check and configure the software'
            - 'test the proper system functionality'
            - 'execute another arbitrary repair activity'

            A: 'bring in a defective computer' : 'The customer'
            'check the defect' : 'the CRS'
            'hand out a repair cost calculation' : 'the CRS'
            'take computer home unrepaired' : 'the customer'
            'check and repair the hardware' : 'the CRS'
            'check and configure the software' : 'the CRS'
            'test the proper system functionality' : 'the CRS'
            'execute another arbitrary repair activity' : 'the CRS'


            Consider the following process:

            The Evanstonian is an upscale independent hotel. When a guest calls room service at The Evanstonian, the room-service manager takes down the order. She then submits an order ticket to the kitchen to begin preparing the food. She also gives an order to the sommelier (i.e., the wine waiter) to fetch wine from the cellar and to prepare any other alcoholic beverages. Eighty percent of room-service orders include wine or some other alcoholic beverage. Finally, she assigns the order to the waiter. While the kitchen and the sommelier are doing their tasks, the waiter readies a cart (i.e., puts a tablecloth on the cart and gathers silverware). The waiter is also responsible for nonalcoholic drinks. Once the food, wine, and cart are ready, the waiter delivers it to the guest’s room. After returning to the room-service station, the waiter debits the guest’s account. The waiter may wait to do the billing if he has another order to prepare or deliver.

            Q: For each activity in this list, who is the participant performing it?
            - 'call room service'
            - 'take down order'
            - 'submit an order ticket'
            - 'begin preparing the food'
            - 'give an order'
            - 'fetch wine'
            - 'prepare alcoholic beverages'
            - 'assign order'
            - 'Ready a cart'
            - 'Deliver Food and wine'
            - 'return to the room-service station'
            - 'debit the guests account'
            - 'wait to do the billing'
            A:
            'call room service' : 'The guest'
            'take down order' : 'The room-service manager'
            'submit order ticket' : 'The room-service manager'
            'begin preparing the food' : 'the kitchen'
            'give an order' : 'the room-service manager'
            'fetch wine' : 'The sommelier'
            'prepare alcoholic beverages' : 'the sommelier'
            'assign oder' : 'the room-service manager'
            'Ready a cart' : 'the waiter'
            'Deliver Food and wine' : 'the waiter'
            'return to the room-service station' : 'the waiter'
            'debit the guests account' : 'the waiter'
            'wait to do the billing' : 'the waiter'


            Consider the following process:

            {process_description}

            Q: For each activity in this list, who is the participant performing it?

            {gpt4_response_activities}"""

        gpt4_response_participants = self.call_api(prompt_participants, "")




        prompt_gateways = f"""
            Considering the context of Business Process Management and process modelling and the following definitions:

            Activity:
            An activity is a unit of work that can be performed by an individual or a group. It is a specific step in the process.

            Process:
            A process is a sequence of activities completed to achieve an outcome.

            Flow:
            A flow object captures the execution flow among the process activities. It is a directional connector between activities in a Process. It defines the activities’ execution order.

            Gateway: A gateway (access) represents a decision point (split/fork), or a point at which different control flows converge (join/merge).


            Consider the following process:

            The Evanstonian is an upscale independent hotel. When a guest calls room service at The Evanstonian, the room-service manager takes down the order. She then submits an order ticket to the kitchen to begin preparing the food.
            She also gives an order to the sommelier (i.e., the wine waiter) to fetch wine from the cellar and to prepare any other alcoholic beverages. Eighty percent of room-service orders include wine or some other alcoholic beverage.
            Finally, she assigns the order to the waiter. While the kitchen and the sommelier are doing their tasks, the waiter readies a cart (i.e., puts a tablecloth on the cart and gathers silverware).
            The waiter is also responsible for nonalcoholic drinks. Once the food, wine, and cart are ready, the waiter delivers it to the guest’s room. After returning to the room-service station, the waiter debits the guest’s account.
            The waiter may wait to do the billing if he has another order to prepare or deliver.

            Q: Consider the extracted activities from the process description. Are there activities in this list, that are executed inside a gateway?
            - 'call room service'
            - 'take down order'
            - 'submit an order ticket'
            - 'prepare the food'
            - 'give an order'
            - 'fetch wine'
            - 'prepare alcoholic beverages'
            - 'assign order'
            - 'Ready a cart'
            - 'Deliver Food and wine'
            - 'return to the room-service station'
            - 'debit the guests account'
            - 'wait to do the billing'

            A: Inside a parallel AND Gateway:
            'fetch wine'
            'prepare alcoholic beverages'
            'prepare the food'
            'ready a cart'

            After AND Join:
            'Deliver Food and wine'

            Inside an exclusive XOR Gateway:
            'wait to do the billing' (conditional based on the presence of another order)


            Consider the following process:
            A customer brings in a defective computer and the CRS checks the defect and hands out a repair cost calculation back.
            If the customer decides that the costs are acceptable, the process continues, otherwise she takes her computer home unrepaired.
            The ongoing repair consists of two activities, which are executed, in an arbitrary order.
            The first activity is to check and repair the hardware, whereas the second activity checks and configures the software.
            After each of these activities, the proper system functionality is tested.
            If an error is detected another arbitrary repair activity is executed, otherwise the repair is finished.

            Q: Consider the extracted activities from the process description. Are there activities in this list, that are executed inside a gateway?

            - 'bring in a defective computer'
            - 'check the defect'
            - 'hand out a repair cost calculation'
            - 'take computer home unrepaired'
            - 'check and repair the hardware'
            - 'check and configure the software'
            - 'test the proper system functionality'
            - 'execute another arbitrary repair activity'

            A:   Inside a parallel AND Gateway:
            - 'check and repair the hardware'
            - 'check and configure the software'

                Inside an exclusive XOR Gateway:
            - 'take computer home unrepaired' (conditional based on accaptable Costs)
            - 'execute another arbitrary repair activity'


            Consider the following process:

            {process_description}


            Q: Consider the extracted activities from the process description. Are there activities in this list, that are executed inside a gateway?
            {gpt4_response_activities}"""

        gpt4_response_gateways = self.call_api(prompt_gateways, "")

        json_structure = """{
            'events': [
                {'id': 'startEvent1', 'type': 'Start', 'name': ''},
                {'id': 'endEvent1', 'type': 'End', 'name': ''}
            ],
            'tasks': [
                {'id': 'task1', 'type': 'UserTask', 'name': 'Check Outage'},
                {'id': 'task2', 'type': 'ServiceTask', 'name': 'Inform Customer'}
            ],
            'gateways': [
                {'id': 'gateway1', 'type': 'ExclusiveGateway', 'name': 'Split1'},
                {'id': 'gateway2', 'type': 'ParallelGateway', 'name': 'ParallelSplit1'}
            ],
            'flows': [
                {'id': 'flow1', 'type': 'SequenceFlow', 'source': 'startEvent1', 'target': 'task1'},
                {'id': 'flow2', 'type': 'SequenceFlow', 'source': 'task1', 'target': 'gateway1'},
                {'id': 'flow3', 'type': 'SequenceFlow', 'source': 'gateway1', 'target': 'task2'},
                {'id': 'flow4', 'type': 'SequenceFlow', 'source': 'task2', 'target': 'endEvent1'}
            ],
            }"""
                                                    
        prompt_all = f""" 
            You are an assistant for breaking down complex process descriptions into BPMN 2.0 elements. Your task is to provide a detailed and accurate breakdown of the business process in a structured format. 
            Ensure that the process flow is clearly delineated, and all decision points are systematically resolved as per BPMN standards.

            Details to include:

            Events:
            - Start Event: Describe the initial event that triggers the process.
            - End Event: Describe the final event that concludes the process.

            Tasks/Activities:
            - List all tasks and activities involved in the process along with a brief description of each.

            Gateways (Splitting/Joining Points):
            - Exclusive Gateways: Describe any points within the process where the flow can ONLY go in ONE direction, including the conditions that determine the direction the flow needs to take.
            - Parallel Gateways: Describe any points within the process where the flow MUST go in MULTIPLE directions.
            Note: Ensure each gateway opened in the process is correspondingly closed, exclusive splits must eventually meet in exclusive joins (with ending process within a direction of exclusive gateway being the only exception), and parallel splits must meet with parallel joins.

            Flows:
            - Sequence Flows: Detail all sequence flows, explaining how tasks and events are interconnected. Ensure accurate representation of the flow, maintaining the order of activities as described. Confirm that each element is connected with only two sequence flows, except for end events and start events, these have only one sequence flow. Flows aren't allowed to be bi-directional, so there has to be a check exclusive gateway if a recurring activity is needed to be done.

            Create a structured JSON output that conforms to the following schema suitable for BPMN XML conversion. Please format the output as JSON with the following keys: 'events', 'tasks', 'gateways', and 'flows'. Only return the JSON text, avoid markdown formatting or formatting of any kind. Each key should contain a list of elements, each with properties that define their roles in the BPMN diagram. For example, tasks should include 'id', 'name', and 'type'; flows should include 'source', 'target', and 'type'; and events should include 'id', 'type', and 'name'. Regard opening gateways as SPLITS and closing gateways as JOINS. Expected JSON structure example (only generate the relevant content, not all elements need to be used):

            {json_structure}


            Here is the process description again, for clarification: 
            A small company manufactures customized bicycles. Whenever the sales department receives an order, a new process instance is created.
            A member of the sales department can then reject or accept the order for a customized bike. In the former case, the process instance is finished.
            In the latter case, the storehouse and the engineering department are informed. The storehouse immediately processes the part list of the order and checks the required quantity of each part.
            If the part is available in-house, it is reserved. If it is not available, it is back-ordered. This procedure is repeated for each item on the part list. In the meantime, the engineering department prepares everything for the assembling of the ordered bicycle.
            If the storehouse has successfully reserved or back-ordered every item of the part list and the preparation activity has finished, the engineering department assembles the bicycle.
            Afterwards, the sales department ships the bicycle to the customer and finishes the process instance.

            You have already extracted the activities:

            {gpt4_response_activities}

            The Actors responsible for performing the activities:

            {gpt4_response_participants}

            and the gateways in the process description:

            {gpt4_response_gateways}

            """


        gpt4_response_final = self.call_api(prompt_all, "")
        
        xml_data = json_to_bpmn(json.loads(gpt4_response_final))

        return xml_data


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

