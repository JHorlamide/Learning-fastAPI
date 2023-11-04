from fastapi import APIRouter, HTTPException

from storeapi.models.posts import (
    CommentIn,
    UserPostIn,
    UserPostWithComments,
    GenericResponseModel,
)

router = APIRouter()

post_table = {}
comment_table = {}


def find_post(post_id: int):
    return post_table.get(post_id)


@router.post("/api/posts", response_model=GenericResponseModel, status_code=201)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post

    return GenericResponseModel(
        status="success",
        message="Post created",
        data=new_post,
    )


@router.get("/api/posts", response_model=GenericResponseModel)
async def get_all_posts():
    return GenericResponseModel(
        status="Success",
        message="Data fetched successfully",
        data=list(post_table.values()),
    )


@router.post("/api/comments", response_model=GenericResponseModel, status_code=201)
async def create_post_comment(comment: CommentIn):
    post = find_post(comment.post_id)

    if not post:
        raise HTTPException(status_code=404, details={"message": "Post not found"})

    data = comment.model_dump()
    last_record_id = len(comment_table)
    new_comment = {**data, "id": last_record_id}
    comment_table[last_record_id] = new_comment

    return GenericResponseModel(
        status="Success",
        message="Comment created",
        data=new_comment,
    )


@router.get("/api/post/{post_id}/comments", response_model=GenericResponseModel)
async def get_comments_on_post(post_id: int):
    post_comments = [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]

    return GenericResponseModel(
        status="Success",
        message="Post comments fetched successfully",
        data=post_comments,
    )


@router.get("/api/post/{post_id}", response_model=GenericResponseModel)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)

    if not post:
        raise HTTPException(status_code=404, details={"message": "Post not found"})

    data_construct: UserPostWithComments = {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }

    return GenericResponseModel(
        status="Success",
        message="Data fetched successfully",
        data=data_construct,
    )
