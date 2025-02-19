__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import sys
from crewai import Crew, Process
from news_agents import NewsAgents, StreamToExpander
from news_tasks import NewsTasks
#from template.fin_template import fin_template


st.set_page_config(page_icon="📰", page_title="Ai News Letter", layout="wide")

def get_report(output_file):
      with open(output_file, 'r') as file:
          file = file.read()
          st.markdown(file)


def download_report(output_file):
  if output_file:
      with open(output_file, 'r') as file:
          st.download_button(
              label=f"📥 {output_file}",
              use_container_width=True,
              data=file,
              file_name=output_file,
              mime='text/markdown'
          )
  else:
      st.error(f"No output file found for task: {output_file}")

# class TravelCrew
class TheCrew():

  def __init__(self, topic, model_name):
      self.topic = topic
      self.model_name = model_name
      self.output_placeholder = st.empty()


  def run(self):
      #agents = BlogAgents()
      agents = NewsAgents(self.model_name)
      tasks = NewsTasks()

      news_agent = agents.news_agent()
      writer_agent = agents.writer_agent()

      news_task = tasks.news_task(self.topic, news_agent)
      #writer_task = tasks.writer_task(self.topic, writer_agent)
      writer_task = tasks.writer_task(self.topic, writer_agent, news_task)

      crew = Crew(
        #agents=[news_agent, writer_agent],
        agents=[news_agent],
        #tasks=[news_task, writer_task],
        tasks=[news_task],
        process=Process.sequential,
        full_output=True,
        share_crew=False,
        #llm=llm_groq,
        #manager_llm=llm,
        #max_iter=24,
        verbose=True
        )

      result = crew.kickoff()
      self.output_placeholder.markdown(result)

      #st.session_state['result'] = result

      return result


## -----
st.header("📅 Weekly :orange-background[News Letter] :orange[Ai]gent 🤖", divider="orange")

# app info
with st.sidebar:
    with st.expander('🤖 0xZee App Info', expanded=False):      
        st.write("🤖 Ai-Generated Weekly News Letter App : Use Ai to egte your weekliy news letter about a specific topic.")
        st.caption("💻 Build with : Streamlit, CrewAi, DuckDuckGo, LLM llama3, Groq API for inference.")
        st.code("github.com/0xZee/streamlit-chatbot")

    # Get an Groq API Key before continuing
    st.subheader("🔐 Groq API Key", divider="violet")
    if "GROQ_API" in st.secrets:
        GROQ_API = st.secrets['GROQ_API']
        st.success("✅ GROQ API Key Set")
    else:
        GROQ_API = st.text_input("Groq API Key", type="password")
    if not GROQ_API:
        st.info("Enter an OpenAI API Key to continue")
        st.stop()
    
    st.sidebar.subheader("🤖 LLM Model", divider="violet")
    # here the model name to take as input in blog_agents.py
    model_name = st.sidebar.selectbox(
        "Select Model (META, MISTRAL, GOOGLE) ", ("llama3-8b-8192", "gemma2-9b-it", "gemma-7b-it", "mixtral-8x7b-32768"))
    st.sidebar.divider()


# User Details container
topic = st.text_input("📰 Enter Your Topic for the News Letter :", placeholder="Ai, Green Energy, Space Exploration...")

plan = st.button("💫 Generate News Letter", use_container_width=True, disabled=not topic)

# Initialize BlogCrew and store it in session state
#if 'blog_crew' not in st.session_state:
#    st.session_state['blog_crew'] = BlogCrew(topic)



# out container
if plan :
  #st.caption("👌 Let's Recap Your Topic Blog :")
  #st.write(f":sparkles: 🎫 Your Ai-Generated Blog : {topic} 📈.")
  #
  with st.spinner(text="🤖 Agents working for the NewsLetter 🔍 ..."):
    # RUN
    with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
      with st.container(height=400, border=False):
          sys.stdout = StreamToExpander(st)
          # CrewAi Launch
          #blog_crew = st.session_state['blog_crew']
          #blog_crew = BlogCrew(topic)
          the_crew = TheCrew(topic, model_name)
          result = the_crew.run()
          
      status.update(label=f" Blog {topic} Ai-Generated ! ✨",
                    state="complete", expanded=False)

    st.subheader(f"📰 {topic} Blog 🖋️", anchor=False, divider="grey")
    st.markdown(result["final_output"])
    st.divider()

    with st.expander('report_task_news.md', expanded=False):
        st.caption('Render report here..')
        get_report('report_task_news.md')
    with st.expander('report_task_writer.md', expanded=False):
        st.caption('Render report here..')
        get_report('report_task_writer.md')
    st.divider()
      
    # downloads reports
    #x, y = st.columns(2)
    #with x:
    #    download_report("blog_report_task_editor.md")
    #with y:
    #    download_report("blog_report_task_writer.md")

    #st.divider()
    # Display each key-value pair in 'usage_metrics'
    #st.json(result['usage_metrics'], expanded=False)
    # expander for each 'exported_output'
    #for i, task in enumerate(result['tasks_outputs']):
    #    with st.expander(f"Agent Processing {i+1} :", expanded=False):
    #        st.markdown(task)
    #st.divider()










