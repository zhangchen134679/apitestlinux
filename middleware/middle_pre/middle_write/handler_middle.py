from common import handler_path
from common import handler_yaml
from common import handler_logging
from common import handler_excel
from common import handler_requests
from common import handler_email
from jsonpath import jsonpath
import random
import time
import os


class Handler(object):

    # loaded_path
    path = handler_path

    # \data\data_prd\data_write..
    __data_path = os.path.join(os.path.join(path.data_path(), "data_prd"), "data_write")

    # \data\data_smoke..
    __data_smoke_path = os.path.join(path.data_path(), "data_smoke")

    # \config\conf_prd\config_write..
    yml_conf = handler_yaml.read_yaml(os.path.join(os.path.join(path.config_path(), "conf_prd"), "config_write.yml"))

    excel_write_common = handler_excel.ExcelHandler(
        os.path.join(__data_path, r"{}".format(yml_conf["excel"]["write_common"])))

    excel_upload_order_info = handler_excel.ExcelHandler(
        os.path.join(__data_path, r"{}".format(yml_conf["excel"]["upload_order_info"])))

    excel_upload_message_info = handler_excel.ExcelHandler(
        os.path.join(__data_path, r"{}".format(yml_conf["excel"]["upload_message_info"])))

    excel_smoke_d2s = handler_excel.ExcelHandler(
        os.path.join(__data_smoke_path, r"{}".format(yml_conf["excel"]["smoke_common"]["d2s"])))

    excel_upload_change_grade_HR = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_HR.xlsx'))

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

    @staticmethod
    def __get_query(brand_code, value, headers, query_type="union_code"):
        data = {
            "Brand_code": brand_code,
            "Program_code": brand_code,
            "queryType": query_type,
            "Value": value
        }
        get_query = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/queryMemberInfo",
                                           method="post",
                                           json=data,
                                           headers=headers)
        return get_query

    @staticmethod
    def random_phone(brand_code, headers):
        while True:
            phone = random.choice(["1333333", "1555555", "1666666", "1777777", "1888888", "1999999"])
            for i in range(0, 4):
                num = random.randint(0, 9)
                phone += str(num)

            query_member = Handler.__get_query(brand_code, value=phone, headers=headers, query_type="mobile")
            try:
                if query_member["code"] not in (0, 2):
                    return phone
                else:
                    pass
                    # Handler.logger.info("__get_query: {}".format(query_member))
            except Exception:
                Handler().logger.error("__get_query: {}".format(query_member))
                raise

    @staticmethod
    def access_token(brand_code):
        data = {
            "grant_type": "password",
            "username": Handler.yml_conf["access_token"][brand_code]["username"],
            "password": Handler.yml_conf["access_token"][brand_code]["password"]
        }
        result = handler_requests.visit(url="https://dl-api.lorealchina.com/api/interface/oauth/token",
                                        method="post",
                                        params=data,
                                        headers={"Authorization": "Basic YWRtaW46Y3JpdXNhZG1pbg=="})
        access_token = result["access_token"]
        return "Bearer " + access_token

    @staticmethod
    def headers(brand_code):
        headers = {"Authorization": Handler.access_token(brand_code=brand_code), "ruid": str(Handler().uuid)}
        return headers

    @property
    def random_num(self):
        string = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'])
        return str(int((time.time()))) + str(random.randint(1, 9999)) + string

    @property
    def random_trade(self):
        return f"{Handler.yml_conf['test_standard']['order'] + Handler().random_num}"

    @property
    def names(self):
        return f"{Handler.yml_conf['test_standard']['names']}"

    @property
    def uuid(self):
        return {"uuid": "test_uuid_{}".format(Handler().random_num)}

    @staticmethod
    def replace_uuid(headers):
        headers["ruid"] = str(Handler().uuid)
        return headers

    def replace_data(self, data):
        import re
        pattern = r"&(.*?)&"
        while re.search(pattern, data):
            key = re.search(pattern, data).group(1)
            data = re.sub(pattern, str(getattr(self, key)), data, count=1)
        return data


