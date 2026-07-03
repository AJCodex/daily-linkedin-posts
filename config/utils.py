"""
Utility functions for API requests, retry logic, and error handling.
Provides reusable functions for robust API interactions.
"""

import requests
import time
from typing import Optional, Dict, Any
from .logger import get_logger
from .constants import MAX_RETRIES, INITIAL_RETRY_DELAY, EXPONENTIAL_BASE

logger = get_logger(__name__)


def validate_api_key(api_key: Optional[str], name: str) -> None:
    """
    Validate that API key is present.
    
    Args:
        api_key: API key value
        name: API key name (for error message)
        
    Raises:
        ValueError: If API key is missing
    """
    if not api_key or not api_key.strip():
        raise ValueError(f"Missing required API key: {name}")


def validate_url(url: Optional[str]) -> bool:
    """
    Basic URL validation.
    
    Args:
        url: URL to validate
        
    Returns:
        True if URL is valid HTTP(S), False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    return url.startswith(("http://", "https://", "file://"))


def api_request_with_retry(
    method: str,
    url: str,
    headers: Dict[str, str],
    json_data: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    operation_name: str = "API Call"
) -> Optional[Dict[str, Any]]:
    """
    Make HTTP request with exponential backoff retry logic.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        url: API endpoint URL
        headers: HTTP headers
        json_data: JSON payload (for POST/PUT)
        timeout: Request timeout in seconds
        operation_name: Description for logging
        
    Returns:
        Response JSON on success, None on failure
        
    Raises:
        requests.exceptions.RequestException: After exhausting retries
    """
    
    if method.upper() not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        raise ValueError(f"Invalid HTTP method: {method}")
    
    if not validate_url(url):
        raise ValueError(f"Invalid URL: {url}")
    
    delay = INITIAL_RETRY_DELAY
    last_error = None
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.debug(f"{operation_name} (attempt {attempt}/{MAX_RETRIES}): {url}")
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=json_data, timeout=timeout)
            else:
                response = requests.request(method, url, headers=headers, json=json_data, timeout=timeout)
            
            response.raise_for_status()
            logger.debug(f"{operation_name} successful (status: {response.status_code})")
            return response.json() if response.text else {}
            
        except requests.exceptions.Timeout:
            last_error = f"Request timeout after {timeout}s"
            logger.warning(f"{operation_name}: {last_error}")
            
        except requests.exceptions.ConnectionError as e:
            last_error = f"Connection error: {str(e)}"
            logger.warning(f"{operation_name}: {last_error}")
            
        except requests.exceptions.HTTPError as e:
            # Don't retry on 4xx errors (except 429 - rate limit)
            if e.response.status_code == 429:
                last_error = "Rate limited (429)"
                logger.warning(f"{operation_name}: {last_error}")
            elif e.response.status_code == 409:
                # 409 Conflict - don't retry, return error
                logger.info(f"{operation_name}: Conflict (409) - content already posted")
                return {"error": "409 Conflict", "response": e.response}
            elif 400 <= e.response.status_code < 500:
                # Client error - don't retry
                logger.error(f"{operation_name}: Client error ({e.response.status_code}): {e}")
                return {"error": str(e), "status_code": e.response.status_code}
            else:
                last_error = f"HTTP error {e.response.status_code}: {str(e)}"
                logger.warning(f"{operation_name}: {last_error}")
        
        except ValueError as e:
            logger.error(f"{operation_name}: Invalid response data: {e}")
            return {"error": "Invalid response format"}
        
        except Exception as e:
            last_error = f"Unexpected error: {type(e).__name__}: {str(e)}"
            logger.error(f"{operation_name}: {last_error}")
        
        # Don't retry after last attempt
        if attempt < MAX_RETRIES:
            logger.debug(f"Retrying after {delay}s...")
            time.sleep(delay)
            delay *= EXPONENTIAL_BASE
    
    # All retries exhausted
    logger.error(f"{operation_name} failed after {MAX_RETRIES} attempts. Last error: {last_error}")
    raise requests.exceptions.RequestException(f"{operation_name} failed: {last_error}")


def safe_json_load(file_path: str, operation_name: str = "Load JSON") -> Optional[Dict[str, Any]]:
    """
    Safely load JSON file with error handling.
    
    Args:
        file_path: Path to JSON file
        operation_name: Description for logging
        
    Returns:
        Parsed JSON data, None if error
    """
    import json
    import os
    
    if not os.path.exists(file_path):
        logger.error(f"{operation_name}: File not found: {file_path}")
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"{operation_name}: Successfully loaded {file_path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"{operation_name}: Invalid JSON in {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"{operation_name}: Error reading {file_path}: {e}")
        return None
