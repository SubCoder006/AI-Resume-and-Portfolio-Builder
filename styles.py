"""
Custom CSS styles for the Streamlit app.
Provides modern, professional UI with gradient effects.
"""

import streamlit as st


def inject_styles():
    """Inject custom CSS into Streamlit app."""
    st.markdown("""
    <style>
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-mesh-orb {
        position: absolute;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        border-radius: 50%;
        top: -100px;
        right: -100px;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .hero h1 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    
    .subtitle {
        font-size: 1rem;
        opacity: 0.95;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    /* Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .card-icon {
        font-size: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin: 0;
        color: #2d3748;
    }
    
    .card-subtitle {
        font-size: 0.9rem;
        color: #718096;
        margin: 0;
    }
    
    /* Stepper */
    .stepper {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
        padding: 0 1rem;
    }
    
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        flex: 1;
    }
    
    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .step.pending .step-circle {
        background: #e2e8f0;
        color: #a0aec0;
    }
    
    .step.active .step-circle {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        animation: pulse 2s infinite;
    }
    
    .step.done .step-circle {
        background: #48bb78;
        color: white;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .step-label {
        font-size: 0.85rem;
        color: #4a5568;
        font-weight: 500;
    }
    
    .step-connector {
        position: absolute;
        top: 20px;
        left: calc(50% + 20px);
        width: calc(100% - 40px);
        height: 2px;
        background: #e2e8f0;
    }
    
    .step.done .step-connector {
        background: #48bb78;
    }
    
    /* Output Card */
    .output-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .output-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .output-text {
        background: #f7fafc;
        padding: 1rem;
        border-radius: 6px;
        border-left: 3px solid #667eea;
        max-height: 400px;
        overflow-y: auto;
    }
    
    /* Buttons */
    .btn-primary button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        transition: transform 0.2s ease !important;
    }
    
    .btn-primary button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4) !important;
    }
    
    .btn-export button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    .btn-download button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    /* Section Divider */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)