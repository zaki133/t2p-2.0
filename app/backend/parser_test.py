import json
from xml_parser import json_to_bpmn

# data = {
#   "events": [
#     {"id": "startEvent1", "type": "Start", "name": "Customer Contacts Support"},
#     {"id": "intermediateEvent1", "type": "Intermediate", "name": "Outage Detected"},
#     {"id": "intermediateEvent2", "type": "Intermediate", "name": "Outage Not Detected"},
#     {"id": "intermediateEvent3", "type": "Intermediate", "name": "Notification Sent"},
#     {"id": "intermediateEvent4", "type": "Intermediate", "name": "Update Provided"},
#     {"id": "endEvent1", "type": "End", "name": "Issue Resolved or Technician Scheduled"}
#   ],
#   "tasks": [
#     {"id": "task1", "name": "Submit Issue Form", "type": "UserTask"},
#     {"id": "task2", "name": "Check for Existing Outage", "type": "ServiceTask"},
#     {"id": "task3", "name": "Inform Customer of Outage", "type": "ServiceTask"},
#     {"id": "task4", "name": "Route Ticket to Specialist", "type": "UserTask"},
#     {"id": "task5", "name": "Evaluate Situation", "type": "UserTask"},
#     {"id": "task6", "name": "Decide on Field Technician Dispatch", "type": "UserTask"},
#     {"id": "task7", "name": "Schedule Field Technician", "type": "UserTask"},
#     {"id": "task8", "name": "Provide Customer Updates", "type": "ServiceTask"}
#   ],
#   "gateways": [
#     {"id": "gateway1", "name": "Outage Check Gateway", "type": "ExclusiveGateway"},
#     {"id": "gateway2", "name": "Field Technician Dispatch Decision", "type": "ExclusiveGateway"}
#   ],
#   "flows": [
#     {"id": "flow1", "source": "startEvent1", "target": "task1", "type": "SequenceFlow"},
#     {"id": "flow2", "source": "task1", "target": "task2", "type": "SequenceFlow"},
#     {"id": "flow3", "source": "task2", "target": "gateway1", "type": "SequenceFlow"},
#     {"id": "flow4", "source": "gateway1", "target": "task3", "type": "SequenceFlow", "condition": "Outage Detected"},
#     {"id": "flow5", "source": "gateway1", "target": "task4", "type": "SequenceFlow", "condition": "Outage Not Detected"},
#     {"id": "flow6", "source": "task3", "target": "intermediateEvent3", "type": "SequenceFlow"},
#     {"id": "flow7", "source": "intermediateEvent3", "target": "endEvent1", "type": "SequenceFlow"},
#     {"id": "flow8", "source": "task4", "target": "task5", "type": "SequenceFlow"},
#     {"id": "flow9", "source": "task5", "target": "gateway2", "type": "SequenceFlow"},
#     {"id": "flow10", "source": "gateway2", "target": "task7", "type": "SequenceFlow", "condition": "Critical"},
#     {"id": "flow11", "source": "gateway2", "target": "task7", "type": "SequenceFlow", "condition": "Non-Critical"},
#     {"id": "flow12", "source": "task7", "target": "task8", "type": "SequenceFlow"},
#     {"id": "flow13", "source": "task8", "target": "intermediateEvent4", "type": "SequenceFlow"},
#     {"id": "flow14", "source": "intermediateEvent4", "target": "endEvent1", "type": "SequenceFlow"}
#   ],
#   "participants": [
#     {"id": "pool1", "name": "Customer", "type": "Pool"},
#     {"id": "pool2", "name": "Telecommunications Company", "type": "Pool"},
#     {"id": "lane1", "name": "Support System", "type": "Lane"},
#     {"id": "lane2", "name": "Technical Support Specialist", "type": "Lane"},
#     {"id": "lane3", "name": "Field Technician", "type": "Lane"}
#   ]
# }

