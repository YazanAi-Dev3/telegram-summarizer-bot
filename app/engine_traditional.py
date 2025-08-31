# app/engine_traditional.py (Corrected Arabic-Enabled Version)

import logging
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer # <-- Corrected Import
# We don't need a stemmer for Arabic with this library, it can work without it.

logger = logging.getLogger(__name__)

# --- Configuration for Arabic ---
LANGUAGE = "arabic"
SENTENCES_COUNT = 5 # Number of sentences to return in the summary

ARABIC_STOP_WORDS = [
    "في", "من", "على", "و", "هو", "هي", "كان", "كانت", "أن", "أو", "إلى", "عن", 
    "هذا", "هذه", "ذلك", "تلك", "هنا", "هناك", "قد", "لقد", "أي", "مع", "به", "له",
    "قال", "قالت", "يكون", "تكون", "تم", "التي", "الذي", "الذين", "كل", "بعض", "ما"
]

logger.info("Initializing Traditional (Sumy) engine for ARABIC.")

def summarize_chunk(text: str) -> str:
    """
    Summarizes a single piece of text using an extractive (LSA) method,
    configured for the Arabic language.
    """
    logger.debug(f"Starting extractive summarization for an Arabic chunk with length: {len(text)}")
    
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    
    # Initialize the LSA summarizer
    summarizer = LsaSummarizer() # This should now be recognized
    
    # Set the custom stop words for Arabic
    summarizer.stop_words = ARABIC_STOP_WORDS
    
    # Generate the summary
    summary_sentences = [str(sentence) for sentence in summarizer(parser.document, SENTENCES_COUNT)]
    
    summary = " ".join(summary_sentences)
    
    logger.debug("Extractive summarization chunk completed successfully.")
    return summary