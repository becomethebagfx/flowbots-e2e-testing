#!/usr/bin/env python3
"""Create UiPath Simple tier test artifacts - S01 to S20"""

import os
import json
import zipfile
from pathlib import Path

# Output directory
OUTPUT_DIR = r"C:\flowbots_lab\artifacts_source\uipath\simple"

# Simple tier tests (S01-S20)
SIMPLE_TESTS = {
    "S01": ("File_Create", "Create text file with timestamp"),
    "S02": ("File_Read", "Read text file content"),
    "S03": ("File_Delete", "Delete specified file"),
    "S04": ("Folder_Create", "Create new directory"),
    "S05": ("Variable_Set", "Set and get variable value"),
    "S06": ("String_Concat", "Concatenate two strings"),
    "S07": ("Number_Add", "Add two numbers"),
    "S08": ("Date_Format", "Format current date"),
    "S09": ("Message_Box", "Display message box"),
    "S10": ("Log_Message", "Write to log"),
    "S11": ("Clipboard_Copy", "Copy text to clipboard"),
    "S12": ("Clipboard_Paste", "Paste from clipboard"),
    "S13": ("Environment_Var", "Read environment variable"),
    "S14": ("Random_Number", "Generate random number"),
    "S15": ("Sleep_Wait", "Wait specified seconds"),
    "S16": ("String_Length", "Get string length"),
    "S17": ("To_Upper", "Convert string to uppercase"),
    "S18": ("To_Lower", "Convert string to lowercase"),
    "S19": ("File_Exists", "Check if file exists"),
    "S20": ("Folder_Exists", "Check if folder exists"),
}

