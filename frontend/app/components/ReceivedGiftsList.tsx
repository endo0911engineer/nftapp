'use client';

import { useEffect, useState } from "react";
import { confirmGiftReceived, fetchReceivedGifts } from "../hooks/useFetchReceivedGifts";


export default function ReceivedGiftsList({ loading, setLoading }: { loading: boolean; setLoading: (state: boolean) => void }) {
    const [gifts, setGifts] = useState([]);

    useEffect(() => {
        fetchReceivedGifts(setGifts, setLoading);
    }, []);

    return (
        <ul>
            {gifts.map((gift) => (
                <li key={gift.id} className="gift-item">
                    <p>Sender: {gift.sender_address}</p>
                    <p>Message: {gift.message}</p>
                    <a href={gift.nft_url} target="_blank" rel="noopener noreferrer">
                        View NFT
                    </a>
                    {gift.status === 'sent' && (
                        <button onClick={() => confirmGiftReceived(gift.id, setGifts, setLoading)}>
                            Confirm Receipt
                        </button>
                    )}
                </li>
            ))}
        </ul>
    );
}