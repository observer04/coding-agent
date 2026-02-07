import argparse
import os
import sys

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

    chat = client.chat.completions.create(
 #       model="anthropic/claude-haiku-4.5",
	model="z-ai/glm-4.5-air:free",
        messages=[{"role": "user", "content": args.p}],
	tools=[{
  "type": "function",
  "function": {
    "name": "Read",
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
}]
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    message = chat.choices[0].message
    
    # Check if the response contains tool_calls
    if message.tool_calls and len(message.tool_calls) > 0:
        # Extract the first tool call
        tool_call = message.tool_calls[0]
        
        # Parse the function name
        function_name = tool_call.function.name
        
        # Parse the arguments (they come as a JSON string)
        import json
        arguments = json.loads(tool_call.function.arguments)
        
        # Execute the Read tool
        if function_name == "Read":
            file_path = arguments["file_path"]
            
            # Read the file and output its contents
            with open(file_path, 'r') as f:
                file_contents = f.read()
            
            # Output the result to stdout
            print(file_contents)
    else:
        # If no tool calls, just print the message content
        print(message.content)


if __name__ == "__main__":
    main()
