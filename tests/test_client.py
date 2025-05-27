"""
Unit tests for TransparenciaAPIClient with mocked responses.
"""

import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

import pytest
import requests

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.client import TransparenciaAPIClient, RateLimiter, CacheManager


class TestRateLimiter:
    """Test RateLimiter class."""
    
    def test_rate_limiter_allows_calls_within_limit(self):
        """Test that rate limiter allows calls within limit."""
        limiter = RateLimiter(max_calls=3, window_seconds=1)
        
        @limiter
        def test_func():
            return "success"
        
        # Should allow 3 calls
        for _ in range(3):
            assert test_func() == "success"
    
    def test_rate_limiter_blocks_excess_calls(self):
        """Test that rate limiter blocks excess calls."""
        limiter = RateLimiter(max_calls=2, window_seconds=0.5)
        call_count = 0
        
        @limiter
        def test_func():
            nonlocal call_count
            call_count += 1
            return call_count
        
        # Make rapid calls
        import time
        start = time.time()
        
        # First two should be immediate
        assert test_func() == 1
        assert test_func() == 2
        
        # Third should be delayed
        assert test_func() == 3
        
        elapsed = time.time() - start
        # Should have taken at least 0.5 seconds due to rate limiting
        assert elapsed >= 0.5


class TestCacheManager:
    """Test CacheManager class."""
    
    @pytest.fixture
    def cache_manager(self, tmp_path):
        """Create cache manager with temp directory."""
        return CacheManager(cache_dir=str(tmp_path / "cache"), ttl=3600)
    
    def test_cache_disabled(self, tmp_path, monkeypatch):
        """Test cache when disabled."""
        monkeypatch.setenv("CACHE_ENABLED", "false")
        cache = CacheManager(cache_dir=str(tmp_path / "cache"))
        
        # Should not cache when disabled
        cache.set("http://test.com", {"param": "value"}, {"data": "test"})
        result = cache.get("http://test.com", {"param": "value"})
        
        assert result is None
    
    def test_cache_set_and_get(self, cache_manager):
        """Test setting and getting from cache."""
        url = "http://test.com/api"
        params = {"page": 1, "size": 10}
        data = {"results": [1, 2, 3]}
        
        # Set cache
        cache_manager.set(url, params, data)
        
        # Get from cache
        cached_data = cache_manager.get(url, params)
        
        assert cached_data == data
    
    def test_cache_expiration(self, tmp_path):
        """Test cache expiration."""
        # Create cache with 1 second TTL
        cache = CacheManager(cache_dir=str(tmp_path / "cache"), ttl=1)
        
        url = "http://test.com/api"
        params = {"page": 1}
        data = {"results": "test"}
        
        # Set cache
        cache.set(url, params, data)
        
        # Should be available immediately
        assert cache.get(url, params) == data
        
        # Wait for expiration
        import time
        time.sleep(1.1)
        
        # Should be expired
        assert cache.get(url, params) is None
    
    def test_cache_key_generation(self, cache_manager):
        """Test cache key generation is consistent."""
        url = "http://test.com"
        params1 = {"b": 2, "a": 1}  # Different order
        params2 = {"a": 1, "b": 2}  # Different order
        
        key1 = cache_manager._get_cache_key(url, params1)
        key2 = cache_manager._get_cache_key(url, params2)
        
        # Keys should be same regardless of parameter order
        assert key1 == key2


