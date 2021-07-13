import graphene
from schemas.blog import UserModelSchema
from models.blog import User
from db_config import db_session

db = db_session.session_factory()

class Query(graphene.ObjectType):

    all_users = graphene.List(UserModelSchema)
    user_by_id = graphene.Field(UserModelSchema, user_id=graphene.Int(required=True))

    def resolve_all_users(self, info):
        query = UserModelSchema.get_query(info)
        return query.all()

    def resolve_user_by_id(self, info, post_id):
        return db.query(User).filter(User.id == post_id).first()
