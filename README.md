
目前不需要注册开发者，只需要申请apikey
apikey申请流程：
1.先注册账户
2.在设置页面，绑定GA
3.在设置页面，申请api，两个字段都必须填写，IP地址目前限制
limit：限价
market：市价

api文档：
https://developer.fcoin.com/zh.html#32c808cbe5


交易手续费：
https://support.fcoin.com/hc/zh-cn/articles/360003715514-%E4%BA%A4%E6%98%93%E6%89%8B%E7%BB%AD%E8%B4%B9%E5%8F%8A%E8%AE%A2%E5%8D%95%E8%A7%84%E5%88%99%E8%AF%B4%E6%98%8E

以下3个参数，需要放在headers中
FC-ACCESS-KEY
FC-ACCESS-SIGNATURE
FC-ACCESS-TIMESTAMP

websocket：
def get_market_price(symbol):
    ws = create_connection("wss://ws.fcoin.com/api/v2/ws")
    ws.recv()
    s = "ticker.{}".format(symbol['name'])
    req = {
        'cmd':'req',
        'args':[s],
        'id':'1'
    }
    ws.send(json.dumps(req))
    r = json.loads(ws.recv())
    ws.close()
    return r['data']['ticker'][0]

深度订阅，实际发送的内容是：{"cmd":"sub","args":["depth.L100.btcusdt"],"id":"1"}

获取订单列表中：
至少传symbol和state

git地址：
https://github.com/FCoinCommunity


Post请求时一定要加json头：
'content-type': 'application/json;charset=UTF-8'
请求的body要传json格式

可以查询以提交和部分成交的数据：
submitted, partial_filled, partial_canceled, filled, canceled
这些状态，可以同时传，中间用逗号隔开

Post签名前的字符串：
POSThttps://api.fcoin.com/v2/orders1528532934527amount=1000&price=0.192011&side=buy&symbol=ftusdt&type=limit
Get签名前的字符串：
GEThttps://api.fcoin.com/v2/orders?limit=20&states=submitted,partial_filled&symbol=ethusdt1528532959168

获取订单接口中before和after表示时间戳，只能有1个时间戳，limit最大支持100

public是要传给服务器的，secret是用来签名的

1002   system busy 是因为下单太快了

获取行情深度接口中，只有L20，L150，full

python版本的签名代码：
def sort_payload(self, payload):
        keys = sorted(payload.keys())
        result = ''
        for i in range(len(keys)):
            if i != 0:
                result += '&' + keys[i] + "=" + str(payload[keys[i]])
            else:
                result += keys[i] + "=" + str(payload[keys[i]])
        return result

    # 对请求数据进行加密编码
    def encrypt_data(self, HTTP_METHOD, HTTP_REQUEST_URI, TIMESTAMP, POST_BODY, secret):
        payload_result = ''
        if POST_BODY != '':
            payload_result = self.sort_payload(POST_BODY)
        data = HTTP_METHOD + HTTP_REQUEST_URI + TIMESTAMP + payload_result
        print(data)
        data_base64 = base64.b64encode(bytes(data, encoding='utf8'))
        # print(data_base64)
        data_base64_sha1 = hmac.new(bytes(secret, encoding='utf8'), data_base64, hashlib.sha1).digest()
        data_base64_sha1_base64 = base64.b64encode(data_base64_sha1)
        # print(data_base64_sha1_base64)
        return str(data_base64_sha1_base64, encoding='utf-8')

    def create_headers(self, HTTP_METHOD, HTTP_REQUEST_URI, TIMESTAMP, POST_BODY, public_key, secret_key):
        signature = self.encrypt_data(HTTP_METHOD, HTTP_REQUEST_URI, str(TIMESTAMP), POST_BODY, secret_key)
        self.headers['FC-ACCESS-KEY'] = public_key
        self.headers['FC-ACCESS-TIMESTAMP'] = str(TIMESTAMP)
        self.headers['FC-ACCESS-SIGNATURE'] = signature

Php版本的签名代码：
// 获取毫秒时间戳
    function get_millisecond() {
        list($t1, $t2) = explode(' ', microtime());
        return (float)sprintf('%.0f', (floatval($t1) + floatval($t2)) * 1000);
    }
    //hmac_sha1算法
    function getSignature($str, $key) {
        $signature = "";
        if (function_exists('hash_hmac')) {
            $signature = base64_encode(hash_hmac("sha1", $str, $key, true));
        } else {
            $blocksize = 64;
            $hashfunc = 'sha1';
            if (strlen($key) > $blocksize) {
                $key = pack('H*', $hashfunc($key));
            }
            $key = str_pad($key, $blocksize, chr(0x00));
            $ipad = str_repeat(chr(0x36), $blocksize);
            $opad = str_repeat(chr(0x5c), $blocksize);
            $hmac = pack(
                'H*', $hashfunc(
                    ($key ^ $opad) . pack(
                        'H*', $hashfunc(
                            ($key ^ $ipad) . $str
                        )
                    )
                )
            );
            $signature = base64_encode($hmac);
        }
        return $signature;
    }
    // 组合参数
    function bind_param($param) {
        if($param){
            $u = [];
            $sort_rank = [];
            foreach($param as $k=>$v) {
                $u[] = $k."=".urlencode($v);
                $sort_rank[] = ord($k);
            }
            asort($u);
            return implode('&', $u);
        }else{
            return '';
        }

    }
    // 生成签名
    function create_sig($param) {
        $this->access_timestamp = $this->get_millisecond();
        $sign_param_1 = $this->req_method.$this->sign_url.$this->api_method.$this->access_timestamp.$this->bind_param($param);
        $sign_param_1 = base64_encode($sign_param_1);
        $signature = $this->getSignature($sign_param_1,SECRET_KEY);
        return $signature;
    }