# data = {
#   "events": [
#     {"id": "startEvent1", "type": "Start", "name": "Customer Reports Service Disruption"},
#     {"id": "intermediateEvent1", "type": "Intermediate", "name": "Notification of Known Outage"},
#     {"id": "intermediateEvent2", "type": "Intermediate", "name": "Regular Updates"},
#     {"id": "endEvent1", "type": "End", "name": "Issue Resolved"}
#   ],
#   "tasks": [
#     {"id": "task1", "name": "Report Service Disruption", "type": "UserTask"},
#     {"id": "task2", "name": "Check for Known Outages", "type": "ServiceTask"},
#     {"id": "task3", "name": "Notify Customer of Outage", "type": "ServiceTask"},
#     {"id": "task4", "name": "Assess the Situation", "type": "UserTask"},
#     {"id": "task5", "name": "Schedule Field Technician", "type": "UserTask"},
#     {"id": "task6", "name": "Send Regular Updates", "type": "ServiceTask"}
#   ],
#   "gateways": [
#     {"id": "gateway1", "name": "Known Outage Check", "type": "ExclusiveGateway"},
#     {"id": "gateway2", "name": "Field Technician Required", "type": "ExclusiveGateway"}
#   ],
#   "flows": [
#     {"id": "flow1", "source": "startEvent1", "target": "task1", "type": "SequenceFlow"},
#     {"id": "flow2", "source": "task1", "target": "task2", "type": "SequenceFlow"},
#     {"id": "flow3", "source": "task2", "target": "gateway1", "type": "SequenceFlow"},
#     {"id": "flow4", "source": "gateway1", "target": "task3", "type": "SequenceFlow", "condition": "Known Outage Yes"},
#     {"id": "flow5", "source": "gateway1", "target": "task4", "type": "SequenceFlow", "condition": "Known Outage No"},
#     {"id": "flow6", "source": "task4", "target": "gateway2", "type": "SequenceFlow"},
#     {"id": "flow7", "source": "gateway2", "target": "task5", "type": "SequenceFlow", "condition": "Technician Required Yes"},
#     {"id": "flow8", "source": "gateway2", "target": "task6", "type": "SequenceFlow", "condition": "Technician Required No"},
#     {"id": "flow9", "source": "task3", "target": "task6", "type": "SequenceFlow"},
#     {"id": "flow10", "source": "task5", "target": "task6", "type": "SequenceFlow"},
#     {"id": "flow11", "source": "task6", "target": "endEvent1", "type": "SequenceFlow"}
#   ],
#   "participants": [
#     {"id": "participant1", "name": "Customer", "type": "Lane"},
#     {"id": "participant2", "name": "Automated System", "type": "Lane"},
#     {"id": "participant3", "name": "Support Specialist", "type": "Lane"},
#     {"id": "participant4", "name": "Field Technician Scheduler", "type": "Lane"}
#   ]
# }

# data = {
#   "events": [
#     {"id": "startEvent1", "type": "Start", "name": "Customer Reports Service Disruption"},
#     {"id": "intermediateEvent1", "type": "Intermediate", "name": "Notification of Known Outage"},
#     {"id": "intermediateEvent2", "type": "Intermediate", "name": "Regular Updates"},
#     {"id": "endEvent1", "type": "End", "name": "Issue Resolved"}
#   ],
#   "tasks": [
#     {"id": "task1", "name": "Report Service Disruption", "type": "UserTask"},
#     {"id": "task2", "name": "Check for Known Outages", "type": "ServiceTask"},
#     {"id": "task3", "name": "Notify Customer of Outage", "type": "ServiceTask"},
#     {"id": "task4", "name": "Assess Situation", "type": "UserTask"},
#     {"id": "task5", "name": "Schedule Field Technician", "type": "UserTask"},
#     {"id": "task6", "name": "Send Regular Updates", "type": "UserTask"}
#   ],
#   "gateways": [
#     {"id": "gateway1", "name": "Known Outage Check", "type": "ExclusiveGateway"}
#   ],
#   "flows": [
#     {"id": "flow1", "source": "startEvent1", "target": "task1", "type": "SequenceFlow"},
#     {"id": "flow2", "source": "task1", "target": "task2", "type": "SequenceFlow"},
#     {"id": "flow3", "source": "task2", "target": "gateway1", "type": "SequenceFlow"},
#     {"id": "flow4", "source": "gateway1", "target": "task3", "type": "SequenceFlow"},
#     {"id": "flow5", "source": "task3", "target": "endEvent1", "type": "SequenceFlow"},
#     {"id": "flow6", "source": "gateway1", "target": "task4", "type": "SequenceFlow"},
#     {"id": "flow7", "source": "task4", "target": "task5", "type": "SequenceFlow"},
#     {"id": "flow8", "source": "task5", "target": "task6", "type": "SequenceFlow"},
#     {"id": "flow9", "source": "task4", "target": "task6", "type": "SequenceFlow"},
#     {"id": "flow10", "source": "task6", "target": "endEvent1", "type": "SequenceFlow"},
#     {"id": "flow11", "source": "task2", "target": "intermediateEvent1", "type": "MessageFlow"},
#     {"id": "flow12", "source": "task4", "target": "task5", "type": "MessageFlow"},
#     {"id": "flow13", "source": "task6", "target": "intermediateEvent2", "type": "MessageFlow"}
#   ],
#   "participants": [
#     {"id": "participant1", "name": "Customer", "type": "Lane"},
#     {"id": "participant2", "name": "Automated System", "type": "Lane"},
#     {"id": "participant3", "name": "Support Specialist", "type": "Lane"},
#     {"id": "participant4", "name": "Field Technician", "type": "Lane"}
#   ]
# }


