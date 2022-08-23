from common import handler_path
from common import handler_yaml
from common import handler_logging
from common import handler_excel
from common import handler_requests
from common import handler_email
from jsonpath import jsonpath
import os
import random
import time


class Handler:
    # 加载handler_path路径配置项
    path = handler_path

    # 通过封装好的handler_yaml读取yml文件配置项
    yml_conf = handler_yaml.read_yaml(os.path.join(path.config_path(), r"conf_pre_back\config_query.yml"))

    # 加载excel配置项
    __excel_config = yml_conf["excel"]
    # 实例化handler_excel
    excel_kie = handler_excel.ExcelHandler(
        os.path.join(path.data_path(), r"data_pre_back\data_query\{}".format(__excel_config["kie"])))

    excel_lrp = handler_excel.ExcelHandler(
        os.path.join(path.data_path(), r"data_pre_back\data_query\{}".format(__excel_config["lrp"])))

    # 加载logger配置项
    __logger_config = yml_conf["logger"]
    # 通过配置文件初始化handler_logging
    logger = handler_logging.logger(get_level=__logger_config["get_level"],
                                    sh_level=__logger_config["sh_level"],
                                    fh_level=__logger_config["fh_level"],
                                    fh_file=os.path.join(path.logs_path(), __logger_config["fh_file"]))

    # 实例化email
    @staticmethod
    def email_send(reports_file):
        # 加载email配置项
        __email_config = Handler.yml_conf["email"]
        email = handler_email.SendMail(user=__email_config["username"], pwd=__email_config["password"],
                                       mail_server=__email_config["server"], mail_sender=__email_config["sender"],
                                       mail_receiver=__email_config["receiver"],
                                       file=reports_file)
        return email

    # 随机生成11位数字
    @staticmethod
    def random_phone(brand_code, headers):
        while True:
            phone = random.choice(["13333333", "14444444", "15555555", "16666666", "17777777", "18888888", "19999999"])
            for i in range(0, 3):
                num = random.randint(0, 9)
                phone += str(num)

            query_member = query_member_info(brand_code, value=phone, headers=headers, query_type="mobile")
            if query_member["code"] != 0:
                Handler().logger.warning("{}可注册...".format(phone))
                return phone

    # 随机生成数字
    @property
    def random_num(self):
        return str(random.randint(10000000000000000, 99999999999999999))

    # 生成uuid
    @property
    def uuid(self):
        return {"uuid": "test_uuid_{}".format(Handler().random_num)}

    # 替换uuid
    @staticmethod
    def replace_uuid(headers):
        headers["ruid"] = str(Handler().uuid)
        return headers

    # 获取access_token
    @staticmethod
    def access_token(username, password):
        Handler.logger.info("access_token接口被调用...")
        data = {
            "grant_type": "password",
            "username": username,
            "password": password
        }
        token = handler_requests.visit(url="https://dl-api.lorealchina.com/api/interface/oauth/token",
                                       method="post",
                                       params=data,
                                       headers={"Authorization": "Basic YWRtaW46Y3JpdXNhZG1pbg=="})
        token = token["access_token"]
        Handler.logger.info("return...token")
        return "Bearer " + token

    # 返回信息头
    @staticmethod
    def headers(username, password):
        headers = {"Authorization": Handler().access_token(username, password), "ruid": str(Handler().uuid)}
        Handler.logger.info("return...headers")
        return headers

    @classmethod
    def brand_code(cls, brand_code):
        return Handler.yml_conf["test_member_data"][brand_code]

    def replace_data(self, brand_code, data):
        import re
        pattern = r"#(.*?)#"
        while re.search(pattern, data):
            key = re.search(pattern, data).group(1)
            data = re.sub(pattern, str(self.brand_code(brand_code)[key]), data, count=1)
        return data

    # def replace_data(self, data):
    #     import re
    #     pattern = r"#(.*?)#"
    #     while re.search(pattern, data):
    #         key = re.search(pattern, data).group(1)
    #         data = re.sub(pattern, str(getattr(self, key)), data, count=1)
    #     return data


# 门店查询
def query_store(brand_code, headers, limit="1"):
    Handler.logger.info("query_store接口被调用...")
    data = {"brand_code": brand_code,
            "program_code": brand_code,
            "limit": limit
            }
    store_list = handler_requests.visit(url=Handler.yml_conf["host"] + "/system/queryStoreList",
                                        method="post",
                                        json=data,
                                        headers=headers)
    return store_list


