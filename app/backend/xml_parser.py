import xml.etree.ElementTree as ET

def json_to_bpmn(bpmn_data):
    ns = {
        'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
        'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
        'di': 'http://www.omg.org/spec/DD/20100524/DI',
        'dc': 'http://www.omg.org/spec/DD/20100524/DC',
        'xsi': "http://www.w3.org/2001/XMLSchema-instance"
    }
    ET.register_namespace('', ns['bpmn'])
    ET.register_namespace('bpmndi', ns['bpmndi'])
    ET.register_namespace('di', ns['di'])
    ET.register_namespace('dc', ns['dc'])
    ET.register_namespace('xsi', ns['xsi'])

    definitions = ET.Element(f"{{{ns['bpmn']}}}definitions", attrib={
        f"{{{ns['xsi']}}}schemaLocation": "http://www.omg.org/spec/BPMN/20100524/MODEL BPMN20.xsd",
        'targetNamespace': "http://example.bpmn.com/schema/bpmn"
    })

    process = ET.SubElement(definitions, f"{{{ns['bpmn']}}}process", attrib={'id': 'Process_1', 'isExecutable': 'false'})

    elements_by_id = {}

    # Create all events, tasks, and gateways
    for event in bpmn_data['events']:
        event_type = 'startEvent' if event['type'] == 'Start' else 'endEvent' if event['type'] == 'End' else 'intermediateCatchEvent'
        bpmn_event = ET.SubElement(process, f"{{{ns['bpmn']}}}{event_type}", id=event['id'], name=event['name'])
        elements_by_id[event['id']] = bpmn_event

    for task in bpmn_data['tasks']:
        bpmn_task = ET.SubElement(process, f"{{{ns['bpmn']}}}{task['type']}", id=task['id'], name=task['name'])
        elements_by_id[task['id']] = bpmn_task

    for gateway in bpmn_data['gateways']:
        gateway_type = 'exclusiveGateway' if gateway['type'] == 'ExclusiveGateway' else 'parallelGateway'
        bpmn_gateway = ET.SubElement(process, f"{{{ns['bpmn']}}}{gateway_type}", id=gateway['id'], name=gateway['name'])
        elements_by_id[gateway['id']] = bpmn_gateway

    for flow in bpmn_data['flows']:
        ET.SubElement(process, f"{{{ns['bpmn']}}}sequenceFlow", id=flow['id'], sourceRef=flow['source'], targetRef=flow['target'])

    # BPMNDI section
    bpmn_di = ET.SubElement(definitions, f"{{{ns['bpmndi']}}}BPMNDiagram", attrib={'id': 'BPMNDiagram_1'})
    bpmn_plane = ET.SubElement(bpmn_di, f"{{{ns['bpmndi']}}}BPMNPlane", attrib={'id': 'BPMNPlane_1', 'bpmnElement': 'Process_1'})

    # Generate diagram elements for tasks, events, gateways
    for element in bpmn_data['tasks'] + bpmn_data['events'] + bpmn_data['gateways']:
        bpmn_shape = ET.SubElement(bpmn_plane, f"{{{ns['bpmndi']}}}BPMNShape", attrib={'id': f"{element['id']}_di", 'bpmnElement': element['id']})
        ET.SubElement(bpmn_shape, f"{{{ns['dc']}}}Bounds", attrib={'x': '100', 'y': '100', 'width': '100', 'height': '80'})

    # Arrange elements
    arrange_elements(bpmn_plane, elements_by_id, bpmn_data)

    # Generate diagram elements for flows
    for flow in bpmn_data['flows']:
        bpmn_edge = ET.SubElement(bpmn_plane, f"{{{ns['bpmndi']}}}BPMNEdge", attrib={'id': f"{flow['id']}_di", 'bpmnElement': flow['id']})
        waypoint1 = ET.SubElement(bpmn_edge, f"{{{ns['di']}}}waypoint")
        waypoint2 = ET.SubElement(bpmn_edge, f"{{{ns['di']}}}waypoint")
        adjust_waypoints(waypoint1, waypoint2, elements_by_id[flow['source']], elements_by_id[flow['target']])

    # Save the arranged XML to a file
    tree = ET.ElementTree(definitions)
    ET.indent(tree, space="  ", level=0)
    tree.write('bpmn_output.bpmn', encoding='utf-8', xml_declaration=True)

    return ET.tostring(definitions, encoding='unicode')

