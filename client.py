import os
import asyncio
from google import genai
from google.genai import types
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import pathlib


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


async def review_file(filename: str) -> str:
    SERVER_PATH = pathlib.Path(__file__).parent / "server.py"

    server_params = StdioServerParameters(
        command="python",
        args=[str(SERVER_PATH)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_response = await session.list_tools()

            gemini_functions = []
            for tool in tools_response.tools:
                gemini_functions.append(
                    types.FunctionDeclaration(
                        name=tool.name,
                        description=tool.description,
                        parameters=tool.inputSchema,
                    )
                )

            gemini_tools = [types.Tool(function_declarations=gemini_functions)]

            prompt = f"""You are an expert code reviewer.
Please review the file '{filename}' and provide structured feedback with these sections:

🐛 BUGS FOUND
⚠️ CODE QUALITY  
✅ GOOD PRACTICES
💡 SUGGESTIONS

Be specific, mention line numbers if possible."""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(tools=gemini_tools)
            )

            while True:
                part = response.candidates[0].content.parts[0]

                if hasattr(part, "function_call") and part.function_call:
                    function_call = part.function_call

                    tool_result = await session.call_tool(
                        function_call.name,
                        dict(function_call.args)
                    )

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            types.Content(role="user", parts=[types.Part(text=prompt)]),
                            types.Content(role="model", parts=[types.Part(function_call=function_call)]),
                            types.Content(role="user", parts=[types.Part(
                                function_response=types.FunctionResponse(
                                    name=function_call.name,
                                    response={"result": tool_result.content[0].text}
                                )
                            )])
                        ],
                        config=types.GenerateContentConfig(tools=gemini_tools)
                    )
                else:
                    return response.text


def review(filename: str) -> str:
    return asyncio.run(review_file(filename))