# 会员注册
def register_member(brand_code, headers, chanel_code="986"):
    Handler.logger.info("register_member接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "name": "tests_ly",
        "mobile": Handler().random_phone(brand_code=brand_code, headers=headers),
        "chanel_code": chanel_code,
        "consentStatus": "1",
        "consentTime": time.strftime("%Y-%m-%d %H:%M:%S"),
        "store_code": query_store(brand_code, headers)["data"][0]["storeNo"]
    }
    headers = Handler.replace_uuid(headers)
    member = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/register",
                                    method="post",
                                    json=data,
                                    headers=headers)
    if member["code"] != 0:
        Handler().logger.error("会员注册: {}".format(member))
    return member


# 会员注册   --- 用来data_initialize.py..
def register_media(brand_code, mobile, store_code, headers):
    Handler.logger.info("register_member接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "mobile": mobile,
        "name": "自动化测试专用_请勿动",
        "birthday": "1995-04-09",
        "chanel_code": "986",
        "consentStatus": "1",
        "consentTime": time.strftime("%Y-%m-%d %H:%M:%S"),
        "store_code": store_code
    }
    headers = Handler.replace_uuid(headers)
    member = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/register",
                                    method="post",
                                    json=data,
                                    headers=headers)
    if member["code"] != 0:
        Handler().logger.error("会员注册: {}".format(member))
    return member


# 查询会员基本信息
def query_member_info(brand_code, value, headers, query_type="union_code"):
    Handler.logger.info("query_member_info接口被调用...")
    data = {
        "Brand_code": brand_code,
        "Program_code": brand_code,
        "queryType": query_type,
        "Value": value
    }
    member_info = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/queryMemberInfo",
                                         method="post",
                                         json=data,
                                         headers=headers)
    return member_info


# 查询当前会员等级
def query_grade(brand_code, value, headers, query_type="union_code"):
    Handler.logger.info("query_grade接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value,
        "category": "default"
    }
    grade = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/queryMemberGrade",
                                   method="post",
                                   json=data,
                                   headers=headers)
    return grade


#  查询会员等级历史
def query_grade_history(brand_code, value, headers, query_type="union_code"):
    Handler.logger.info("query_grade_history接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value
    }
    grade_history = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/queryMemberGradeHistory",
                                           method="post",
                                           json=data,
                                           headers=headers)
    return grade_history


# 订单列表查询
def query_order(brand_code, value, headers, query_type="union_code", order_type=1):
    Handler.logger.info("query_order接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value,
        "orderType": order_type,  # // 交易类型 1 交易 2积分兑换
        "limit": "20",
        "pageNo": "1"
    }
    order_list = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/queryMemberOrderList",
                                        method="post",
                                        json=data,
                                        headers=headers)
    return order_list


# 订单明细查询
def query_order_detail(brand_code, value, trade_no, headers, query_type="union_code", detail_type=1):
    Handler.logger.info("query_order_detail接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value,
        "tradeNo": trade_no,
        "detailType": detail_type                 # 1.订单明细, 2兑换明细
    }

    order_detail = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/queryMemberOrderDetailList",
                                          method="post",
                                          json=data,
                                          headers=headers)
    return order_detail


#  会员当前积分查询
def query_points(brand_code, value, headers, query_type="union_code"):
    Handler.logger.info("query_points接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value,
        "pointTypeGroup": "BP"
    }
    member_points = handler_requests.visit(Handler.yml_conf["host"] + "/member/queryMemberPoints",
                                           method="post",
                                           json=data,
                                           headers=headers)
    return member_points


# 积分变更
def change_points(brand_code, value, points, vender_seq_code, headers, query_type="union_code",
                  change_type="RED", point_type="RDP", change_channel="11", vender_code="2"):
    Handler.logger.info("change_points接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value,
        "changeType": change_type,
        "pointType": point_type,
        "changeSouce": change_channel,
        "points": points,
        "vender_seq_code": vender_seq_code,
        "vender_code": vender_code,
        "remark": "积分变更接口"
    }
    headers = Handler.replace_uuid(headers)
    points_change = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/changeMemberPoints",
                                           method="post",
                                           json=data,
                                           headers=headers)
    return points_change


