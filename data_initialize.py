# prd环境
from middleware.middle_prd.middle_query import handler_middle

# pre环境
# from middleware.middle_pre.middle_query import handler_middle

from jsonpath import jsonpath

# yml_conf
yml_conf = handler_middle.Handler.yml_conf

# loaded_brand
brand = yml_conf["brand"]["lrp"]

# return..headers
headers = handler_middle.Handler().headers(brand_code=brand)

ba_code = yml_conf["crm_employee"][brand]
tb_store_name = yml_conf["crm_store"][brand]["name"]
tb_store_code = yml_conf["crm_store"][brand]["deal_store_no"]
offline_store_code = yml_conf["crm_store"][brand]["offline_store_no"]
product_code = yml_conf["crm_product"][brand]["code"]
product_name = yml_conf["crm_product"][brand]["name"]
online_trade_no = yml_conf["crm_trade_no"][brand]["online"]["trade_no"]
online_trade_time = yml_conf["crm_trade_no"][brand]["online"]["trade_time"]
offline_trade_no = yml_conf["crm_trade_no"][brand]["offline"]["trade_no"]
offline_trade_time = yml_conf["crm_trade_no"][brand]["offline"]["trade_time"]

# 从配置文件读取test_member_data..供应商编号..流水号..sourceTag
conf_test_member_data = yml_conf["test_member_data"][brand]

# 从配置文件读取企业微信BA绑定解绑数据..
ba_userid = yml_conf["crm_wechat"]["ba_userid"]
opDate = yml_conf["crm_wechat"]["opDate"]
# ----------------------------------------------------------------------------------------------------------------------

"""调用会员注册"""
# --> 主测试账号
union_code_15890533563 = handler_middle.register_media(
    brand_code=brand, mobile="15890533563", store_code=tb_store_code, ba_code=ba_code, headers=headers)

#  --> 辅助测试账号1
union_code_18538783563 = handler_middle.register_media(
    brand_code=brand, mobile="18538783563", store_code=tb_store_code, ba_code=ba_code, headers=headers)
#
#  --> 辅助测试账号2
union_code_13213332698 = handler_middle.register_media(
    brand_code=brand, mobile="13213332698", store_code=tb_store_code, ba_code=ba_code, headers=headers)

"""提取会员的union_code"""
union_code_15890533563 = union_code_15890533563["data"]["union_code"]
union_code_18538783563 = union_code_18538783563["data"]["union_code"]
union_code_13213332698 = union_code_13213332698["data"]["union_code"]


"""调用全渠道会员绑定接口"""
# --> 主测试账号...绑定天猫、京东、微信
bind = handler_middle.MemberBinding(brand, binding_type="1", value=union_code_15890533563, headers=headers)
bind.wx_bind(channel="6P0", open_id="openId_666666", union_id="unionId_666666")
bind.tb_bind(channel="976", tb_nick="nickname_666666")
bind.jd_bind(channel="9AL", user_id="jd_pin_666666")

print("主测试账号...绑定天猫、京东、微信")

#  --> 辅助测试账号1...绑定天猫、京东、微信
bind = handler_middle.MemberBinding(brand, binding_type="1", value=union_code_18538783563, headers=headers)
bind.wx_bind(channel="6P0", open_id="openId_999999", union_id="unionId_999999")
bind.tb_bind(channel="976", tb_nick="nickname_999999")
bind.jd_bind(channel="9AL", user_id="jd_pin_999999")
print("辅助测试账号1...绑定天猫、京东、微信")
# ----------------------------------------------------------------------------------------------------------------------

# 调用会员积分变更(可欠账)接口    --- 让辅助测试账号(18538783563)欠账,用于查询接口test_query_member_arrears_detail.py
res = handler_middle.deduction_point(brand_code=brand, value=union_code_18538783563, points=2000, headers=headers)
print("让辅助测试账号(18538783563)欠账", res)

# ----------------------------------------------------------------------------------------------------------------------

# 调用会员积分变更(可欠账)接口    --- 让辅助测试账号(13213332698)欠账,用于查询接口test_query_member_arrears_detail.py
res = handler_middle.deduction_point(brand_code=brand, value=union_code_13213332698, points=1800, headers=headers)
print("让辅助测试账号(13213332698)欠账", res)

# ----------------------------------------------------------------------------------------------------------------------

# 调用保存会员入会礼品记录接口    --- 让主测试账号(15890533563)增加一个入会礼品记录,用于test_query_member_gift_record.py
res = handler_middle.save_member_gift_record(brand_code=brand, union_code=union_code_15890533563, headers=headers)
print("让主测试账号(15890533563)增加一个入会礼品记录", res)

# ----------------------------------------------------------------------------------------------------------------------

# 调用上传订单接口    --- 让主测试账号(15890533563)存在订单数据
res = handler_middle.upload_order(brand_code=brand, member_id=union_code_15890533563,
                                  trade_no=online_trade_no, trade_time=online_trade_time,
                                  total_price=1000, trade_price=1000, price=1000, amt=1000,
                                  commodity_code=product_code, commodity_name=product_name, headers=headers,
                                  store_code=tb_store_code, employee_code=ba_code)
