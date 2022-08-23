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
    物流状态新逻辑 不需要考虑 success  closed 这二个状态
        场景如下：
        1下单100 订单状态为2已计算  传 TRADE_CLOSED 退10 退10 退80
        2下单100 订单状态为2已计算  传 TRADE_CLOSED 退100
        3下单100 订单状态为2已计算 退10 退10 退80
        4下单100 订单状态为2已计算 退100
        5下单100 订单状态为2已计算 退10  传 TRADE_CLOSED 退10 退80
        6下单100 订单状态为2已计算 退10  传 TRADE_CLOSED 退90
        7 下单100订单状态为8拦截状态 传 TRADE_CLOSED  退10 退10 退80
        8 下单100订单状态为8拦截状态 传 TRADE_CLOSED   退100
        9 下单100订单状态为8拦截状态 退10 退10 退80 传 TRADE_CLOSED
        10 下单100订单状态为8拦截状态 退100 传 TRADE_CLOSED
        11下单100订单状态为8拦截状态 退10 传 TRADE_CLOSED  退10 退80
        12 下单100订单状态为8拦截状态 退10 传 TRADE_FINISHED 退10 传 TRADE_CLOSED 退10 退70
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

    def upload_order_info(self, tradeno):   # TRADE_FINISHED   WAIT_BUYER_CONFIRM_GOODS(
        if brand == 'ysl' or brand == 'gac':  # 发货算分


            upload_order_info_response = handler_middle.upload_order_info_new(
                brand_code=brand, tradeno=tradeno, headers=handler_middle.Handler().replace_uuid(self.headers),
                status='WAIT_BUYER_CONFIRM_GOODS')
            if upload_order_info_response['code'] == 0:
                logger.info('订单变更状态成功')
                time.sleep(self.sleep)
            else:
                logger.info('订单变更状态失败')

        else: # 确认收货算分
            upload_order_info_response = handler_middle.upload_order_info_new(
                brand_code=brand, tradeno=tradeno, headers=handler_middle.Handler().replace_uuid(self.headers),
                status='TRADE_FINISHED')
            if upload_order_info_response['code'] == 0:
                logger.info('订单变更状态成功')
                time.sleep(self.sleep)
            else:
                logger.info('订单变更状态失败')

    def upload_order_info1(self, tradeno):  # TRADE_FINISHED   WAIT_BUYER_CONFIRM_GOODS(
            # 付款以后用户退款成功，交易自动关闭
        upload_order_info_response = handler_middle.upload_order_info_new(
             brand_code=brand, tradeno=tradeno, headers=handler_middle.Handler().replace_uuid(self.headers),
             status='TRADE_CLOSED')
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



    def upload_order(self, trade_no,member_code,amt,number=4,total_price='200',trade_price='200',price='200',orderType='1',
                     channel_type="union_code",  originalOrderId=''):
        response = handler_middle.upload_order(
                                    brand_code=brand,
                                    headers=handler_middle.Handler().replace_uuid(self.headers),
                                    store_code=self.store, trade_no=trade_no, total_price=total_price,
                                    trade_price=trade_price, price=price, amt=amt,orderType=orderType,
                                    commodity_code=self.sku, channel_type=channel_type,member_id=member_code,
                                    originalOrderId=originalOrderId,number=number)
        if orderType == '1':
            logger.info("正单号：{}".format(trade_no))
        elif orderType == '2':
            logger.info("退单号：{}".format(trade_no))
        return response

    def order_detail(self,member_code, trade_no,query_type="union_code"):
        response =handler_middle.query_order_detail(brand_code=brand,value=member_code, trade_no=trade_no,
                                                    headers=handler_middle.Handler().replace_uuid(self.headers)
                                                    ,query_type=query_type, detail_type=1)
        return response
        # response['data']['orderDetails'][0]['tradeNo']


    def test_bind_1(self):
        # 注册
        member_code=self.reg()
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1,member_code,100)
        time.sleep(self.sleep)
        # 确认收货
        self.upload_order_info(trade_no_1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point1 = self.order_detail(member_code, trade_no_1)
            self.assertEqual(trade_no_1, point1['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第1条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第1条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        ## 交易自动关闭
        self.upload_order_info1(trade_no_1)
        # 退单10
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, member_code,10, originalOrderId=trade_no_1, orderType='2',number=1)

        # 退单10
        trade_no_3 = trade_no_1 + 'tt'
        self.upload_order(trade_no_3, member_code,10, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual([], point2['data']['orderDetails'])
            self.result = "pass"
            logger.info("第2条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第2条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        try:
            # 查订单明细
            point3 = self.order_detail(member_code, trade_no_3)
            self.assertEqual([], point3['data']['orderDetails'])
            self.result = "pass"
            logger.info("第3条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第3条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        # 退单80
        trade_no_4 = trade_no_1 + 'ttt'
        self.upload_order(trade_no_4, member_code,80, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual(trade_no_2, point2['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第4条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第4条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        try:
            # 查订单明细
            point3 = self.order_detail(member_code, trade_no_3)
            self.assertEqual(trade_no_3, point3['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第5条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第5条用例失败..Fail...Expected, Actual {}".format(err))
            raise err
        try:
            # 查订单明细
            point4 =self.order_detail(member_code, trade_no_4)
            self.assertEqual(trade_no_4, point4['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第6条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第6条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

    def test_bind_2(self):
        # 注册
        member_code = self.reg()
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, member_code, 100)
        time.sleep(self.sleep)
        # 确认收货
        self.upload_order_info(trade_no_1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point1 = self.order_detail(member_code, trade_no_1)
            self.assertEqual(trade_no_1, point1['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第1条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第1条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        ## 交易自动关闭
        self.upload_order_info1(trade_no_1)
        # 退单100
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, member_code, 100, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)

        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual(trade_no_2, point2['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第2条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第2条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

    def test_bind_3(self):
        # 注册
        member_code = self.reg()
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, member_code, 100)
        time.sleep(self.sleep)
        # 确认收货
        self.upload_order_info(trade_no_1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point1 = self.order_detail(member_code, trade_no_1)
            self.assertEqual(trade_no_1, point1['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第1条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第1条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        # 退单10
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual(trade_no_2, point2['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第2条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第2条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

            # 退单10
        trade_no_3 = trade_no_1 + 'tt'
        self.upload_order(trade_no_3, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point3 = self.order_detail(member_code, trade_no_3)
            self.assertEqual(trade_no_3, point3['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第3条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第3条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

            # 退单80
        trade_no_4 = trade_no_1 + 'ttt'
        self.upload_order(trade_no_4, member_code, 80, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point4 = self.order_detail(member_code, trade_no_4)
            self.assertEqual(trade_no_4, point4['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第4条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第4条用例失败..Fail...Expected, Actual {}".format(err))
            raise err



    def test_bind_4(self):
        # 注册
        member_code = self.reg()
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, member_code, 100)
        time.sleep(self.sleep)
        # 确认收货
        self.upload_order_info(trade_no_1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point1 = self.order_detail(member_code, trade_no_1)
            self.assertEqual(trade_no_1, point1['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第1条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第1条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

            # 退单100
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, member_code, 100, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual(trade_no_2, point2['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第2条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第2条用例失败..Fail...Expected, Actual {}".format(err))
            raise err


    def test_bind_5(self):
        # 注册
        member_code = self.reg()
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, member_code, 100)
        time.sleep(self.sleep)
        # 确认收货
        self.upload_order_info(trade_no_1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point1 = self.order_detail(member_code, trade_no_1)
            self.assertEqual(trade_no_1, point1['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第1条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第1条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

            # 退单10
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual(trade_no_2, point2['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第2条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第2条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        ## 交易自动关闭
        self.upload_order_info1(trade_no_1)
        time.sleep(self.sleep)
        # 退单10
        trade_no_3 = trade_no_1 + 'tt'
        self.upload_order(trade_no_3, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)

        try:
            # 查订单明细
            point3 = self.order_detail(member_code, trade_no_3)
            self.assertEqual([], point3['data']['orderDetails'])
            self.result = "pass"
            logger.info("第3条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第3条用例失败..Fail...Expected, Actual {}".format(err))
            raise err
        time.sleep(self.sleep)
        # 退单80
        trade_no_4 = trade_no_1 + 'ttt'
        self.upload_order(trade_no_4, member_code, 80, originalOrderId=trade_no_1, orderType='2',number=1)

        time.sleep(self.sleep)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point4 = self.order_detail(member_code, trade_no_4)
            self.assertEqual(trade_no_4, point4['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第4条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第4条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        try:
            # 查订单明细
            point3 = self.order_detail(member_code, trade_no_3)
            self.assertEqual(trade_no_3, point3['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第5条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第5条用例失败..Fail...Expected, Actual {}".format(err))
            raise err


    def test_bind_6(self):
        # 注册
        member_code = self.reg()
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, member_code, 100)
        time.sleep(self.sleep)
        # 确认收货
        self.upload_order_info(trade_no_1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point1 = self.order_detail(member_code, trade_no_1)
            self.assertEqual(trade_no_1, point1['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第1条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第1条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

           # 退单10
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual(trade_no_2, point2['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第2条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第2条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        ## 交易自动关闭
        self.upload_order_info1(trade_no_1)
        # 退单90
        trade_no_3 = trade_no_1 + 'tt'
        self.upload_order(trade_no_3, member_code, 90, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point3 = self.order_detail(member_code, trade_no_3)
            self.assertEqual(trade_no_3, point3['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第3条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第3条用例失败..Fail...Expected, Actual {}".format(err))
            raise err





    def test_bind_7(self):
        # 注册
        member_code = self.reg()
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, member_code, 100)

        try:
            # 查订单明细
            point0 = self.order_detail(member_code, trade_no_1)
            self.assertEqual([], point0['data']['orderDetails'])
            self.result = "pass"
            logger.info("第1条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第1条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        #交易自动关闭
        self.upload_order_info1(trade_no_1)
        # 退单10
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)
        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual([], point2['data']['orderDetails'])
            self.result = "pass"
            logger.info("第2条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第2条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        # 退单10
        trade_no_3 = trade_no_1 + 'tt'
        self.upload_order(trade_no_3, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)
        try:
            # 查订单明细
            point3 = self.order_detail(member_code, trade_no_3)
            self.assertEqual([], point3['data']['orderDetails'])
            self.result = "pass"
            logger.info("第3条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第3条用例失败..Fail...Expected, Actual {}".format(err))
            raise err
        # 退单80
        trade_no_4 = trade_no_1 + 'tTT'
        self.upload_order(trade_no_4, member_code, 80, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point3 = self.order_detail(member_code, trade_no_3)
            self.assertEqual([], point3['data']['orderDetails'])
            self.result = "pass"
            logger.info("第4条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第4条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual([], point2['data']['orderDetails'])
            self.result = "pass"
            logger.info("第5条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第5条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        try:
            # 查订单明细
            point4 = self.order_detail(member_code, trade_no_4)
            self.assertEqual([],point4['data']['orderDetails'])
            self.result = "pass"
            logger.info("第6条用例成功")
        except Exception as err:
            self.result = "fail"
            logger.error("第6条用例失败..Fail...Expected, Actual {}".format(err))
            raise err



    def test_bind_8(self):
        # 注册
        member_code = self.reg()
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, member_code, 100)

        try:
            # 查订单明细
            point0 = self.order_detail(member_code, trade_no_1)
            self.assertEqual([], point0['data']['orderDetails'])
            self.result = "pass"
            logger.info("第1条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第1条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        # 交易自动关闭
        self.upload_order_info1(trade_no_1)
        # 退单100
        trade_no_2=trade_no_1 + 't'
        self.upload_order(trade_no_2, member_code, 100, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)

        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual([], point2['data']['orderDetails'])
            self.result = "pass"
            logger.info("第2条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第2条用例失败..Fail...Expected, Actual {}".format(err))
            raise err




    def test_bind_9(self):
        # 注册
        member_code = self.reg()
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, member_code, 100)

        try:
            # 查订单明细
            point0 = self.order_detail(member_code, trade_no_1)
            self.assertEqual([], point0['data']['orderDetails'])
            self.result = "pass"
            logger.info("第1条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第1条用例失败..Fail...Expected, Actual {}".format(err))
            raise err
        # 退单10
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)
        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual([], point2['data']['orderDetails'])
            self.result = "pass"
            logger.info("第2条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第2条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        # 退单10
        trade_no_3 = trade_no_1 + 'tt'
        self.upload_order(trade_no_3, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)
        try:
            # 查订单明细
            point3 = self.order_detail(member_code, trade_no_3)
            self.assertEqual([], point3['data']['orderDetails'])
            self.result = "pass"
            logger.info("第3条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第3条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        # 退单80
        trade_no_4 = trade_no_1 + 'ttt'
        self.upload_order(trade_no_4, member_code, 80, originalOrderId=trade_no_1, orderType='2',number=1)
        try:
            # 查订单明细
            point4 = self.order_detail(member_code, trade_no_4)
            self.assertEqual([], point4['data']['orderDetails'])
            self.result = "pass"
            logger.info("第3条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第3条用例失败..Fail...Expected, Actual {}".format(err))
            raise err


        #交易关闭
        self.upload_order_info1(trade_no_1)

        time.sleep(self.sleep)
        try:
            # 查订单明细
            point4 = self.order_detail(member_code, trade_no_4)
            self.assertEqual([], point4['data']['orderDetails'])
            self.result = "pass"
            logger.info("第4条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第4条用例失败..Fail...Expected, Actual {}".format(err))
            raise err
        try:
            # 查订单明细
            point3 = self.order_detail(member_code, trade_no_3)
            self.assertEqual([], point3['data']['orderDetails'])
            self.result = "pass"
            logger.info("第5条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第5条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual([], point2['data']['orderDetails'])
            self.result = "pass"
            logger.info("第6条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第6条用例失败..Fail...Expected, Actual {}".format(err))
            raise err



    def test_bind_10(self):
        # 注册
        member_code = self.reg()
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, member_code, 100)

        try:
            # 查订单明细
            point0 = self.order_detail(member_code, trade_no_1)
            self.assertEqual([], point0['data']['orderDetails'])
            self.result = "pass"
            logger.info("第1条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第1条用例失败..Fail...Expected, Actual {}".format(err))
            raise err
        # 退单100
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, member_code, 100, originalOrderId=trade_no_1, orderType='2',number=1)
        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual([], point2['data']['orderDetails'])
            self.result = "pass"
            logger.info("第2条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第2条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

         #交易自动关闭
        self.upload_order_info1(trade_no_1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual([], point2['data']['orderDetails'])
            self.result = "pass"
            logger.info("第3条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第3条用例失败..Fail...Expected, Actual {}".format(err))
            raise err


    def test_bind_11(self):
        # 注册
        member_code = self.reg()
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, member_code, 100)

        try:
            # 查订单明细
            point0 = self.order_detail(member_code, trade_no_1)
            self.assertEqual([], point0['data']['orderDetails'])
            self.result = "pass"
            logger.info("第1条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第1条用例失败..Fail...Expected, Actual {}".format(err))
            raise err
        # 退单10
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)
        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual([], point2['data']['orderDetails'])
            self.result = "pass"
            logger.info("第2条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第2条用例失败..Fail...Expected, Actual {}".format(err))
            raise err
        #交易自动关闭
        self.upload_order_info1(trade_no_1)

        # 退单10
        trade_no_3 = trade_no_1 + 'tt'
        self.upload_order(trade_no_3, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)
        try:
            # 查订单明细
            point3 = self.order_detail(member_code, trade_no_3)
            self.assertEqual([], point3['data']['orderDetails'])
            self.result = "pass"
            logger.info("第3条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第3条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

            # 退单80
        trade_no_4 = trade_no_1 + 'ttt'
        self.upload_order(trade_no_4, member_code, 80, originalOrderId=trade_no_1, orderType='2',number=1)
        try:
            # 查订单明细
            point4 = self.order_detail(member_code, trade_no_4)
            self.assertEqual([], point4['data']['orderDetails'])
            self.result = "pass"
            logger.info("第3条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第3条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

            # 交易关闭
        self.upload_order_info1(trade_no_1)

        time.sleep(self.sleep)
        try:
            # 查订单明细
            point4 = self.order_detail(member_code, trade_no_4)
            self.assertEqual([], point4['data']['orderDetails'])
            self.result = "pass"
            logger.info("第4条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第4条用例失败..Fail...Expected, Actual {}".format(err))
            raise err
        try:
            # 查订单明细
            point3 = self.order_detail(member_code, trade_no_3)
            self.assertEqual([], point3['data']['orderDetails'])
            self.result = "pass"
            logger.info("第5条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第5条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual([], point2['data']['orderDetails'])
            self.result = "pass"
            logger.info("第6条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第6条用例失败..Fail...Expected, Actual {}".format(err))
            raise err


    def test_bind_12(self):
        # 注册
        member_code = self.reg()
        # 随机正单号
        trade_no_1 = "test_arvato_" + str(int(time.time()))
        # 正单
        self.upload_order(trade_no_1, member_code, 100)

        try:
            # 查订单明细
            point0 = self.order_detail(member_code, trade_no_1)
            self.assertEqual([], point0['data']['orderDetails'])
            self.result = "pass"
            logger.info("第1条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第1条用例失败..Fail...Expected, Actual {}".format(err))
            raise err
        # 退单10
        trade_no_2 = trade_no_1 + 't'
        self.upload_order(trade_no_2, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)
        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual([], point2['data']['orderDetails'])
            self.result = "pass"
            logger.info("第2条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第2条用例失败..Fail...Expected, Actual {}".format(err))
            raise err
        time.sleep(self.sleep)
        # 确认收货
        self.upload_order_info(trade_no_1)
        time.sleep(self.sleep)

        try:
            # 查订单明细
            point1 = self.order_detail(member_code, trade_no_1)
            self.assertEqual(trade_no_1, point1['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第8条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第8条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        try:
            # 查订单明细
            point2 = self.order_detail(member_code, trade_no_2)
            self.assertEqual(trade_no_2, point2['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第3条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第3条用例失败..Fail...Expected, Actual {}".format(err))
            raise err


        # 退单10
        trade_no_3 = trade_no_1 + 'tt'
        self.upload_order(trade_no_3, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point3 = self.order_detail(member_code, trade_no_3)
            self.assertEqual(trade_no_3, point3['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第4条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第4条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        #交易自动关闭
        self.upload_order_info1(trade_no_1)

        #退单10
        trade_no_4 = trade_no_1 + 'ttt'
        self.upload_order(trade_no_4, member_code, 10, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)
        try:
            # 查订单明细
            point4 = self.order_detail(member_code, trade_no_4)
            self.assertEqual([], point4['data']['orderDetails'])
            self.result = "pass"
            logger.info("第5条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第5条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        #退单70
        trade_no_5 = trade_no_1 + 'tttt'
        self.upload_order(trade_no_5, member_code, 70, originalOrderId=trade_no_1, orderType='2',number=1)
        time.sleep(self.sleep)

        try:
            # 查订单明细
            point5 = self.order_detail(member_code, trade_no_5)
            self.assertEqual(trade_no_5, point5['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第6条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第6条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

        try:
            # 查订单明细
            point4 = self.order_detail(member_code, trade_no_4)
            self.assertEqual(trade_no_4, point4['data']['orderDetails'][0]['tradeNo'])
            self.result = "pass"
            logger.info("第7条用例成功")

        except Exception as err:
            self.result = "fail"
            logger.error("第7条用例失败..Fail...Expected, Actual {}".format(err))
            raise err

if __name__ == "__main__":
    unittest.main()
