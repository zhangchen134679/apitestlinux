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
    yml_conf = handler_yaml.read_yaml(os.path.join(path.config_path(), r"conf_pre_apitest_back\config_write.yml"))

    # 加载excel配置项
    __excel_config = yml_conf["excel"]

    # 实例化handler_excel
    excel_kie = handler_excel.ExcelHandler(
        os.path.join(path.data_path(), r"data_pre_back\data_write\{}".format(__excel_config["kie"])))

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
            else:
                Handler().logger.error("{}已存在...".format(phone))
                continue

    # 随机生成数字
    @property
    def random_num(self):
        return str(random.randint(1000000000000000000000, 99000000000000000000000))

    # 随机生成订单编号
    @property
    def random_trade(self):
        return "test_trade_{}".format(Handler().random_num)

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

    """
    # 获取access_token
    @property
    def access_token(self):
        data = {
            "grant_type": "password",
            "username": Handler.yml_conf["users_data"]["pre"]["user"],
            "password": Handler.yml_conf["users_data"]["pre"]["pwd"]
        }
        token = handler_requests.visit(url="http://crmapp.lorealchina.com/vb/oauth/token",
                                       method="post",
                                       params=data,
                                       headers={"Authorization": "Basic bGFuY29tZV9hcHA6MTIzNDU2Nzg="})
        return token["access_token"]

    # 返回信息头
    @property
    def headers(self):
        return {"access_token": Handler().access_token, "ruid": str(Handler().uuid), "principal": "admin"}
    """

    """
    def replace_data(self, data):
        import re
        pattern = r"#(.*?)#"
        while re.search(pattern, data):
            key = re.search(pattern, data).group(1)
            data = re.sub(pattern, str(getattr(self, key)), data, count=1)
        return data
    """


# 门店查询
def query_store(brand_code, headers, limit="5"):
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
def register_member(brand_code, store_code, headers, chanel_code="6P0"):
    Handler.logger.info("register_member接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "name": "tests_ly",
        "mobile": Handler().random_phone(brand_code=brand_code, headers=headers),
        "chanel_code": chanel_code,
        "consentStatus": "1",
        "consentTime": time.strftime("%Y-%m-%d %H:%M:%S"),
        "store_code": store_code
    }
    headers["ruid"] = str(Handler().uuid)
    media = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/register",
                                   method="post",
                                   json=data,
                                   headers=headers)
    if media["code"] != 0:
        Handler().logger.error("会员注册: {}".format(media))
    return media


# 会员注册_绑定媒体信息
def register_media(brand_code, store_code, tb_store_name, headers):
    Handler.logger.info("register_member接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "name": "tests_ly",
        "mobile": Handler().random_phone(brand_code=brand_code, headers=headers),
        "chanel_code": "976",
        "consentStatus": "1",
        "consentTime": time.strftime("%Y-%m-%d %H:%M:%S"),
        "store_code": store_code,
        "media_account": [
            {
                "type": "3",
                "accountNo": "openId_" + str(int(time.time())),
                "unionId": "unionId_" + str(int(time.time())),
                "fromSocialCode": "微信公众号"
            },
            {
                "type": "2",
                "nickname": "nickname_" + str(int(time.time())),
                "fromSocialCode": tb_store_name
            },
            {
                "type": "6",
                "accountNo": "jd_pin_" + str(int(time.time())),
                "fromSocialCode": "京东旗舰店"
            }
        ]
    }
    headers["ruid"] = str(Handler().uuid)
    media = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/register",
                                   method="post",
                                   json=data,
                                   headers=headers)
    if media["code"] != 0:
        Handler().logger.error("会员注册: {}".format(media))
    return media


# 查询会员基本信息
def query_member_info(brand_code, value, headers, query_type="mobile"):
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
    grade = handler_requests.visit(url=Handler.yml_conf["host"]["pre"] + "/member/queryMemberGrade",
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
    grade_history = handler_requests.visit(url=Handler.yml_conf["host"]["pre"] + "/member/queryMemberGradeHistory",
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
    order_list = handler_requests.visit(url=Handler.yml_conf["host"]["pre"] + "/member/queryMemberOrderList",
                                        method="post",
                                        json=data,
                                        headers=headers)
    return order_list


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
def change_points(brand_code, value, points, random_seq_code, headers, query_type="union_code",
                  change_type="RED", point_type="RDP", change_channel="11", code="2"):
    Handler.logger.info("change_points接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value,
        "changeType": change_type,                   # 变动方式      ACC RED
        "pointType": point_type,                     # 积分类型      附件4
        "changeSouce": change_channel,               # 积分变动渠道  附件1
        "points": points,                            # 积分数量
        "vender_seq_code": random_seq_code,          # 流水号        调用方确保该值唯一
        "vender_code": code,                         # 供应商编号     附件9
        "remark": "积分变更接口"
    }
    headers["ruid"] = str(Handler().uuid)
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
def upload_order(brand_code, member_id, trade_no, total_price, trade_price, price, amt,
                 headers, commodity_code, commodity_name):
    Handler.logger.info("upload_order接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "storeCode": jsonpath(query_store(brand_code, headers), "$..data..storeNo")[0],
        "channelType": "union_code",
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
                "quant": 1,
                "amt": amt
            }
        ]
    }
    order = handler_requests.visit(url=Handler.yml_conf["host"] + "/order/uploadOrderInfo",
                                   method="post",
                                   json=data,
                                   headers=Handler().headers)
    return order


