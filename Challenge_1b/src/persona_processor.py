"""
Persona Processor for Challenge 1B - Persona-Driven Document Intelligence
Applies persona-specific context and perspective to document analysis.
"""

import re
from typing import Dict, List, Any
from collections import Counter
import math


class PersonaProcessor:
    """Processes documents through a specific persona lens"""
    
    def __init__(self):
        # Define persona-specific keyword mappings
        self.role_terms = {
            "researcher": ["research", "study", "analysis", "methodology", "data", "experiment", "hypothesis", "literature", "publication", "findings", "results", "conclusion"],
            "student": ["learn", "study", "understand", "concept", "theory", "practice", "example", "exercise", "exam", "assignment", "knowledge", "skill"],
            "analyst": ["analyze", "evaluate", "assess", "trend", "pattern", "metric", "performance", "comparison", "forecast", "strategy", "insight", "recommendation"],
            "teacher": ["teach", "explain", "instruction", "curriculum", "lesson", "education", "training", "guidance", "demonstration", "assessment", "learning", "development"],
            "manager": ["manage", "plan", "organize", "control", "strategy", "decision", "resource", "team", "process", "objective", "performance", "leadership"],
            "entrepreneur": ["business", "opportunity", "market", "innovation", "startup", "venture", "revenue", "growth", "investment", "competition", "strategy", "scalability"]
        }
        
        # Job-to-be-done keywords
        self.task_terms = {
            "review": ["review", "summary", "overview", "evaluation", "assessment", "analysis"],
            "learn": ["learn", "understand", "study", "master", "practice", "acquire"],
            "analyze": ["analyze", "examine", "investigate", "evaluate", "assess", "compare"],
            "prepare": ["prepare", "plan", "organize", "design", "develop", "create"],
            "summarize": ["summarize", "condense", "extract", "highlight", "synthesize", "distill"]
        }

    def _compute_task_alignment_score(self, text_content: str, task_description: str) -> float:
        """Calculate how well content aligns with the specific job task"""
        normalized_content = text_content.lower()
        normalized_task = task_description.lower()
        
        # Extract key terms from job task
        task_keywords = set(re.findall(r'\b\w{4,}\b', normalized_task))  # Words with 4+ characters
        content_keywords = set(re.findall(r'\b\w{4,}\b', normalized_content))
        
        if not task_keywords:
            return 0.0
        
        # Calculate overlap
        matched_terms = len(task_keywords.intersection(content_keywords))
        similarity_score = matched_terms / len(task_keywords)
        
        return min(similarity_score, 1.0)

    def _extract_role_specific_observations(self, text_content: str, role_category: str, task_category: str) -> List[str]:
        """Extract insights specific to the persona's perspective"""
        observations = []
        normalized_text = text_content.lower()
        
        # Persona-specific insights
        if role_category == "researcher":
            if any(keyword in normalized_text for keyword in ["methodology", "method", "approach"]):
                observations.append("Research methodology identified")
            if any(keyword in normalized_text for keyword in ["data", "dataset", "sample"]):
                observations.append("Data sources and datasets mentioned")
            if any(keyword in normalized_text for keyword in ["result", "finding", "conclusion"]):
                observations.append("Research findings and results presented")
        
        elif role_category == "student":
            if any(keyword in normalized_text for keyword in ["concept", "principle", "theory"]):
                observations.append("Key concepts for learning identified")
            if any(keyword in normalized_text for keyword in ["example", "illustration", "case"]):
                observations.append("Examples and illustrations available")
            if any(keyword in normalized_text for keyword in ["exercise", "problem", "practice"]):
                observations.append("Practice materials and exercises found")
        
        elif role_category == "analyst":
            if any(keyword in normalized_text for keyword in ["trend", "pattern", "analysis"]):
                observations.append("Analytical insights and trends identified")
            if any(keyword in normalized_text for keyword in ["metric", "kpi", "performance"]):
                observations.append("Performance metrics and KPIs mentioned")
            if any(keyword in normalized_text for keyword in ["forecast", "prediction", "projection"]):
                observations.append("Forecasting and predictive information")
        
        # Job-specific insights
        if task_category == "review":
            if any(keyword in normalized_text for keyword in ["summary", "overview", "abstract"]):
                observations.append("Summary content suitable for review")
        elif task_category == "analyze":
            if any(keyword in normalized_text for keyword in ["comparison", "contrast", "versus"]):
                observations.append("Comparative analysis opportunities")
        
        return observations

    def _determine_importance_level(self, relevance_metric: float, observation_list: List[str], concept_list: List[str]) -> str:
        """Determine section priority based on persona analysis"""
        if relevance_metric >= 0.6 and len(observation_list) >= 2:
            return "high"
        elif relevance_metric >= 0.3 and (len(observation_list) >= 1 or len(concept_list) >= 3):
            return "medium"
        else:
            return "low"

    def _find_relevant_concepts(self, text_content: str, role_category: str) -> List[str]:
        """Identify key concepts relevant to the persona"""
        normalized_content = text_content.lower()
        word_tokens = re.findall(r'\b\w+\b', normalized_content)
        
        # Filter for relevant keywords based on persona
        applicable_terms = self.role_terms.get(role_category, [])
        
        # Count frequency of relevant words
        token_frequency = Counter(word_tokens)
        
        # Extract most common relevant concepts
        important_concepts = []
        for token in word_tokens:
            if (token in applicable_terms and 
                token_frequency[token] >= 1 and 
                len(token) > 3 and 
                token not in important_concepts):
                important_concepts.append(token)
        
        return important_concepts[:10]  # Return top 10 concepts

    def process_with_persona(self, doc_analysis: Dict[str, Any], user_persona: Dict[str, str], user_job: Dict[str, str]) -> Dict[str, Any]:
        """
        Process document analysis through persona perspective.
        
        Args:
            doc_analysis: Output from DocumentAnalyzer
            user_persona: Persona configuration with role description
            user_job: Job-to-be-done specification
            
        Returns:
            Enhanced analysis with persona-specific insights
        """
        role_description = user_persona.get("role", "").lower()
        task_description = user_job.get("task", "").lower()
        
        # Identify persona type
        detected_role = self._classify_user_role(role_description)
        detected_task = self._classify_user_task(task_description)
        
        # Process sections with persona context
        processed_sections = []
        for section_data in doc_analysis.get("sections", []):
            enhanced_data = self._augment_section_with_role_context(
                section_data, detected_role, detected_task, role_description, task_description
            )
            processed_sections.append(enhanced_data)
        
        # Generate persona-specific metadata
        role_metadata = self._build_role_analysis_summary(
            processed_sections, detected_role, role_description
        )
        
        return {
            "persona_type": detected_role,
            "persona_role": role_description,
            "job_type": task_description,
            "job_context": task_description,
            "sections": processed_sections
        }

    def _compute_relevance_score(self, text_content: str, role_category: str, task_category: str, task_description: str) -> float:
        """Calculate how relevant content is to the persona"""
        normalized_content = text_content.lower()
        word_tokens = re.findall(r'\b\w+\b', normalized_content)
        token_count = len(word_tokens)
        
        if token_count == 0:
            return 0.0
        
        # Score based on persona keywords
        role_specific_terms = self.role_terms.get(role_category, [])
        role_matches = sum(1 for token in word_tokens if token in role_specific_terms)
        role_relevance = role_matches / token_count
        
        # Score based on job keywords
        task_specific_terms = self.task_terms.get(task_category, [])
        task_matches = sum(1 for token in word_tokens if token in task_specific_terms)
        task_relevance = task_matches / token_count
        
        # Score based on specific job task terms
        task_word_set = set(re.findall(r'\b\w+\b', task_description.lower()))
        direct_matches = sum(1 for token in word_tokens if token in task_word_set and len(token) > 3)
        direct_relevance = direct_matches / token_count
        
        # Weighted combination
        combined_score = (0.4 * role_relevance + 0.3 * task_relevance + 0.3 * direct_relevance)
        
        return min(combined_score * 10, 1.0)  # Scale and cap at 1.0

    def _classify_user_task(self, task_description: str) -> str:
        """Identify the primary job type from task description"""
        normalized_task = task_description.lower()
        
        task_scores = {}
        for task_type, keyword_list in self.task_terms.items():
            score = sum(1 for keyword in keyword_list if keyword in normalized_task)
            if score > 0:
                task_scores[task_type] = score
        
        if task_scores:
            return max(task_scores, key=task_scores.get)
        
        return "general"

    def _build_role_analysis_summary(self, section_list: List[Dict[str, Any]], role_category: str, role_description: str) -> Dict[str, Any]:
        """Generate metadata about the persona analysis"""
        section_count = len(section_list)
        high_importance = sum(1 for section in section_list if section.get("persona_priority") == "high")
        medium_importance = sum(1 for section in section_list if section.get("persona_priority") == "medium")
        
        mean_relevance = sum(section.get("persona_relevance_score", 0) for section in section_list) / max(section_count, 1)
        
        combined_observations = []
        for section in section_list:
            combined_observations.extend(section.get("persona_insights", []))
        
        observation_frequency = Counter(combined_observations)
        key_observations = [insight for insight, count in observation_frequency.most_common(5)]
        
        return {
            "persona_type": role_category,
            "total_sections_analyzed": section_count,
            "high_priority_sections": high_importance,
            "medium_priority_sections": medium_importance,
            "low_priority_sections": section_count - high_importance - medium_importance,
            "average_relevance_score": round(mean_relevance, 3),
            "top_insights": key_observations
        }

    def _augment_section_with_role_context(self, section_data: Dict[str, Any], role_category: str, task_category: str, role_description: str, task_description: str) -> Dict[str, Any]:
        """Enhance a section with persona-specific analysis"""
        section_content = section_data.get("content", "")
        section_header = section_data.get("section_title", "")
        
        # Calculate persona relevance score
        relevance_metric = self._compute_relevance_score(section_content + " " + section_header, role_category, task_category, task_description)
        
        # Extract persona-specific insights
        role_observations = self._extract_role_specific_observations(section_content, role_category, task_category)
        
        # Identify key concepts
        important_concepts = self._find_relevant_concepts(section_content, role_category)
        
        # Enhanced section with persona context
        augmented_section = section_data.copy()
        augmented_section.update({
            "persona_relevance_score": relevance_metric,
            "persona_insights": role_observations,
            "key_concepts": important_concepts,
            "persona_priority": self._determine_importance_level(relevance_metric, role_observations, important_concepts),
            "job_alignment_score": self._compute_task_alignment_score(section_content + " " + section_header, task_description)
        })
        
        return augmented_section

    def _classify_user_role(self, role_description: str) -> str:
        """Identify the primary persona type from role description"""
        normalized_role = role_description.lower()
        
        role_scores = {}
        for role_type, keyword_list in self.role_terms.items():
            score = sum(1 for keyword in keyword_list if keyword in normalized_role)
            if score > 0:
                role_scores[role_type] = score
        
        if role_scores:
            return max(role_scores, key=role_scores.get)
        
        # Fallback based on common terms
        if any(term in normalized_role for term in ["phd", "research", "scientist", "academic"]):
            return "researcher"
        elif any(term in normalized_role for term in ["student", "undergraduate", "graduate"]):
            return "student"
        elif any(term in normalized_role for term in ["analyst", "investment", "business"]):
            return "analyst"
        elif any(term in normalized_role for term in ["teacher", "trainer", "instructor"]):
            return "teacher"
        elif any(term in normalized_role for term in ["manager", "director", "executive"]):
            return "manager"
        elif any(term in normalized_role for term in ["entrepreneur", "founder", "startup"]):
            return "entrepreneur"
        
        return "general"