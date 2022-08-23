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

    # loaded_path
    path = handler_path

    # 路径:\data\data_prd\data_query..
    data_path = os.path.join(os.path.join(path.data_path(), "data_prd"), "data_query")

    # \config\conf_prd\config_write..
    yml_conf = handler_yaml.read_yaml(os.path.join(os.path.join(path.config_path(), "conf_prd"), "config_query.yml"))

    excel_query_common = handler_excel.ExcelHandler(
        os.path.join(path.data_path(), r"data_prd\data_query\{}".format(yml_conf["excel"]["query_common"])))

    excel_query_invocation_info = handler_excel.ExcelHandler(
        os.path.join(path.data_path(), r"data_prd\data_query\{}".format(yml_conf["excel"]["query_invocation_info"])))

    excel_member_grade_calculator = handler_excel.ExcelHandler(
        os.path.join(path.data_path(), r"data_prd\data_query\{}".format(yml_conf["excel"]["member_grade_calculator"])))

    @property
    def logger(self):
        logger = handler_logging.logger(
            get_level=Handler.yml_conf["logger"]["get_level"],
            sh_level=Handler.yml_conf["logger"]["sh_level"],
            fh_level=Handler.yml_conf["logger"]["fh_level"],
            fh_file=os.path.join(Handler.path.logs_path(), Handler.yml_conf["logger"]["fh_file"])
        )
        return logger

    @staticmethod
    def email_send(reports_file):
        email = handler_email.SendMail(
            user=Handler.yml_conf['email']['username'],
            pwd=Handler.yml_conf['email']['password'],
            mail_server=Handler.yml_conf['email']['server'],
            mail_sender=Handler.yml_conf['email']['sender'],
            mail_receiver=Handler.yml_conf['email']['receiver'],
            file=reports_file
        )
        return email

    # 随机生成11位数字
    @staticmethod
    def random_phone(brand_code, headers):
        while True:
            phone = random.choice(["13333333", "15555555", "16666666", "17777777", "18888888", "19999999"])
            for i in range(0, 3):
                num = random.randint(0, 9)
                phone += str(num)

            query_member = query_member_info(brand_code, value=phone, headers=headers, query_type="mobile")
            if query_member["code"] != 0:
                return phone
            else:
                continue

    # 随机生成数字
    @property
    def random_num(self):
        string = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'])
        return str(int((time.time()))) + str(random.randint(1, 9999)) + string

    @property
    def names(self):
        return f"{Handler.yml_conf['test_standard']['names']}"

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
    def access_token(brand_code):
        data = {
            "grant_type": "password",
            "username": Handler.yml_conf["access_token"][brand_code]["username"],
            "password": Handler.yml_conf["access_token"][brand_code]["password"]
        }
        token = handler_requests.visit(url="https://dl-api.lorealchina.com/api/interface/oauth/token",
                                       method="post",
                                       params=data,
                                       headers={"Authorization": "Basic YWRtaW46Y3JpdXNhZG1pbg=="})
        token = token["access_token"]
        return "Bearer " + token

    # 返回信息头
    @staticmethod
    def headers(brand_code):
        headers = {"Authorization": Handler.access_token(brand_code=brand_code), "ruid": str(Handler().uuid)}
        return headers

    @classmethod
    def conf_member_data(cls, brand_code):
        return Handler.yml_conf["test_member_data"][brand_code]

    @classmethod
    def crm_trade_no(cls, brand_code, channel):
        return Handler.yml_conf["crm_trade_no"][brand_code][channel]

    @classmethod
    def replace_data(cls, brand_code, data):
        import re
        pattern = r"&(.*?)&"
        while re.search(pattern, data):
            key = re.search(pattern, data).group(1)
            if key in ("tradeNo", "oriOrderId"):
                data = re.sub(pattern, str(cls.crm_trade_no(brand_code, channel="online")["trade_no"]), data, count=1)
            else:
                data = re.sub(pattern, str(cls.conf_member_data(brand_code)[key]), data, count=1)
        return data

    """if pattern in ("test_tradeNo_online", "test_tradeNo_offline"):
                if pattern == "test_tradeNo_online":
                    data = re.sub(pattern, str(self.crm_trade_no(brand_code, channel="online")[key]), data, count=1)
                else:
                    data = re.sub(pattern, str(self.crm_trade_no(brand_code, channel="offline")[key]), data, count=1)
            else:
                data = re.sub(pattern, str(self.conf_member_data(brand_code)[key]), data, count=1)
        return data"""

    # def replace_data(self, data):
    #     import re
    #     pattern = r"#(.*?)#"
    #     while re.search(pattern, data):
    #         key = re.search(pattern, data).group(1)
    #         data = re.sub(pattern, str(getattr(self, key)), data, count=1)
    #     return data


