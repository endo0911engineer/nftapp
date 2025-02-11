const API_BASE_URL = process.env.Next_PUBLIC_API_BASE_URL;
import { ethers } from "ethers"; 

export async function authenticateWithMetaMask() {
    if(!window.ethereum) {
        alert("MetaMaskがインストールされていません。インストールしてください。");
        return { success: false};
    }

    try {
        //MetaMaskに接続してウォレットアドレスを取得
        const provider = new ethers.BrowserProvider(window.ethereum);
        
        // すでにウォレットが接続済みか確認
        const accounts = await provider.send("eth_accounts", []);
        let walletAddress = accounts.length > 0 ? accounts[0] : null;

        if (!walletAddress) {
            const newAccounts = await provider.send("eth_requestAccounts", []);
            walletAddress = newAccounts[0];
        }

        console.log("wallet Address:", walletAddress);
        
        const signer = await provider.getSigner();

        // サーバーから署名用メッセージを取得
        const messageRes = await fetch(`http://127.0.0.1:8000/api/get_sign_message/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ walletAddress }),
        });

        if(!messageRes.ok) {
            alert("署名用メッセージの取得に失敗しました。");
            return;
        }
        
        const { message } = await messageRes.json();
        // 署名
        const signature = await signer.signMessage(message);

        // サーバーにウォレットアドレスと署名を送信
        const authRes = await fetch(`http://127.0.0.1:8000/api/authenticate/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ walletAddress, signature, message }),
        });

        if (authRes.ok) {
            localStorage.setItem("walletAddress", walletAddress);

            return {
                success: true,
                walletAddress: walletAddress,
            }
        } else {
            alert("認証に失敗しました。");
            return { success: false };
        }
    } catch (error) {
        console.error("MetaMask認証エラー:", error);
        alert("認証に失敗しました。");
        return { success: false };
    }
}