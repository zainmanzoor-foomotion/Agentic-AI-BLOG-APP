from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.blog_state import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self,llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)
    
    def build(self):
        return self.graph
    
    def build_topic_graph(self):
        """Build the graph to generate blogs using based on topic"""

        self.blog_node = BlogNode(self.llm)

        self.graph.add_node("title_creation", self.blog_node.title_creation)
        self.graph.add_node("content_generation", self.blog_node.content_generation)
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)
        return self.graph
    
    def build_language_graph(self):
        """
        Build the graph to generate blogs using based on language
        """

        self.blog_node = BlogNode(self.llm)
        self.graph.add_node("title_creation", self.blog_node.title_creation)
        self.graph.add_node("content_generation", self.blog_node.content_generation)
        self.graph.add_node("urdu_translation", lambda state: self.blog_node.translation({**state, "current_language": "urdu"}))
        self.graph.add_node("punjabi_translation", lambda state: self.blog_node.translation({**state, "current_language": "punjabi"}))
        self.graph.add_node("route", self.blog_node.route)
        
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", "route")

        self.graph.add_conditional_edges('route',self.blog_node.route_decision,{
            "urdu":"urdu_translation",
            "punjabi":"punjabi_translation"
        })

        self.graph.add_edge("urdu_translation", END)
        self.graph.add_edge("punjabi_translation", END)

        return self.graph

    def setup_graph(self,usecase):
        if usecase == "topic":
            self.build_topic_graph()
            return self.graph.compile()
        elif usecase == "language":
            self.build_language_graph()
            return self.graph.compile()
        else:
            raise ValueError("Invalid usecase")
