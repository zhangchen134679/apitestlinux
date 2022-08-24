from common import handler_path
from common import handler_yaml
from common import handler_logging
from common import handler_excel
from common import handler_requests
from common import handler_email
from jsonpath import jsonpath
from dateutil.relativedelta import relativedelta
from datetime import date,datetime,timedelta
import random
import time
import os
# import datetime

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(dir_path)
host_address = {
    'va': 'conf_prd',
    'vb': 'conf_pre'
}
data_address = {
    'va': 'data_prd',
    'vb': 'data_pre'
}
with open(dir_path + '/middle_write/' + 'test.txt', 'r') as f:
    brand = f.read()
read_conf_address = host_address[brand]
read_data_address = data_address[brand]

class Handler(object):

    # loaded_path
    path = handler_path

    # \data\data_prd\data_write..
    __data_path = os.path.join(os.path.join(path.data_path(), 'data_prd'), "data_write")

    print(__data_path)

    # \data\data_smoke..
    __data_smoke_path = os.path.join(path.data_path(), "data_smoke")

    # \config\conf_prd\config_write..
    yml_conf = handler_yaml.read_yaml(os.path.join(os.path.join(path.config_path(), read_conf_address), "config_write.yml"))

    excel_write_common = handler_excel.ExcelHandler(
        os.path.join(__data_path, r"{}".format(yml_conf["excel"]["write_common"])))

    excel_upload_order_info = handler_excel.ExcelHandler(
        os.path.join(__data_path, r"{}".format(yml_conf["excel"]["upload_order_info"])))

    excel_upload_change_grade = handler_excel.ExcelHandler(
        os.path.join(__data_path, r"{}".format(yml_conf["excel"]["upload_change_grade"])))

    excel_upload_change_grade_MM = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_MM.xlsx'))

    excel_upload_change_grade_itc = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_itc.xlsx'))

    excel_upload_change_grade_MNY = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_MNY.xlsx'))

    excel_upload_change_grade_UD = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_UD.xlsx'))

    excel_upload_change_grade_D2S = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_D2S.xlsx'))

    excel_upload_change_grade_CERAVE = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_CERAVE.xlsx'))

    excel_upload_change_grade_LRL = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_LRL.xlsx'))

    excel_upload_change_grade_HR = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_HR.xlsx'))

    excel_upload_change_grade_3CE = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_3CE.xlsx'))

    excel_upload_change_grade_LAN = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_LAN.xlsx'))

    excel_upload_CR_ALL = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_CR_ALL.xlsx'))

    excel_upload_change_grade_VCH = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_VCH.xlsx'))

    excel_upload_change_grade_YSL = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_YSL.xlsx'))

    excel_upload_change_grade_GAC = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_GAC.xlsx'))

    excel_upload_change_grade_KIE = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_KIE.xlsx'))

    excel_upload_change_grade_SGMB = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_SGMB.xlsx'))

    excel_upload_change_grade_lp = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_lp.xlsx'))

    excel_upload_change_grade_skc = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_skc.xlsx'))

    excel_upload_change_grade_shu = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_shu.xlsx'))

    excel_upload_change_grade_bio = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_bio.xlsx'))

    excel_upload_change_grade_lrp = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_lrp.xlsx'))

    excel_upload_change_grade_AC = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_AC.xlsx'))

    excel_upload_change_grade_VLT = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_VLT.xlsx'))

    excel_upload_change_grade_MBB = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_MBB.xlsx'))

    excel_upload_change_grade_MG = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_MG.xlsx'))

    excel_upload_change_grade_KS = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_KS.xlsx'))

    excel_upload_change_grade_TAK = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_TAK.xlsx'))

    excel_upload_change_grade_YS = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_YS.xlsx'))

    excel_upload_change_grade_NYX = handler_excel.ExcelHandler(
        os.path.join(__data_path, 'Arvato_NYX.xlsx'))

    excel_upload_message_info = handler_excel.ExcelHandler(
        os.path.join(__data_path, r"{}".format(yml_conf["excel"]["upload_message_info"])))

    excel_write_common_simple = handler_excel.ExcelHandler(
        os.path.join(__data_path, r"data_simple\{}".format(yml_conf["excel"]["data_simple"]["write_common"])))

    excel_upload_order_info_simple = handler_excel.ExcelHandler(
        os.path.join(__data_path, r"data_simple\{}".format(yml_conf["excel"]["data_simple"]["upload_order_info"])))

    excel_upload_message_info_simple = handler_excel.ExcelHandler(
        os.path.join(__data_path, r"data_simple\{}".format(yml_conf["excel"]["data_simple"]["upload_message_info"])))

    excel_smoke_d2s = handler_excel.ExcelHandler(
        os.path.join(__data_smoke_path, r"{}".format(yml_conf["excel"]["smoke_common"]["d2s"])))

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
                if query_member["code"] != 0:
                    if query_member["code"] == 2:
                        return Handler().logger.error("__get_query: {}".format(query_member))
                    return phone
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
def register_member(brand_code, headers, birthday="1995-01-09",  chanel_code="986"):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "name": Handler.yml_conf['test_standard']['names'],
        "birthday": birthday,
        "mobile": Handler().random_phone(brand_code=brand_code, headers=headers),
        "Chanel_code".lower(): chanel_code,
        "consentStatus": "1",
        "consentTime": "1995-01-09 00:00:00",
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
    member = handler_requests.visit(url=Handler.yml_conf["host"] + "/member/registerNew",
                                    method="post",
                                    json=data,
                                    headers=headers)
    # print('注册参数{}'.format(data))
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
            Handler().logger.error(f"query_member_info: {query_member}")
        return query_member
    except Exception:
        Handler().logger.error("%s query_member_info: %s" % (brand_code, query_member),)
        raise


