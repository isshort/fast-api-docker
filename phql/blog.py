from schemas.blog import User as UserSchema, UserAuthenticateSchema
import graphene
import bcrypt
from models.blog import User
from db_config import db_session

db = db_session.session_factory()


class UserAuthentication(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, email, password):
        user = UserAuthenticateSchema(email=email, password=password)
        db_user_info = db.query(User).filter(User.email == email).first()
        if bcrypt.checkpw(user.password.encode("utf-8"), db_user_info.password.encode("utf-8")):
            ok = True
        else:
            ok = False
        return UserAuthentication(ok=ok)


class CreateNewUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        age = graphene.Int(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, email, phone, age, password):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        # print("hashed_password", hashed_password)
        password_hash = hashed_password.decode("utf8")
        # print("password hash is ", password_hash)
        user = UserSchema(email=email, phone=phone, age=age, password=password_hash)
        db_user = User(email=user.email, phone=user.phone, age=user.age, password=password_hash)
        db.add(db_user)
        try:
            db.commit()
            db.refresh(db_user)
            ok = True
            return CreateNewUser(ok=ok)
        except:
            db.rollback()
            raise


class CreateNews(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        age = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, email, phone, age):
        user = UserSchema(email=email, phone=phone, age=age)
        db_user = User(email=user.email, phone=user.phone, age=user.age)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        ok = True
        return CreateNews(ok=ok)


class CreateUserMutations(graphene.ObjectType):
    create_news = CreateNews.Field()
    create_new_user = CreateNewUser.Field()
    authenticate_user=UserAuthentication.Field()
