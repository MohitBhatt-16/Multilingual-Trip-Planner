from crewai import Agent
from textwrap import dedent
from langchain_groq import ChatGroq
from tools_created.search_tools import SearchTools
from tools_created.calculator_tools import CalculatorTools
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
# from crewai_tools import (
#     SerperDevTool)
load_dotenv()

"""
Creating Agent Cheat Sheet
- Think like a boss. Work backwards from the goal and think which employee
    you need to hire to get the job done.
- Define the Captain of the crew who orient the other agents towards the goal.
- Define which experts the captain needs to communicate with and delegate tasks to 
    build a top down structure of the crew

Goal : 
- Create a travel itienary with detailed per day plans,
    including budget, packing suggestions, and safety tips

Captain/Manager/Boss:
- Expert Travel Agent

Employees/Experts to hire:
- City Selection Expert
- Local Tour Guide
- Accommodation Agent
- Transportation Agent
- Budget Agent
- Packing Guide Agent
- Weather Forecasting Agent
- Safety Advisor Agent

Notes : 
- Agents should be results driven and have a clear goal in mind
- Role is their job title
- Goals should accountable
- Backstory should be their resume
"""
# search_tool = SerperDevTool()

class TravelAgents:
    def __init__(self):
        self.CHATGroq = ChatGroq(model="groq/llama3-70b-8192", temperature=0)
    
    def locations_decider_agent(self):
        return Agent(
            role = "Cities/Location Decider Expert Agent",
            backstory = dedent(
                f"""Expert in deciding best locations/ best spots to visit near the destinations.
                I have decades of expierence finding best locations / best spots according to the weather of the location, number of days, number of travellers, budget, destination and travellers interests etc"""
            ),
            goal = dedent(
                f"""
                    Create a list of all the best locations to visit near the destination according to the number of days, number of travellers, budget, destination and Traveller interests.
                    Make sure that the locations/ spots are decided in a such a way that it maximizes user exerience in the trip and can explore the maximum but also should be practical
                    so that the trip can be covered in the given time frame and cost. Make sure to analyze the distance between the location and the time to cover it and accordingly plan the locations.
                """
            ),
            tools = [
                SearchTools.search_internet,
                CalculatorTools.calculate,
            ],
            verbose = True,
            llm = self.CHATGroq
        )
    
    

    def budget_planner_agent(self):
        return Agent(
            role = "Expense Planner",
            backstory = dedent(
                f"""Expert in planning and dividing budget for different activites to be done at different locations decided earlier.
                I have decades of experience making best budget allocation according to the number of days, number of travelers, travellers interset etc"""
            ),
            goal = dedent(
                f"""
                Create a practical budget breakdown according to the locations decided earlier for different activites according to the number of days, number of travellers according to the cities/ locations decided earlier.
                Make sure that cost allocated to each activites/ events is practical and in such a way tha it maximizes the overall experience of the travellers
                and also they can enjoy the trip to the fullest.
                """
            ),
            tools = [
                SearchTools.search_internet,
                CalculatorTools.calculate,
                # search_tool
            ],
            verbose = True,
            llm = self.CHATGroq
        ) 
    
    def expert_travel_agent(self):
        return Agent(
            role = "Expert Travel Agent",
            backstory = dedent(
                f"""Expert in travel planning and logistics.
                I have decades of experience making best travel budget iteneraries according to the number of travelers and days."""
            ),
            goal = dedent(
                f"""Create a travel itenary with detailed everyday plans of activites and different activites to do everyday,
                keeping into account number and type of traveler, budget ,no of days, packing suggestions, 
                and safety tips keeping everything to be cost effective. Make sure that cost of everything is practical and budget friendly"""
            ),
            tools = [
                SearchTools.search_internet,
                CalculatorTools.calculate,
                # search_tool
            ],
            verbose = True,
            llm = self.CHATGroq
        )

    def trip_finalizer_agent(self):
        return Agent(
            role = "Expert Trip Finalizer",
            backstory = dedent(
                f"""
                As a manager I have the sole responsibility to give the best trip plan according to all the data gathered by all the agents and user input.
                I have decades of experience and sole responsibility to make the best plan and make the user happy
                """
            ),
            goal = dedent(
                f"""
                Create a travel itenary with flow of trip from one location to another complete everyday plans and activites to be done,
                keeping into account number and type of traveller their intereset, budget, no of days, locations selected earlier as per weather and budget breakdown,
                also give them advice on packing suggestions as per activites and weather decided. also give them some safety tips as per local rituals ongoing scams,
                Keep everything budget friendly and best.
                """
            ),
            tools = [
                SearchTools.search_internet,
                CalculatorTools.calculate,
                # search_tool
            ],
            verbose = True,
            llm = self.CHATGroq
        )
    

    def search_agent(self):
        return Agent(
            role = "",
            backstory = dedent(
                f"""
                I have decades of experience answering travel and trip related questions of any domain user asks for according to the trip planned."""
            ),
            goal = dedent(
                f"""
                Prepare a best answer for the query asked by the user and their trip details.
                Try preparing the best and most relevant answer for the user
                """
            ),
            tools = [
                SearchTools.search_internet,
                CalculatorTools.calculate,
                # search_tool
            ],
            verbose = True,
            llm = self.CHATGroq
        )