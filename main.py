import os
from crewai import Crew
from tasks import TravelTasks
from dotenv import load_dotenv
import streamlit as st
from agents import TravelAgents
from crewai import Process
from langchain_groq import ChatGroq
load_dotenv()

class TripCrew:
    def __init__(self, origin,no_of_days, destination, date_range, interests,budget,no_of_child,no_of_adults):
        self.origin = origin
        self.destination = destination
        self.date_range = date_range
        self.no_of_days = no_of_days
        self.intrests = interests
        self.budget = budget
        self.no_of_child = no_of_child
        self.no_of_adults = no_of_adults

    def run(self):
        # Define you custom agents and tasks in agents.py and tasks.py
        agents = TravelAgents()
        tasks = TravelTasks()

        # Define your custom agents and tasks here
        location_decider_agent = agents.locations_decider_agent()
        budget_planner_agent = agents.budget_planner_agent()
        expert_travel_agent = agents.expert_travel_agent()
        trip_flow_finalizer = agents.trip_finalizer_agent()

        divide_budget = tasks.divide_budget(
            budget_planner_agent,
            self.origin,
            self.destination,
            self.no_of_days,
            self.intrests,
            self.budget,
            self.no_of_child,
            self.no_of_adults
        )
        # Custom tasks include agent name and variables as input
        plan_itinerary = tasks.plan_itinerary(
            expert_travel_agent,
            self.no_of_days,
            self.destination,
            self.date_range,
            self.intrests,
            self.budget,
            self.no_of_child,
            self.no_of_adults
        )

        location_planner = tasks.locations_decider(
            location_decider_agent,
            self.no_of_days,
            self.intrests,
            self.budget,
            self.no_of_child,
            self.no_of_adults,
            self.origin,
            self.destination
            
        )

        trip_finalizer = tasks.finalize_trip(
            trip_flow_finalizer,
            self.origin,
            self.destination,
            self.intrests,
            self.no_of_days,
            self.date_range,
            self.budget,
            self.no_of_child,
            self.no_of_adults
            
        )
        

        crew = Crew(
            agents=[location_decider_agent,
                    budget_planner_agent,
                    expert_travel_agent,
                    trip_flow_finalizer,
                    ],
            tasks = [
                location_planner,
                divide_budget,
                plan_itinerary,
                trip_finalizer,
                ],
            # process=Process.hierarchical,
            # manager_llm=ChatGroq(model="groq/llama3-70b-8192"),
            verbose= True,

        )
        result = crew.kickoff()
        return result

class TripAnswer:
    def __init__(self, origin,no_of_days, destination, date_range, interests,budget,no_of_child,no_of_adults,query):
        self.origin = origin
        self.destination = destination
        self.date_range = date_range
        self.no_of_days = no_of_days
        self.intrests = interests
        self.budget = budget
        self.no_of_child = no_of_child
        self.no_of_adults = no_of_adults
        self.query = query

    def run(self):
        agents = TravelAgents()
        tasks = TravelTasks()
        search_agent = agents.search_agent()
        search_answer = tasks.answer_questions(
            search_agent,
            self.origin,
            self.destination,
            self.intrests,
            self.no_of_days,
            self.date_range,
            self.budget,
            self.no_of_child,
            self.no_of_adults,
            self.query
            
        )
        crew = Crew(
            agents = [search_agent,],
            tasks = [search_answer,],
            verbose=True,
        )
        result = crew.kickoff()
        return result