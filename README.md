自动化框架结构

这是框架的使用说明:
common: 公共方法存放目录  
config: 配置文件存放目录
data:   测试数据存放目录
library:第三方下载模块存放目录
logs:   日志存放目录 
middleware: 中间层, common方法的实例, 接口依赖
reports:测试报告存放目录
tests:  测试用例类模块存放目录
run:    收集用例/运行用例/启动项目的主程序

Arvato_write_common.xlsx:
    存放的各品牌通用测试用例...不同品牌的预期结果在对应的expect_response

Arvato_upload_order_info.xlsx:
    存放的是各品牌的订单测试用例:upload_order_verifyGrade, upload_order_verifyOrder
    upload_order_verifyOrder: 通过9种不同的channelType进行购买订单;及参数的验证;
    upload_order_verifyGrade: 验证每个等级的升降级规则;

Arvato_upload_message_info.xlsx:
    存放的各品牌的上传消息测试用例:bio, lrp, ac, cerave

add smoke test

品牌升降级：tests\test_order
升降级用例：data\data_write\arvat_upload_change_grade.xlsx