# UiPath XAML templates for each test
XAML_TEMPLATES = {
    "S01": '''<Activity mc:Ignorable="sap sap2010" x:Class="FileCreate"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
  xmlns:sap="http://schemas.microsoft.com/netfx/2009/xaml/activities/presentation"
  xmlns:sap2010="http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation"
  xmlns:scg="clr-namespace:System.Collections.Generic;assembly=mscorlib"
  xmlns:sco="clr-namespace:System.Collections.ObjectModel;assembly=mscorlib"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  xmlns:ui="http://schemas.uipath.com/workflow/activities">
  <Sequence DisplayName="File Create">
    <ui:WriteTextFile FileName="C:\\flowbots_lab\\output\\test_file.txt" Text="Created at: " />
  </Sequence>
</Activity>''',

    "S02": '''<Activity mc:Ignorable="sap sap2010" x:Class="FileRead"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  xmlns:ui="http://schemas.uipath.com/workflow/activities">
  <Sequence DisplayName="File Read">
    <ui:ReadTextFile FileName="C:\\flowbots_lab\\input\\data.txt" />
  </Sequence>
</Activity>''',

    "S03": '''<Activity mc:Ignorable="sap sap2010" x:Class="FileDelete"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  xmlns:ui="http://schemas.uipath.com/workflow/activities">
  <Sequence DisplayName="File Delete">
    <ui:DeleteFile FileName="C:\\flowbots_lab\\output\\temp_file.txt" />
  </Sequence>
</Activity>''',

    "S04": '''<Activity mc:Ignorable="sap sap2010" x:Class="FolderCreate"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  xmlns:ui="http://schemas.uipath.com/workflow/activities">
  <Sequence DisplayName="Folder Create">
    <ui:CreateDirectory DirectoryName="C:\\flowbots_lab\\output\\new_folder" />
  </Sequence>
</Activity>''',

    "S05": '''<Activity mc:Ignorable="sap sap2010" x:Class="VariableSet"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <Sequence DisplayName="Variable Set">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="testVar" Default="Hello World" />
    </Sequence.Variables>
    <Assign DisplayName="Set Variable">
      <Assign.To><OutArgument x:TypeArguments="x:String">[testVar]</OutArgument></Assign.To>
      <Assign.Value><InArgument x:TypeArguments="x:String">"Test Value"</InArgument></Assign.Value>
    </Assign>
  </Sequence>
</Activity>''',

    "S06": '''<Activity mc:Ignorable="sap sap2010" x:Class="StringConcat"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <Sequence DisplayName="String Concat">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="str1" Default="Hello" />
      <Variable x:TypeArguments="x:String" Name="str2" Default="World" />
      <Variable x:TypeArguments="x:String" Name="result" />
    </Sequence.Variables>
    <Assign DisplayName="Concatenate">
      <Assign.To><OutArgument x:TypeArguments="x:String">[result]</OutArgument></Assign.To>
      <Assign.Value><InArgument x:TypeArguments="x:String">[str1 + " " + str2]</InArgument></Assign.Value>
    </Assign>
  </Sequence>
</Activity>''',

    "S07": '''<Activity mc:Ignorable="sap sap2010" x:Class="NumberAdd"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <Sequence DisplayName="Number Add">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:Int32" Name="num1" Default="10" />
      <Variable x:TypeArguments="x:Int32" Name="num2" Default="20" />
      <Variable x:TypeArguments="x:Int32" Name="sum" />
    </Sequence.Variables>
    <Assign DisplayName="Add Numbers">
      <Assign.To><OutArgument x:TypeArguments="x:Int32">[sum]</OutArgument></Assign.To>
      <Assign.Value><InArgument x:TypeArguments="x:Int32">[num1 + num2]</InArgument></Assign.Value>
    </Assign>
  </Sequence>
</Activity>''',

    "S08": '''<Activity mc:Ignorable="sap sap2010" x:Class="DateFormat"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <Sequence DisplayName="Date Format">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="formattedDate" />
    </Sequence.Variables>
    <Assign DisplayName="Format Date">
      <Assign.To><OutArgument x:TypeArguments="x:String">[formattedDate]</OutArgument></Assign.To>
      <Assign.Value><InArgument x:TypeArguments="x:String">[DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")]</InArgument></Assign.Value>
    </Assign>
  </Sequence>
</Activity>''',

    "S09": '''<Activity mc:Ignorable="sap sap2010" x:Class="MessageBox"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  xmlns:ui="http://schemas.uipath.com/workflow/activities">
  <Sequence DisplayName="Message Box">
    <ui:MessageBox Text="Hello from UiPath!" Caption="Test Message" />
  </Sequence>
</Activity>''',

    "S10": '''<Activity mc:Ignorable="sap sap2010" x:Class="LogMessage"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  xmlns:ui="http://schemas.uipath.com/workflow/activities">
  <Sequence DisplayName="Log Message">
    <ui:LogMessage Level="Info" Message="Test log message from UiPath" />
  </Sequence>
</Activity>''',

    "S11": '''<Activity mc:Ignorable="sap sap2010" x:Class="ClipboardCopy"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  xmlns:ui="http://schemas.uipath.com/workflow/activities">
  <Sequence DisplayName="Clipboard Copy">
    <ui:SetToClipboard Text="Text copied to clipboard" />
  </Sequence>
</Activity>''',

    "S12": '''<Activity mc:Ignorable="sap sap2010" x:Class="ClipboardPaste"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  xmlns:ui="http://schemas.uipath.com/workflow/activities">
  <Sequence DisplayName="Clipboard Paste">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="clipboardText" />
    </Sequence.Variables>
    <ui:GetFromClipboard>
      <ui:GetFromClipboard.Result>
        <OutArgument x:TypeArguments="x:String">[clipboardText]</OutArgument>
      </ui:GetFromClipboard.Result>
    </ui:GetFromClipboard>
  </Sequence>
</Activity>''',

    "S13": '''<Activity mc:Ignorable="sap sap2010" x:Class="EnvironmentVar"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  xmlns:ui="http://schemas.uipath.com/workflow/activities">
  <Sequence DisplayName="Environment Var">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="envValue" />
    </Sequence.Variables>
    <ui:GetEnvironmentVariable VariableName="USERNAME">
      <ui:GetEnvironmentVariable.Result>
        <OutArgument x:TypeArguments="x:String">[envValue]</OutArgument>
      </ui:GetEnvironmentVariable.Result>
    </ui:GetEnvironmentVariable>
  </Sequence>
</Activity>''',

    "S14": '''<Activity mc:Ignorable="sap sap2010" x:Class="RandomNumber"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <Sequence DisplayName="Random Number">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:Int32" Name="randomNum" />
    </Sequence.Variables>
    <Assign DisplayName="Generate Random">
      <Assign.To><OutArgument x:TypeArguments="x:Int32">[randomNum]</OutArgument></Assign.To>
      <Assign.Value><InArgument x:TypeArguments="x:Int32">[New Random().Next(1, 100)]</InArgument></Assign.Value>
    </Assign>
  </Sequence>
</Activity>''',

    "S15": '''<Activity mc:Ignorable="sap sap2010" x:Class="SleepWait"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  xmlns:ui="http://schemas.uipath.com/workflow/activities">
  <Sequence DisplayName="Sleep Wait">
    <ui:Delay Duration="00:00:02" />
  </Sequence>
</Activity>''',

    "S16": '''<Activity mc:Ignorable="sap sap2010" x:Class="StringLength"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <Sequence DisplayName="String Length">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="testStr" Default="Hello World" />
      <Variable x:TypeArguments="x:Int32" Name="length" />
    </Sequence.Variables>
    <Assign DisplayName="Get Length">
      <Assign.To><OutArgument x:TypeArguments="x:Int32">[length]</OutArgument></Assign.To>
      <Assign.Value><InArgument x:TypeArguments="x:Int32">[testStr.Length]</InArgument></Assign.Value>
    </Assign>
  </Sequence>
</Activity>''',

    "S17": '''<Activity mc:Ignorable="sap sap2010" x:Class="ToUpper"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <Sequence DisplayName="To Upper">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="input" Default="hello world" />
      <Variable x:TypeArguments="x:String" Name="output" />
    </Sequence.Variables>
    <Assign DisplayName="Convert To Upper">
      <Assign.To><OutArgument x:TypeArguments="x:String">[output]</OutArgument></Assign.To>
      <Assign.Value><InArgument x:TypeArguments="x:String">[input.ToUpper()]</InArgument></Assign.Value>
    </Assign>
  </Sequence>
</Activity>''',

    "S18": '''<Activity mc:Ignorable="sap sap2010" x:Class="ToLower"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <Sequence DisplayName="To Lower">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:String" Name="input" Default="HELLO WORLD" />
      <Variable x:TypeArguments="x:String" Name="output" />
    </Sequence.Variables>
    <Assign DisplayName="Convert To Lower">
      <Assign.To><OutArgument x:TypeArguments="x:String">[output]</OutArgument></Assign.To>
      <Assign.Value><InArgument x:TypeArguments="x:String">[input.ToLower()]</InArgument></Assign.Value>
    </Assign>
  </Sequence>
</Activity>''',

    "S19": '''<Activity mc:Ignorable="sap sap2010" x:Class="FileExists"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  xmlns:ui="http://schemas.uipath.com/workflow/activities">
  <Sequence DisplayName="File Exists">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:Boolean" Name="exists" />
    </Sequence.Variables>
    <ui:PathExists Path="C:\\flowbots_lab\\input\\data.txt" PathType="File">
      <ui:PathExists.Exists>
        <OutArgument x:TypeArguments="x:Boolean">[exists]</OutArgument>
      </ui:PathExists.Exists>
    </ui:PathExists>
  </Sequence>
</Activity>''',

    "S20": '''<Activity mc:Ignorable="sap sap2010" x:Class="FolderExists"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  xmlns:ui="http://schemas.uipath.com/workflow/activities">
  <Sequence DisplayName="Folder Exists">
    <Sequence.Variables>
      <Variable x:TypeArguments="x:Boolean" Name="exists" />
    </Sequence.Variables>
    <ui:PathExists Path="C:\\flowbots_lab\\output" PathType="Folder">
      <ui:PathExists.Exists>
        <OutArgument x:TypeArguments="x:Boolean">[exists]</OutArgument>
      </ui:PathExists.Exists>
    </ui:PathExists>
  </Sequence>
</Activity>''',
}

