const API_BASE_URL = process.env.Next_PUBLIC_API_BASE_URL;

export async function handleMintNFT({ address, message, image, setLoading}: { address: string; message: string; image: File | null; setLoading: (state: boolean) => void }) {
    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("recipient_address", address);
      formData.append("image", image as Blob);
      formData.append("message", message);

      //Call backend API to mint NFT
      const res = await fetch(`${API_BASE_URL}/api/mint_nft`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Failed to process the NFT minting request");
      }
      
      const data = await res.json();
      console.log("NFT Minted Successfully", data);
      alert("NFT Minted Successfully!");
    } catch (error) {
      console.error("Error during NFT minting:", error);
      alert("Failed to mint NFT. Please try again.");
    } finally {
        setLoading(false);
    }
};