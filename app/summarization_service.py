# app/summarization_service.py

import logging
from app.config import SUMMARIZER_MODE

logger = logging.getLogger(__name__)

# --- The Engine Switcher ---
# Based on the config, we decide which function to use throughout this file.
if SUMMARIZER_MODE == "transformer":
    from app.engine_transformer import summarize_chunk, tokenizer
    MAX_UNITS_PER_CHUNK = 512 # Tokens
    logger.info("Summarization service is using the TRANSFORMER engine.")
    def count_units(text: str) -> int:
        return tokenizer(text, return_tensors="pt").input_ids.shape[1]
    def split_text_into_chunks(text: str) -> list[str]:
        tokens = tokenizer.encode(text)
        chunks = []
        for i in range(0, len(tokens), MAX_UNITS_PER_CHUNK):
            chunk_tokens = tokens[i:i + MAX_UNITS_PER_CHUNK]
            chunks.append(tokenizer.decode(chunk_tokens, skip_special_tokens=True))
        return chunks

else: # Default to traditional
    from app.engine_traditional import summarize_chunk
    MAX_UNITS_PER_CHUNK = 1500 # Words
    logger.info("Summarization service is using the TRADITIONAL engine.")
    def count_units(text: str) -> int:
        return len(text.split())
    def split_text_into_chunks(text: str) -> list[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), MAX_UNITS_PER_CHUNK):
            chunk_words = words[i:i + MAX_UNITS_PER_CHUNK]
            chunks.append(" ".join(chunk_words))
        return chunks

# The rest of the file remains the same, but it will now use the correct
# `summarize_chunk`, `count_units`, and `split_text_into_chunks` based on the mode.

def create_summary(messages: list[str]) -> str:
    logger.info(f"Received {len(messages)} messages to summarize.")
    full_conversation_text = "\n".join(messages)

    if not full_conversation_text.strip():
        logger.warning("Attempted to summarize an empty conversation.")
        return "المحادثة فارغة، لا يوجد شيء لتلخيصه."

    unit_count = count_units(full_conversation_text)
    logger.info(f"Total unit count of conversation is: {unit_count} ({'tokens' if SUMMARIZER_MODE == 'transformer' else 'words'})")

    if unit_count <= MAX_UNITS_PER_CHUNK:
        logger.info("Unit count is within the limit. Using single-pass summarization.")
        return summarize_chunk(full_conversation_text)
    else:
        logger.info("Unit count exceeds the limit. Using hierarchical summarization.")
        chunks = split_text_into_chunks(full_conversation_text)
        logger.info(f"Split text into {len(chunks)} chunks for summarization.")
        
        intermediate_summaries = [summarize_chunk(chunk) for chunk in chunks]
        combined_summary_text = "\n".join(intermediate_summaries)
        
        logger.info("Summarizing the combined intermediate summaries to get the final result.")
        final_summary = summarize_chunk(combined_summary_text)
        return final_summary