# 上传兑换信息(新)
def submit_gift_info(brand_code, value, trade_no, code, random_seq_code, total_points, commodity_code, commodity_name,
                     headers, query_type="union_code", order_type="1", total_count=1, commodity_type="P"):
    Handler.logger.info("submit_gift_info接口被调用...")
    data = {"brand_code": brand_code,
            "program_code": brand_code,
            "storeCode": jsonpath(query_store(brand_code, headers), "$..storeNo"[0]),
            "queryType": query_type,
            "value": value,
            "orderType": order_type,
            "tradeNo": trade_no,
            "vender_code": code,
            "vender_seq_code": random_seq_code,
            "tradeTime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "Paymenttime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "TotalCount": total_count,
            "totalPoints": total_points,
            "productList": [
                {
                    "commodityCode": commodity_code,
                    "commodityName": commodity_name,
                    "commodityType": commodity_type,
                    "points": total_points,
                    "discountPoints": 0,
                    "quant": total_count,
                    "amt": total_points
                }
            ]
            }
    gift_info = handler_requests.visit(url=Handler.yml_conf["host"] + "/order/submitGiftInfo",
                                       method="post",
                                       json=data,
                                       headers=Handler().headers)
    return gift_info


# 上传订单
def upload_order(brand_code, store_code, employee_code, member_id, trade_no, total_price, trade_price, price, amt,
                 headers, commodity_code, commodity_name, trade_time, channel_type="union_code"):
    Handler.logger.info("upload_order接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "storeCode": store_code,
        "employeeCode": employee_code,
        "channelType": channel_type,
        "channelMemberId": member_id,
        "orderType": 1,
        "tradeNo": trade_no,
        "tradeTime": trade_time,
        "totalCount": 1,
        "totalPrice": total_price,
        "tradePrice": trade_price,
        "discountPrice": 0,
        "postAmount": 10,
        "remark": "",
        "productList": [
            {
                "commodityCode": commodity_code,
                "commodityName": commodity_name,
                "price": price,
                "discountPrice": 0,
                "quant": 1,
                "amt": amt
            }
        ]
    }
    headers = Handler.replace_uuid(headers)
    order = handler_requests.visit(url=Handler.yml_conf["host"] + "/order/uploadOrderInfo",
                                   method="post",
                                   json=data,
                                   headers=headers)
    return order


# 设置自定义会员标签
def set_define_member_tags(brand_code, union_code, source_tag, key, value, headers):
    Handler.logger.info("set_define_member_tags接口被调用...")
    data = {"brand_code": brand_code,
            "program_code": brand_code,
            "member_code": union_code,
            "sourceTag": source_tag,
            "labels": {
                key: value
            }}
    headers = Handler.replace_uuid(headers)
    tags = handler_requests.visit(url=Handler.yml_conf["host"] + "/tag/addTags",
                                  method="post",
                                  json=data,
                                  headers=headers)
    return tags


# 保存会员入会礼品记录
def save_member_gift_record(brand_code, union_code, headers, campaign_code="campaign_code", gift_code="gift_code"):
    Handler.logger.info("save_member_gift_record接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "member_code": union_code,
        "campaign_code": campaign_code,
        "gift_code": gift_code,
        "store_code": jsonpath(query_store(brand_code, headers), "$..storeNo")[0]
    }
    headers = Handler.replace_uuid(headers)
    gift_record = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/recordJoinGift",
                                         method="post",
                                         json=data,
                                         headers=headers)
    return gift_record


# 查询会员入会礼品记录
def query_member_gift_record(brand_code, union_code):
    Handler.logger.info("query_member_gift_record接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "member_code": union_code
    }
    query_gift_record = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/queryJoinGift",
                                               method="post",
                                               json=data,
                                               headers=Handler().headers)
    return query_gift_record


# 会员退会
def quit_member(brand_code, value, headers, query_type="union_code"):
    Handler.logger.warning("quit_member接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value
    }
    Handler.logger.warning("quit_member接口开始执行requests...")
    headers = Handler.replace_uuid(headers)
    resp = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/quitMember",
                                  method="post",
                                  json=data,
                                  headers=headers)
    Handler.logger.warning("quit_member接口调用成功,开始return...")
    return resp


# 会员积分变更(可欠账)
def deduction_point(brand_code, points, value, headers):
    Handler.logger.warning("deduction_point接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": "union_code",
        "value": value,
        "pointType": "RDP",
        "points": points,
        "changeType": "RED",
        "changeSouce": "01",
        "vender_seq_code": str(int(time.time())),
        "vender_code": "1",
        "begin_date": "20200911",
        "end_date": "20211231",
        "remark": "test_验证查询会员欠账明细"
    }
    headers = Handler.replace_uuid(headers)
    point_deduction = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/deductionPoint",
                                             method="post",
                                             json=data,
                                             headers=headers)
    return point_deduction


