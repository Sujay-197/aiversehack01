"""
RAG-based Resume Parser using LangChain
Stores example parsed resumes and uses them for few-shot learning
"""
from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
import os
import json
import uuid
from backend.models import ResumeEvidence, Skill

class RAGResumeParser:
    """
    Resume parser using RAG for few-shot learning
    Stores example resumes and retrieves similar ones for context
    """
    
    # Example parsed resumes (few-shot learning pool)
    EXAMPLE_RESUMES = [
        {
            "resume_text": """
John Smith
john@email.com

Senior Software Engineer with 8 years building scalable systems

EXPERIENCE
- Staff Engineer, TechCorp (2020-2024, 4 years)
  Built microservices in Python and Go
  Managed team of 5 engineers
  
- Backend Engineer, StartupXYZ (2016-2020, 4 years)
  Developed REST APIs with Django
  Worked with PostgreSQL and Redis

SKILLS: Python, Go, Django, PostgreSQL, Redis, Docker, AWS
""",
            "parsed_output": {
                "full_name": "John Smith",
                "email": "john@email.com",
                "summary": "Senior Software Engineer with 8 years building scalable systems",
                "skills": [
                    {"name": "Python", "category": "Language", "years_of_experience": 8.0},
                    {"name": "Go", "category": "Language", "years_of_experience": 4.0},
                    {"name": "Django", "category": "Framework", "years_of_experience": 4.0},
                    {"name": "PostgreSQL", "category": "Database", "years_of_experience": 4.0},
                    {"name": "Docker", "category": "Tool", "years_of_experience": 3.0},
                    {"name": "AWS", "category": "Cloud", "years_of_experience": 3.0}
                ],
                "work_experience": [
                    {"title": "Staff Engineer", "company": "TechCorp", "years": 4.0},
                    {"title": "Backend Engineer", "company": "StartupXYZ", "years": 4.0}
                ]
            }
        },
        {
            "resume_text": """
Sarah Chen
sarah.chen@gmail.com

Full Stack Developer | React & Node.js Specialist

PROFESSIONAL EXPERIENCE
Frontend Engineer @ WebCo (2022-Present, 2 years)
- Built responsive UIs with React and TypeScript
- Implemented state management with Redux

Junior Developer @ AgencyCo (2020-2022, 2 years)
- Created landing pages with HTML/CSS/JavaScript
- Basic Node.js backend work

TECHNICAL SKILLS
Languages: JavaScript, TypeScript, HTML, CSS
Frameworks: React, Node.js, Express
Tools: Git, Webpack, npm
""",
            "parsed_output": {
                "full_name": "Sarah Chen",
                "email": "sarah.chen@gmail.com",
                "summary": "Full Stack Developer specializing in React and Node.js",
                "skills": [
                    {"name": "JavaScript", "category": "Language", "years_of_experience": 4.0},
                    {"name": "TypeScript", "category": "Language", "years_of_experience": 2.0},
                    {"name": "React", "category": "Framework", "years_of_experience": 2.0},
                    {"name": "Node.js", "category": "Framework", "years_of_experience": 4.0},
                    {"name": "HTML", "category": "Language", "years_of_experience": 4.0},
                    {"name": "CSS", "category": "Language", "years_of_experience": 4.0}
                ],
                "work_experience": [
                    {"title": "Frontend Engineer", "company": "WebCo", "years": 2.0},
                    {"title": "Junior Developer", "company": "AgencyCo", "years": 2.0}
                ]
            }
        }
    ]
    
    def __init__(self, api_key: str = None):
        """
        Initialize RAG parser
        
        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
        """
        key = api_key or os.getenv("GEMINI_API_KEY", "keyapi")
        
        if key == "keyapi":
            print("[WARNING] Using placeholder API key. Set GEMINI_API_KEY.")
        
        # Initialize LangChain components
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=key,
            temperature=0  # Deterministic for parsing
        )
        
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=key
        )
        
        # Build vector store from examples
        self.vector_store = self._build_vector_store()
    
    def _build_vector_store(self) -> FAISS:
        """
        Create FAISS vector store from example resumes
        """
        documents = []
        for idx, example in enumerate(self.EXAMPLE_RESUMES):
            # Store resume text + metadata about parsed output
            metadata = {
                "example_id": idx,
                "parsed_json": json.dumps(example["parsed_output"])
            }
            doc = Document(
                page_content=example["resume_text"],
                metadata=metadata
            )
            documents.append(doc)
        
        # Create vector store
        vector_store = FAISS.from_documents(
            documents,
            self.embeddings
        )
        
        return vector_store
    
    def parse(self, resume_text: str, user_id: uuid.UUID = None) -> ResumeEvidence:
        """
        Parse resume using RAG approach
        
        Args:
            resume_text: Raw resume text
            user_id: Optional user ID
            
        Returns:
            ResumeEvidence object
        """
        if user_id is None:
            user_id = uuid.uuid4()
        
        # Step 1: Retrieve similar resume examples
        similar_docs = self.vector_store.similarity_search(
            resume_text,
            k=2  # Get top 2 similar resumes
        )
        
        # Step 2: Build few-shot examples from retrieved docs
        few_shot_examples = []
        for doc in similar_docs:
            parsed_json = doc.metadata.get("parsed_json")
            few_shot_examples.append({
                "resume": doc.page_content,
                "parsed": parsed_json
            })
        
        # Step 3: Create prompt with examples
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a resume parser. Extract structured data as JSON.

Here are example parses to guide you:

{examples}

Now parse this resume following the same format:"""),
            ("user", "{resume_text}")
        ])
        
        # Format examples
        examples_str = "\n\n".join([
            f"Example {i+1}:\nResume:\n{ex['resume']}\n\nParsed Output:\n{ex['parsed']}"
            for i, ex in enumerate(few_shot_examples)
        ])
        
        # Step 4: Generate parse
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                "examples": examples_str,
                "resume_text": resume_text
            })
            
            # Extract JSON from response
            content = response.content
            
            # Try to parse JSON
            if "```json" in content:
                start = content.find("```json") + 7
                end = content.find("```", start)
                json_str = content[start:end].strip()
            else:
                json_str = content
            
            data = json.loads(json_str)
            
            # Convert to Pydantic models
            skills = [
                Skill(
                    name=s["name"],
                    category=s.get("category", "Technical"),
                    years_of_experience=s.get("years_of_experience", 0.0)
                )
                for s in data.get("skills", [])
            ]
            
            return ResumeEvidence(
                user_id=user_id,
                full_name=data.get("full_name", "Unknown"),
                email=data.get("email"),
                summary=data.get("summary"),
                skills=skills,
                work_experience=data.get("work_experience", []),
                education=data.get("education", [])
            )
        
        except Exception as e:
            print(f"[RAG Parser Error] {e}")
            # Fallback to empty resume
            return ResumeEvidence(
                user_id=user_id,
                full_name="Unknown",
                email=None,
                summary=None,
                skills=[],
                work_experience=[],
                education=[]
            )
    
    def add_example(self, resume_text: str, parsed_output: Dict):
        """
        Add new example to the RAG knowledge base
        Useful for continuous learning
        
        Args:
            resume_text: Raw resume
            parsed_output: Correct parsed output
        """
        # Add to examples list
        self.EXAMPLE_RESUMES.append({
            "resume_text": resume_text,
            "parsed_output": parsed_output
        })
        
        # Rebuild vector store
        self.vector_store = self._build_vector_store()
        print(f"[RAG Parser] Added new example. Total: {len(self.EXAMPLE_RESUMES)}")
