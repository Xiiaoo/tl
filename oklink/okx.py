import requests
import time
import execjs
import pymongo
from multiprocessing import Process, JoinableQueue as Queue


ctx = execjs.compile(open('金融\\Okx\\apikey.js', 'r', encoding='utf-8').read())



def get_data(pageNum, queue):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-apikey': ctx.call('get_apikey')
    }
    params = {
        'offset': pageNum*20,
        'limit': '20',
        'curType': 'large',
        'sort': 'realTransferValue,desc',
        't': str(int(time.time()*1000)),
    }
    res = requests.get('https://www.oklink.com/api/explorer/v1/btc/transactionsNoRestrict',
                       headers=headers, params=params).json()['data']['hits']
    for info in res:
        block_info = {}
        block_info['hash']=info['hash']
        block_info['blockHeight']=info['blockHeight']
        block_info['blockHash']=info['blockHash']
        block_info['size']=info['size']
        queue.put(block_info)

def save_block_info(queue):
    mongo_client = pymongo.MongoClient(host='localhost', port=27017)
    collection = mongo_client['Wecent']['OKX']
    while True:
        dict_data = queue.get()  # 阻塞
        collection.insert_one(dict_data)
        print('保存成功:', dict_data)
        queue.task_done()


if __name__ == '__main__':
    dict_queue = Queue()
    process_list = list()
    for page in range(1, 501):
        p_get_info = Process(target=get_data, args=(page, dict_queue))
        process_list.append(p_get_info)

    p_save_work = Process(target=save_block_info, args=(dict_queue,))
    process_list.append(p_save_work)

    for process in process_list:
        # 子进程设置为守护进程
        process.daemon = True
        process.start()

    time.sleep(3)  # 创建进程以及启动进程的速度比较慢
    dict_queue.join()  # 队列中的所有数据全部取出之后释放主进程
    print('进程任务完成...')

