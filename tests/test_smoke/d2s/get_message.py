from middleware.middle_prd.middle_write.handler_middle import ReplaceDate as _ReplaceDate, Handler as _Handler


class ReplaceDate(_ReplaceDate, _Handler):

    @property
    def vender_seq_code(self):
        return _Handler().random_num

    @property
    def tradeNo(self):
        return _Handler().random_trade

    # re替换数据
    def replace_data(self, data):
        import re
        data = super().replace_data(data)
        return data


if __name__ == "__main__":
    token = _Handler().headers('d2s')
    print(ReplaceDate('d2s', headers=token, value=None, query_type="union_code").vender_seq_code)
    print(ReplaceDate('d2s', headers=token, value=None, query_type="union_code").tradeNo)