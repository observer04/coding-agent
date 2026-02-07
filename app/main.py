import argparse
import json
import os
import sys
import subprocess

from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Initialize the conversation with the user's prompt
    messages = [{"role": "user", "content": args.p}]
    
    # Define the tools array (can be reused across iterations)
    tools = [{
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read and return the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
  "type": "function",
  "function": {
    "name": "write_file",
    "description": "Write content to a file",
    "parameters": {
      "type": "object",
      "required": ["file_path", "content"],
      "properties": {
        "file_path": {
          "type": "string",
          "description": "The path of the file to write to"
        },
        "content": {
          "type": "string",
          "description": "The content to write to the file"
        }
      }
    }
  }
},
{
  "type": "function",
  "function": {
    "name": "Bash",
    "description": "Execute a shell command",
    "parameters": {
      "type": "object",
      "required": ["command"],
      "properties": {
        "command": {
          "type": "string",
          "description": "The command to execute"
        }
      }
    }
  }
}

    ]
    
    # Agent loop: continue until the model responds without tool calls
    while True:
        # Send the current conversation to the model
        chat = client.chat.completions.create(
            model="z-ai/glm-4.5-air:free",
            # model="anthropic/claude-haiku-4.5",
            messages=messages,
            tools=tools
        )
        
        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")
        
        message = chat.choices[0].message
        
        # Add the assistant's response to the conversation
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": message.tool_calls if message.tool_calls else None
        })
        
        # Check if the response contains tool calls
        if message.tool_calls and len(message.tool_calls) > 0:
            # Execute each requested tool
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                # Execute the Read tool
                if function_name == "read_file":
                    file_path = arguments["file_path"]
                    
                    try:
                        # Read the file
                        with open(file_path, 'r') as f:
                            file_contents = f.read()
                        tool_result = file_contents
                    except Exception as e:
                        tool_result = f"Error reading file: {str(e)}"
                    
                    # Add the tool result to the conversation
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })
                elif function_name == "write_file":
                    file_path = arguments["file_path"]
                    content = arguments["content"]
                    
                    try:
                        # Write the file
                        with open(file_path, 'w') as f:
                            f.write(content)
                        tool_result = "File written successfully"
                    except Exception as e:
                        tool_result = f"Error writing file: {str(e)}"
                    
                    # Add the tool result to the conversation
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })
                elif function_name == "Bash":
                    command = arguments["command"]
                    
                    try:
                        # Execute the command
                        result = subprocess.run(command, shell=True, capture_output=True, text=True)
                        tool_result = f"Command executed successfully:\n{result.stdout}"
                    except Exception as e:
                        tool_result = f"Error executing command: {str(e)}"
                    
                    # Add the tool result to the conversation
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })
        else:
            # No tool calls - we have the final response
            print(message.content)
            break


if __name__ == "__main__":
    main()
