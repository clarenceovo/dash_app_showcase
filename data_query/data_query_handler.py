from transport.db_transport import db_connector
import pandas as pd
def get_oi_exchange():
    db_conn = db_connector()
    try:
        ret = db_conn.CUSTOM("SELECT DISTINCT(exchange) as exchange FROM trading_data.open_interest;");
        return ret
    except Exception as e:
        return None

def get_contract_pair(exchange):
    db_conn = db_connector()
    try:
        ret = db_conn.CUSTOM(f"SELECT DISTINCT(contract) as exchange FROM trading_data.open_interest WHERE exchange = '{exchange}';");
        return ret
    except Exception as e:
        print(e)
        return None

def get_oi_data(code):
    db_conn = db_connector()
    tmp = code.split("@")
    exchange, contract = tmp[0],tmp[1]
    query = f"SELECT datetime ,price , open_interest FROM trading_data.open_interest WHERE exchange = '{exchange}' and contract = '{contract}';"
    try:
        ret = db_conn.CUSTOM(query)
        return pd.DataFrame(ret)
    except Exception as e:
        print(e)
        return None

def get_funding_contract(exchange):
    db_conn = db_connector()
    query = f"SELECT DISTINCT(contract_code)  FROM trading_data.funding_rate WHERE exchange= {exchange} ORDER BY contract_code;"
    try:
        ret = db_conn.CUSTOM(query)
        return pd.DataFrame(ret)
    except Exception as e:
        print(e)
        return None
def get_funding_exchange():
    db_conn = db_connector()
    query = f"SELECT DISTINCT(exchange)  FROM trading_data.funding_rate;"
    try:
        ret = db_conn.CUSTOM(query)
        return pd.DataFrame(ret)
    except Exception as e:
        print(e)
        return None
def get_funding_contract(exchange):
    db_conn = db_connector()
    query = f"SELECT DISTINCT(contract_code)  FROM trading_data.funding_rate WHERE exchange= '{exchange}' ORDER BY contract_code;"
    try:
        ret = db_conn.CUSTOM(query)
        return pd.DataFrame(ret)
    except Exception as e:
        print(e)
        return None

def get_funding(label):
    db_conn = db_connector()
    tmp = label.split("@")
    exchange, contract = tmp[0],tmp[1]
    #
    query = f"SELECT date,contract_code,funding_rate FROM trading_data.funding_rate WHERE " \
            f"exchange = '{exchange}' AND contract_code = '{contract}' order by date desc limit 21900;"
    try:
        ret = db_conn.CUSTOM(query)
        return pd.DataFrame(ret)
    except Exception as e:
        print(e)
        return None


def get_funding_table(label):
    db_conn = db_connector()
    tmp = label.split("@")
    exchange, contract = tmp[0],tmp[1]
    query = f"SELECT date,contract_code,funding_rate FROM trading_data.funding_rate WHERE " \
            f"exchange = '{exchange}' AND contract_code = '{contract}' order by date desc limit 2880;"
    try:
        ret = db_conn.CUSTOM(query)
        return pd.DataFrame(ret)
    except Exception as e:
        print(e)
        return None
"""def get_contract_pair(exchange,contract):
    db_conn = db_connector()
    try:
        ret = db_conn.CUSTOM(f"SELECT  as exchange FROM trading_data.open_interest WHERE exchange = '{exchange}' and contract = '{contract}';");
        return ret
    except Exception as e:
        print(e)
        return None"""