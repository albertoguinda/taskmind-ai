"""
Mock AI Engine.

Simple rule-based AI for development without downloading models.
"""

import re
from typing import List

from apps.tasks.domain import Analysis, UrgencyScore
from .ai_service import AIService


class MockAIEngine(AIService):
    """
    Mock AI engine using simple keyword matching.
    
    This is used for development/testing without loading real AI models.
    It provides fast, deterministic results for demo purposes.
    """
    
    # Keywords that indicate urgency
    URGENT_KEYWORDS = {
        'urgent', 'asap', 'immediately', 'critical', 'emergency',
        'production', 'down', 'broken', 'bug', 'error', 'crash',
        'security', 'vulnerability', 'exploit', 'breach',
    }
    
    HIGH_KEYWORDS = {
        'important', 'priority', 'deadline', 'client', 'customer',
        'issue', 'problem', 'fix', 'resolve', 'blocked',
    }
    
    def analyze_task_text(self, text: str) -> Analysis:
        """
        Analyze text using keyword matching.
        
        Args:
            text: Task text to analyze
            
        Returns:
            Analysis with calculated urgency
        """
        text_lower = text.lower()
        
        # Calculate urgency score based on keyword matches
        urgency = self._calculate_urgency(text_lower)
        
        # Extract keywords
        keywords = self._extract_keywords(text_lower)
        
        # Simple sentiment (positive if no negative words)
        sentiment = self._calculate_sentiment(text_lower)
        
        return Analysis(
            urgency_score=UrgencyScore(value=urgency),
            keywords=keywords,
            confidence=0.9,  # Mock confidence
            sentiment=sentiment,
        )
    
    def _calculate_urgency(self, text: str) -> float:
        """Calculate urgency score from text."""
        score = 0.5  # Base score
        
        # Check for urgent keywords
        urgent_count = sum(1 for kw in self.URGENT_KEYWORDS if kw in text)
        high_count = sum(1 for kw in self.HIGH_KEYWORDS if kw in text)
        
        # Increase score based on matches
        score += urgent_count * 0.15
        score += high_count * 0.08
        
        # Check for urgency indicators
        if '!' in text:
            score += 0.1
        if any(word in text for word in ['now', 'today', 'tonight']):
            score += 0.1
        
        # Cap at 1.0
        return min(score, 1.0)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        # Find all words that match urgent or high priority keywords
        found_keywords = []
        
        for keyword in self.URGENT_KEYWORDS | self.HIGH_KEYWORDS:
            if keyword in text:
                found_keywords.append(keyword)
        
        # Also extract capitalized words (likely important)
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        found_keywords.extend(words[:3])  # Max 3 capitalized words
        
        return list(set(found_keywords))[:10]  # Max 10 keywords
    
    def _calculate_sentiment(self, text: str) -> float:
        """Calculate sentiment score."""
        negative_words = {'problem', 'issue', 'bug', 'error', 'broken', 'fail'}
        positive_words = {'improve', 'enhance', 'optimize', 'feature', 'add'}
        
        neg_count = sum(1 for word in negative_words if word in text)
        pos_count = sum(1 for word in positive_words if word in text)
        
        # Simple calculation
        if neg_count > pos_count:
            return -0.3
        elif pos_count > neg_count:
            return 0.3
        return 0.0