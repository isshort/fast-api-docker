from datetime import timedelta

from help.help import create_access_token, decode_access_token
from schemas.blog import User as UserSchema, UserAuthenticateSchema, NewsSchema
import graphene
import bcrypt
from models.blog import User, News
from db_config import db_session
from jwt import PyJWTError
db = db_session.session_factory()


class UserAuthentication(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    token = graphene.String()

    @staticmethod
    def mutate(root, info, email, password):
        user = UserAuthenticateSchema(email=email, password=password)
        db_user_info = db.query(User).filter(User.email == email).first()
        if bcrypt.checkpw(user.password.encode("utf-8"), db_user_info.password.encode("utf-8")):
            access_token_expires = timedelta(minutes=60)
            access_token = create_access_token(data={"user": email}, expires_delta=access_token_expires)
            ok = True
            return UserAuthentication(ok=ok, token=access_token)
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
        # https://stackoverflow.com/questions/34548846/flask-bcrypt-valueerror-invalid-salt

        # print("password hash is ", password_hash)
        user = UserSchema(email=email, phone=phone, age=age, password=password_hash)
        db_user = User(email=user.email, phone=user.phone, age=user.age, password=password_hash)
        db.add(db_user)
        # https://docs.sqlalchemy.org/en/13/faq/sessions.html#this-session-s-transaction-has-been-rolled-back-due-to-a-previous-exception-during-flush-or-similar

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
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        token = graphene.String(required=True)

    result = graphene.String()

    @staticmethod
    def mutate(root, info, title, description, token):
        try:
            payload = decode_access_token(data=token)
            email = payload.get("user")
            if email is None:
                raise PyJWTError("Invalid Credential 1")
        except PyJWTError:
            raise PyJWTError("Invalid Credential 2")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise PyJWTError("Invalid Credential 3")
        new = NewsSchema(title=title, description=description)
        db_new = News(title=new.title, description=new.description)
        db.add(db_new)
        db.commit()
        db.refresh(db_new)
        result = "Added New POST "
        return CreateNews(result=result)


class CreateUserMutations(graphene.ObjectType):
    create_news = CreateNews.Field()
    create_new_user = CreateNewUser.Field()
    authenticate_user = UserAuthentication.Field()
