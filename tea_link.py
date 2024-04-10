tea_dict = {'桃氣茶':'https://reurl.cc/97laLY',
            '康福茶':'https://reurl.cc/lg1AA9',
            '森纖茶':'https://reurl.cc/A45YY3',
            '沁香茶':'https://reurl.cc/D40EEE',
            '水潤茶':'https://reurl.cc/E4Aee0',
            '棗安茶':'https://reurl.cc/N4W99k',
            '橙舒茶':'https://reurl.cc/zlVELy',
            '輕纖茶':'https://reurl.cc/Z9mvgW',
            '頌夏茶':'https://reurl.cc/dLYAgy',
            }

def check_tea_link(response_text):
    for key in tea_dict:      
        if key in response_text:
           
           return tea_dict[key]
