def is_valid_stock_code(stock_code):
    """
    Validate stock code format.
    A valid stock code should be alphanumeric and between 1 to 5 characters.
    """
    return stock_code.isalnum() and 1 <= len(stock_code) <= 5


def normalize_stock_code(stock_code):
    """
    Normalize stock code by converting to uppercase.
    """
    return stock_code.upper() if is_valid_stock_code(stock_code) else None


def check_stock_code_exists(stock_code):
    """
    Placeholder function to check if stock code exists in the database.
    In a real implementation, this would query a database or API.
    """
    # Example logic:
    # return stock_code in ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    return True  # Assuming all codes exist for this example

