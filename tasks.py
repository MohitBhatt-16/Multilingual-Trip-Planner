from crewai import Task
from textwrap import dedent

# This is an example of how to define custom tasks.
# You can define as many tasks as you want
# You can also define custom agents in agents.py

"""
Creating Tasks Cheat Sheet:
- Begin with the end in mind. Identify the specific outcome your tasks are aiming to achieve.
- Break down the outcome into actionable task, assigning each task to the appropriate agent.
- Ensure tasks are descriptive, providing clear insturctions and expected deliverables.

Goal:
- Develop a detailed itinerary, inclucding city selection, attractions, and practical travel advice.

Key Steps for Task Creation;
1. Identify the Desired Outcome: Define what success looks like for your project.
    -A detailed travel Itenary.

2. Task Breakdown: Divide the goal into smaller, managebale tasks that agents can execute.
    - Itenary Planning: develop a detailed plan for each day of the trip
    - City Selection: Analyze and pick the best cities to visit.
    - Local Tour Guide: Find a local expert to provide insights and recommendations
    - Accommodation Decider : Find and analyze the best accommodation
    - Transportation Planner : Find the best transportation plan which is cost effetive and practical
    - manage_budget : Analyze all the cose in the trip to make the whole trip under budget
    - packing_suggestions : Suggest all the essentials things to pack according to weather, destination, travellers (child, adults)
    - weather_forecast : Find the complete weather forecast of all the cities places suggested.
    - safety_advice : Suggest the safety points to keep in mind according to the local customs, activites etc.
    
3. Assign tasks to Agents: Match tasks with agents based on their roes and expertise.
4. Task Description Template:
    - Use this template as a guide to define each task in your CrewAI application.
    - This template helps ensure that each task is clearly defined, actionable, and aligned with the specific goals of

Template : 
-----------
def [task_name](self, agent, [parameters]):
    return Task(description = dedent(f'''
    **Task**; [Provide a concise name or summary of the task]
    **Description**: [Detailed descripition of what the agent is expected to do, including actionable steps and expression]

    **Parameters**:
    - [Parameter 1]: [Description]
    - [Parameter 2]: [Description]
    ... [Add more parameters as needed]

    **Note**: [Optional section for incentives or encouragement for high-quality work. This can include tips, additional context, or motivations to encourage agents to deliver their best work]
    '''),agent = agent)
"""

class TravelTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a 10,000 ruppees commission!"
    

    def locations_decider(self, agent, no_of_days,interests, budget, no_of_child, no_of_adults, origin, destination):
        return Task(
            description = dedent(
                f"""
                **Task** : Decide the locations to visit.
                **Description** : Serch for all the locations and cities as per origin and destionation to visit as per travellers interest, budget etc.
                Finalize the best and feasibile locations and decide the flow of the trip as per the interest, budget, days etc.
                Make sure that flow is practical and best for the traveller to give the traveller best experience.
        

                **Parameters**:
                - No of Days: {no_of_days}
                - Traveler Interests : {interests}
                - Budget : {budget}
                - No of Child : {no_of_child}
                - No of Adults : {no_of_adults}
                - Origin : {origin}
                - Destination : {destination}
                **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output = "A complete list of best locations to visit as per time, distance, weather and traveler interest"
        )
    
    def divide_budget(self, agent, origin, destination, no_of_days,interests, budget, no_of_child, no_of_adults):
        return Task(
            description = dedent(
                f"""
                **Task** : Divide the budget for different things.
                **Description** : Divide the given budget practically for different things like transportation, food,
                hotel accommodation, places to visit, entry fees etc. Make sure that the budget is practically divided to
                bring the best of the trip allocate good budget for activites, entry fees of different places etc.

                **Parameters**:
                - No of Days: {no_of_days}
                - Origin : {origin}
                - Destination : {destination}
                - Traveler Interests : {interests}
                - Budget : {budget}
                - No of Child : {no_of_child}
                - No of Adults : {no_of_adults}
                **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output = "A practical budget breakdown of the assigned budget for different activites and locations decided "
        )
    def plan_itinerary(self, agent,no_of_days, city, travel_dates, interests, budget,no_of_child,no_of_adults):
        return Task(
            description = dedent(
                f"""
                **Task** : Develop a Travel Itinerary
                **Description** : Expand the city guide into a complete travel itinerary with detailed
                everyday plans and activites to do according to type and number of travellers, including weather forecasts, places to eat, packing suggestions,
                and a budget breakdown. You must suggest actual places to visit, actual hotels to stay, and actual restaurants to go to,
                This itineary should cover actual aspects of the trip from arrival to departure till we reaches to the origin back, integrating the city guide information with practical travel logistics.
                The Itenary should be decided according to the number of travelers and also their type like child or adult.

                **Parameters**:
                - City: {city}
                - Trip Date: {travel_dates}
                - No of days: {no_of_days}
                - Traveler Interests: {interests}
                - Budget: {budget}
                - No of Child: {no_of_child}
                - No of Adults: {no_of_adults} 

                **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output="A detailed demanded long travel everyday itinerary giving a detailed breakdown of things to do on each day including places to visit , hotels, restaurants, weather forecasts, packing suggestions, and a budget breakdown based on number and type of travelers"
        )
    
    def finalize_trip (self, agent, origin, cities, interests,no_of_days, travel_dates,budget,no_of_child,no_of_adults):
        return Task(
            description = dedent(f"""
                    **Task**: Finalize the whole trip
                    **Description**: Analyxe the whole data finded by you and other agents and decide the best trip baed on specific
                        criteria such as number and type of travellers, days in trip, weather patterns, seasonal events, budget specified, locations decided, distance between them
                        and travel costs,
                        This task involves comparing multiple locations, considering factors like current weather
                        conditions, distance between them, traveler interest found there, upcoming cultural or seasonal events, number of days left and overall travel expenses.
                        Your final answer must be a detailed report on the chosen city,
                        inculding actual transportation costs, weather forecast, attaractions, and budget specified 
                        try not to deflect much from the specified budget a little deflection is allowed 
                        try to decide the best practical of everything but cost effective, also stick with the format needed like everyday plans and flow of the trip according to distance and time to reach is very important etc.

                    **Parameters**:
                    - Origin: {origin}
                    - Cities: {cities}
                    - Interests: {interests}
                    - No of days: {no_of_days}
                    - Travel Date: {travel_dates}
                    - Budget: {budget}
                    - No of Child: {no_of_child}
                    - No of Adults: {no_of_adults}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output="A precise report on the chosen city,including number and type of travelers, transportation costs, weather forecast, and attractions. Also best packing and safety tips.Striclty stick to the format of output required like everyday plans for the travllers and flow"
        )
    

    def answer_questions (self, agent, origin, cities, interests,no_of_days, travel_dates,budget,no_of_child,no_of_adults,trip_planned,query):
        return Task(
            description = dedent(f"""
                    **Task**: Answer travellers queries
                    **Description**: Analyze traveler query and details and try to prepare the best answer containing solution of the travellers query as per its details and the trip planned previously
                                 The answer should be uptodate and accurate and should answer all the queries of the traveller
                    **Parameters**:
                    - Origin: {origin}
                    - Cities: {cities}
                    - Interests: {interests}
                    - No of days: {no_of_days}
                    - Travel Date: {travel_dates}
                    - Budget: {budget}
                    - No of Child: {no_of_child}
                    - No of Adults: {no_of_adults}
                    - Trip Planned: {trip_planned}
                    - Query: {query}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output="A precise, uptodate and best answer for the query asked by the traveller"
        )
    

    