# 门店查询
def query_store(brand_code, headers, limit="5"):
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
def register_member(brand_code, headers, chanel_code="986", var=''):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "name": Handler.yml_conf['test_standard']['names'],
        "birthday": "1995-04-09",
        "mobile": Handler().random_phone(brand_code=brand_code, headers=headers),
        "Chanel_code".lower(): chanel_code,
        "consentStatus": "1",
        "consentTime": "1995-04-09 00:00:00",
        "store_code": Handler.yml_conf["crm_store"][brand_code]["deal_store_no"],
        "regTime": "1995-04-09 00:00:00"
    }
    if chanel_code == "976":
        data["media_account"] = [
            {
                "type": "2",
                "nickname": "nickname_{}".format(Handler().random_num),
                "fromSocialCode": Handler.yml_conf["crm_store"][brand_code]["name"]
            }
        ]
    headers = Handler.replace_uuid(headers)
    member = handler_requests.visit(url=Handler.yml_conf["host"] + var + "/member/registerNew",
                                    method="post",
                                    json=data,
                                    headers=headers)
    try:
        if member["code"] != 0:
            Handler().logger.error("register_member: {}".format(member))
        return member
    except Exception as err:
        Handler().logger.error("register_member: {}".format(member))
        raise err


# 会员注册_绑定媒体信息
def register_wechat(brand_code, headers):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "name": Handler.yml_conf['test_standard']['names'],
        "birthday": "1995-04-09",
        "mobile": Handler().random_phone(brand_code=brand_code, headers=headers),
        "Chanel_code".lower(): "986",
        "consentStatus": "1",
        "consentTime": time.strftime("%Y-%m-%d %H:%M:%S"),
        "store_code": Handler.yml_conf["crm_store"][brand_code]["deal_store_no"],
        "media_account": [
            {
                "type": "3",
                "accountNo": "openId_{}".format(Handler().random_num),
                "unionId": "unionId_{}".format(Handler().random_num),
                "fromSocialCode": "微信公众号"
            }
        ]
    }
    headers = Handler.replace_uuid(headers)
    media = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/register",
                                   method="post",
                                   json=data,
                                   headers=headers)
    try:
        if media["code"] != 0:
            Handler().logger.error("register_wechat: {}".format(media))
        return media
    except Exception as err:
        Handler().logger.error("register_wechat: {}".format(media))
        raise err


# 查询会员基本信息
def query_member_info(brand_code, value, headers, query_type="union_code"):
    data = {
        "Brand_code": brand_code,
        "Program_code": brand_code,
        "queryType": query_type,
        "Value": value
    }
    query_member = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/queryMemberInfo",
                                          method="post",
                                          json=data,
                                          headers=headers)
    try:
        if query_member["code"] != 0:
            Handler().logger.error("%s query_member_info: %s" % (brand_code, query_member),)
        return query_member
    except Exception:
        Handler().logger.error("%s query_member_info: %s" % (brand_code, query_member),)
        raise


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


#  会员当前积分查询
def query_points(brand_code, value, headers, query_type="union_code", point_type="BP"):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value,
        "pointTypeGroup": point_type
    }
    member_points = handler_requests.visit(Handler.yml_conf["host"] + "/member/queryMemberPoints",
                                           method="post",
                                           json=data,
                                           headers=headers)
    return member_points


#  会员积分明细查询
def query_points_detail(brand_code, value, headers, query_type="union_code", point_type="BP"):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value,
        "pageNo": "1",
        "limit": "10",
        "pointTypeGroup": point_type
    }
    member_points = handler_requests.visit(Handler.yml_conf["host"] + "/member/queryMemberPointsDetailList",
                                           method="post",
                                           json=data,
                                           headers=headers)
    return member_points


# 订单列表查询
def query_order(brand_code, value, headers, query_type="union_code", order_type=1):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value,
        "orderType": order_type,
        "limit": "20",
        "pageNo": "1"
    }
    order_list = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/queryMemberOrderList",
                                        method="post",
                                        json=data,
                                        headers=headers)
    return order_list


# 订单明细查询
def query_order_detail(brand_code, value, trade_no, headers, query_type="union_code", detail_type=2):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value,
        "tradeNo": trade_no,
        "detailType": detail_type       # 交易类型: 1.订单明细 2.兑换明细  type:int
    }
    order_detail = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/queryMemberOrderDetailList",
                                          method="post",
                                          json=data,
                                          headers=headers)
    return order_detail


