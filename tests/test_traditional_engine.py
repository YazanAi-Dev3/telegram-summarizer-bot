# tests/test_traditional_engine.py

# We import the specific function we want to test
from app.engine_traditional import summarize_chunk

def test_summarize_chunk_returns_string():
    """
    Tests if the summarizer returns a string for a valid input.
    """
    sample_text = (
        "This is the first sentence of our test. "
        "This second sentence provides more context. "
        "The third sentence is here to add length. "
        "Another sentence makes the text even longer. "
        "We need enough sentences for the summarizer to work. "
        "The final sentence concludes our sample paragraph."
    )
    
    # Call the function we are testing
    summary = summarize_chunk(sample_text)
    
    # Assert that the output is of the correct type (a string)
    assert isinstance(summary, str)

def test_summarize_chunk_not_empty():
    """
    Tests if the summarizer returns a non-empty string for a sufficiently long text.
    """
    sample_text = (
        "This is the first sentence of our test. "
        "This second sentence provides more context. "
        "The third sentence is here to add length. "
        "Another sentence makes the text even longer. "
        "We need enough sentences for the summarizer to work. "
        "The final sentence concludes our sample paragraph."
    )
    
    summary = summarize_chunk(sample_text)
    
    # Assert that the summary string is not empty
    assert len(summary) > 0

def test_summarize_chunk_empty_input():
    """
    Tests how the function behaves with an empty string input.
    """
    summary = summarize_chunk("")
    
    # Assert that for an empty input, we get an empty output
    assert summary == ""