# 3.2.58 企业微信BA绑定解绑
def wechat_ba_bind(brand_code, cus_userid, ba_userid, bind_type, member_code, ba_code, headers, opDate, cus_unionid):
    data = {
        "brand_code": brand_code,    # 参数必填
        "program_code": brand_code,  # 参数必填
        "cusUserId": cus_userid,     # 参数必填
        "baUserId": ba_userid,       # 参数必填
        "bindStatus": "1",           # 参数必填   1:绑定 2:解绑
        "bindType": bind_type,       # 参数必填   0:无意义 1:一绑 2:二绑
        "memberCode": member_code,
        "cusUnionId": cus_unionid,
        "baCode": ba_code,
        "opDate": opDate
    }
    headers = Handler.replace_uuid(headers)
    wechat = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/saveWechatBaBind",
                                    method="post",
                                    json=data,
                                    headers=headers)
    return wechat


# # 全渠道会员绑定解绑(新)
# class MemberBinding:
#     """会员媒体信息解绑解绑..."""
#     Handler.logger.info("member_binding接口被调用...")
#
#     def __init__(self, brand_code, value, headers, binding_type="1", query_type="union_code"):
#         self.brand_code = brand_code
#         self.binding_type = binding_type
#         self.value = value
#         self.headers = headers
#         self.query_type = query_type
#
#         """
#             调用方法时,需要用到的传参
#             根据渠道的不同.用到params的参数也不同..
#             通过key,value的形式将params的值赋值到字典.访问接口时通过json=self.data进行传参..
#                 """
#         self.__data = {
#             "brand_code": self.brand_code,
#             "program_code": self.brand_code,
#             "channel": None,
#             "type": self.binding_type,
#             "params": None
#         }
#
#     def __get_url(self):
#         """
#         根据用户传入的类型..通过if判断
#         最终return指向的接口调用...
#             """
#         headers = Handler.replace_uuid(self.headers)
#         resp = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/binding",
#                                       method="post",
#                                       json=self.__data,
#                                       headers=headers)
#         return resp
#
#     def __get_query(self):
#         """
#         调用查询会员基本信息接口
#         每次调用方法时, 初始化一次会员信息查询...
#             """
#         query_member = query_member_info(self.brand_code, value=self.value,
#                                          headers=self.headers, query_type=self.query_type)
#         return query_member
#
#     # 微信
#     def wx_bind(self, channel, open_id, union_id):
#         query_member = self.__get_query()
#         if self.binding_type == "0":
#             params = {
#                 "mobile": jsonpath(query_member, "$..mobile")[0],
#                 "open_id": jsonpath(query_member, "$..media_account[?(@.type=='3')].accountNo")[0],
#                 "seller_name": jsonpath(query_member, "$..media_account[?(@.type=='3')].fromSocialCode")[0]
#             }
#         else:
#             params = {
#                 "mobile": jsonpath(query_member, "$..mobile")[0],
#                 "open_id": open_id,
#                 "seller_name": "微信公众号",
#                 "union_id": union_id
#             }
#         self.__data["params"] = params
#         self.__data["channel"] = channel
#         return self.__get_url()
#
#     # 京东
#     def jd_bind(self, channel, user_id):
#         query_member = self.__get_query()
#         if self.binding_type == "0":
#             params = {
#                 "mobile": jsonpath(query_member, "$..mobile")[0],
#                 "user_id": jsonpath(
#                     query_member, "$..media_account[?(@.type=='6' && @.bindStatus=='1')].accountNo")[0],
#                 "seller_name": jsonpath(
#                     query_member, "$..media_account[?(@.type=='6' && @.bindStatus=='1')].fromSocialCode")[0]
#             }
#         else:
#             params = {
#                 "mobile": jsonpath(query_member, "$..mobile")[0],
#                 "user_id": user_id,
#                 "seller_name": "京东旗舰店"
#             }
#         self.__data["params"] = params
#         self.__data["channel"] = channel
#         return self.__get_url()
#
#     # 天猫
#     def tb_bind(self, channel, tb_nick):
#         query_member = self.__get_query()
#         if self.binding_type == "0":
#             params = {
#                 "mix_mobile": jsonpath(query_member, "$..media_account[?(@.type=='2')].accountNo")[0],
#                 "taobao_nick": jsonpath(query_member, "$..media_account[?(@.type=='2')].nickname")[0],
#                 "seller_name": jsonpath(query_member, "$..media_account[?(@.type=='2')].fromSocialCode")[0]
#             }
#         else:
#             params = {
#                 "mix_mobile": jsonpath(query_member, "$..media_account[?(@.type=='2')].accountNo")[0],
#                 "taobao_nick": tb_nick,
#                 "seller_name": jsonpath(query_member, "$..media_account[?(@.type=='2')].fromSocialCode")[0]
#             }
#         self.__data["params"] = params
#         self.__data["channel"] = channel
#         return self.__get_url()


if __name__ == "__main__":
    pass