from datetime import datetime
from crewai import Task
#DuckDuckGoSearchRunTool DuckDuckGoSearchResults DuckDuckGoSearchRun
from langchain_groq import ChatGroq
from news_agents import NewsAgents




# TASKS
class NewsTasks():

    # Task: Location
    def news_task(self, topic, agent):
        return Task(
            description=f"""Use news_search tool to collect 11 recent news articles about {topic}.
            Then, compile them into 11 rich articles, each article 'body' along with 'source', article's 'date', 'image' and 'url'. 
            Please, proceed with first results you got, when Using news_search tool.
            """,
            expected_output ="""
            In markdown format with sections and bullets : A rich News Letter post with the 11 articles 'body', along with article's 'source', 'date' and 'url'.
            Use emojies in accordance in the beginings of the sections's titles.
            Here's a Markdown template to Follow : 
            # [Introduction]
            ## [Here A rich paragraph about {topic} trends based on the collected news]
            ---
            # [The News Letter for topic]
            ## [The output from news_agent for each news article]
            ### [News's 'title']
            ONLY IF 'image' is available : [News's 'image', format as : ![image](image)]]
            [News's 'body']
            [here display in a list : date, source, url of the news]
            """,
            agent=agent,
            output_file='report_task_news.md',
        )

    # Task: Location
    def writer_task(self, topic, agent, context):    
        return Task(
            description=f"""
            Develop a rich paragraph about {topic} trends based on the news as an introduction.
            Then, following below : render the 11 articles from news_agent context
            in a long news letter post with introduction and sections about {topic}.
            """,
            expected_output="""
            A rich structured News Letter post in markdown format.
            Use emojies in accordance in the beginings of the sections's titles.
            Format to Follow : 
            # [Introduction]
            ## [Section 1 : rich paragraph about {topic} trends based on the collected news]
            # [The News Letter for topic]
            ## [Section 2 : The output from news_agent for each news article]
            ### [News's 'title']
            ONLY IF 'image' is available : [News's 'image', format as : ![image](image)]]
            [News's 'body']
            [**here date, source, url of the news in a list**]
            """,
            agent=agent,
            context=[context],
            output_file='report_task_writer.md',
        )

    # tip section
    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $1000 and grant you any wish you want!"

#
