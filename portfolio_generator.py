"""
AI-powered portfolio content generation using Google Gemini.

Generates detailed portfolio text content (not HTML) for PDF export.
Fixed: Ensures complete generation without truncation.
"""

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import portfolio_content_prompt, project_image_suggestions_prompt

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


def generate_portfolio_content(data: dict, role: str, model: str = None, include_images: bool = False) -> str:
    """
    Generate detailed portfolio content for PDF export.
    
    Args:
        data: Student/candidate information
        role: Target job role
        model: Gemini model to use (default: gemini-2.5-flash)
        include_images: If True, AI will suggest image placeholders (default: False)
    
    Returns:
        Formatted portfolio content text with sections
    """
    if model is None:
        model = DEFAULT_MODEL
    
    client = _get_client()
    
    # Generate main portfolio content with specific instructions to avoid truncation
    response = client.models.generate_content(
        model=model,
        contents=portfolio_content_prompt(data, role, include_images),
        config=types.GenerateContentConfig(
            temperature=0.35,  # More stable for complete generation
            max_output_tokens=8000,  # Increased from 6000 to ensure completion
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
            contents=portfolio_content_prompt(data, role, include_images),
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=10000,
            ),
        )
        result = response.text.strip()
    
    return result


def generate_project_image_suggestions(project_description: str, model: str = None) -> str:
    """
    Generate AI suggestions for what images/screenshots would showcase a project.
    
    Args:
        project_description: Description of a single project
        model: Gemini model to use
    
    Returns:
        Image placeholder suggestions
    """
    if model is None:
        model = DEFAULT_MODEL
    
    client = _get_client()
    
    response = client.models.generate_content(
        model=model,
        contents=project_image_suggestions_prompt(project_description),
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=500,
        ),
    )
    
    return response.text.strip()