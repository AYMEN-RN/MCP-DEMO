from langchain.agents import create_agent
from langchain_google_genai  import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.messages import HumanMessage
import asyncio

load_dotenv(override=True)

mcp_client = MultiServerMCPClient({
    "mcp-server": {
        "transport": "streamable_http",
        "url": "http://localhost:24000/mcp"
    }
})

async def main():
    tools = await mcp_client.get_tools()
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="Answer the user questions using provided tools."
    )

    while True:
        user_input = input("Question:")
        if user_input.lower() == 'exit':
            break

        resp = await agent.ainvoke({
            "messages": [
                HumanMessage(user_input)
            ]
        })

        content = resp['messages'][-1].content
        if isinstance(content, list):
            print(content[0].get('text', ''))
        else:
            print(content)

if __name__ == "__main__": 
    asyncio.run(main())