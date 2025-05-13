import redis
import json
import config
import logging
from redis.exceptions import RedisError

# Setup logging
logger = logging.getLogger(__name__)

# Initialize Redis client as None - will be lazily connected
redis_client = None
redis_available = True

def get_redis_client():
    """Get Redis client with connection pooling and timeout"""
    global redis_client, redis_available
    
    # If Redis is not available, don't try to connect again
    if not redis_available:
        return None
        
    # If client already exists, return it
    if redis_client is not None:
        return redis_client
        
    try:
        # Create Redis connection pool with timeout
        pool = redis.ConnectionPool(
            host=config.REDIS_HOST,
            port=int(config.REDIS_PORT),
            db=int(config.REDIS_DB),
            password=config.REDIS_PASSWORD,
            decode_responses=True,
            socket_timeout=2,  # 2 second timeout
            socket_connect_timeout=2,  # 2 second connection timeout
            health_check_interval=30  # Check connection every 30 seconds
        )
        
        # Create Redis client with connection pool
        redis_client = redis.Redis(connection_pool=pool)
        
        # Test connection
        redis_client.ping()
        return redis_client
    except (RedisError, Exception) as e:
        logger.warning(f"Redis connection failed: {str(e)}")
        redis_available = False  # Mark Redis as unavailable
        return None

def get_cached_snippet(snippet_id):
    """Get HTML snippet from cache"""
    client = get_redis_client()
    if not client:
        return None  # Redis not available, skip cache
        
    try:
        cached_data = client.get(f"snippet:{snippet_id}")
        if cached_data:
            return json.loads(cached_data)
    except RedisError as e:
        logger.warning(f"Error getting cached snippet: {str(e)}")
    
    return None

def cache_snippet(snippet):
    """Cache HTML snippet"""
    snippet_data = {
        'id': str(snippet.id),
        'html_content': snippet.html_content,
        'created_at': snippet.created_at.isoformat()
    }
    
    client = get_redis_client()
    if client:  # Only try to cache if Redis is available
        try:
            client.setex(
                f"snippet:{snippet.id}",
                60 * 60 * 24,  # Cache for 24 hours
                json.dumps(snippet_data)
            )
        except RedisError as e:
            logger.warning(f"Error caching snippet: {str(e)}")
    
    return snippet_data
