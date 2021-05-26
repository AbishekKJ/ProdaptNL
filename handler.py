import json
from prodaptnl import ProdaptNLService


def get_user_posts_comments(event, context):
    pdpt_obj = ProdaptNLService.get_data_from_external_api()
    path = event.get("path", "")
    fetch_by_id_map = {"post": "post_id",
                       "comment": "comment_id"}
    response = {"headers": {
        'Access-Control-Allow-Origin': '*'
    }}
    if path:
        if path == "/prodapt/service/posts":
            data = pdpt_obj.get_posts()
            response["statusCode"] = 200
            response["body"] = json.dumps(data)
            return response
        elif "/prodapt/service/post/" in path or "/prodapt/service/comment/" in path:
            path_parameters = event.get("pathParameters", {})
            print("path paramaters", path_parameters)
            if path_parameters:
                id_field = path.split("/")[-2]
                print("id field", id_field)
                key = fetch_by_id_map.get(id_field)
                value = path_parameters.get(key, "")
                print("value", value)
                print("id of value", type(value))
                try:
                    value = int(value)
                    data = pdpt_obj.get_post_comment_by_id(id_field, value)
                    response["statusCode"] = 200
                    response["body"] = json.dumps(data)
                except Exception as e:
                    response["statusCode"] = 412
                    response["body"] = f"{id_field} id should be Integer"
                return response
    response["statusCode"] = 404
    response["body"] = "Data not found"
    return response