def arrange_elements(bpmn_plane, elements_by_id, bpmn_data):
    ns = {
        'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
        'dc': 'http://www.omg.org/spec/DD/20100524/DC',
        'di': 'http://www.omg.org/spec/DD/20100524/DI',
    }

    x_offset = 100
    y_offset = 100
    vertical_spacing = 150
    horizontal_spacing = 250

    current_y = y_offset

    # Arrange start events
    for i, event in enumerate([e for e in bpmn_data['events'] if e['type'] == 'Start']):
        update_bpmn_shape_position(bpmn_plane, elements_by_id[event['id']], x_offset, current_y + i * vertical_spacing)
        elements_by_id[event['id']].attrib['x'] = str(x_offset)
        elements_by_id[event['id']].attrib['y'] = str(current_y + i * vertical_spacing)

    x_offset += horizontal_spacing

    # Track processed elements to avoid duplicates
    processed_elements = set(e['id'] for e in bpmn_data['events'] if e['type'] == 'Start')

    # Arrange the elements based on the flow
    def arrange_element(element_id, x_offset, current_y, vertical_spacing):
        if element_id in processed_elements:
            return x_offset, current_y

        element = elements_by_id[element_id]
        update_bpmn_shape_position(bpmn_plane, element, x_offset, current_y)
        element.attrib['x'] = str(x_offset)
        element.attrib['y'] = str(current_y)

        processed_elements.add(element_id)

        # Process the next elements in the flow
        outgoing_flows = [flow for flow in bpmn_data['flows'] if flow['source'] == element_id]
        if outgoing_flows:
            split_y_offsets = {}
            for i, flow in enumerate(outgoing_flows):
                target_id = flow['target']
                if any(g['id'] == target_id and g['type'] == 'ExclusiveGateway' for g in bpmn_data['gateways']):
                    for j, split_flow in enumerate([f for f in bpmn_data['flows'] if f['source'] == target_id]):
                        split_x_offset, split_y_offset = arrange_element(split_flow['target'], x_offset + horizontal_spacing, current_y + j * vertical_spacing, vertical_spacing)
                        split_y_offsets[split_flow['target']] = split_y_offset
                else:
                    x_offset, current_y = arrange_element(target_id, x_offset + horizontal_spacing, current_y, vertical_spacing)
            if split_y_offsets:
                current_y = max(split_y_offsets.values()) + vertical_spacing
        return x_offset, current_y

    for element in bpmn_data['tasks'] + bpmn_data['gateways']:
        if element['id'] not in processed_elements:
            x_offset, current_y = arrange_element(element['id'], x_offset, current_y, vertical_spacing)
            current_y += vertical_spacing

    x_offset += horizontal_spacing

    # Arrange end events
    for i, event in enumerate([e for e in bpmn_data['events'] if e['type'] == 'End']):
        update_bpmn_shape_position(bpmn_plane, elements_by_id[event['id']], x_offset, y_offset + i * vertical_spacing)
        elements_by_id[event['id']].attrib['x'] = str(x_offset)
        elements_by_id[event['id']].attrib['y'] = str(y_offset + i * vertical_spacing)

def adjust_waypoints(waypoint1, waypoint2, source_element, target_element):
    source_x = float(source_element.attrib['x']) + 100 / 2  # Center of the source element
    source_y = float(source_element.attrib['y']) + 80 / 2   # Center of the source element
    target_x = float(target_element.attrib['x']) + 100 / 2  # Center of the target element
    target_y = float(target_element.attrib['y']) + 80 / 2   # Center of the target element
    waypoint1.attrib['x'] = str(source_x)
    waypoint1.attrib['y'] = str(source_y)
    waypoint2.attrib['x'] = str(target_x)
    waypoint2.attrib['y'] = str(target_y)

def update_bpmn_shape_position(bpmn_plane, element, x, y):
    ns = {
        'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
        'dc': 'http://www.omg.org/spec/DD/20100524/DC',
    }
    bpmn_shape_id = f"{element.attrib['id']}_di"
    bpmn_shape = bpmn_plane.find(f".//{{{ns['bpmndi']}}}BPMNShape[@id='{bpmn_shape_id}']")
    if bpmn_shape is not None:
        bounds = bpmn_shape.find(f"{{{ns['dc']}}}Bounds")
        if bounds is not None:
            bounds.set('x', str(x))
            bounds.set('y', str(y))

data = {
  "events": [
    {"id": "startEvent1", "type": "Start", "name": "Customer Reports Service Disruption"},
    {"id": "endEvent1", "type": "End", "name": "Issue Resolved"}
  ],
  "tasks": [
    {"id": "task1", "type": "ServiceTask", "name": "Check for Known Outages"},
    {"id": "task2", "type": "ServiceTask", "name": "Notify Customer of Outage"},
    {"id": "task3", "type": "UserTask", "name": "Assess Situation"},
    {"id": "task4", "type": "UserTask", "name": "Schedule Field Technician"},
    {"id": "task5", "type": "ServiceTask", "name": "Provide Regular Updates"}
  ],
  "gateways": [
    {"id": "gateway1", "type": "ExclusiveGateway", "name": "Outage Found?"},
    {"id": "gateway2", "type": "ExclusiveGateway", "name": "Field Technician Needed?"}
  ],
  "flows": [
    {"id": "flow1", "type": "SequenceFlow", "source": "startEvent1", "target": "task1"},
    {"id": "flow2", "type": "SequenceFlow", "source": "task1", "target": "gateway1"},
    {"id": "flow3", "type": "SequenceFlow", "source": "gateway1", "target": "task2", "condition": "Yes"},
    {"id": "flow4", "type": "SequenceFlow", "source": "task2", "target": "endEvent1"},
    {"id": "flow5", "type": "SequenceFlow", "source": "gateway1", "target": "task3", "condition": "No"},
    {"id": "flow6", "type": "SequenceFlow", "source": "task3", "target": "gateway2"},
    {"id": "flow7", "type": "SequenceFlow", "source": "gateway2", "target": "task4", "condition": "Yes"},
    {"id": "flow8", "type": "SequenceFlow", "source": "task4", "target": "task5"},
    {"id": "flow9", "type": "SequenceFlow", "source": "gateway2", "target": "task5", "condition": "No"},
    {"id": "flow10", "type": "SequenceFlow", "source": "task5", "target": "endEvent1"}
  ]
}

print(json_to_bpmn(data))