print("让主测试账号(15890533563)存在订单数据", res)

# ----------------------------------------------------------------------------------------------------------------------

# 调用上传订单接口    --- 让辅助测试账号(18538783563)买一笔线下订单,用于test_query_offline_trade_count.py
res = handler_middle.upload_order(brand_code=brand, member_id=union_code_18538783563,
                                  trade_no=offline_trade_no, trade_time=offline_trade_time,
                                  total_price=1000, trade_price=1000, price=1000, amt=1000,
                                  commodity_code=product_code, commodity_name=product_name, headers=headers,
                                  store_code=offline_store_code, employee_code=ba_code)
print("让辅助测试账号(18538783563)买一笔线下订单", res)

# ----------------------------------------------------------------------------------------------------------------------

# 调用设置自定义会员标签接口    brand_code, union_code, source_tag, key, value, headers
res = handler_middle.set_define_member_tags(brand_code=brand, union_code=union_code_15890533563,
                                            source_tag=conf_test_member_data["sourceTag"], key="hobby", value="Python",
                                            headers=headers)
print("给主测试账号15890533563设置自定义会员标签", res)

# ----------------------------------------------------------------------------------------------------------------------

# 调用积分变更接口    --- 让主测试账号(15890533563)走一笔积分变更,用于test_query_points_change_status.py
change_point = handler_middle.change_points(brand_code=brand, value=union_code_15890533563, points=1000,
                                            change_type="ACC", point_type="ABP", headers=headers,
                                            vender_code=conf_test_member_data["{}".format(str.lower("venDer_code"))],
                                            vender_seq_code=conf_test_member_data["venDer_seq_code".lower()])

print("调用积分变更接口    --- 让主测试账号(15890533563)走一笔积分变更：resp,", change_point)

# ----------------------------------------------------------------------------------------------------------------------
cus_unionId_18538783563 = '200169508021'
union_code_15890533563 = '200169507920'
# 调用查询会员基本信息接口...
query_15890533563 = handler_middle.query_member_info(brand_code=brand, value=union_code_15890533563, headers=headers)
query_18538783563 = handler_middle.query_member_info(brand_code=brand, value=union_code_18538783563, headers=headers)

# 提取15890533563会员的openid
cus_userid_15890533563 = jsonpath(query_15890533563, "$..media_account[?(@.type=='3')].accountNo")[0]

# 提取18538783563会员的openid
cus_userid_18538783563 = jsonpath(query_18538783563, "$..media_account[?(@.type=='3')].accountNo")[0]

# 提取15890533563会员的unionId
cus_unionId_15890533563 = jsonpath(query_15890533563, "$..media_account[?(@.type=='3')].unionId")[0]

# 提取18538783563会员的unionId
cus_unionId_18538783563 = jsonpath(query_18538783563, "$..media_account[?(@.type=='3')].unionId")[0]
# ----------------------------------------------------------------------------------------------------------------------

# 调用企业微信BA绑定解绑接口    --- 让主测试账号(15890533563)进行四次绑定BA,用于test_query_wechat_ba_bind.py
for index in range(0, 4):
    res158 = handler_middle.wechat_ba_bind(brand_code=brand, cus_userid=cus_userid_15890533563,
                                           cus_unionid=cus_unionId_15890533563,
                                           member_code=union_code_15890533563, ba_userid=ba_userid, bind_type=str(index),
                                           ba_code=ba_code, opDate=opDate, headers=headers)
print("主测试账号(15890533563)四次绑定BA成功")


# 调用企业微信BA绑定解绑接口    --- 让辅助测试账号(18538783563)进行四次绑定BA,用于test_query_wechat_ba_bind.py
for index in range(0, 4):
    res158 = handler_middle.wechat_ba_bind(brand_code=brand, cus_userid=cus_userid_18538783563,
                                           cus_unionid=cus_unionId_18538783563,
                                           member_code=union_code_18538783563, ba_userid=ba_userid, bind_type=str(index),
                                           ba_code=ba_code, opDate=opDate, headers=headers)
print("辅助测试账号(18538783563)四次绑定BA成功")


if __name__ == "__main__":
    pass

# 需要删除并重置初始化数据时, 需要清空订单编号和会员解绑退会操作..
# select * from crm_ba_customer_social_num where c_code = '200157501627';
# delete from crm_ba_customer_social_num where c_code = '200157501627';

# 通过数据库给主账号15890533563手机号初始化动态标签
"""
INSERT INTO "crm_member_tags"("member_code","brand_code","program_code","source_tag","tags")
VALUES ('200169507920','lrp','lrp','CCC',
'{
    "1": "2021-01-01 00:00:00",
    "2": 356.00,
    "3": "雪颜珍白精华粉底液 R0 17ml",
    "5": null,
    "6": 1,
    "7": "",
    "8": [
        [
            "2021-01-01 00:00:00|offline|G0797001|雪颜珍白精华粉底液 R0 17ml"
        ]
    ]
}');
"""

# 给手机号13213332698手动添加至黑名单状态, test_memberInfo_verification

