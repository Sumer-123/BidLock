from state.redis_client import get_redis_client


def acquire_lock(job_id: str, freelancer_id: str) -> bool:
    r = get_redis_client()
    lock_key = f"lock:{job_id}"

    # SET nx=True means "Only set this key if it does NOT exist"
    # ex=30 means "Auto-delete this lock after 30 seconds" (prevent deadlocks)
    is_locked = r.set(lock_key, freelancer_id, nx=True, ex=30)

    return bool(is_locked)


def release_lock(job_id: str):
    r = get_redis_client()
    r.delete(f"lock:{job_id}")