# 订单历史订单
def query_order_history(brand_code, value, headers, query_type="union_code",
                        page_no="1", page_size="10", begin_date="20190101", end_date="20220101"):
    data = {
        "brandCode": brand_code,
        "programCode": brand_code,
        "queryType": query_type,
        "value": value,
        "beginDate": begin_date,
        "endDate": end_date,
        "pageNo": page_no,
        "pageSize": page_size
    }
    order_history = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/queryOrderHistoryInfo",
                                          method="post",
                                          json=data,
                                          headers=headers)
    return order_history


# 上传会员活动信息
def send_activity_info(brand_code, value, trade_no,detail_no,sku_code,headers, query_type="union_code",
                       act_code="EC30010001AC", act_name="空瓶回收"):
    data = {
        "brandCode": brand_code,
        "programCode": brand_code,
        "queryType": query_type,
        "value": value,
        "actSno": trade_no,
        "actCode": act_code,
        "actName": act_name,
        "actInfo":[
        {
            "orderNo":trade_no,
            "detailNo":detail_no,
            "skuCode":sku_code,
            "points":"28",
            "quantity":"1"
        }
        ]
    }
    headers = Handler.replace_uuid(headers)
    order_sendactivityinfo = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/sendActivityInfo",
                                          method="post",
                                          json=data,
                                          headers=headers)
    return order_sendactivityinfo

# 积分变更
def change_points(brand_code, value, points, vender_seq_code, headers, query_type="union_code",
                  change_type="ACC", point_type="ABP", change_channel="07", vender_code="1"):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value,
        "changeType": change_type,                   # 变动方式      ACC RED
        "pointType": point_type,                     # 积分类型      附件4
        "changeSouce": change_channel,               # 积分变动渠道   附件1
        "points": points,                            # 积分数量
        "venDer_seq_code".lower(): vender_seq_code,  # 流水号        调用方确保该值唯一
        "venDer_code".lower(): vender_code,          # 供应商编号     附件9
        "remark": "积分变更接口"
    }
    headers = Handler.replace_uuid(headers)
    points_change = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/changeMemberPoints",
                                           method="post",
                                           json=data,
                                           headers=headers)
    return points_change


# 上传兑换信息(新)
def submit_gift_info(brand_code, value, store_code, trade_no, vender_code, vender_seq_code, total_points, headers,
                     commodity_code, commodity_name, query_type="union_code", order_type="1", commodity_type="P"):
    data = {"brand_code": brand_code,
            "program_code": brand_code,
            "storeCode": store_code,
            "queryType": query_type,
            "value": value,
            "orderType": order_type,
            "tradeNo": trade_no,
            "venDer_code".lower(): vender_code,
            "venDer_seq_code".lower(): vender_seq_code,
            "tradeTime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "Paymenttime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "TotalCount": 1,
            "totalPoints": total_points,
            "productList": [
                {
                    "commodityCode": commodity_code,
                    "commodityName": commodity_name,
                    "commodityType": commodity_type,
                    "points": total_points,
                    "discountPoints": 0,
                    "quAnt".lower(): 1,
                    "amt": total_points
                }
            ]
            }
    headers = Handler.replace_uuid(headers)
    gift_info = handler_requests.visit(url=Handler.yml_conf["host"] + "/order/submitGiftInfo",
                                       method="post",
                                       json=data,
                                       headers=headers)
    return gift_info


# 上传订单
def upload_order(brand_code, member_id, store_code, trade_no, total_price, trade_price, price, amt,
                 headers, commodity_code, commodity_name, channel_type="union_code"):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "storeCode": store_code,
        "channelType": channel_type,
        "channelMemberId": member_id,
        "orderType": 1,
        "tradeNo": trade_no,
        "tradeTime": time.strftime("%Y-%m-%d %H:%M:%S"),
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
def member_add_tags(brand_code, union_code, source_tag, key, value, headers):
    data = {"brand_code": brand_code,
            "program_code": brand_code,
            "member_code": union_code,
            "sourceTag": source_tag,
            "labels": {
                key: value
            }}
    tags = handler_requests.visit(url=Handler.yml_conf["host"] + "/tag/addTags",
                                  method="post",
                                  json=data,
                                  headers=headers)
    return tags


# 查询自定义会员标签
def query_member_tags(brand_code, value, source_tag, headers, var=''):
    data = {"brand_code": brand_code,
            "program_code": brand_code,
            "member_code": value,
            "sourceTag": source_tag
            }
    tags = handler_requests.visit(url=Handler.yml_conf["host"] + var + "/tag/viewTags",
                                  method="post",
                                  json=data,
                                  headers=headers)
    return tags


