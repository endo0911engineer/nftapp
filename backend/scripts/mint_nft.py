from web3 import web3
import sys
import json

# Arguments: recipient_address, image_url, message
recipient_address = sys.argv[1]
image_url = sys.argv[2]
message = sys.argv[3]

# Blockchain setup for Ganache
GANACHE_URL = "https://127.0.0.1:8545"
PRIVATE_KEY = "YOUR_GANACHE_PRIVATE_KEY"
CONTRACT_ADDRESS = "YOUR_LOCAL_CONTRACT_ADDRESS"
ABI = json.load(open("scrits/abi/contract_abi.json"))

def call_generate_image(message, image_url):
    try:
        # generate_image.py をサブプロセスとして呼び出す
        result = subprocess.run(
            ["python3", "scripts/generate_image.py", message, image_url],
            capture_output=True,
            text=true
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        
        # JSONとして解析
        return json.loads(result.stdout)
    except Exception as e:
        return {"error": str(e)}

def mint_nft(recepient_address, image_path):
    try:
        # Web3設定
        web3 = Web3(Web3.HTTPProvider(INFURA_URL))
        account = web3.eth.account.from_key(PRIVATE_KEY)
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

        # メタデータ生成
        metadata = {"image": image_path, "description": message}

        # トランザクションの準備
        nonce = web3.eth.get_transaction_count(account.address)
        transaction = contract.functions.mintNFT(recipient_address, json.dumps(metadata)).build_transaction({
            'chainId': 1337,
            'gas': 6721975,
            'gasPrice': web3.toWei('1', 'gwei'),
            'nonce': nonce
        })

        # 署名して送信
        signed_txn = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # ミント後にNFTを送信するためのトランザクション
        token_id = "ミントされたNFTのID"
        transfer_txn = contract.functions.transferForm(account.address, recipient_address, token_id).build_transaction({
            'chainId': 1337,
            'gas': 6721975,
            'gasPrice': web3.toWei('1', 'gwei'),
            'nonce': nonce + 1  # 別のnonceを使う
        })

        # 送信するトランザクションに署名
        signed_transfer_txn = web3.eth.account.sign_transaction(transfer_txn, PRIVATE_KEY)
        transfer_txn_hash = web3.eth.send_raw_transaction(signed_transfer_txn.rawTransaction)
        
        return {"transaction_hash": web3.to_hex(tx_hash)}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(json.dumps({"error": "Invalid arguments"}))
        sys.exit(1)

    recipient_addredd = sys.argv[1]
    image_url = sys.argv[2]
    message = sys.argv[3]

    # 画像生成
    image_result = call_geerate_image(message, image_url)
    if "error" in image_result:
        print(json.dumps(image_result))
        sys.exit(1)

    # NFTをミント
    mint_result = mint_nft(recipient_address, image_result["output_path"])
    if "error" in mint_result:
        print(json.dumps(mint_result))
        sys.exit(1)

    # 成功レスポンス
    response = {
        "image": image_result,
        "mint": mint_result
    }
    print(json.dumps(response))