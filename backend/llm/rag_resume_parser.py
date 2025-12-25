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
    
from backend.config import config

class RAGResumeParser:
    """
    Resume parser using RAG for few-shot learning
    Stores example resumes and retrieves similar ones for context
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize RAG parser
        
        Args:
            api_key: Gemini API key (defaults to Config.GEMINI_API_KEY)
        """
        key = api_key or config.GEMINI_API_KEY or "keyapi"
        
        if key == "keyapi":
            print("[WARNING] Using placeholder API key. Set GEMINI_API_KEY environment variable.")
        
        # Initialize LangChain components
        self.llm = ChatGoogleGenerativeAI(
            model=config.LLM.MODEL_NAME,
            google_api_key=key,
            temperature=config.LLM.TEMPERATURE_DETERMINISTIC
        )
        
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=config.LLM.EMBEDDING_MODEL,
            google_api_key=key
        )
        
        # Build vector store from examples
        self.vector_store = self._build_vector_store()
    
    def _load_examples(self) -> List[Dict]:
        """Load examples from JSON file"""
        try:
            with open(config.RAG_EXAMPLES_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[WARNING] Examples file not found at {config.RAG_EXAMPLES_PATH}")
            return []

    def _build_vector_store(self) -> FAISS:
        """
        Create FAISS vector store from example resumes
        """
        documents = []
        examples = self._load_examples()
        
        for idx, example in enumerate(examples):
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
        if not documents:
             # Create empty store if no docs (handled by LangChain usually, or use dummy)
             pass 

        vector_store = FAISS.from_documents(
            documents,
            self.embeddings
        )
        
        return vector_store
        
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
        Useful for continuous learning. Persists to JSON file.
        
        Args:
            resume_text: Raw resume
            parsed_output: Correct parsed output
        """
        # Load existing
        examples = self._load_examples()
        
        # Add new
        examples.append({
            "resume_text": resume_text,
            "parsed_output": parsed_output
        })
        
        # Save back to file
        try:
            with open(config.RAG_EXAMPLES_PATH, 'w', encoding='utf-8') as f:
                json.dump(examples, f, indent=2)
            print(f"[RAG Parser] Added new example and saved to file. Total: {len(examples)}")
        except Exception as e:
             print(f"[RAG Parser Error] Failed to save example: {e}")
        
        # Rebuild vector store
        self.vector_store = self._build_vector_store()
