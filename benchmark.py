"""
Performance benchmarking script for the Python Space Agents system.
"""

import asyncio
import time
import json
from typing import Dict, Any, List
from pathlib import Path
import statistics
import structlog

from main import create_space
from utils.performance import performance_monitor, simple_cache, clear_all_caches
from config.llm_config import clear_llm_cache

logger = structlog.get_logger()


class PerformanceBenchmark:
    """Benchmark the space creation performance."""
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        
    def reset(self):
        """Reset benchmark data."""
        self.results.clear()
        clear_all_caches()
        clear_llm_cache()
        
    async def run_single_benchmark(self, request: str, run_id: int) -> Dict[str, Any]:
        """Run a single benchmark iteration."""
        logger.info("Starting benchmark run", run_id=run_id)
        
        start_time = time.time()
        try:
            result = await create_space(request)
            duration = time.time() - start_time
            
            # Get performance metrics
            cache_stats = simple_cache.get_stats()
            perf_report = performance_monitor.get_report()
            
            benchmark_result = {
                "run_id": run_id,
                "duration": duration,
                "success": True,
                "steps": len(result),
                "cache_hit_rate": cache_stats["hit_rate"],
                "total_operations": perf_report["summary"]["total_operations"],
                "total_llm_time": perf_report["summary"]["total_time"],
                "error": None
            }
            
            logger.info("Benchmark run completed", 
                       run_id=run_id, 
                       duration=round(duration, 2),
                       cache_hit_rate=cache_stats["hit_rate"])
            
            return benchmark_result
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error("Benchmark run failed", run_id=run_id, error=str(e))
            
            return {
                "run_id": run_id,
                "duration": duration,
                "success": False,
                "steps": 0,
                "cache_hit_rate": 0,
                "total_operations": 0,
                "total_llm_time": 0,
                "error": str(e)
            }
    
    async def run_benchmark_suite(self, requests: List[str], iterations: int = 3) -> Dict[str, Any]:
        """Run a complete benchmark suite."""
        logger.info("Starting benchmark suite", 
                   requests=len(requests), 
                   iterations=iterations)
        
        suite_results = []
        
        for req_idx, request in enumerate(requests):
            logger.info("Benchmarking request", 
                       request_idx=req_idx, 
                       request=request[:100])
            
            request_results = []
            
            # Run cold start (no cache)
            self.reset()
            cold_result = await self.run_single_benchmark(request, 0)
            cold_result["type"] = "cold_start"
            request_results.append(cold_result)
            
            # Run warm iterations (with cache)
            for i in range(1, iterations + 1):
                warm_result = await self.run_single_benchmark(request, i)
                warm_result["type"] = "warm"
                request_results.append(warm_result)
                
                # Small delay between runs
                await asyncio.sleep(1)
            
            suite_results.append({
                "request": request,
                "request_idx": req_idx,
                "runs": request_results
            })
        
        return self._analyze_results(suite_results)
    
    def _analyze_results(self, suite_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze benchmark results."""
        all_durations = []
        cold_durations = []
        warm_durations = []
        success_count = 0
        total_runs = 0
        
        for request_result in suite_results:
            for run in request_result["runs"]:
                total_runs += 1
                if run["success"]:
                    success_count += 1
                    all_durations.append(run["duration"])
                    
                    if run["type"] == "cold_start":
                        cold_durations.append(run["duration"])
                    else:
                        warm_durations.append(run["duration"])
        
        analysis = {
            "summary": {
                "total_runs": total_runs,
                "success_rate": (success_count / total_runs) * 100 if total_runs > 0 else 0,
                "avg_duration": statistics.mean(all_durations) if all_durations else 0,
                "median_duration": statistics.median(all_durations) if all_durations else 0,
                "min_duration": min(all_durations) if all_durations else 0,
                "max_duration": max(all_durations) if all_durations else 0,
            },
            "cold_vs_warm": {
                "cold_avg": statistics.mean(cold_durations) if cold_durations else 0,
                "warm_avg": statistics.mean(warm_durations) if warm_durations else 0,
                "improvement": 0
            },
            "detailed_results": suite_results
        }
        
        # Calculate cache improvement
        if cold_durations and warm_durations:
            cold_avg = statistics.mean(cold_durations)
            warm_avg = statistics.mean(warm_durations)
            improvement = ((cold_avg - warm_avg) / cold_avg) * 100
            analysis["cold_vs_warm"]["improvement"] = improvement
        
        return analysis


async def main():
    """Run performance benchmarks."""
    # Test requests of varying complexity
    test_requests = [
        "Create a simple space for dog lovers with basic feeds and welcome message",
        
        "Create a comprehensive space for a blockchain gaming community with feeds, governance tools, NFT galleries, and trading widgets",
        
        "Create a space for a local photography club with galleries, chat, resource links, and social feeds from Instagram and Twitter",
    ]
    
    benchmark = PerformanceBenchmark()
    
    print("🚀 Starting Performance Benchmark Suite")
    print(f"📊 Testing {len(test_requests)} requests with 3 iterations each")
    print("=" * 50)
    
    results = await benchmark.run_benchmark_suite(test_requests, iterations=3)
    
    # Display results
    print("\n📈 BENCHMARK RESULTS")
    print("=" * 50)
    
    summary = results["summary"]
    print(f"Total Runs: {summary['total_runs']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print(f"Average Duration: {summary['avg_duration']:.2f}s")
    print(f"Median Duration: {summary['median_duration']:.2f}s")
    print(f"Range: {summary['min_duration']:.2f}s - {summary['max_duration']:.2f}s")
    
    cold_warm = results["cold_vs_warm"]
    print(f"\n🔥 COLD vs WARM PERFORMANCE")
    print(f"Cold Start Average: {cold_warm['cold_avg']:.2f}s")
    print(f"Warm Run Average: {cold_warm['warm_avg']:.2f}s")
    if cold_warm['improvement'] > 0:
        print(f"Cache Improvement: {cold_warm['improvement']:.1f}% faster")
    
    # Save detailed results
    results_file = Path("benchmark_results.json")
    with results_file.open("w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to {results_file}")
    print("\n✅ Benchmark completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
