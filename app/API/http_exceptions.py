from fastapi import HTTPException, status

http_exc_404_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resourse not found",
)

http_exc_409_conflict = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="This doctor is currently making an appointment",
)
