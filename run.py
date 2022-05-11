import datetime

HEADERS = 'event_time,event_type,product_id,category_id,category_code,brand,price,user_id,user_session'
HEADERS = HEADERS.split(',')
print(HEADERS)


class C5200:
    
    def __init__(self):
        self.brands = set()
        self.event_types = set()
        self.view_ct = 0
        self.purchase_ct = 0
        self.hourly_purchase = {}
        self.price_range = {
            '0-50': 0,
            '50-100': 0,
            '100-200': 0,
            '200-300': 0,
            '300-400': 0,
            '400-500': 0,
            '500-1000': 0,
            '1000+': 0
        }
        for i in range(0, 24):
            self.hourly_purchase[int(i)] = 0
    
    def process(self, line):
        row = line.split(',')
        etype = row[1]
        brand = row[5]
        price = float(row[6])
        event_time = row[0]
        hour = event_time.split()[1].split(':')[0]
        hour = int(hour)
        
        self.brands.add(brand)
        self.event_types.add(etype)
        if etype == 'purchase':
            self.purchase_ct += 1
            # count hourly purchase.
            self.hourly_purchase[hour] += 1
            # count for price range
            if price <= 50: self.price_range['0-50'] += 1
            elif price <= 100: self.price_range['50-100'] += 1
            elif price <= 200: self.price_range['100-200'] += 1
            elif price <= 300: self.price_range['200-300'] += 1
            elif price <= 400: self.price_range['300-400'] += 1
            elif price <= 500: self.price_range['400-500'] += 1
            elif price <= 1000: self.price_range['500-1000'] += 1
            else: self.price_range['1000+'] += 1
            
        elif etype == 'view':
            self.view_ct += 1
            
    def run(self, limit=67_502_000):
        limit = limit or 67502000
        with open('data.csv', 'r', encoding='utf-8') as fp:
            ct = 0
            for line in fp:
                ct += 1
                if ct == 1: continue # skip first line.
                if ct % 1_000_000 == 0: print(ct / 1_000_000, '/ 67')
                if ct > limit: break
                self.process(line)
        
        print(self.hourly_purchase) 
        # {0: 2822, 1: 4215, 2: 11156, 3: 26336, 4: 44089, 5: 53361, 6: 57427, 7: 58705, 8: 65261, 9: 71434, 10: 69042, 11: 64271, 12: 61257, 13: 59671, 14: 59474, 15: 52599, 16: 46220, 17: 45342, 18: 23642, 19: 17063, 20: 10153, 21: 6319, 22: 4289, 23: 2791}
        print(float(self.purchase_ct) / float(self.view_ct)) 
        # 0.01442723602813325 so the purchase rate is 1.4%
        print(self.price_range)
        '''
        {
            '0-50': 152856, 
            '50-100': 114018, 
            '100-200': 244631, 
            '200-300': 134998, 
            '300-400': 63640, 
            '400-500': 44665, 
            '500-1000': 116348, 
            '1000+': 45783
        }
        '''

C5200().run(limit=None)    