# data = {
#   "events": [
#     {"id": "startEvent1", "type": "Start", "name": "Customer Reports Service Disruption"},
#     {"id": "intermediateEvent1", "type": "Intermediate", "name": "Notification Sent"},
#     {"id": "intermediateEvent2", "type": "Intermediate", "name": "Regular Updates Sent"},
#     {"id": "endEvent1", "type": "End", "name": "Issue Resolved"}
#   ],
#   "tasks": [
#     {"id": "task1", "name": "Check for Known Outages", "type": "ServiceTask"},
#     {"id": "task2", "name": "Notify Customer of Outage", "type": "ServiceTask"},
#     {"id": "task3", "name": "Assess the Situation", "type": "UserTask"},
#     {"id": "task4", "name": "Schedule Field Technician", "type": "UserTask"},
#     {"id": "task5", "name": "Send Regular Updates", "type": "ServiceTask"}
#   ],
#   "gateways": [
#     {"id": "gateway1", "name": "Known Outage Check", "type": "ExclusiveGateway"},
#     {"id": "gateway2", "name": "Field Technician Required", "type": "ExclusiveGateway"}
#   ],
#   "flows": [
#     {"id": "flow1", "source": "startEvent1", "target": "task1", "type": "SequenceFlow"},
#     {"id": "flow2", "source": "task1", "target": "gateway1", "type": "SequenceFlow"},
#     {"id": "flow3", "source": "gateway1", "target": "task2", "type": "SequenceFlow"},
#     {"id": "flow4", "source": "gateway1", "target": "task3", "type": "SequenceFlow"},
#     {"id": "flow5", "source": "task2", "target": "task5", "type": "SequenceFlow"},
#     {"id": "flow6", "source": "task3", "target": "gateway2", "type": "SequenceFlow"},
#     {"id": "flow7", "source": "gateway2", "target": "task4", "type": "SequenceFlow"},
#     {"id": "flow8", "source": "gateway2", "target": "task5", "type": "SequenceFlow"},
#     {"id": "flow9", "source": "task4", "target": "task5", "type": "SequenceFlow"},
#     {"id": "flow10", "source": "task5", "target": "endEvent1", "type": "SequenceFlow"},
#     {"id": "flow11", "source": "task1", "target": "intermediateEvent1", "type": "MessageFlow"},
#     {"id": "flow12", "source": "task3", "target": "intermediateEvent2", "type": "MessageFlow"}
#   ],
#   "participants": [
#     {"id": "participant1", "name": "Customer", "type": "Pool"},
#     {"id": "participant2", "name": "Support System", "type": "Pool"},
#     {"id": "lane1", "name": "System", "type": "Lane"},
#     {"id": "lane2", "name": "Support Specialist", "type": "Lane"},
#     {"id": "lane3", "name": "Field Technician", "type": "Lane"}
#   ]
# }

data = {
  "events": [
    {"id": "startEvent1", "type": "Start", "name": "Process Start"},
    {"id": "intermediateEvent1", "type": "Intermediate", "name": "Notification Sent"},
    {"id": "intermediateEvent2", "type": "Intermediate", "name": "Updates Sent"},
    {"id": "endEvent1", "type": "End", "name": "Process End"}
  ],
  "tasks": [
    {"id": "task1", "name": "Check for Known Outages", "type": "ServiceTask"},
    {"id": "task2", "name": "Notify Customer of Outage", "type": "ServiceTask"},
    {"id": "task3", "name": "Assess the Situation", "type": "UserTask"},
    {"id": "task4", "name": "Schedule Field Technician", "type": "UserTask"},
    {"id": "task5", "name": "Send Regular Updates", "type": "UserTask"},
    {"id": "task6", "name": "Resolve Issue", "type": "UserTask"}
  ],
  "gateways": [
    {"id": "gateway1", "name": "Outage Check Decision", "type": "ExclusiveGateway"},
    {"id": "gateway2", "name": "Field Technician Decision", "type": "ExclusiveGateway"}
  ],
  "flows": [
    {"id": "flow1", "source": "startEvent1", "target": "task1", "type": "SequenceFlow"},
    {"id": "flow2", "source": "task1", "target": "gateway1", "type": "SequenceFlow"},
    {"id": "flow3", "source": "gateway1", "target": "task2", "type": "SequenceFlow"},
    {"id": "flow4", "source": "gateway1", "target": "task3", "type": "SequenceFlow"},
    {"id": "flow5", "source": "task2", "target": "intermediateEvent1", "type": "SequenceFlow"},
    {"id": "flow6", "source": "intermediateEvent1", "target": "endEvent1", "type": "SequenceFlow"},
    {"id": "flow7", "source": "task3", "target": "gateway2", "type": "SequenceFlow"},
    {"id": "flow8", "source": "gateway2", "target": "task4", "type": "SequenceFlow"},
    {"id": "flow9", "source": "gateway2", "target": "task5", "type": "SequenceFlow"},
    {"id": "flow10", "source": "task4", "target": "task5", "type": "SequenceFlow"},
    {"id": "flow11", "source": "task5", "target": "intermediateEvent2", "type": "SequenceFlow"},
    {"id": "flow12", "source": "intermediateEvent2", "target": "task6", "type": "SequenceFlow"},
    {"id": "flow13", "source": "task6", "target": "endEvent1", "type": "SequenceFlow"}
  ],
  "participants": [
    {"id": "pool1", "name": "Customer", "type": "Pool"},
    {"id": "pool2", "name": "Support System", "type": "Pool"},
    {"id": "lane1", "name": "Automated System", "type": "Lane"},
    {"id": "lane2", "name": "Support Specialist", "type": "Lane"},
    {"id": "lane3", "name": "Field Technician Scheduler", "type": "Lane"}
  ]
}

json_to_bpmn(data)