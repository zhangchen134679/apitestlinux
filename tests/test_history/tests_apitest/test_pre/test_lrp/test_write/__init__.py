data = {
    "brand_code": "brand_code",
    "program_code": "brand_code",
    "name": "tests_ly",
    "birthday": "1995-04-09",
    "mobile": "Handler().random_phone(brand_code=brand_code, headers=headers)",
    "chanel_code": "chanel_code",
    "consentStatus": "1",
    "consentTime": "1995-04-09 00:00:00",
    "store_code": "store_code"
}

data["media_account"] = [
{
    "type": "2",
    "accountNo": "openId_{}",
    "unionId": "unionId_{}",
    "fromSocialCode": "微信公众号"
}
]
print(data)
#
        # "media_account": [
        #     {
        #         "type": "2",
        #         "accountNo": "openId_{}".format(Handler().random_num),
        #         "unionId": "unionId_{}".format(Handler().random_num),
        #         "fromSocialCode": "微信公众号"
        #     }
        # ]}