# libraries
import pytest

# local
from core.models import Posts, Users, UserRoleEnum, OtherPostInfo
from core.schemas.user import IvolunteerPageTagsEnum
from beanie import PydanticObjectId

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="function", autouse=True)
async def create_post_data(clean_db):
    await clean_db

    admin_user = Users(
        _id=PydanticObjectId("65d767d163bc47aa66a84ef8"),
        email="atang@betterme.news",
        discord_id="123456",
        name="Atang",
        avatar_url="https://pic.com",
        roles=[UserRoleEnum.ADMIN],
        last_logged_in_at="2222-02-22 22:22:22",
    )
    await admin_user.insert()

    post_documents = []
    other_info = OtherPostInfo(deadline=None)
    post_documents.append(
        Posts(
            _id=PydanticObjectId("65d76b73cbc29b3c618ec673"),
            # info
            created_at="1111-11-11 11:11:11",
            created_by=admin_user,
            discord_post_id=1234567,
            # content
            title="Some title",
            description="Some description",
            tags=[
                IvolunteerPageTagsEnum.CLUB,
                IvolunteerPageTagsEnum.VOLUNTEER,
            ],
            other_information=other_info,
            banner_img="https://s3.tebi.io/testfiles.betterme.news/6e590aaf_Ban-sao-cua-Kich-thuoc-800x500px_Anh-Dai-Dien-Bai-Dang-Website-iVolunteer-40.png",
            content="Some title",
            author="Ivolunteer.vn",
            # SEO
            keywords=[
                "keyword 1",
                "keyword 2",
                "keyword 3",
            ],
            og_img="https://s3.tebi.io/testfiles.betterme.news/6e590aaf_Ban-sao-cua-Kich-thuoc-800x500px_Anh-Dai-Dien-Bai-Dang-Website-iVolunteer-40.png",
        )
    )

    await Posts.insert_many(post_documents)


@pytest.mark.asyncio
async def test_get_post_success(client, create_post_data):
    """
    INPUT:
        Get post that id exist
    OUTPUT:
        Get post successfully
    """
    await create_post_data

    response = client.get("/api/posts/some-slug-here_65d76b73cbc29b3c618ec673")
    assert response.status_code == 200
    assert response.json() == {
        "id": "65d76b73cbc29b3c618ec673",
        "author": "Ivolunteer.vn",
        "banner_img": "https://s3.tebi.io/testfiles.betterme.news/6e590aaf_Ban-sao-cua-Kich-thuoc-800x500px_Anh-Dai-Dien-Bai-Dang-Website-iVolunteer-40.png",
        "content": "Some title",
        "created_at": "1111-11-11T11:11:11",
        "description": "Some description",
        "keywords": ["keyword 1", "keyword 2", "keyword 3"],
        "og_img": "https://s3.tebi.io/testfiles.betterme.news/6e590aaf_Ban-sao-cua-Kich-thuoc-800x500px_Anh-Dai-Dien-Bai-Dang-Website-iVolunteer-40.png",
        "other_information": {"deadline": None},
        "tags": ["Câu lạc bộ", "Tình nguyện"],
        "thumbnail_img": None,
        "title": "Some title",
        "view": 1,
    }


@pytest.mark.asyncio
async def test_get_post_with_not_exist(client, create_post_data):
    """
    INPUT:
        Get post that id not exist
    OUTPUT:
        Get post failed
    """
    await create_post_data

    response = client.get("/api/posts/slug-here_1111111111111111111")
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


@pytest.mark.asyncio
async def test_get_post_increase_view(client, create_post_data):
    """
    INPUT:
        Get post
    OUTPUT:
        - Get post successfully
        - View increase after call
    """
    await create_post_data

    response = client.get("/api/posts/some-slug-here_65d76b73cbc29b3c618ec673")
    assert response.status_code == 200
    assert response.json()["view"] == 1
    response = client.get("/api/posts/some-slug-here_65d76b73cbc29b3c618ec673")
    assert response.status_code == 200
    assert response.json()["view"] == 2


@pytest.mark.asyncio
async def test_get_post_not_increase_view(client, create_post_data):
    """
    INPUT:
        Get post
    OUTPUT:
        - Get post successfully
        - View increase after call
    """
    await create_post_data

    response = client.get(
        "/api/posts/some-slug-here_65d76b73cbc29b3c618ec673", params={"increase_view": False}
    )
    assert response.status_code == 200
    assert response.json()["view"] == 1
    response = client.get("/api/posts/some-slug-here_65d76b73cbc29b3c618ec673")
    assert response.status_code == 200
    assert response.json()["view"] == 1