# 保存会员入会礼品记录
def member_gift_record(brand_code, union_code, store_code, headers, campaign_code="campaign_code", gift_code="gift_code"):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "member_code": union_code,
        "campaign_code": campaign_code,
        "gift_code": gift_code,
        "store_code": store_code
    }
    headers = Handler.replace_uuid(headers)
    gift_record = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/recordJoinGift",
                                         method="post",
                                         json=data,
                                         headers=headers)
    return gift_record


# 查询会员入会礼品记录
def query_member_gift_record(brand_code, value, headers):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "member_code": value
    }
    query_gift_record = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/queryJoinGift",
                                               method="post",
                                               json=data,
                                               headers=headers)
    return query_gift_record


# 会员退会
def quit_member(brand_code, value, headers, query_type="mobile"):
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


class ReplaceDate(object):
    """
    可以传入union_code查询会员基本信息,通过re全部替换用例中的value值
    employee_code..用于替换用例中upload_order_verifyOrder..
    product_code..用于替换用例中upload_order_verifyOrder..upload_order_verifyGrade..submit_gift_info..
    product_name..用于替换用例中upload_order_verifyOrder..upload_order_verifyGrade..submit_gift_info..
    store_code..
    """
    def __init__(self, brand_code, headers, value=None, query_type="union_code"):
        self.brand = brand_code
        self.headers = headers

        if value is not None and value:
            self.get_query = query_member_info(self.brand, value=value, headers=headers, query_type=query_type)

    @property
    def brand_code(self):
        return self.brand

    @property
    def time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def names(self):
        return f"{Handler.yml_conf['test_standard']['names']}"

    @property
    def employee_code(self):
        return Handler.yml_conf["crm_employee"][self.brand]

    @property
    def product_code(self):
        return Handler.yml_conf["crm_product"][self.brand]["code"]

    @property
    def product_name(self):
        return Handler.yml_conf["crm_product"][self.brand]["name"]

    @property
    def tb_store_name(self):
        return Handler.yml_conf["crm_store"][self.brand]["name"]

    @property
    def store_code(self):
        if self.brand == "kie":
            return Handler.yml_conf["crm_store"][self.brand]["replace_deal_store_no"]
        else:
            return Handler.yml_conf["crm_store"][self.brand]["deal_store_no"]

    @property
    def offline_store_code(self):
        """
        :param 读取配置文件的线下门店替换case29中天猫门店, 从而验证更新时..门店不会被更新..test_3_2_03会员基本信息更新.py
            """
        return Handler.yml_conf["crm_store"][self.brand]["offline_store_no"]

    @property
    def random_mobile(self):
        return Handler().random_phone(self.brand, headers=self.headers)

    @property
    def mobile(self):
        return jsonpath(self.get_query, "$..mobile")[0]

    @property
    def union_code(self):
        return jsonpath(self.get_query, "$..union_code")[0]

    @property
    def cardno(self):
        return jsonpath(self.get_query, "$..cardno")[0]

    @property
    def marsMemberNum(self):
        return jsonpath(self.get_query, "$..marsMemberNum")[0]

    @property
    def openId(self):
        try:
            return jsonpath(self.get_query, "$..media_account[?(@.type=='3')].accountNo")[0]
        except TypeError:
            Handler().logger.error("jsonpath..openId: {}".format(self.get_query))

    @property
    def unionId(self):
        try:
            return jsonpath(self.get_query, "$..media_account[?(@.type=='3')].unionId")[0]
        except TypeError:
            Handler().logger.error("jsonpath..unionId: {}".format(self.get_query))

    @property
    def encryptMobile(self):
        try:
            return jsonpath(self.get_query, "$..media_account[?(@.type=='2')].accountNo")[0]
        except TypeError:
            Handler().logger.error("jsonpath..encryptMobile: {}".format(self.get_query))

    @property
    def taobaoid(self):
        try:
            json_nickname = jsonpath(self.get_query, "$..media_account[?(@.type=='2')].nickname")[0]
            if not json_nickname:
                Handler().logger.error("jsonpath..taobaoid: {}".format(self.get_query))
                return json_nickname
            return json_nickname
        except TypeError:
            Handler().logger.error("jsonpath..taobaoid: {}".format(self.get_query))

    @property
    def JDpin(self):
        try:
            return jsonpath(self.get_query, "$.data.media_account[?(@.type=='6')].accountNo")[0]
        except TypeError:
            Handler().logger.error("jsonpath..JDpin: {}".format(self.get_query))

    # re替换数据
    def replace_data(self, data):
        import re
        pattern = r"&(.*?)&"
        while re.search(pattern, data):
            key = re.search(pattern, data).group(1)
            data = re.sub(pattern, str(getattr(self, key)), data, count=1)
        return data


