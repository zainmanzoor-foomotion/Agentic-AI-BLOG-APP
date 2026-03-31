from src.states.blog_state import BlogState
from langchain_core.messages import HumanMessage
from src.states.blog_state import Blog

class BlogNode:
    """Blog generation nodes"""
    def __init__(self, llm):
        self.llm = llm
    
    def title_creation(self, state:BlogState):
        """create title of blog"""
        if "topic" in state and state['topic']:
            prompt=""" You are expert blog content writer. You marked down formatting. 
            Generate a blog title for the {topic}. This title should be creative and seo friendly and dont provide the think part"""

            system_msg=prompt.format(topic=state['topic'])
            response = self.llm.invoke(system_msg)
            return {"blog": {"title": response.content}}
    
    def content_generation(self, state:BlogState):
        """generate the content of blog"""
        if "topic" in state and state['topic']:
            prompt=""" You are expert blog content writer. You marked down formatting. 
            Generate a detailed blog content with detailed breakdown for the {topic}. This content should be creative and seo friendly 
            and dont provide the think part in response"""

            system_msg=prompt.format(topic=state['topic'])
            response = self.llm.invoke(system_msg)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}

    def translation(self, state: BlogState):
        """
        Translate the content to the specified language.
        """
        translation_prompt = """
        Translate the following content into {current_language}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.

        ORIGINAL CONTENT:
        {blog_content}
        """

        blog_content=state['blog']['content']
        current_language=state['current_language']
        
        message=[HumanMessage(translation_prompt.format(current_language=current_language, blog_content=blog_content))]
        translation_content=self.llm.invoke(message)
        return {"blog": {"content": translation_content.content}}
    
    def route(self, state: BlogState):
        return {"current_language": state['current_language']}
    
    def route_decision(self, state: BlogState):
        """
        Route to translation nodes based on language selection.
        """
        if state['current_language'] == "urdu":
            return "urdu"
        elif state['current_language'] == "punjabi":
            return "punjabi"
        else:
            return state['current_language']