# 设置自定义会员标签
def set_define_member_tags(brand_code, union_code, source_tag, key, value):
    Handler.logger.info("set_define_member_tags接口被调用...")
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
                                  headers=Handler().headers)
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
    gift_record = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/recordJoinGift",
                                         method="post",
                                         json=data,
                                         headers=Handler().headers)
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
def quit_member(brand_code, value, headers, query_type="mobile"):
    Handler.logger.info("quit_member接口被调用...")
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value
    }
    headers["ruid"] = str(Handler().uuid)
    resp = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/quitMember",
                                  method="post",
                                  json=data,
                                  headers=headers)
    return resp


# 全渠道会员绑定解绑(新)
class MemberBinding:
    """会员媒体信息解绑,且解绑后退会操作"""
    Handler.logger.info("member_binding接口被调用...")

    def __init__(self, brand_code, binding_type, value, headers, query_type="union_code"):
        self.brand_code = brand_code
        self.binding_type = binding_type
        self.value = value
        self.headers = headers
        self.query_type = query_type

        # 调用查询会员基本信息接口
        self.query_member = query_member_info(self.brand_code, value=self.value,
                                              headers=self.headers, query_type=self.query_type)

    # 微信
    def wx_bind(self, channel):
        data = {
            "brand_code": self.brand_code,
            "program_code": self.brand_code,
            "channel": channel,
            "type": self.binding_type,
            "params": {
                "mobile": jsonpath(self.query_member, "$..mobile")[0],
                "open_id": jsonpath(self.query_member, "$..media_account[?(@.type=='3')].accountNo")[0],
                "seller_name": jsonpath(self.query_member, "$..media_account[?(@.type=='3')].fromSocialCode")[0]
            }
        }
        headers = Handler.replace_uuid(self.headers)
        resp = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/binding",
                                      method="post",
                                      json=data,
                                      headers=headers)
        return resp

    # 京东
    def jd_bind(self, channel):
        data = {
            "brand_code": self.brand_code,
            "program_code": self.brand_code,
            "channel": channel,
            "type": self.binding_type,
            "params": {
                "mobile": jsonpath(self.query_member, "$..mobile")[0],
                "user_id": jsonpath(
                    self.query_member, "$..media_account[?(@.type=='6' && @.bindStatus=='1')].accountNo")[0],
                "seller_name": jsonpath(
                    self.query_member, "$..media_account[?(@.type=='6' && @.bindStatus=='1')].fromSocialCode")[0]
            }
        }
        headers = Handler.replace_uuid(self.headers)
        resp = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/binding",
                                      method="post",
                                      json=data,
                                      headers=headers)
        return resp

    # 天猫
    def tb_bind(self, channel):
        data = {
            "brand_code": self.brand_code,
            "program_code": self.brand_code,
            "channel": channel,
            "type": self.binding_type,
            "params": {
                "mix_mobile": jsonpath(
                    self.query_member, "$..media_account[?(@.type=='2' && @.bindStatus=='1')].accountNo")[0],
                "taobao_nick": jsonpath(
                    self.query_member, "$..media_account[?(@.type=='2' && @.bindStatus=='1')].nickname")[0],
                "seller_name": jsonpath(
                    self.query_member, "$..media_account[?(@.type=='2' && @.bindStatus=='1')].fromSocialCode")[0]}
        }
        headers = Handler.replace_uuid(self.headers)
        resp = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/binding",
                                      method="post",
                                      json=data,
                                      headers=headers)
        return resp

    def all_bind(self):
        self.tb_bind(channel="976")
        self.jd_bind(channel="9AL")
        self.wx_bind(channel="6P0")

    def quit_member(self):
        headers = Handler.replace_uuid(self.headers)
        resp = quit_member(self.brand_code, value=self.value, headers=headers, query_type=self.query_type)
        return resp

    def try_bind(self):
        try:
            self.tb_bind("976")
        except TypeError:
            pass
        finally:
            try:
                self.jd_bind("9AL")
            except TypeError:
                pass
            finally:
                try:
                    self.wx_bind("6P0")
                except TypeError:
                    pass
                finally:
                    self.quit_member()



if __name__ == "__main__":
    pass
    # print(set_define_member_tags("lrp", "2245000Q9Y", "CCC", "A", "B"))
    # print(query_member_info("lrp", "2245000Q9Y", Handler().headers))
    # print(Handler().access_token)
    # print(Handler().headers)
    # print(register_media("lrp", Handler().headers, "40000"))
    # print(register_member("mg"))
    # print(query_grade("gac", "018S0001DDW"))
    # print(query_order("mg", "0000005792143"))
    # print(query_points("mg", "0000014051141"))
    # print(query_grade_history("mg", "0000017551149"))
    # print(Handler().headers)
    # print(register_member("lrp"))
    # print(query_store("kie", headers=Handler().headers))