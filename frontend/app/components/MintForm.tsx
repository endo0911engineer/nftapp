'use client';
import { useState } from 'react';
import { handleMintNFT } from '../hooks/useMintNFT';

export default function MintForm() {
  const [address, setAddress] = useState('');
  const [message, setMessage] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    await handleMintNFT({ address, message, image, setLoading });
  };

  return (
    <div className="form">
      <input
        type="text"
        placeholder="Recipient Address"
        value={address}
        onChange={(e) => setAddress(e.target.value)}
      />
      <textarea
        placeholder="Message"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <input type="file" onChange={(e) => setImage(e.target.files?.[0] || null)} />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Processing...' : 'Mint NFT'}
      </button>
    </div>
  );
}