# 门店查询
def query_store(brand_code, headers, limit="1"):
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
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "name": Handler.yml_conf['test_standard']['names'],
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
def register_media(brand_code, mobile, store_code, ba_code, headers):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "mobile": mobile,
        "officePhone": "021-12345678",
        "name": "自动化测试专用_请勿动",
        "birthday": "1995-04-09",
        "gender": "F",
        "email": "924433468@qq.com",
        "chanel_code": "986",
        "store_code": store_code,
        "ba_code": ba_code,
        "RB_Member": "小黑板专用",
        "consentStatus": "1",
        "consentTime": "1995-04-09 00:00:00",
        "regTime": "1995-04-09 00:00:00",
        "address": [
            {
                "address_type": "1",
                "isDefault": "Y",
                "provinceCode": "SH",
                "cityCode": "C1764",
                "countyCode": "C2468",
                "zipcode": "00000",
                "location": "大宁中心广场",
                "Phone": "021-8888888888"
            }
        ],
        "certificate": [
            {
                "type": "1", "cardNo": "412702199504093176"
            }
        ]
    }
    headers = Handler.replace_uuid(headers)
    member = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/registerNew",
                                    method="post",
                                    json=data,
                                    headers=headers)
    if member["code"] != 0:
        Handler().logger.error("会员注册: {}".format(member))
    return member


# 查询会员基本信息
def query_member_info(brand_code, value, headers, query_type="union_code"):
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
        "Paymenttime": trade_time,
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
                "quAnt".lower(): 1,
                "amt": amt,
                "type": "YFG"
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
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value
    }
    headers = Handler.replace_uuid(headers)
    resp = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/quitMember",
                                  method="post",
                                  json=data,
                                  headers=headers)
    return resp


# 会员积分变更(可欠账)
def deduction_point(brand_code, points, value, headers):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": "union_code",
        "value": value,
        "pointType": "RDP",
        "points": points,
        "changeType": "RED",
        "changeSouce": "01",
        str.lower("venDer_seq_code"): str(int(time.time())),
        str.lower("venDer_code"): "1",
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


# 全渠道会员绑定解绑(新)
class MemberBinding:
    """会员媒体信息解绑解绑..."""
    def __init__(self, brand_code, value, headers, binding_type="1", query_type="union_code"):
        self.brand_code = brand_code
        self.binding_type = binding_type
        self.value = value
        self.headers = headers
        self.query_type = query_type

        """
            调用方法时,需要用到的传参
            根据渠道的不同.用到params的参数也不同..
            通过key,value的形式将params的值赋值到字典.访问接口时通过json=self.data进行传参..
                """
        self.__data = {
            "brand_code": self.brand_code,
            "program_code": self.brand_code,
            "channel": None,
            "type": self.binding_type,
            "params": None
        }

    def __get_url(self):
        """
        根据用户传入的类型..通过if判断
        最终return指向的接口调用...
            """
        headers = Handler.replace_uuid(self.headers)
        resp = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/binding",
                                      method="post",
                                      json=self.__data,
                                      headers=headers)
        return resp

    def __get_query(self):
        """
        调用查询会员基本信息接口
        每次调用方法时, 初始化一次会员信息查询...
            """
        query_member = query_member_info(self.brand_code, value=self.value,
                                         headers=self.headers, query_type=self.query_type)
        return query_member

    # 微信
    def wx_bind(self, channel, open_id, union_id):
        query_member = self.__get_query()
        if self.binding_type == "0":
            params = {
                "mobile": jsonpath(query_member, "$..mobile")[0],
                "open_id": jsonpath(query_member, "$..media_account[?(@.type=='3')].accountNo")[0],
                "seller_name": jsonpath(query_member, "$..media_account[?(@.type=='3')].fromSocialCode")[0]
            }
        else:
            params = {
                "mobile": jsonpath(query_member, "$..mobile")[0],
                "open_id": open_id,
                "seller_name": "微信公众号",
                "union_id": union_id
            }
        self.__data["params"] = params
        self.__data["channel"] = channel
        return self.__get_url()

    # 京东
    def jd_bind(self, channel, user_id):
        query_member = self.__get_query()
        if self.binding_type == "0":
            params = {
                "mobile": jsonpath(query_member, "$..mobile")[0],
                "user_id": jsonpath(
                    query_member, "$..media_account[?(@.type=='6' && @.bindStatus=='1')].accountNo")[0],
                "seller_name": jsonpath(
                    query_member, "$..media_account[?(@.type=='6' && @.bindStatus=='1')].fromSocialCode")[0]
            }
        else:
            params = {
                "mobile": jsonpath(query_member, "$..mobile")[0],
                "user_id": user_id,
                "seller_name": "京东旗舰店"
            }
        self.__data["params"] = params
        self.__data["channel"] = channel
        return self.__get_url()

    # 天猫
    def tb_bind(self, channel, tb_nick):
        query_member = self.__get_query()
        if self.binding_type == "0":
            params = {
                "mix_mobile": jsonpath(query_member, "$..media_account[?(@.type=='2')].accountNo")[0],
                str.lower("TaoBao_nick"): jsonpath(query_member, "$..media_account[?(@.type=='2')].nickname")[0],
                "seller_name": jsonpath(query_member, "$..media_account[?(@.type=='2')].fromSocialCode")[0]
            }
        else:
            params = {
                "mix_mobile": jsonpath(query_member, "$..media_account[?(@.type=='2')].accountNo")[0],
                str.lower("TaoBao_nick"): tb_nick,
                "seller_name": jsonpath(query_member, "$..media_account[?(@.type=='2')].fromSocialCode")[0]
            }
        self.__data["params"] = params
        self.__data["channel"] = channel
        return self.__get_url()


if __name__ == "__main__":
    dd = Handler.headers('lrp')
    print(dd)
    print(Handler().uuid)
    pass
