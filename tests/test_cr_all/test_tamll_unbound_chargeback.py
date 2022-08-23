from middleware.middle_prd.middle_write import handler_middle
import unittest
from jsonpath import jsonpath
import time

logger = handler_middle.Handler().logger
with open('brand.txt', 'r') as f:
    brand = f.read()


class TestBing(unittest.TestCase):
    '''
    需求：
    会员购买订单后解绑，退单时会按照原单中匹配的会员卡号进行退单
    天猫渠道购买订单后解绑，退单按照原单中member_code进行退单处理

    测试场景：
    场景一：天猫渠道解绑后，全部退单
    场景二：天猫渠道解绑后，部分退单
    场景三：天猫渠道解绑后，不关联原单退单
    天猫渠道购买订单后解绑，退单中对应两个不同的会员，退单根据原单的会员号进行匹配 完成退单操作
    场景四：ouid不同，正单和退单中的ouid不是同一个
    场景五： ouid相同，同一个ouid解绑后重新注册生产新会员
    场景六：正单状态未更新物流，解绑后进行退单，更新物流状态，正单和退单均计算成功，完成退单操作
    场景七：正单状态未更新物流，解绑后重新绑定新的会员，然后进行退单操作，更新物流状态，退单匹配到原单的会员名下，计算成功
    '''
    member_list = []

    @classmethod
    def setUpClass(cls) -> None:

        # 从配置文件读取store
        cls.store = handler_middle.Handler.yml_conf["crm_store"][brand]["deal_store_no"]
        # 从配置文件读取sku
        cls.sku = handler_middle.Handler.yml_conf["crm_product"][brand]["code"]
        # 调用信息头return..headers
        cls.headers = handler_middle.Handler().headers(brand_code=brand)
        # 获取天猫门店名称
        cls.seller_name = handler_middle.Handler().yml_conf["crm_store"][brand]["name"]
        cls.sleep = 20
        logger.info('正在执行品牌为{}'.format(brand))

    @classmethod
    def tearDownClass(cls) -> None:
        # 调用会员退会接口
        for index in range(0, len(cls.member_list)):
            handler_middle.quit_member(
                brand, value=cls.member_list[index], headers=handler_middle.Handler().replace_uuid(cls.headers),
                query_type="union_code")
        logger.info('{}退会成功'.format(cls.member_list))

    def upload_order_info(self, tradeno):

        # 确认收货
        upload_order_info_response = handler_middle.upload_order_info_new(
            brand_code=brand, tradeno=tradeno, headers=handler_middle.Handler().replace_uuid(self.headers),
            status='TRADE_FINISHED')
        if upload_order_info_response['code'] == 0:
            logger.info('订单变更状态成功')
            time.sleep(self.sleep)
        else:
            logger.info('订单变更状态失败')

    def reg(self):
        member = handler_middle.register_member(brand, headers=handler_middle.Handler().replace_uuid(self.headers))
        member_code = member["data"]["union_code"]
        self.member_list.append(member_code)
        logger.info("会员号为：{}".format(member_code))
        return member_code

    def query_member_mix_mobile(self, member_code):
        member_info = handler_middle.query_member_info(brand, headers=self.headers, value=member_code)
        # 查询 ouid ，omid等
        mix_mobile = jsonpath(member_info, "$..media_account[?(@.type=='2')].accountNo")[0]
        return mix_mobile

    def upload_order(self, trade_no, tmallOuid,total_price='200',trade_price='200',price='200',amt='100',orderType='1',
                     originalOrderId=''):
        response = handler_middle.upload_order(
                                    brand_code=brand,
                                    headers=handler_middle.Handler().replace_uuid(self.headers),
                                    store_code=self.store, trade_no=trade_no, total_price=total_price,
                                    trade_price=trade_price, price=price, amt=amt,orderType=orderType,
                                    commodity_code=self.sku, channel_type="ouid", tmallOuid=tmallOuid,
                                    originalOrderId=originalOrderId)
        if orderType == '1':
            logger.info("正单号：{}".format(trade_no))
        elif orderType == '2':
            logger.info("退单号：{}".format(trade_no))
        return response

    def query_member_points(self,member_code):
        if brand == 'lp':
            actual_point = handler_middle.query_member_points(brand_code=brand, member_code=member_code,
                                                              headers=self.headers,pointTypeGroup="ON")
            point=actual_point['data']['points'][0]['evalidPoints']
            logger.info('当前积分为：{}'.format(point))
            return point
        else:
            actual_point = handler_middle.query_member_points(brand_code=brand, member_code=member_code,
                                                              headers=self.headers)
            point = actual_point['data']['points'][0]['evalidPoints']
            logger.info('当前积分为：{}'.format(point))
            return point



    def bind(self,mix_mobile, ouid, bind_type):
        response = handler_middle.bind_tmall(brand,
                                             headers=handler_middle.Handler().replace_uuid(self.headers),
                                             mix_mobile=mix_mobile, ouid=ouid, bind_type=bind_type,
                                             seller_name=self.seller_name)
        result =response['data']['bindCode']
        if bind_type == '1':
            logger.info("tmallouid:{}--绑定状态：{}".format(ouid,result))
        elif bind_type == '2':
            logger.info("tmallouid:{}--解绑状态：{}".format(ouid,result))
        else:
            pass

    def test_bind_1(self):
        # 注册
        member_code=self.reg()
        # 查询
        mix_mobile = self.query_member_mix_mobile(member_code)
        ouid_1 = "test_arvato_tm_" + str(int(time.time()))
        logger.info("tmall_ouid为：{}".format(ouid_1))
        time.sleep(self.sleep)
        # 绑定
        self.bind(mix_mobile,ouid_1,'1')
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1,ouid_1)
        time.sleep(self.sleep)
        # 确认收货
        self.upload_order_info(trade_no_1)
        # 查询积分
        self.query_member_points(member_code)
        # 解绑
        self.bind(mix_mobile, ouid_1, '2')
        # 退单
        time.sleep(self.sleep)
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, ouid_1, originalOrderId=trade_no_1, orderType='2')
        time.sleep(self.sleep)
        try:
            # 查积分
            point = self.query_member_points(member_code)
            self.assertEqual(point, 0)
            self.result = "pass"
            logger.info("第1条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第1条用例失败..Fail...Expected, Actual {}".format(err))

    def test_bind_2(self):

        # 注册
        member_code = self.reg()
        # 查询
        mix_mobile = self.query_member_mix_mobile(member_code)
        ouid_1 = "test_arvato_tm_" + str(int(time.time()))
        logger.info("tmall_ouid为：{}".format(ouid_1))
        time.sleep(self.sleep)
        # 绑定
        self.bind(mix_mobile, ouid_1, '1')
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, ouid_1)
        time.sleep(self.sleep)
        # 确认收货
        self.upload_order_info(trade_no_1)
        # 查询积分
        self.query_member_points(member_code)
        # 解绑
        self.bind(mix_mobile, ouid_1, '2')
        # 退单
        time.sleep(self.sleep)
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, ouid_1, originalOrderId=trade_no_1, orderType='2', total_price='50',
                          trade_price='50', price='50', amt='50')
        time.sleep(self.sleep)
        try:
            # 查积分
            point = self.query_member_points(member_code)
            self.assertEqual(point, 50)
            self.result = "pass"
            logger.info("第2条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第2条用例失败..Fail...Expected, Actual {}".format(err))

    def test_bind_3(self):
        # 注册
        member_code = self.reg()
        # 查询
        mix_mobile = self.query_member_mix_mobile(member_code)
        ouid_1 = "test_arvato_tm_" + str(int(time.time()))
        logger.info("tmall_ouid为：{}".format(ouid_1))
        time.sleep(self.sleep)
        # 绑定
        self.bind(mix_mobile, ouid_1, '1')
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, ouid_1)
        time.sleep(self.sleep)
        # 确认收货
        self.upload_order_info(trade_no_1)
        # 查询积分
        self.query_member_points(member_code)
        # 解绑
        self.bind(mix_mobile, ouid_1, '2')
        # 退单
        time.sleep(self.sleep)
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, ouid_1, orderType='2')
        time.sleep(self.sleep)
        try:
            # 查积分
            point = self.query_member_points(member_code)
            self.assertEqual(point, 100)
            self.result = "pass"
            logger.info("第3条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第3条用例失败..Fail...Expected, Actual {}".format(err))

    def test_bind_4(self):
        # 注册
        member_code = self.reg()
        # 查询
        mix_mobile = self.query_member_mix_mobile(member_code)
        ouid_1 = "test_arvato_tm_" + str(int(time.time()))
        logger.info("tmall_ouid为：{}".format(ouid_1))
        time.sleep(self.sleep)
        # 绑定
        self.bind(mix_mobile, ouid_1, '1')
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, ouid_1)
        time.sleep(self.sleep)
        # 确认收货
        self.upload_order_info(trade_no_1)
        # 查询积分
        self.query_member_points(member_code)
        # 解绑
        self.bind(mix_mobile, ouid_1, '2')
        # 注册
        member_code_2 = self.reg()
        # 查询
        mix_mobile_2 = self.query_member_mix_mobile(member_code_2)
        ouid_2 = "test_arvato_tm_" + str(int(time.time()))
        logger.info("tmall_ouid为：{}".format(ouid_2))
        time.sleep(self.sleep)
        # 绑定
        self.bind(mix_mobile_2, ouid_2, '1')
        # 退单
        time.sleep(self.sleep)
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, ouid_2, originalOrderId=trade_no_1, orderType='2')
        time.sleep(self.sleep)
        # 解绑
        self.bind(mix_mobile_2, ouid_2, '2')
        try:
            # 查积分
            point = self.query_member_points(member_code)
            self.assertEqual(point, 0)
            self.result = "pass"
            logger.info("第4条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第4条用例失败..Fail...Expected, Actual {}".format(err))

    def test_bind_5(self):

        # 注册
        member_code = self.reg()
        # 查询
        mix_mobile = self.query_member_mix_mobile(member_code)
        ouid_1 = "test_arvato_tm_" + str(int(time.time()))
        logger.info("tmall_ouid为：{}".format(ouid_1))
        time.sleep(self.sleep)
        # 绑定
        self.bind(mix_mobile, ouid_1, '1')
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, ouid_1)
        time.sleep(self.sleep)
        # 确认收货
        self.upload_order_info(trade_no_1)
        # 查询积分
        self.query_member_points(member_code)
        # 解绑
        self.bind(mix_mobile, ouid_1, '2')
        # 注册
        member_code_2 = self.reg()
        # 查询
        mix_mobile_2 = self.query_member_mix_mobile(member_code_2)
        time.sleep(self.sleep)
        # 绑定
        self.bind(mix_mobile_2, ouid_1, '1')
        # 退单
        time.sleep(self.sleep)
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, ouid_1, originalOrderId=trade_no_1, orderType='2')
        time.sleep(self.sleep)
        # 解绑
        self.bind(mix_mobile_2, ouid_1, '2')
        try:
            # 查积分
            point = self.query_member_points(member_code)
            self.assertEqual(point, 0)
            self.result = "pass"
            logger.info("第5条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第5条用例失败..Fail...Expected, Actual {}".format(err))

    def test_bind_6(self):
        # 注册
        member_code = self.reg()
        # 查询
        mix_mobile = self.query_member_mix_mobile(member_code)
        ouid_1 = "test_arvato_tm_" + str(int(time.time()))
        logger.info("tmall_ouid为：{}".format(ouid_1))
        time.sleep(self.sleep)
        # 绑定
        self.bind(mix_mobile, ouid_1, '1')
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, ouid_1)
        time.sleep(self.sleep)
        # 解绑
        self.bind(mix_mobile, ouid_1, '2')
        # 退单
        time.sleep(self.sleep)
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, ouid_1, originalOrderId=trade_no_1, orderType='2')
        time.sleep(self.sleep)
        # 确认收货
        self.upload_order_info(trade_no_1)
        time.sleep(self.sleep)
        # 查询积分
        self.query_member_points(member_code)
        try:
            # 查积分
            point = self.query_member_points(member_code)
            self.assertEqual(point, 0)
            self.result = "pass"
            logger.info("第6条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第6条用例失败..Fail...Expected, Actual {}".format(err))

    def test_bind_7(self):
        # 注册
        member_code = self.reg()
        # 查询
        mix_mobile = self.query_member_mix_mobile(member_code)
        ouid_1 = "test_arvato_tm_" + str(int(time.time()))
        logger.info("tmall_ouid为：{}".format(ouid_1))
        time.sleep(self.sleep)
        # 绑定
        self.bind(mix_mobile, ouid_1, '1')
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, ouid_1)
        time.sleep(self.sleep)
        # 解绑
        self.bind(mix_mobile, ouid_1, '2')
        # 注册
        member_code_2 = self.reg()
        # 查询
        mix_mobile_2 = self.query_member_mix_mobile(member_code_2)
        time.sleep(self.sleep)
        # 绑定
        self.bind(mix_mobile_2, ouid_1, '1')
        # 退单
        time.sleep(self.sleep)
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, ouid_1, originalOrderId=trade_no_1, orderType='2')
        time.sleep(self.sleep)
        # 解绑
        self.bind(mix_mobile_2, ouid_1, '2')
        # 确认收货
        self.upload_order_info(trade_no_1)
        time.sleep(self.sleep)
        # 查询积分
        self.query_member_points(member_code)
        try:
            # 查积分
            point = self.query_member_points(member_code)
            self.assertEqual(point, 0)
            self.result = "pass"
            logger.info("第7条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第7条用例失败..Fail...Expected, Actual {}".format(err))


if __name__ == "__main__":
    unittest.main()