# 全渠道会员绑定解绑(新)
class MemberBinding(object):
    """会员媒体信息解绑解绑退会..."""

    def __init__(self, brand_code, value, headers, binding_type="1", query_type="union_code"):
        self.brand_code = brand_code
        self.binding_type = binding_type
        self.value = value
        self.headers = headers
        self.query_type = query_type

        self.__data = {
            "brand_code": self.brand_code,
            "program_code": self.brand_code,
            "channel": None,
            "type": self.binding_type,
            "params": None
        }

    def __get_query(self):
        result = query_member_info(self.brand_code, value=self.value,
                                   headers=self.headers, query_type=self.query_type)
        return result

    # 微信
    def wx_bind(self, channel):
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
                "open_id": "open_id" + str(int(time.time())),
                "seller_name": "微信公众号",
                "union_id": "union_id" + str(int(time.time()))
            }
        return self.replace_data(channel, params)

    # 京东
    def jd_bind(self, channel):
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
                "user_id": "jd_pin" + str(int(time.time())),
                "seller_name": "京东旗舰店"
            }
        return self.replace_data(channel, params)

    # 天猫
    def tb_bind(self, channel):
        query_member = self.__get_query()
        if self.binding_type == "0":
            params = {
                "mix_mobile": jsonpath(
                    query_member, "$..media_account[?(@.type=='2' && @.bindStatus=='1')].accountNo")[0],
                "TaoBao_nick".lower(): jsonpath(
                    query_member, "$..media_account[?(@.type=='2' && @.bindStatus=='1')].nickname")[0],
                "seller_name": jsonpath(
                    query_member, "$..media_account[?(@.type=='2' && @.bindStatus=='1')].fromSocialCode")[0]
            }
        else:
            params = {
                "mix_mobile": jsonpath(query_member, "$..media_account[?(@.type=='2')].accountNo")[0],
                "TaoBao_nick".lower(): "tb_nike" + str(int(time.time())),
                "seller_name": jsonpath(query_member, "$..media_account[?(@.type=='2')].fromSocialCode")[0]
            }
        return self.replace_data(channel, params)

    def all_bind(self):
        self.tb_bind(channel="976")
        self.jd_bind(channel="9AL")
        self.wx_bind(channel="6P0")

    def try_bind(self):
        try:
            self.tb_bind("976")
        finally:
            try:
                self.jd_bind("9AL")
            finally:
                try:
                    self.wx_bind("6P0")
                finally:
                    return "quit_member: {}".format(self.quit_member())

    def quit_member(self):
        headers = Handler.replace_uuid(self.headers)
        result = quit_member(self.brand_code, value=self.value, headers=headers, query_type=self.query_type)
        return result

    def replace_data(self, channel, params):
        self.__data['channel'] = channel
        self.__data['params'] = params
        return self.__run()

    def __run(self):
        """
        根据用户传入的类型..通过if判断
        最终return指向的接口调用...
        """
        headers = Handler.replace_uuid(self.headers)
        result = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/binding",
                                        method="post",
                                        json=self.__data,
                                        headers=headers)
        return result


if __name__ == "__main__":
    # brand = "lrl"
    # token = (Handler().headers(brand))
    # print(token)
    # print(register_member(brand, headers=token))
    # bind = MemberBinding(brand, '13213332698', headers=token, binding_type="0", query_type="mobile")
    # print(bind.try_bind())
    # aa = Handler().excel_smoke_d2s
    # bb = aa.read_data('smoke_request')
    # print(bb)

    pass
    # from middleware.middle_prd.middle_write import handler_middle
    token = Handler().headers('hr')
    # result = register_member('lrp', headers=token)
    # result = result['data']['union_code']
    # member = MemberBinding('lrp', value=result, headers=token)
    # aa = member.jd_bind('9AL')
    # print(aa)
    # bb = query_member_info('lrp', value=result, headers=token)
    print(token)
