#!/usr/bin/env python3
"""Create Blue Prism Simple tier test artifacts - S01 to S20"""

import os
import json
import zipfile
from pathlib import Path
from datetime import datetime
import uuid

# Output directory
OUTPUT_DIR = r"C:\flowbots_lab\artifacts_source\blueprism\simple"

# Blue Prism uses XML-based .bprelease format
# Each release contains a process definition

def generate_bp_xml(test_id: str, name: str, description: str, actions: list) -> str:
    """Generate Blue Prism process XML"""
    process_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    # Build actions XML
    actions_xml = ""
    for i, action in enumerate(actions):
        action_id = str(uuid.uuid4())
        actions_xml += f"""
        <stage stageid="{action_id}" name="{action['name']}" type="{action['type']}">
            <subsheetid>{process_id}</subsheetid>
            <loginhibit alialialialialialiased="true" />
            {action.get('content', '')}
        </stage>"""

    return f'''<?xml version="1.0" encoding="utf-8"?>
<bpr:release xmlns:bpr="http://www.blueprism.co.uk/product/release">
    <bpr:name>{name}</bpr:name>
    <bpr:release-notes>{description} - Test ID: {test_id}</bpr:release-notes>
    <bpr:created>{timestamp}</bpr:created>
    <bpr:package-id>{process_id}</bpr:package-id>
    <bpr:package-name>Simple_{name}</bpr:package-name>
    <bpr:contents>
        <process name="Simple_{name}" id="{process_id}" byrefcollection="true">
            <view>
                <camerax>0</camerax>
                <cameray>0</cameray>
                <zoom>1</zoom>
            </view>
            <preconditions />
            <endpoint-in />
            <endpoint-out />
            <subsheet subsheetid="{process_id}" type="Main" published="True">
                <name>Main Page</name>
                <view>
                    <camerax>0</camerax>
                    <cameray>0</cameray>
                    <zoom>1</zoom>
                </view>
            </subsheet>
            <stage stageid="{str(uuid.uuid4())}" name="Start" type="Start">
                <subsheetid>{process_id}</subsheetid>
                <loginhibit onnever="True" />
                <narrative>Process start point</narrative>
            </stage>
            {actions_xml}
            <stage stageid="{str(uuid.uuid4())}" name="End" type="End">
                <subsheetid>{process_id}</subsheetid>
                <loginhibit onnever="True" />
                <narrative>Process end point</narrative>
            </stage>
        </process>
    </bpr:contents>
</bpr:release>'''


