"""
Performance monitoring and optimization utilities
"""

import time
import functools
from typing import Callable, Any, Dict
from collections import defaultdict
import numpy as np


class PerformanceMonitor:
    """Monitor performance metrics for emotion detection"""
    
    def __init__(self):
        """Initialize performance monitor"""
        self.metrics = defaultdict(list)
        self.frame_times = []
        self.detection_times = []
        self.prediction_times = []
    
    def record_frame_time(self, duration: float) -> None:
        """Record frame processing time"""
        self.frame_times.append(duration)
        self.metrics["frame_time"].append(duration)
    
    def record_detection_time(self, duration: float) -> None:
        """Record face detection time"""
        self.detection_times.append(duration)
        self.metrics["detection_time"].append(duration)
    
    def record_prediction_time(self, duration: float) -> None:
        """Record emotion prediction time"""
        self.prediction_times.append(duration)
        self.metrics["prediction_time"].append(duration)
    
    def get_statistics(self) -> Dict[str, Dict[str, float]]:
        """
        Get performance statistics
        
        Returns:
            dict: Statistics for each metric
        """
        stats = {}
        
        for metric_name, values in self.metrics.items():
            if values:
                stats[metric_name] = {
                    "mean": np.mean(values),
                    "median": np.median(values),
                    "min": np.min(values),
                    "max": np.max(values),
                    "std": np.std(values),
                    "count": len(values)
                }
        
        return stats
    
    def get_fps(self) -> float:
        """
        Calculate average FPS
        
        Returns:
            float: Frames per second
        """
        if not self.frame_times:
            return 0.0
        
        avg_frame_time = np.mean(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
    
    def get_summary(self) -> str:
        """
        Get formatted summary of performance
        
        Returns:
            str: Performance summary
        """
        stats = self.get_statistics()
        fps = self.get_fps()
        
        summary = ["Performance Summary:", "=" * 50]
        summary.append(f"Average FPS: {fps:.2f}")
        
        for metric_name, metric_stats in stats.items():
            summary.append(f"\n{metric_name.replace('_', ' ').title()}:")
            summary.append(f"  Mean: {metric_stats['mean']*1000:.2f}ms")
            summary.append(f"  Median: {metric_stats['median']*1000:.2f}ms")
            summary.append(f"  Min: {metric_stats['min']*1000:.2f}ms")
            summary.append(f"  Max: {metric_stats['max']*1000:.2f}ms")
            summary.append(f"  Std Dev: {metric_stats['std']*1000:.2f}ms")
            summary.append(f"  Samples: {metric_stats['count']}")
        
        return "\n".join(summary)
    
    def reset(self) -> None:
        """Reset all metrics"""
        self.metrics.clear()
        self.frame_times.clear()
        self.detection_times.clear()
        self.prediction_times.clear()
    
    def __str__(self) -> str:
        """String representation"""
        return self.get_summary()


def timer(metric_name: str = "execution_time"):
    """
    Decorator to time function execution
    
    Args:
        metric_name: Name of the metric to record
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            # Print timing info
            print(f"{func.__name__} took {duration*1000:.2f}ms")
            
            return result
        return wrapper
    return decorator


class FrameOptimizer:
    """Optimize frame processing for better performance"""
    
    @staticmethod
    def resize_frame(frame: np.ndarray, max_width: int = 640) -> np.ndarray:
        """
        Resize frame while maintaining aspect ratio
        
        Args:
            frame: Input frame
            max_width: Maximum width
            
        Returns:
            np.ndarray: Resized frame
        """
        height, width = frame.shape[:2]
        
        if width > max_width:
            scale = max_width / width
            new_width = max_width
            new_height = int(height * scale)
            return cv2.resize(frame, (new_width, new_height))
        
        return frame
    
    @staticmethod
    def skip_frames(frame_count: int, skip_rate: int = 2) -> bool:
        """
        Determine if frame should be skipped
        
        Args:
            frame_count: Current frame number
            skip_rate: Process every Nth frame
            
        Returns:
            bool: True if frame should be processed
        """
        return frame_count % skip_rate == 0
    
    @staticmethod
    def apply_roi(frame: np.ndarray, faces: list) -> np.ndarray:
        """
        Apply region of interest to reduce processing area
        
        Args:
            frame: Input frame
            faces: List of detected face coordinates
            
        Returns:
            np.ndarray: ROI frame
        """
        if not faces:
            return frame
        
        # Get bounding box for all faces
        x_min = min(x for (x, y, w, h) in faces)
        y_min = min(y for (x, y, w, h) in faces)
        x_max = max(x + w for (x, y, w, h) in faces)
        y_max = max(y + h for (x, y, w, h) in faces)
        
        # Add padding
        padding = 50
        height, width = frame.shape[:2]
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(width, x_max + padding)
        y_max = min(height, y_max + padding)
        
        return frame[y_min:y_max, x_min:x_max]


class CacheManager:
    """Manage caching for model predictions"""
    
    def __init__(self, max_size: int = 100):
        """
        Initialize cache manager
        
        Args:
            max_size: Maximum cache size
        """
        self.cache: Dict[str, Any] = {}
        self.max_size = max_size
        self.access_count: Dict[str, int] = defaultdict(int)
    
    def get(self, key: str) -> Any:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if key in self.cache:
            self.access_count[key] += 1
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
        """
        if len(self.cache) >= self.max_size:
            # Remove least accessed item
            least_accessed = min(self.access_count, key=self.access_count.get)
            del self.cache[least_accessed]
            del self.access_count[least_accessed]
        
        self.cache[key] = value
        self.access_count[key] = 0
    
    def clear(self) -> None:
        """Clear cache"""
        self.cache.clear()
        self.access_count.clear()
    
    def __len__(self) -> int:
        """Return cache size"""
        return len(self.cache)


# Example usage
if __name__ == "__main__":
    import cv2
    
    # Create performance monitor
    monitor = PerformanceMonitor()
    
    # Simulate some measurements
    for _ in range(100):
        monitor.record_frame_time(0.033)  # ~30 FPS
        monitor.record_detection_time(0.015)
        monitor.record_prediction_time(0.010)
    
    # Print summary
    print(monitor.get_summary())
    print(f"\nAverage FPS: {monitor.get_fps():.2f}")
    
    # Test timer decorator
    @timer("test_function")
    def slow_function():
        time.sleep(0.1)
        return "Done"
    
    result = slow_function()
    
    # Test cache
    cache = CacheManager(max_size=5)
    cache.set("test", "value")
    print(f"\nCache value: {cache.get('test')}")
    print(f"Cache size: {len(cache)}")
