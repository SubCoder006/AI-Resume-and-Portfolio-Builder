"""
AI-powered portfolio content generation using Google Gemini.

Generates pure text portfolio content for PDF export.
NO images, NO image references, NO placeholders - text only.
"""

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import portfolio_content_prompt

load_dotenv()

DEFAULT_MODEL = "gemini-2.5-flash"
_client = None


def _get_client():
    """Get or create Gemini client."""
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not set. Add it to .env\n"
                "Get a free key at https://aistudio.google.com/app/apikey"
            )
        _client = genai.Client(api_key=api_key)
    return _client


def generate_portfolio_content(data: dict, role: str, model: str = None) -> str:
    """
    Generate detailed pure text portfolio content for PDF export.
    
    NO images, NO image placeholders - pure text content only.
    
    Args:
        data: Student/candidate information
        role: Target job role
        model: Gemini model to use (default: gemini-2.5-flash)
    
    Returns:
        Formatted text-only portfolio content
    """
    if model is None:
        model = DEFAULT_MODEL
    
    client = _get_client()
    
    # Generate pure text portfolio content
    response = client.models.generate_content(
        model=model,
        contents=portfolio_content_prompt(data, role),
        config=types.GenerateContentConfig(
            temperature=0.35,  # Stable for complete generation
            max_output_tokens=10000,  # Ensure full content
            stop_sequences=None,  # Don't stop early
        ),
    )
    
    result = response.text.strip()
    
    # Validation: Check for truncation indicators
    truncation_indicators = ["...", " trad", " pro", "The trad", "This pro"]
    has_truncation = any(indicator in result for indicator in truncation_indicators)
    
    if has_truncation:
        print("Warning: Portfolio content may be truncated. Regenerating...")
        # Try once more with even more tokens
        response = client.models.generate_content(
            model=model,
            contents=portfolio_content_prompt(data, role),
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=20000,
            ),
        )
        result = response.text.strip()
    
    return result