# Simple tier tests (S01-S20) - Blue Prism format
BP_TESTS = {
    "S01": ("File_Create", "Create text file with timestamp", [
        {"name": "Write File", "type": "Action", "content": '<action name="File - Write Text"><object>Utility - File Management</object><input name="File Path" type="text" expr="&quot;C:\\flowbots_lab\\output\\test_file.txt&quot;" /><input name="Text" type="text" expr="&quot;Created at: &quot; &amp; Now()" /></action>'}
    ]),

    "S02": ("File_Read", "Read text file content", [
        {"name": "Read File", "type": "Action", "content": '<action name="File - Read Text"><object>Utility - File Management</object><input name="File Path" type="text" expr="&quot;C:\\flowbots_lab\\input\\data.txt&quot;" /><output name="Contents" type="text" stage="FileContent" /></action>'}
    ]),

    "S03": ("File_Delete", "Delete specified file", [
        {"name": "Delete File", "type": "Action", "content": '<action name="File - Delete"><object>Utility - File Management</object><input name="File Path" type="text" expr="&quot;C:\\flowbots_lab\\output\\temp_file.txt&quot;" /></action>'}
    ]),

    "S04": ("Folder_Create", "Create new directory", [
        {"name": "Create Folder", "type": "Action", "content": '<action name="Folder - Create"><object>Utility - File Management</object><input name="Folder Path" type="text" expr="&quot;C:\\flowbots_lab\\output\\new_folder&quot;" /></action>'}
    ]),

    "S05": ("Variable_Set", "Set and get variable value", [
        {"name": "Set Variable", "type": "Calculation", "content": '<calculation expression="&quot;Hello World&quot;" stage="testVar" />'}
    ]),

    "S06": ("String_Concat", "Concatenate two strings", [
        {"name": "Set Str1", "type": "Calculation", "content": '<calculation expression="&quot;Hello&quot;" stage="str1" />'},
        {"name": "Set Str2", "type": "Calculation", "content": '<calculation expression="&quot;World&quot;" stage="str2" />'},
        {"name": "Concat", "type": "Calculation", "content": '<calculation expression="[str1] &amp; &quot; &quot; &amp; [str2]" stage="result" />'}
    ]),

    "S07": ("Number_Add", "Add two numbers", [
        {"name": "Set Num1", "type": "Calculation", "content": '<calculation expression="10" stage="num1" />'},
        {"name": "Set Num2", "type": "Calculation", "content": '<calculation expression="20" stage="num2" />'},
        {"name": "Add", "type": "Calculation", "content": '<calculation expression="[num1] + [num2]" stage="sum" />'}
    ]),

    "S08": ("Date_Format", "Format current date", [
        {"name": "Get Date", "type": "Calculation", "content": '<calculation expression="Now()" stage="CurrentDateTime" />'},
        {"name": "Format Date", "type": "Calculation", "content": '<calculation expression="Format([CurrentDateTime], &quot;yyyy-MM-dd HH:mm:ss&quot;)" stage="formattedDate" />'}
    ]),

    "S09": ("Message_Box", "Display message box", [
        {"name": "Show Message", "type": "Action", "content": '<action name="Show Message"><object>Utility - General</object><input name="Title" type="text" expr="&quot;Test Message&quot;" /><input name="Message" type="text" expr="&quot;Hello from Blue Prism!&quot;" /></action>'}
    ]),

    "S10": ("Log_Message", "Write to log", [
        {"name": "Write Log", "type": "Action", "content": '<action name="File - Append Text"><object>Utility - File Management</object><input name="File Path" type="text" expr="&quot;C:\\flowbots_lab\\logs\\bp_log.txt&quot;" /><input name="Text" type="text" expr="&quot;Test log message from Blue Prism&quot;" /></action>'}
    ]),

    "S11": ("Clipboard_Copy", "Copy text to clipboard", [
        {"name": "Set Clipboard", "type": "Action", "content": '<action name="Set Clipboard"><object>Utility - Environment</object><input name="Text" type="text" expr="&quot;Text copied to clipboard&quot;" /></action>'}
    ]),

    "S12": ("Clipboard_Paste", "Paste from clipboard", [
        {"name": "Get Clipboard", "type": "Action", "content": '<action name="Get Clipboard"><object>Utility - Environment</object><output name="Text" type="text" stage="ClipboardText" /></action>'}
    ]),

    "S13": ("Environment_Var", "Read environment variable", [
        {"name": "Get Env Var", "type": "Action", "content": '<action name="Get Environment Variable"><object>Utility - Environment</object><input name="Name" type="text" expr="&quot;USERNAME&quot;" /><output name="Value" type="text" stage="envValue" /></action>'}
    ]),

    "S14": ("Random_Number", "Generate random number", [
        {"name": "Generate Random", "type": "Calculation", "content": '<calculation expression="RND(1, 100)" stage="randomNum" />'}
    ]),

    "S15": ("Sleep_Wait", "Wait specified seconds", [
        {"name": "Wait", "type": "Wait", "content": '<wait duration="2" />'}
    ]),

    "S16": ("String_Length", "Get string length", [
        {"name": "Set String", "type": "Calculation", "content": '<calculation expression="&quot;Hello World&quot;" stage="testStr" />'},
        {"name": "Get Length", "type": "Calculation", "content": '<calculation expression="Len([testStr])" stage="length" />'}
    ]),

    "S17": ("To_Upper", "Convert string to uppercase", [
        {"name": "Set Input", "type": "Calculation", "content": '<calculation expression="&quot;hello world&quot;" stage="input" />'},
        {"name": "To Upper", "type": "Calculation", "content": '<calculation expression="Upper([input])" stage="output" />'}
    ]),

    "S18": ("To_Lower", "Convert string to lowercase", [
        {"name": "Set Input", "type": "Calculation", "content": '<calculation expression="&quot;HELLO WORLD&quot;" stage="input" />'},
        {"name": "To Lower", "type": "Calculation", "content": '<calculation expression="Lower([input])" stage="output" />'}
    ]),

    "S19": ("File_Exists", "Check if file exists", [
        {"name": "Check File", "type": "Action", "content": '<action name="File - Exists"><object>Utility - File Management</object><input name="File Path" type="text" expr="&quot;C:\\flowbots_lab\\input\\data.txt&quot;" /><output name="Exists" type="flag" stage="exists" /></action>'}
    ]),

    "S20": ("Folder_Exists", "Check if folder exists", [
        {"name": "Check Folder", "type": "Action", "content": '<action name="Folder - Exists"><object>Utility - File Management</object><input name="Folder Path" type="text" expr="&quot;C:\\flowbots_lab\\output&quot;" /><output name="Exists" type="flag" stage="exists" /></action>'}
    ]),
}


def create_bp_package(test_id: str, name: str, description: str, actions: list) -> str:
    """Create a Blue Prism .bprelease package"""
    project_name = f"Simple_{name}"
    output_path = os.path.join(OUTPUT_DIR, f"{project_name}.bprelease")

    # Generate XML content
    xml_content = generate_bp_xml(test_id, name, description, actions)

    # Write as .bprelease (XML file)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    # Also create a .zip version with metadata
    zip_path = output_path + ".zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{project_name}.bprelease", xml_content)
        metadata = {
            "name": project_name,
            "description": description,
            "version": "1.0.0",
            "testId": test_id,
            "platform": "Blue Prism"
        }
        zf.writestr("metadata.json", json.dumps(metadata, indent=2))

    return output_path


def main():
    """Create all Simple tier Blue Prism test artifacts"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Creating Blue Prism Simple tier artifacts in {OUTPUT_DIR}")
    print("=" * 60)

    created = []
    for test_id, (name, description, actions) in BP_TESTS.items():
        try:
            output = create_bp_package(test_id, name, description, actions)
            print(f"[{test_id}] Created: {os.path.basename(output)}")
            created.append(output)
        except Exception as e:
            print(f"[{test_id}] ERROR: {e}")

    print("=" * 60)
    print(f"Created {len(created)}/20 Blue Prism Simple tier artifacts")
    return created


if __name__ == "__main__":
    main()