def create_project_json(name: str, description: str) -> str:
    """Create project.json content"""
    return json.dumps({
        "name": name,
        "description": description,
        "main": "Main.xaml",
        "dependencies": {
            "UiPath.System.Activities": "[22.4.1]",
            "UiPath.UIAutomation.Activities": "[22.4.4]"
        },
        "webServices": [],
        "entitiesStores": [],
        "schemaVersion": "4.0",
        "studioVersion": "22.4.3",
        "projectVersion": "1.0.0",
        "runtimeOptions": {
            "autoDispose": False,
            "netFrameworkLazyAssemblyLoad": False,
            "isPausable": True,
            "isAttended": False,
            "requiresUserInteraction": True,
            "supportsPersistence": False,
            "workflowSerialization": "DataContract",
            "excludedLoggedData": ["Private:*", "*password*"],
            "executionType": "Workflow",
            "readyForPiP": False,
            "startsInPiP": False,
            "mustRestoreAllDependencies": True,
            "pipType": "ChildSession"
        },
        "designOptions": {
            "projectProfile": "Developement",
            "outputType": "Process",
            "libraryOptions": {"includeOriginalXaml": False, "privateWorkflows": []},
            "fileInfoCollection": []
        },
        "expressionLanguage": "VisualBasic",
        "isTemplate": False,
        "publishUrl": "",
        "templateProjectData": {},
        "publishData": {}
    }, indent=2)


def create_uipath_nupkg(test_id: str, name: str, description: str, xaml: str) -> str:
    """Create a UiPath .nupkg package"""
    project_name = f"Simple_{name}"
    output_path = os.path.join(OUTPUT_DIR, f"{project_name}.nupkg")

    # Create temp directory structure
    temp_dir = os.path.join(OUTPUT_DIR, f"temp_{test_id}")
    os.makedirs(temp_dir, exist_ok=True)

    # Write Main.xaml
    with open(os.path.join(temp_dir, "Main.xaml"), "w", encoding="utf-8") as f:
        f.write(xaml)

    # Write project.json
    with open(os.path.join(temp_dir, "project.json"), "w", encoding="utf-8") as f:
        f.write(create_project_json(project_name, description))

    # Create .nupkg (it's just a zip file)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(os.path.join(temp_dir, "Main.xaml"), "Main.xaml")
        zf.write(os.path.join(temp_dir, "project.json"), "project.json")

    # Cleanup temp
    import shutil
    shutil.rmtree(temp_dir)

    return output_path


def main():
    """Create all Simple tier UiPath test artifacts"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Creating UiPath Simple tier artifacts in {OUTPUT_DIR}")
    print("=" * 60)

    created = []
    for test_id, (name, description) in SIMPLE_TESTS.items():
        try:
            xaml = XAML_TEMPLATES.get(test_id, XAML_TEMPLATES["S05"])  # Default to S05 if missing
            output = create_uipath_nupkg(test_id, name, description, xaml)
            print(f"[{test_id}] Created: {os.path.basename(output)}")
            created.append(output)
        except Exception as e:
            print(f"[{test_id}] ERROR: {e}")

    print("=" * 60)
    print(f"Created {len(created)}/20 UiPath Simple tier artifacts")
    return created


if __name__ == "__main__":
    main()
