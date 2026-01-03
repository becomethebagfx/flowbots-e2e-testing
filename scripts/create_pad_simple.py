#!/usr/bin/env python3
"""Create Power Automate Desktop Simple tier test artifacts - S01 to S20"""

import os
import json
import zipfile
from pathlib import Path

# Output directory
OUTPUT_DIR = r"C:\flowbots_lab\artifacts_source\pad\simple"

# Simple tier tests (S01-S20) - PAD Robin script format
# Using double quotes for Python strings to avoid conflicts with PAD $''' syntax
PAD_SCRIPTS = {
    "S01": ("File_Create", "Create text file with timestamp",
        "File.WriteText File: $'''C:\\\\flowbots_lab\\\\output\\\\test_file.txt''' TextToWrite: $'''Created at: %CurrentDateTime%''' AppendNewLine: True IfFileExists: File.IfFileExists.Overwrite Encoding: File.FileEncoding.UTF8"),

    "S02": ("File_Read", "Read text file content",
        "File.ReadTextFromFile.ReadText File: $'''C:\\\\flowbots_lab\\\\input\\\\data.txt''' Encoding: File.TextFileEncoding.UTF8 Content=> FileContent"),

    "S03": ("File_Delete", "Delete specified file",
        "File.Delete Files: $'''C:\\\\flowbots_lab\\\\output\\\\temp_file.txt'''"),

    "S04": ("Folder_Create", "Create new directory",
        "Folder.Create FolderPath: $'''C:\\\\flowbots_lab\\\\output\\\\new_folder''' Folder=> NewFolder"),

    "S05": ("Variable_Set", "Set and get variable value",
        "SET testVar TO $'''Hello World'''\nSET testVar TO $'''Test Value'''"),

    "S06": ("String_Concat", "Concatenate two strings",
        "SET str1 TO $'''Hello'''\nSET str2 TO $'''World'''\nText.Join TextList: [str1, str2] StandardDelimiter: Text.StandardDelimiter.Space Result=> result"),

    "S07": ("Number_Add", "Add two numbers",
        "SET num1 TO 10\nSET num2 TO 20\nSET sum TO num1 + num2"),

    "S08": ("Date_Format", "Format current date",
        "DateTime.GetCurrentDateTime.Local DateTimeFormat: DateTime.DateTimeFormat.DateAndTime CurrentDateTime=> CurrentDateTime\nText.ConvertDateTimeToText.FromCustomDateTime DateTime: CurrentDateTime CustomFormat: $'''yyyy-MM-dd HH:mm:ss''' Result=> formattedDate"),

    "S09": ("Message_Box", "Display message box",
        "Display.ShowMessageDialog.ShowMessage Title: $'''Test Message''' Message: $'''Hello from PAD!''' Icon: Display.Icon.None Buttons: Display.Buttons.OK DefaultButton: Display.DefaultButton.Button1 IsTopMost: False ButtonPressed=> ButtonPressed"),

    "S10": ("Log_Message", "Write to log",
        "File.WriteText File: $'''C:\\\\flowbots_lab\\\\logs\\\\pad_log.txt''' TextToWrite: $'''Test log message from PAD''' AppendNewLine: True IfFileExists: File.IfFileExists.Append Encoding: File.FileEncoding.UTF8"),

    "S11": ("Clipboard_Copy", "Copy text to clipboard",
        "Clipboard.SetText Text: $'''Text copied to clipboard'''"),

    "S12": ("Clipboard_Paste", "Paste from clipboard",
        "Clipboard.GetText ClipboardText=> ClipboardText"),

    "S13": ("Environment_Var", "Read environment variable",
        "System.GetEnvironmentVariable.GetEnvironmentVariable Name: $'''USERNAME''' Value=> envValue"),

    "S14": ("Random_Number", "Generate random number",
        "Variables.GenerateRandomNumber MinimumValue: 1 MaximumValue: 100 RandomNumber=> randomNum"),

    "S15": ("Sleep_Wait", "Wait specified seconds",
        "WAIT 2"),

    "S16": ("String_Length", "Get string length",
        "SET testStr TO $'''Hello World'''\nText.GetLength Text: testStr Length=> length"),

    "S17": ("To_Upper", "Convert string to uppercase",
        "SET input TO $'''hello world'''\nText.ChangeCase Text: input TextCase: Text.CaseType.Uppercase Result=> output"),

    "S18": ("To_Lower", "Convert string to lowercase",
        "SET input TO $'''HELLO WORLD'''\nText.ChangeCase Text: input TextCase: Text.CaseType.Lowercase Result=> output"),

    "S19": ("File_Exists", "Check if file exists",
        "File.IfFile.Exists File: $'''C:\\\\flowbots_lab\\\\input\\\\data.txt'''\n    SET exists TO True\nEND"),

    "S20": ("Folder_Exists", "Check if folder exists",
        "Folder.IfFolder.Exists Folder: $'''C:\\\\flowbots_lab\\\\output'''\n    SET exists TO True\nEND"),
}


def create_pad_package(test_id: str, name: str, description: str, script: str) -> str:
    """Create a PAD .zip package"""
    project_name = f"Simple_{name}"
    output_path = os.path.join(OUTPUT_DIR, f"{project_name}.zip")

    # Create .pad file content (Robin script)
    pad_content = f"""# Power Automate Desktop Flow
# Name: {project_name}
# Description: {description}
# Test ID: {test_id}

{script.strip()}
"""

    # Create .zip package
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{project_name}.pad", pad_content)

        # Add metadata
        metadata = {
            "name": project_name,
            "description": description,
            "version": "1.0.0",
            "testId": test_id
        }
        zf.writestr("metadata.json", json.dumps(metadata, indent=2))

    return output_path


def main():
    """Create all Simple tier PAD test artifacts"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Creating PAD Simple tier artifacts in {OUTPUT_DIR}")
    print("=" * 60)

    created = []
    for test_id, (name, description, script) in PAD_SCRIPTS.items():
        try:
            output = create_pad_package(test_id, name, description, script)
            print(f"[{test_id}] Created: {os.path.basename(output)}")
            created.append(output)
        except Exception as e:
            print(f"[{test_id}] ERROR: {e}")

    print("=" * 60)
    print(f"Created {len(created)}/20 PAD Simple tier artifacts")
    return created


if __name__ == "__main__":
    main()
