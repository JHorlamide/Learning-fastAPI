from typing import Any, Optional

from pydantic import BaseModel


class GenericResponseModel(BaseModel):
    data: Optional[Any] = None
    message: str
    status: str


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    id: int


class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comment]
    comments: list[Comment]
