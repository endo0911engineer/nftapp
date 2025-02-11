from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.contrib.auth import logout
import json
from .models import Gift
from .models import User
from eth_account.messages import encode_defunct
from eth_account import Account
import uuid
import time
from web3 import Web3


# ギフト送信API
@csrf_exempt
def send_gift(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            gift = Gift(
                sender_address=data.get("sender_address"),
                recipient_adress=data.get("recipient_address"),
                message=data.get("message"),
                nft_url=data.get("nft_url"),
                status="sent",
                created_at=now()
            )
            gift.save()
            return JsonResponse({"message": "Gift sent successfully", "gift": {
                "id": gift_id,
                "sender_address": gift.sender_address,
                "recipient_address": gift.recipient_address,
                "message": gift.message,
                "nft_url": gift.nft_url,
                "status": gift.status,
                "created_at": gift.created_at,
            }})
        except Exception as e:
            return JsonResponse({"error": "failed to send gift", "details": str(e)}, status=400)

# 受信したギフト一覧API
def received_gifts(request):
    if request.method == "GET":
        recipient_address = request.GET.get("recipient_address")
        if not recipient_address:
            return JsonResponse({"error": "recipient_address is required"}, status=400)
        gifts = Gift.objects.filter(recipient_address=recipient_address, status="sent")
        gift_list = [
            {
                "id": gift.id,
                "sender_address": gift.sender_address,
                "recipient_address": gift.recipient_address,
                "message": gift.message,
                "nft_url": gift.nft_url,
                "status": gift.status,
                "created_at": gift.created_at,
            }
            for gift in gifts
        ]
        return JsonResponse(gift_list, safe=False)

# ギフト確認API
@csrf_exempt
def confirm_gift(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            gift_id = data['gift_id']
            gift = Gift.objects.get(id=gift_id)
            gift.status = 'received'
            gift.save()

            return JsonResponse({"message": "Gift received"})
        except Gift.DoesNotExist:
            return JsonResponse({"error": "Gift not found"}, status=404)
        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({"error": f"Invalid confirmation data: {str(e)}"}, status=400)

    return jsonResponse({"error": "Invalid request method"}, status=405)       


# NFTをMINTするAPI
@csrf_exempt
def mint_nft(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            recipient_address = data.get('recipient_address')
            image_url = data.get('image_url')
            message = data.get('message')

            if not (recipient_address and image_url and message):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # mint_nft.py呼び出し
            script_path = "scripts/mint_nft.py"
            cmd = [
                "python3",
                script_path,
                recipient_address,
                image_url,
                message,
            ]
            result = subprocess.run(cmd, capture_output=true, text=True)

            return JsonResponse({"message": "NFT minted succcessfully", "output": result.stdout})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON paylosd"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

# GanacheのURL設定
w3 = Web3(Web3.HTTPProvider(""))

@csrf_exempt
def authenticate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            wallet_address = data.get("walletAddress")
            signature = data.get("signature")
            message = data.get("message")

            print(data)

            if not wallet_address or not signature or not message:
                return JsonResponse({"error": "Wallet address, signature, and message are required"}, status=400)

            # メッセージのエンコード
            message_obj = encode_defunct(text=message)

            # 署名の検証
            signer = w3.eth.account.recover_message(message_obj, signature=signature)
            if signer.lower() != wallet_address.lower():
                return JsonResponse({"error": "Invalid signature. "}, status=400)

            # ユーザーが存在しない場合エラー
            if not User.objects.filter(wallet_address=wallet_address).exists():
                return JsonResponse({"error": "user not found. Please sign up first."}, status=400)

            # セッションにユーザー情報を保存
            request.session['wallet_address'] = wallet_address

            
            return JsonResponse({"success": True, "walletAddress": wallet_address})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
def get_sign_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            wallet_address = data.get("walletAddress")
            if not wallet_address:
                return JsonResponse({"error": "Wallet address is required"}, status=400)

            # ユーザーが存在しない場合、新規作成
            user, created = User.objects.get_or_create(wallet_address=wallet_address)

            # 署名用メッセージを生成
            message = f"ログイン用署名: {wallet_address} - {uuid.uuid4()} - {int(time.time())}"

            return JsonResponse({"message": message})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method"}, status=405)

# ログアウト用エンドポイント
@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        # セッション削除
        request.session.flush()
        return JsonResponse({"success": True, "message": "Logged out successfully"})
    return JsonResponse({"error": "Invalid method"}, status=405)

# ユーザーのログインを確認するエンドポイント
@csrf_exempt
def check_authentication(request):
    if request.method == "GET":
        wallet_address = request.session.get('wallet_address')
        
        if wallet_address:
            return JsonResponse({"authenticated": True, "walletAddress": wallet_address})
        else:
            return JsonResponse({"authenticated": False})
    
    return JsonResponse({"error": "Invalid method"}, status=405)