class TestTransparenciaAPIClient:
    """Test TransparenciaAPIClient class."""
    
    @pytest.fixture
    def mock_env(self, monkeypatch):
        """Mock environment variables."""
        monkeypatch.setenv("TRANSPARENCIA_API_TOKEN", "test_token")
        monkeypatch.setenv("TRANSPARENCIA_API_EMAIL", "test@email.com")
        monkeypatch.setenv("API_RATE_LIMIT", "30")
        monkeypatch.setenv("API_TIMEOUT", "60")
        monkeypatch.setenv("CACHE_TTL", "3600")
        monkeypatch.setenv("LOG_LEVEL", "INFO")
    
    @pytest.fixture
    def client(self, mock_env, tmp_path, monkeypatch):
        """Create client instance with mocked environment."""
        # Use temp directory for cache
        monkeypatch.setattr("src.api.client.CacheManager.__init__", 
                            lambda self, **kwargs: CacheManager.__init__(
                                self, cache_dir=str(tmp_path / "cache"), ttl=3600))
        return TransparenciaAPIClient()
    
    def test_client_initialization_without_token(self, monkeypatch):
        """Test client initialization fails without token."""
        monkeypatch.delenv("TRANSPARENCIA_API_TOKEN", raising=False)
        
        with pytest.raises(ValueError, match="TRANSPARENCIA_API_TOKEN not found"):
            TransparenciaAPIClient()
    
    def test_client_initialization_with_token(self, client):
        """Test client initializes with proper configuration."""
        assert client.api_token == "test_token"
        assert client.api_email == "test@email.com"
        assert client.rate_limit == 30
        assert client.timeout == 60
        assert client.cache_ttl == 3600
    
    @patch('src.api.client.requests.Session.get')
    def test_make_request_success(self, mock_get, client):
        """Test successful API request."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_response.headers = {}
        mock_get.return_value = mock_response
        
        result = client._make_request("/test-endpoint", {"param": "value"})
        
        assert result == {"data": "test"}
        mock_get.assert_called_once()
    
    @patch('src.api.client.requests.Session.get')
    def test_make_request_with_rate_limit_header(self, mock_get, client):
        """Test request with rate limit headers."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_response.headers = {"X-Rate-Limit-Remaining": "25"}
        mock_get.return_value = mock_response
        
        result = client._make_request("/test-endpoint")
        
        assert result == {"data": "test"}
    
    @patch('src.api.client.requests.Session.get')
    def test_make_request_timeout(self, mock_get, client):
        """Test request timeout handling."""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        with pytest.raises(requests.exceptions.Timeout):
            client._make_request("/test-endpoint")
    
    @patch('src.api.client.requests.Session.get')
    def test_make_request_connection_error(self, mock_get, client):
        """Test connection error handling."""
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        with pytest.raises(requests.exceptions.ConnectionError):
            client._make_request("/test-endpoint")
    
    @patch('src.api.client.requests.Session.get')
    def test_make_request_http_error(self, mock_get, client):
        """Test HTTP error handling."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response
        
        with pytest.raises(requests.exceptions.HTTPError):
            client._make_request("/test-endpoint")
    
    @patch('src.api.client.requests.Session.get')
    def test_make_request_invalid_json(self, mock_get, client):
        """Test invalid JSON response handling."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid", "", 0)
        mock_response.headers = {}
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="Invalid JSON response"):
            client._make_request("/test-endpoint")
    
    @patch('src.api.client.TransparenciaAPIClient._make_request')
    def test_test_connection_success(self, mock_request, client):
        """Test connection test success."""
        mock_request.return_value = [{"codigo": "123"}]
        
        result = client.test_connection()
        
        assert result is True
        mock_request.assert_called_once_with("/orgaos-siafi", {"pagina": 1, "quantidade": 1})
    
    @patch('src.api.client.TransparenciaAPIClient._make_request')
    def test_test_connection_failure(self, mock_request, client):
        """Test connection test failure."""
        mock_request.side_effect = Exception("Connection failed")
        
        result = client.test_connection()
        
        assert result is False
    
    @patch('src.api.client.TransparenciaAPIClient._make_request')
    def test_get_contratos(self, mock_request, client):
        """Test get_contratos method."""
        expected_data = [{"contrato": "123"}]
        mock_request.return_value = expected_data
        
        result = client.get_contratos(ano=2023)
        
        assert result == expected_data
        mock_request.assert_called_once_with("/contratos", {"ano": 2023})
    
    @patch('src.api.client.TransparenciaAPIClient._make_request')
    def test_get_servidores(self, mock_request, client):
        """Test get_servidores method."""
        expected_data = [{"nome": "João"}]
        mock_request.return_value = expected_data
        
        result = client.get_servidores(nome="João")
        
        assert result == expected_data
        mock_request.assert_called_once_with("/servidores", {"nome": "João"})
    
    @patch('src.api.client.TransparenciaAPIClient._make_request')
    def test_get_empresas_sancionadas_valid_type(self, mock_request, client):
        """Test get_empresas_sancionadas with valid type."""
        expected_data = [{"empresa": "ABC"}]
        mock_request.return_value = expected_data
        
        result = client.get_empresas_sancionadas(tipo="ceis")
        
        assert result == expected_data
        mock_request.assert_called_once_with("/ceis", {})
    
    def test_get_empresas_sancionadas_invalid_type(self, client):
        """Test get_empresas_sancionadas with invalid type."""
        with pytest.raises(ValueError, match="Tipo de sanção inválido"):
            client.get_empresas_sancionadas(tipo="invalid")
    
    @patch('src.api.client.TransparenciaAPIClient._make_request')
    def test_get_orgaos_valid_sistema(self, mock_request, client):
        """Test get_orgaos with valid sistema."""
        expected_data = [{"codigo": "123"}]
        mock_request.return_value = expected_data
        
        result = client.get_orgaos(sistema="siafi")
        
        assert result == expected_data
        mock_request.assert_called_once_with("/orgaos-siafi", {})
    
    def test_get_orgaos_invalid_sistema(self, client):
        """Test get_orgaos with invalid sistema."""
        with pytest.raises(ValueError, match="Sistema inválido"):
            client.get_orgaos(sistema="invalid")
    
    @patch('src.api.client.TransparenciaAPIClient._make_request')
    def test_paginate_single_page(self, mock_request, client):
        """Test pagination with single page."""
        mock_request.return_value = [{"id": 1}, {"id": 2}]
        
        # Create a mock method
        mock_method = Mock(side_effect=lambda **kwargs: mock_request("endpoint", kwargs))
        
        result = client.paginate(mock_method, max_pages=1, page_size=10)
        
        assert len(result) == 2
        assert result == [{"id": 1}, {"id": 2}]
    
    @patch('src.api.client.TransparenciaAPIClient._make_request')
    def test_paginate_multiple_pages(self, mock_request, client):
        """Test pagination with multiple pages."""
        # Return different data for each page, empty on third
        mock_request.side_effect = [
            [{"id": 1}, {"id": 2}],
            [{"id": 3}, {"id": 4}],
            []  # Empty to stop pagination
        ]
        
        mock_method = Mock(side_effect=lambda **kwargs: mock_request("endpoint", kwargs))
        
        result = client.paginate(mock_method, page_size=2)
        
        assert len(result) == 4
        assert result == [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}]
    
    @patch('src.api.client.TransparenciaAPIClient._make_request')
    def test_paginate_with_error(self, mock_request, client):
        """Test pagination handles errors gracefully."""
        # First page succeeds, second page fails
        mock_request.side_effect = [
            [{"id": 1}, {"id": 2}],
            Exception("API Error")
        ]
        
        mock_method = Mock(side_effect=lambda **kwargs: mock_request("endpoint", kwargs))
        
        result = client.paginate(mock_method, page_size=2)
        
        # Should return data from first page only
        assert len(result) == 2
        assert result == [{"id": 1}, {"id": 2}]
    
    def test_get_available_endpoints(self, client):
        """Test getting available endpoints."""
        endpoints = client.get_available_endpoints()
        
        assert isinstance(endpoints, dict)
        assert len(endpoints) > 0
        assert "despesas_contratos" in endpoints
        assert endpoints["despesas_contratos"] == "/contratos"
    
    def test_clear_cache(self, client, tmp_path):
        """Test clearing cache."""
        # Create some cache files
        cache_dir = tmp_path / "cache"
        cache_dir.mkdir(exist_ok=True)
        
        # Create dummy cache files
        (cache_dir / "test1.json").write_text("{}")
        (cache_dir / "test2.json").write_text("{}")
        
        # Mock the cache directory path
        with patch('src.api.client.Path', return_value=cache_dir):
            client.clear_cache()
        
        # Check files were deleted
        assert not (cache_dir / "test1.json").exists()
        assert not (cache_dir / "test2.json").exists()
    
    def test_get_stats(self, client, tmp_path):
        """Test getting client statistics."""
        # Create some cache files
        cache_dir = tmp_path / "cache"
        cache_dir.mkdir(exist_ok=True)
        (cache_dir / "test1.json").write_text("{}")
        (cache_dir / "test2.json").write_text("{}")
        
        # Mock the cache directory path
        with patch('src.api.client.Path') as mock_path:
            mock_path.return_value.exists.return_value = True
            mock_path.return_value.glob.return_value = [
                cache_dir / "test1.json",
                cache_dir / "test2.json"
            ]
            
            stats = client.get_stats()
        
        assert stats["rate_limit"] == 30
        assert stats["timeout"] == 60
        assert stats["cache_ttl"] == 3600
        assert stats["cache_enabled"] is True
        assert stats["cached_items"] == 2
        assert stats["endpoints_available"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])