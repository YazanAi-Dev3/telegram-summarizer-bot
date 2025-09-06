# app/engine_traditional.py (Improved Arabic Version)

import logging
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from nltk.corpus import stopwords # Import stopwords from NLTK
from nltk.stem.isri import ISRIStemmer # Import the Arabic stemmer from NLTK

logger = logging.getLogger(__name__)

# --- Configuration for Arabic ---
LANGUAGE = "arabic"
SENTENCES_COUNT = 5 # Number of sentences to return in the summary

logger.info("Initializing Traditional (Sumy) engine with NLTK Arabic enhancements.")

def summarize_chunk(text: str) -> str:
    """
    Summarizes a single piece of text using an extractive (LSA) method,
    enhanced with NLTK's Arabic stemmer and stopwords.
    """
    logger.debug(f"Starting extractive summarization for an Arabic chunk with length: {len(text)}")
    
    # Use a tokenizer that understands Arabic.
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    
    # Initialize the Arabic stemmer from NLTK.
    stemmer = ISRIStemmer()
    
    # Initialize the LSA summarizer and provide it with our new stemmer.
    summarizer = LsaSummarizer(stemmer)
    
    # Use the comprehensive list of Arabic stopwords from NLTK.
    summarizer.stop_words = stopwords.words(LANGUAGE)
    
    # Generate the summary
    summary_sentences = [str(sentence) for sentence in summarizer(parser.document, SENTENCES_COUNT)]
    
    summary = " ".join(summary_sentences)
    
    logger.debug("Extractive summarization chunk completed successfully.")
    return summary