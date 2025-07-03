"""
Performance monitoring and caching utilities.
"""

import time
import json
import hashlib
from typing import Any, Dict, Optional, Callable, TypeVar
from functools import wraps, lru_cache
from pathlib import Path
import structlog

logger = structlog.get_logger()

T = TypeVar('T')


class PerformanceMonitor:
    """Performance monitoring and metrics collection."""
    
    def __init__(self):
        self.metrics: Dict[str, Dict[str, Any]] = {}
        
    def time_operation(self, operation_name: str):
        """Decorator to time operations."""
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> T:
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time
                    
                    if operation_name not in self.metrics:
                        self.metrics[operation_name] = {
                            "total_calls": 0,
                            "total_time": 0,
                            "avg_time": 0,
                            "min_time": float('inf'),
                            "max_time": 0
                        }
                    
                    metrics = self.metrics[operation_name]
                    metrics["total_calls"] += 1
                    metrics["total_time"] += duration
                    metrics["avg_time"] = metrics["total_time"] / metrics["total_calls"]
                    metrics["min_time"] = min(metrics["min_time"], duration)
                    metrics["max_time"] = max(metrics["max_time"], duration)
                    
                    logger.info(
                        "Operation completed",
                        operation=operation_name,
                        duration=round(duration, 3),
                        avg_duration=round(metrics["avg_time"], 3)
                    )
                    
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    logger.error(
                        "Operation failed",
                        operation=operation_name,
                        duration=round(duration, 3),
                        error=str(e)
                    )
                    raise
            return wrapper
        return decorator
    
    def get_report(self) -> Dict[str, Any]:
        """Get performance report."""
        return {
            "metrics": self.metrics,
            "summary": {
                "total_operations": sum(m["total_calls"] for m in self.metrics.values()),
                "total_time": sum(m["total_time"] for m in self.metrics.values()),
                "slowest_operation": max(
                    self.metrics.items(), 
                    key=lambda x: x[1]["avg_time"],
                    default=("none", {"avg_time": 0})
                )[0]
            }
        }


class SimpleCache:
    """Simple disk-based cache for LLM responses."""
    
    def __init__(self, cache_dir: str = ".agent_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.hits = 0
        self.misses = 0
    
    def _get_cache_key(self, prompt: str, model: str, temperature: float) -> str:
        """Generate cache key from prompt and parameters."""
        cache_content = f"{prompt}:{model}:{temperature}"
        return hashlib.md5(cache_content.encode()).hexdigest()
    
    def get(self, prompt: str, model: str, temperature: float) -> Optional[str]:
        """Get cached response."""
        try:
            cache_key = self._get_cache_key(prompt, model, temperature)
            cache_file = self.cache_dir / f"{cache_key}.json"
            
            if cache_file.exists():
                with cache_file.open('r') as f:
                    cached_data = json.load(f)
                    self.hits += 1
                    logger.debug("Cache hit", cache_key=cache_key[:8])
                    return cached_data["response"]
        except Exception as e:
            logger.warning("Cache read error", error=str(e))
        
        self.misses += 1
        return None
    
    def set(self, prompt: str, model: str, temperature: float, response: str):
        """Cache response."""
        try:
            cache_key = self._get_cache_key(prompt, model, temperature)
            cache_file = self.cache_dir / f"{cache_key}.json"
            
            cache_data = {
                "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "model": model,
                "temperature": temperature,
                "response": response,
                "timestamp": time.time()
            }
            
            with cache_file.open('w') as f:
                json.dump(cache_data, f, indent=2)
            
            logger.debug("Response cached", cache_key=cache_key[:8])
        except Exception as e:
            logger.warning("Cache write error", error=str(e))
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0
        
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate * 100, 1),
            "cache_files": len(list(self.cache_dir.glob("*.json")))
        }
    
    def clear(self):
        """Clear cache."""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
        self.hits = 0
        self.misses = 0
        logger.info("Cache cleared")


# Global instances
performance_monitor = PerformanceMonitor()
simple_cache = SimpleCache()


@lru_cache(maxsize=128)
def get_cached_validation_result(validation_data: str, validation_type: str) -> str:
    """Cache validation results to avoid repeated validation of identical data."""
    # This is just a memory cache for validation results
    # The actual validation will be done by the calling function
    return f"cached_validation_{hash(validation_data + validation_type)}"


def clear_all_caches():
    """Clear all performance caches."""
    simple_cache.clear()
    get_cached_validation_result.cache_clear()
    logger.info("All caches cleared")
