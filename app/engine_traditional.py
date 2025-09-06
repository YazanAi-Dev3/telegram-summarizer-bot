# app/engine_traditional.py (Corrected Stemmer Version)

import logging
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from nltk.corpus import stopwords
from nltk.stem.isri import ISRIStemmer

logger = logging.getLogger(__name__)

LANGUAGE = "arabic"
SENTENCES_COUNT = 5

logger.info("Initializing Traditional (Sumy) engine with NLTK Arabic enhancements.")

def summarize_chunk(text: str) -> str:
    """
    Summarizes a single piece of text using an extractive (LSA) method,
    enhanced with NLTK's Arabic stemmer and stopwords.
    """
    logger.debug(f"Starting extractive summarization for an Arabic chunk with length: {len(text)}")
    
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    
    # --- THE IMPORTANT CHANGE IS HERE ---
    # 1. Initialize the Arabic stemmer object from NLTK.
    stemmer_instance = ISRIStemmer()
    
    # 2. Initialize the LSA summarizer. We pass the .stem METHOD, not the whole object.
    summarizer = LsaSummarizer(stemmer_instance.stem)
    
    # Use the comprehensive list of Arabic stopwords from NLTK.
    summarizer.stop_words = stopwords.words(LANGUAGE)
    
    # Generate the summary
    summary_sentences = [str(sentence) for sentence in summarizer(parser.document, SENTENCES_COUNT)]
    
    summary = " ".join(summary_sentences)
    
    logger.debug("Extractive summarization chunk completed successfully.")
    return summary