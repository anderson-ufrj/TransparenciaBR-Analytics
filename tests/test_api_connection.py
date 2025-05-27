"""
Integration tests for API connection and basic functionality.
"""

import os
import sys
import time
import pytest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.client import TransparenciaAPIClient


class TestAPIConnection:
    """Test API connection and authentication."""
    
    @pytest.fixture
    def client(self):
        """Create API client instance."""
        return TransparenciaAPIClient()
    
    def test_environment_variables(self):
        """Test that required environment variables are set."""
        assert os.getenv("TRANSPARENCIA_API_TOKEN") is not None, \
            "TRANSPARENCIA_API_TOKEN environment variable not set"
        assert os.getenv("TRANSPARENCIA_API_EMAIL") is not None, \
            "TRANSPARENCIA_API_EMAIL environment variable not set"
    
    def test_client_initialization(self, client):
        """Test that client initializes correctly."""
        assert client.api_token is not None
        assert client.api_email is not None
        assert client.rate_limit == 30
        assert client.timeout == 60
        assert client.cache_ttl == 3600
    
    def test_connection(self, client):
        """Test API connection."""
        result = client.test_connection()
        assert result is True, "API connection test failed"
    
    def test_basic_endpoint(self, client):
        """Test a basic API endpoint."""
        # Test fetching organizations
        result = client.get_orgaos(sistema="siafi", pagina=1, quantidade=10)
        
        assert isinstance(result, list), "Expected list response"
        assert len(result) > 0, "No data returned from API"
        
        # Check data structure
        if result:
            first_item = result[0]
            assert isinstance(first_item, dict), "Expected dict items in response"
            # Basic fields that should be present
            assert any(key in first_item for key in ["codigo", "descricao", "nome"]), \
                "Expected standard fields not found in response"
    
    def test_rate_limiting(self, client):
        """Test that rate limiting works."""
        # Make rapid requests to test rate limiting
        start_time = time.time()
        request_count = 0
        
        # Try to make 5 rapid requests
        for i in range(5):
            try:
                client.get_orgaos(sistema="siafi", pagina=i+1, quantidade=1)
                request_count += 1
            except Exception as e:
                pytest.fail(f"Request failed: {e}")
        
        elapsed_time = time.time() - start_time
        
        # All requests should succeed (rate limiter should handle limiting)
        assert request_count == 5, "Not all requests completed"
        print(f"Completed {request_count} requests in {elapsed_time:.2f} seconds")
    
    def test_cache_functionality(self, client):
        """Test cache functionality."""
        # Clear cache first
        client.clear_cache()
        
        # First request (should hit API)
        start_time = time.time()
        result1 = client.get_orgaos(sistema="siafi", pagina=1, quantidade=5)
        first_request_time = time.time() - start_time
        
        # Second request with same parameters (should hit cache)
        start_time = time.time()
        result2 = client.get_orgaos(sistema="siafi", pagina=1, quantidade=5)
        second_request_time = time.time() - start_time
        
        # Cache should make second request faster
        assert second_request_time < first_request_time, \
            "Cache doesn't appear to be working (second request not faster)"
        
        # Results should be identical
        assert result1 == result2, "Cached results don't match original"
        
        print(f"First request: {first_request_time:.3f}s, "
              f"Cached request: {second_request_time:.3f}s")
    
    def test_error_handling(self, client):
        """Test error handling for invalid requests."""
        # Test with invalid endpoint
        with pytest.raises(KeyError):
            client._make_request("/invalid-endpoint")
        
        # Test with invalid sistema parameter
        with pytest.raises(ValueError):
            client.get_orgaos(sistema="invalid")
        
        # Test with invalid sanção type
        with pytest.raises(ValueError):
            client.get_empresas_sancionadas(tipo="invalid")
    
    def test_pagination(self, client):
        """Test pagination functionality."""
        # Get first page
        page1 = client.get_orgaos(sistema="siafi", pagina=1, quantidade=5)
        
        # Get second page
        page2 = client.get_orgaos(sistema="siafi", pagina=2, quantidade=5)
        
        # Pages should have different content
        assert page1 != page2, "Different pages returned same content"
        
        # Both should have data
        assert len(page1) > 0 and len(page2) > 0, "Pages missing data"
    
    def test_available_endpoints(self, client):
        """Test getting available endpoints."""
        endpoints = client.get_available_endpoints()
        
        assert isinstance(endpoints, dict), "Expected dict of endpoints"
        assert len(endpoints) > 0, "No endpoints available"
        
        # Check some expected endpoints
        expected_endpoints = [
            "despesas_contratos",
            "servidores",
            "beneficios_bolsa_familia",
            "licitacoes"
        ]
        
        for endpoint in expected_endpoints:
            assert endpoint in endpoints, f"Expected endpoint '{endpoint}' not found"
    
    def test_client_stats(self, client):
        """Test getting client statistics."""
        stats = client.get_stats()
        
        assert isinstance(stats, dict), "Expected dict of stats"
        assert "rate_limit" in stats
        assert "timeout" in stats
        assert "cache_ttl" in stats
        assert "cache_enabled" in stats
        assert "cached_items" in stats
        assert "endpoints_available" in stats
        
        # Verify values
        assert stats["rate_limit"] == 30
        assert stats["timeout"] == 60
        assert stats["cache_enabled"] is True


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])