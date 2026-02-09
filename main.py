from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain.agents import create_agent
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

async def main():
    client=MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathserver.py"],
                "transport":"stdio",
            },
            "weather":{
                "url":"http://localhost:8000/mcp",
                "transport": "streamable_http",
            },
            "file":{
                "command":"python",
                "args":["fileserver.py"],
                "transport":"stdio",
            }
        }
    )

    os.environ["HUGGINGFACEHUB_API_TOKEN"]=os.getenv("HUGGINGFACEHUB_API_TOKEN")

    tools=await client.get_tools()
    llm=HuggingFaceEndpoint(repo_id="Qwen/Qwen3-Coder-Next",task="text-generation",max_new_tokens=512,
                           do_sample=False,repetition_penalty=1.03,provider="auto",  )
    model=ChatHuggingFace(llm=llm)
    agent=create_agent(model=model,tools=tools,
                       system_prompt="You are a helpful human assistant. Use the tools depends on content.",)
    
    maths_response=await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )

    print("Math response:", maths_response['messages'][-1].content)

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in Ramanathapuram?"}]}
    )
    print("Weather response:", weather_response['messages'][-1].content)

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in Chennai?"}]}
    )
    print("Weather response:", weather_response['messages'][-1].content)

    maths_response=await agent.ainvoke(
        {"messages": [{"role": "user", "content": "input is 5 and three what is Secret calculation?"}]}
    )

    print("Math response:", maths_response['messages'][-1].content)

    save_response= await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Tell about tamil music history, for this content you can use your llm knowledge and then save as file format"}]}
    )

    print("Weather response:", save_response['messages'][-1].content)


asyncio.run(main())