# 查询当前会员等级
def query_grade(brand_code, value, headers, query_type="union_code", category="default"):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "queryType": query_type,
        "value": value,
        "category": category
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
def upload_order(brand_code, store_code, trade_no, total_price, trade_price, price, amt,
                 headers, commodity_code, channel_type="union_code", commodity_name='',orderType='1',
                 member_id='', tmallOuid='', originalOrderId='' ,number=1,tradeTime='time.strftime("%Y-%m-%d %H:%M:%S")'):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "storeCode": store_code,
        "channelType": channel_type,
        "channelMemberId": member_id,
        "tmallOuid":tmallOuid,
        "orderType": orderType,
        "tradeNo": trade_no,
        "tradeTime": tradeTime,
        "totalCount": number,
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
                "quAnt".lower(): number,
                "amt": amt,
                "originalOrderId":originalOrderId
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
def query_member_tags(brand_code, value, source_tag, headers):
    data = {"brand_code": brand_code,
            "program_code": brand_code,
            "member_code": value,
            "sourceTag": source_tag
            }
    tags = handler_requests.visit(url=Handler.yml_conf["host"] + "/tag/viewTags",
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


#  订单状态更新
def upload_order_info_new(brand_code, tradeno, headers, status='TRADE_FINISHED'):
    data = {
        "brand_code": brand_code,
        "order_no": tradeno,
        "program_code": brand_code,
        "status": status
    }

    response = handler_requests.visit(url=Handler.yml_conf["host"] + '/order/updateOrderStatus',
                                      method="post",
                                      json=data,
                                      headers=headers)
    return response


#  会员积分查询
def query_member_points(brand_code, member_code, headers, pointTypeGroup="BP"):
    data = {
        "brand_code": brand_code,
        "queryType": "union_code",
        "program_code": brand_code,
        "value": member_code,
        "pointTypeGroup": pointTypeGroup
    }

    response = handler_requests.visit(url=Handler.yml_conf["host"] + '/member/queryMemberPoints',
                                      method="post",
                                      json=data,
                                      headers=headers)
    return response


#  绑定解绑天猫
def bind_tmall(brand_code, mix_mobile, ouid, headers, bind_type, seller_name, omid='', nick=''):
    data = {
        "brand_code": brand_code,
        "program_code": brand_code,
        "channel": "976",
        "type": bind_type,
        "params": {
            "mix_mobile": mix_mobile,
            "taobao_nick": nick,
            "seller_name": seller_name,
            "tmall_ouid": ouid,
            "tmall_omid": omid }
            }

    response = handler_requests.visit(url=Handler.yml_conf["host"] + '/member/binding',
                                      method="post",
                                      json=data,
                                      headers=headers)
    return response


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

        if value:
            self.get_query = query_member_info(brand_code=self.brand,
                                               value=value, headers=headers, query_type=query_type)

    @property
    def brand_code(self):
        return self.brand

    @property
    def time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

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

    @property
    def gradeEndDate_100(self):
        # 等级有效期时间 100年 等级升级后在降级的100年
        return (datetime.now() + relativedelta(years=100)-relativedelta(days=1)).strftime("%Y%m%d")

    @property
    def gradeEndDate_12(self):
        # 等级有效期时间 12个月
        return (datetime.now() + relativedelta(years=1)-relativedelta(days=1)).strftime("%Y%m%d")

    @property
    def gradeEndDate_24(self):
        # 等级有效期时间 24个月
        return (datetime.now() + relativedelta(years=2)-relativedelta(days=1)).strftime("%Y%m%d")

    @property
    def gradeEndDate_36(self):
        # 等级有效期时间 36个月
        return (datetime.now() + relativedelta(years=3) - relativedelta(days=1)).strftime("%Y%m%d")

    @property
    def gradeStartDate(self):
        # 等级开始时间
        return datetime.now().strftime("%Y%m%d")

    @property
    def gradeEndDate_100_cs(self):
        # 等级有效期时间 初始注册的100年
        return (datetime.now() + relativedelta(years=100)).strftime("%Y%m%d")

    @property
    def gradeEndDate_12_natural(self):
        # 等级有效期时间 12个自然月
        return (date(datetime.now().year,datetime.now().month,1)+relativedelta(months=13) - relativedelta(days=1)).strftime("%Y%m%d")

    @property
    def today(self):
        # 今天
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def yesterday(self):
        # 昨天
        return (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def tomorrow(self):
        # 明天
        return (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def qiantian(self):
        # 前天
        return (datetime.now()-timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def ninetytwodaysago(self):
        # 92天前
        return (datetime.now()-timedelta(days=92)).strftime("%Y-%m-%d %H:%M:%S")

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
#订单状态更新
def upload_Order_Info(brand_code,tradeNo,store_code,headers):

    if brand_code == 'lancome':
        status = "WAIT_BUYER_CONFIRM_GOODS"
    else:
        status = "TRADE_FINISHED"
    params= {
        "brand_code": brand_code,
        "program_code": brand_code,
        "order_no": tradeNo,
        "refund_no": "",
        "status": status,
        "store_code": store_code,
        "details": [
                {
                    "sku_code": "",
                    "detail_status": "",
                    "refund_status": ""
                },{
                    "sku_code": "",
                    "detail_status": "",
                    "refund_status": ""
                    }
                    ]
                }
    print(params)
    resp = handler_requests.visit(
        url = Handler.yml_conf["host"] + '/order/updateOrderStatus',
        method = 'post',
        headers = headers,
        json = params
    )
    try:
        assert resp['code'] == 0
        return '更新订单信息成功'
    except AssertionError as err:
        print("更新订单信息失败：{}".format(err))
        print("请求参数：{}".format(params))
        print('请求结果：{}'.format(resp))
        raise err

if __name__ == "__main__":
    brand = 'lrp'
    # mobile = ['15890533563', '18538783563', '13213332698']
    # token = Handler().headers(brand)
    # get_input_result = input('输入yes退会测试会员:')
    # if get_input_result == 'yes':
    #     for item in range(len(mobile)):
    #         unbind = MemberBinding(brand, value=mobile[item], headers=token, binding_type="0", query_type="mobile")
    #         print(unbind.try_bind())
    # else:
    #     raise Exception('over...')
    # print(Handler.yml_conf)
    aa = Handler().excel_smoke_d2s
    bb = aa.read_data('smoke_request')
    print(bb)
    # print(Handler.yml_conf["excel"]["data_simple"]["write_common"])