from init import *

def receivable_auctions_filter(auctions_type):
    auctions = list(mongo.db[auctions_type].find())
    print(auctions)
    params = mongo.db.params.find_one()

    if not params:
        return 'params is none'
    elif params['advanced_amount'] / params['account_receivable'] > 0.01:
        return 'single invoice not less than 1%'

    # auctions_list = []
    # 通过全部筛选条件的发票
    passing_all_criteria = []
    # 只通过必要准则的发票
    passing_the_critical_criteria = []
    # 相同卖家编号的预付金额总和
    advanced_amount_seller_no_sum = {}
    # 相同债务人的预付金额总和
    advanced_amount_obligor_name_sum = {}

    for auction in auctions:
        for key, value in auction.items():
            if key == 'seller_no':
                advanced_amount_seller_no_sum[value] = 0
            elif key == 'obligor_name':
                advanced_amount_obligor_name_sum[value] = 0

    for auction in auctions:
        # 如果是美元计算需要转换成港币
        if auction['currency'] == 'USD':
            advanced_amount_seller_no_sum[auction['seller_no']] += auction[
                                                                       'ss_auction_total_advance_amount_in_usd'] * 7.8
            advanced_amount_obligor_name_sum[auction['obligor_name']] += auction[
                                                                             'ss_auction_total_advance_amount_in_usd'] * 7.8
        elif auction['currency'] == 'HKD':
            advanced_amount_seller_no_sum[auction['seller_no']] += auction['ss_auction_total_advance_amount_in_hkd']
            advanced_amount_obligor_name_sum[auction['obligor_name']] += auction[
                'ss_auction_total_advance_amount_in_hkd']
    # print(advanced_amount_seller_no_sum)
    # print(advanced_amount_obligor_name_sum)

    single_seller_less_than_3_percent = []
    single_obligor_less_than_6_percent = []

    for k1, v1 in advanced_amount_seller_no_sum.items():
        if v1 / params['account_receivable'] <= 0.03:
            single_seller_less_than_3_percent.append(k1)

    for k2, v2 in advanced_amount_obligor_name_sum.items():
        if v2 / params['account_receivable'] <= 0.06:
            single_obligor_less_than_6_percent.append(k2)

    for auction in auctions:
        if auction['seller_no'] in single_seller_less_than_3_percent and auction[
            'obligor_name'] in single_obligor_less_than_6_percent and auction['no_of_days'] <= 120 and auction[
            'ss_average_late_day'] <= 20 and \
                auction['suggested_basis_point'] >= 1050:
            # 通过必要准则的拍卖
            passing_the_critical_criteria.append(auction)

            # 通过全部准则的拍卖
            if auction['credit_insurance'] == 1 and auction['obligor_qupital_rating'] >= 4 and params[
                'advanced_amount'] / auction['revenue'] <= 0.1 and auction['sos_successful_auction'] > 0:  # Todo: 需要确定revenue是USD还是HKD
                passing_all_criteria.append(auction)

    return passing_all_criteria, passing_the_critical_criteria, auctions


if __name__ == '__main__':
    pass
