from flask_restplus import Resource, abort
from flask import request
from app.addons.database_blacklist.blacklist_helpers import is_token_valid
from app.addons.utils import masked_json_template
from app.models.user.user import User
from . import *


@api.route('')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class UserRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_results)
    @api.expect(register_data)
    def post(self):
        '''Add new user'''
        try:
            json_data = api.payload
            resp = User().register(json_data)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_list_with(all_user_data)
    def get(self):
        '''Get all user data'''
        try:
            try:
                get_args = {
                    "filter": request.args.get('filter', default="", type=str),
                    "range": request.args.get('range', default="", type=str),
                    "sort": request.args.get('sort', default="", type=str)
                }
            except:
                get_args = None

            resp = User().get_users(get_args)
            if resp["results"] is None:
                resp["results"] = []
            return masked_json_template(resp, 200, no_checking=True)
        except:
            abort(400, "Input unrecognizable.")

    # @api.doc(security=None)
    # @api.marshal_with(delete_data_results)
    # @api.doc(params={
    #     'filter': {'description': 'filter'},
    #     'range': {'description': 'range'},
    #     'sort': {'description': 'sort'}
    # })
    # def delete(self):
    #     '''Delete all existing User data'''
    #     try:
    #         try:
    #             get_args = {
    #                 "filter": request.args.get('filter', default="{}", type=str),
    #                 "range": request.args.get('range', default="[]", type=str),
    #                 "sort": request.args.get('sort', default="[]", type=str)
    #             }
    #         except:
    #             get_args = None
    #         resp = User().delete_all_user_data(get_args)
    #         return masked_json_template(resp, 200)
    #     except:
    #         abort(400, "Input unrecognizable.")

@api.route('/<userid>')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class UserIDFindRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_results)
    def get(self, userid):
        '''Get user data by user ID'''
        try:
            resp = User().get_data_by_userid(userid)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(update_results)
    @api.expect(editable_data)
    def put(self, userid):
        '''Update user data by user ID'''
        try:
            json_data = api.payload
            resp = User().update_data_by_userid(userid, json_data)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(register_results)
    def delete(self, userid):
        '''Delete user data by user ID'''
        try:
            resp = User().delete_data_by_userid(userid)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

#
# @api.route('/<hobby>/<register_after>')
# # @api.hide
# @api.response(404, 'Json Input should be provided.')
# @api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
# class UserHobbyFindRoute(Resource):
#     @api.doc(security=None)
#     @api.marshal_with(register_results)
#     def get(self, hobby, register_after):
#         '''Get user's hobby'''
#         try:
#             resp = User().get_data_by_hobby(hobby, register_after)
#             return masked_json_template(resp, 200)
#         except:
#             abort(400, "Input unrecognizable.")
#
#
@api.route('/register_between/<start_date>/<end_date>')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class UserHobbyBetweenRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(all_user_data)
    def get(self, start_date, end_date):
        '''Get data by ranged dates'''
        try:
            resp = User().get_data_between(start_date, end_date)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")
