const API_BASE_URL = 'http://127.0.0.1:8000';

export async function fetchReceivedGifts(setGifts: (gifts: any[]) => void, setLoading: (state: boolean) => void) {
  const walletAddress = localStorage.getItem("walletAddress");

  if (!walletAddress) {
    console.error("ウォレットアドレスが見つかりません。ログインしてください。");
    return;
  }

  try {
      setLoading(true);
      const res = await fetch(`${API_BASE_URL}/api/received_gifts?recipient_address=${walletAddress}`);
      const data = await res.json();
      if (res.ok) {
        setGifts(data);
        console.log("Received gifts:", data);
      } else {
        console.error("failed to fetch received gifts:", data);
      }
    } catch (error) {
      console.error("Error fetching received gifts:", error);
    } finally {
      setLoading(false);
    }
};

export async function confirmGiftReceived(giftId: string, setGifts: (gifts: any[]) => void, setLoading: (state: boolean) => void) {
    try {
        setLoading(true);
        const res = await fetch(`${API_BASE_URL}/api/confirm_gift`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ gift_id: giftId }),
        });

        if (!res.ok) {
            throw new Error('Failed to confirm gift');
        }

        alert("Gift confirmed succesfully!");
        fetchReceivedGifts(setGifts, setLoading);
    } catch (error) {
      console.error("Error confirming gift:", error);
    } finally {
        setLoading(false);
    }
};