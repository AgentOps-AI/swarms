import json
import re
from typing import Any, List

from swarms.prompts.tools import (
    SCENARIOS,
)
from swarms.tools.tool import BaseTool
from swarms.tools.tool_func_doc_scraper import scrape_tool_func_docs


def tool_find_by_name(tool_name: str, tools: List[Any]):
    """Find the tool by name"""
    for tool in tools:
        if tool.name == tool_name:
            return tool
    return None


def extract_tool_commands(text: str):
    """
    Extract the tool commands from the text

    Example:
    ```json
    {
        "tool": "tool_name",
        "params": {
            "tool1": "inputs",
            "param2": "value2"
        }
    }
    ```

    """
    # Regex to find JSON like strings
    pattern = r"```json(.+?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    json_commands = []
    for match in matches:
        try:
            json_commands = json.loads(match)
            json_commands.append(json_commands)
        except Exception as error:
            print(f"Error parsing JSON command: {error}")


def parse_and_execute_tools(response: str):
    """Parse and execute the tools"""
    json_commands = extract_tool_commands(response)
    for command in json_commands:
        tool_name = command.get("tool")
        params = command.get("parmas", {})
        execute_tools(tool_name, params)


def execute_tools(tool_name, params):
    """Execute the tool with the provided params"""
    tool = tool_find_by_name(tool_name)
    if tool:
        # Execute the tool with the provided parameters
        tool_result = tool.run(**params)
        print(tool_result)


def parse_tool_docs(tools: List[BaseTool]):
    """Parse the tool docs"""
    tool_docs = []
    for tool in tools:
        docs = tool_docs.append(scrape_tool_func_docs(tool))
    return str(docs)


def tools_prompt_prep(docs: str = None, scenarios: str = SCENARIOS):
    """
    Tools prompt prep

    Args:
        docs (str, optional): _description_. Defaults to None.
        scenarios (str, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    PROMPT = f"""
    # Task
    You will be provided with a list of APIs. These APIs will have a
    description and a list of parameters and return types for each tool. Your
    task involves creating varied, complex, and detailed user scenarios
    that require to call API calls. You must select what api to call based on 
    the context of the task and the scenario.

    For instance, given the APIs: SearchHotels, BookHotel, CancelBooking,
    GetNFLNews. Given that GetNFLNews is explicitly provided, your scenario
    should articulate something akin to:

    "The user wants to see if the Broncos won their last game (GetNFLNews).
    They then want to see if that qualifies them for the playoffs and who
    they will be playing against (GetNFLNews). The Broncos did make it into
    the playoffs, so the user wants watch the game in person. They want to
    look for hotels where the playoffs are occurring (GetNBANews +
    SearchHotels). After looking at the options, the user chooses to book a
    3-day stay at the cheapest 4-star option (BookHotel)."
    13

    This scenario exemplifies a scenario using 5 API calls. The scenario is
    complex, detailed, and concise as desired. The scenario also includes two
    APIs used in tandem, the required API, GetNBANews to search for the
    playoffs location and SearchHotels to find hotels based on the returned
    location. Usage of multiple APIs in tandem is highly desirable and will
    receive a higher score. Ideally each scenario should contain one or more
    instances of multiple APIs being used in tandem.

    Note that this scenario does not use all the APIs given and re-uses the "
    GetNBANews" API. Re-using APIs is allowed, but each scenario should
    involve as many different APIs as the user demands. Note that API usage is also included
    in the scenario, but exact parameters ar necessary. You must use a
    different combination of APIs for each scenario. All APIs must be used in
    at least one scenario. You can only use the APIs provided in the APIs
    section.
    
    Note that API calls are not explicitly mentioned and their uses are
    included in parentheses. This behaviour should be mimicked in your
    response.
    
    Output the tool usage in a strict json format with the function name and input to 
    the function. For example, Deliver your response in this format:
    
    ‘‘‘
    {scenarios}
    ‘‘‘
    # APIs
    ‘‘‘
    {docs}
    ‘‘‘
    # Response
    ‘‘‘
    """
    return PROMPT
