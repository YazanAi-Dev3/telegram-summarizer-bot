# app/ai_model.py

import logging
from transformers import pipeline, AutoTokenizer # Import AutoTokenizer
import torch

logger = logging.getLogger(__name__)

# --- Configuration ---
# Use the new Arabic model
MODEL_NAME = "marefa-nlp/summarization-arabic-english-news"

# --- Model and Tokenizer Loading ---
logger.info(f"Loading summarization model and tokenizer for: {MODEL_NAME}")
device = 0 if torch.cuda.is_available() else -1

# Load the summarization pipeline (no change here)
summarizer = pipeline(
    "summarization",
    model=MODEL_NAME,
    device=device
)

# Load the tokenizer associated with our model
# We will use this in other parts of the app to count tokens
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

logger.info("Model and tokenizer loaded successfully.")

def summarize_chunk(text: str) -> str:
    """Summarizes a single piece of text (a chunk of a conversation)."""
    logger.debug(f"Starting summarization for a chunk of text with length: {len(text)}")
    summary_result = summarizer(text, max_length=256, min_length=30, do_sample=False)
    summary_text = summary_result[0]['summary_text']
    logger.debug("Summarization chunk completed successfully.")
    return summary_text
if __name__ == '__main__':
    print("--- Testing the AI Model Standalone ---")
    
    sample_conversation = """
    Alex: Hey team, I've pushed the latest changes for the login feature. Can someone review it?
    Sarah: On it. I'll check it out in the next hour.
    Mike: I saw the push. Looks good at a glance, but I noticed we're not handling the 'Forgot Password' case.
    Alex: Good catch, Mike. I completely forgot about that. I'll add a new task for it.
    Sarah: Review complete. The logic is solid, but please add some more comments to the session handling part. It's a bit complex.
    Alex: Will do. Thanks for the quick feedback, both of you!
    """
    
    print("\n[Original Conversation]")
    print(sample_conversation)
    
    # Call the function to get the summary
    summary = summarize_chunk(sample_conversation)
    
    print("\n[Generated Summary]")
    print(summary)
    print("\n--- Test Complete ---")