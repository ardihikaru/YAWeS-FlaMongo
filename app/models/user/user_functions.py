from mongoengine import DoesNotExist, NotUniqueError

from app import app, rc, local_settings
from sqlalchemy.orm.exc import NoResultFound
from app.addons.redis.translator import redis_get, redis_set
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, decode_token, get_jti
from app.addons.utils import sqlresp_to_dict, mongo_list_to_dict, mongo_dict_to_dict
# from datetime import date  # eg.g date.today())
from sqlalchemy import Date, cast, and_  # detailed here: https://docs.sqlalchemy.org/en/13/core/sqlelement.html?
from datetime import datetime


def insert_new_data(user_model, new_data, msg):
    new_data.pop("password_confirm")
    try:
        inserted_data = user_model(**new_data).save()
    except NotUniqueError as e:
        return False, None, "Duplicate Email `%s`" % new_data["email"]
        # return False, str(e)

    new_data["id"] = inserted_data.id
    new_data["created_time"] = inserted_data.created_time
    new_data["updated_at"] = inserted_data.updated_at

    if len(inserted_data) > 0:
        return True, inserted_data, msg
    else:
        return False, None, msg


def get_all_users(user_model, args=None):
    try:
        data = user_model.objects().to_json()
        # if args is not None:
        #     if len(args["range"]) == 0:
        #         args["range"] = [local_settings["pagination"]["offset"], local_settings["pagination"]["limit"]]
        # else:
        #     args = {
        #         "filter": {},
        #         "range": [local_settings["pagination"]["offset"], local_settings["pagination"]["limit"]],
        #         "sort": []
        #     }
        # data_all = ses.query(user_model).all()
        # data = ses.query(user_model).offset(args["range"][0]).limit(args["range"][1]).all()
    except NoResultFound:
        return False, None, 0
    data_dict = mongo_list_to_dict(data)

    if len(data_dict) > 0:
        return True, data_dict, len(data_dict)
    else:
        return False, None, 0


def get_user_by_userid(user_model, userid):
    try:
        data = user_model.objects.get(id=userid).to_json()
    # except DoesNotExist:
    except Exception as e:
        return False, None, str(e)

    dict_data = mongo_dict_to_dict(data)

    return True, dict_data, None


def get_user_by_username(user_model, username):
    try:
        data = user_model.objects.get(username=username).to_json()
    # except DoesNotExist:
    except Exception as e:
        return False, None

    dict_data = mongo_dict_to_dict(data)

    return True, dict_data


def del_user_by_userid(user_model, userid):
    try:
        user_model.objects.get(id=userid).delete()
    # except DoesNotExist:
    except Exception as e:
        return False, str(e)

    return True, None


def upd_user_by_userid(user_model, userid, new_data):
    try:
        user_model.objects.get(id=userid).update(**new_data)
    # except DoesNotExist:
    except Exception as e:
        return False, None, str(e)

    new_data["id"] = userid
    new_data["updated_at"] = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

    return True, new_data, None


def store_jwt_data(json_data):
    my_identity = {
        "username": json_data["username"]
    }

    access_token = create_access_token(identity=my_identity)
    refresh_token = create_refresh_token(identity=my_identity)

    access_jti = get_jti(encoded_token=access_token)
    refresh_jti = get_jti(encoded_token=refresh_token)

    redis_set(rc, access_jti, False, app.config["LIMIT_ACCESS_TOKEN"])
    redis_set(rc, refresh_jti, False, app.config["LIMIT_REFRESH_TOKEN"])

    access_token_expired = decode_token(access_token)["exp"]
    refresh_token_expired = decode_token(refresh_token)["exp"]

    # redis_set(rc, json_data["username"] + "-access-token-exp", False, app.config["LIMIT_ACCESS_TOKEN"])
    # redis_set(rc, json_data["username"] + "-refresh-token-exp", False, app.config["LIMIT_REFRESH_TOKEN"])

    return access_token, refresh_token, access_token_expired, refresh_token_expired


def get_user_data_by_hobby(ses, user_model, hobby, register_after):
    try:
        data = ses.query(user_model).filter_by(hobby=hobby).filter(cast(user_model.create_time, Date) >= register_after).all()
    except NoResultFound:
        return False, None
    dict_user = sqlresp_to_dict(data)

    if len(dict_user) > 0:
        return True, dict_user
    else:
        return False, None


def get_user_data_by_hobby_between(ses, user_model, hobby, start_date, end_date):
    try:
        data = ses.query(user_model).filter_by(hobby=hobby).filter(
            and_(
                cast(user_model.create_time, Date) >= start_date,
                cast(user_model.create_time, Date) <= end_date
            )
        ).all()
    except NoResultFound:
        return False, None
    dict_user = sqlresp_to_dict(data)

    if len(dict_user) > 0:
        return True, dict_user
    else:
        return False, None


def del_all_data(ses, data_model, args=None):
    deleted_data = []
    no_filter = True
    try:
        data = None
        if len(args["filter"]) > 0:
            if "id" in args["filter"]:
                for i in range(len(args["filter"]["id"])):
                    uid = args["filter"]["id"][i]
                    data = ses.query(data_model).filter_by(id=uid).one()
                    deleted_data.append(data.to_dict())
                    ses.query(data_model).filter_by(id=uid).delete()
                    no_filter = False
        if no_filter:
            data = ses.query(data_model).all()
            ses.query(data_model).delete()
    except NoResultFound:
        return False, None, "User not found"

    if no_filter:
        dict_drone = sqlresp_to_dict(data)
    else:
        dict_drone = deleted_data

    if len(dict_drone) > 0:
        return True, dict_drone, None
    else:
        return False, None, None

